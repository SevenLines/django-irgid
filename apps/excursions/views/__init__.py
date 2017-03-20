# coding=utf-8
# Create your views here.
import json
from calendar import Calendar
from datetime import date, datetime

from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Min, Max
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.template.context import RequestContext
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import DetailView, View
from django.views.generic.detail import SingleObjectMixin

from excursions.models import ExcursionCategory, Excursion, ExcursionImage, ExcursionCalendar, ExcursionAppointment
from excursions.utils import get_price_list
from excursions.views import ajax
from excursions.views.base import _excursion_save, _excursion_context
from irgid.utils import require_in_POST
from irgid.views import TitledView
from excursions.tasks import send_appointment


@method_decorator(xframe_options_exempt, name='dispatch')
class MainPageView(TitledView):
    title = u'Иргид - экскурсионное агентство'
    template_name = 'excursions/main-page/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)

        categories = ExcursionCategory.objects.common_with_all(self.request.user)
        popular_excursions = Excursion.objects.filter(popular=True)
        popular_excursions = list(popular_excursions)
        if len(popular_excursions) < 4:
            popular_excursions = []
        else:
            popular_excursions = popular_excursions[:4]

        context.update({
            'categories': categories,
            'gallery': ExcursionCategory.objects.gallery(),
            'travel': ExcursionCategory.objects.travel(),
            'popular_excursions': popular_excursions,
        })
        return context


class BaseModelDeleteView(LoginRequiredMixin, SingleObjectMixin, View):
    def post(self, request, *args, **kwargs):
        self.get_object().delete()

        if request.is_ajax():
            result = HttpResponse()
        else:
            result = redirect(request.META.get('HTTP_REFERER', reverse('index')))

        return result


@method_decorator(xframe_options_exempt, name='dispatch')
class CategoryView(DetailView):
    model = ExcursionCategory
    template_name = 'excursions/category/index.html'
    category = None

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        self.category = self.object

        if not self.request.user.is_authenticated():
            if not self.category.get_excursions(self.request).exists():
                raise Http404
            if not self.category.visible and not (self.category.is_gallery or self.category.is_travel):
                raise Http404

        categories = ExcursionCategory.objects.common(self.request.user)

        context.update({
            'current_category': self.category,
            'excursions': self.category.get_excursions(self.request).order_by("title"),
            'title': self.category.title,
            'categories': categories,
            'meta': {
                'description': u"Категория: %s; Описание: %s"
                               % (self.category.title, self.category.description.strip())
            }
        })

        return context


@method_decorator(xframe_options_exempt, name='dispatch')
class ExcursionItemBaseView(DetailView):
    model = Excursion
    template_name = "excursions/excursion/index.html"
    excursion = None
    category = None

    def get_context_data(self, **kwargs):
        context = super(ExcursionItemBaseView, self).get_context_data(**kwargs)
        self.excursion = self.object
        self.category = self.excursion.category

        if not self.request.user.is_authenticated():
            if not self.excursion.published:
                raise Http404
            if not self.category:
                raise Http404
            if not self.category.visible and not (self.category.is_gallery or self.category.is_travel):
                raise Http404

        context['title'] = self.excursion.title

        context['gallery'] = self.excursion.images.all()
        if not self.request.user.is_authenticated():
            context['gallery'] = context['gallery'].filter(hidden=False)

        context['current_excursion'] = self.excursion
        context['current_category'] = self.category
        context['excursions'] = self.category.get_excursions(self.request).order_by("title") if self.category else []
        context['categories'] = ExcursionCategory.objects.common(self.request.user)
        context['price_list'] = json.dumps(get_price_list(self.excursion.priceList))
        context['price_headers'] = 'headers_excursions'
        context['file_browser'] = ExcursionImage.objects.filter(excursion=self.excursion).order_by("order")
        context['meta'] = {
            'description': u"Экскурсия: {}; Описание: {}".format(self.excursion.title, self.excursion.short_description)
        }

        return context


class ExcursionItemView(ExcursionItemBaseView):
    template_name = "excursions/excursion/index.html"


class ExcursionGalleryItemView(ExcursionItemBaseView):
    template_name = "excursions/gallery/excursion/index.html"

    def get_context_data(self, **kwargs):
        context = super(ExcursionGalleryItemView, self).get_context_data(**kwargs)

        gallery = ExcursionCategory.objects.gallery()

        if not gallery or self.category != gallery:
            raise Http404

        context.update({
            'meta': {
                'description': u"Галерея: %s; Описание: %s" % (self.excursion.title, self.excursion.short_description)
            }
        })

        return context


class ExcursionTravelItemView(ExcursionItemBaseView):
    template_name = "excursions/travel/excursion/index.html"

    def get_context_data(self, **kwargs):
        context = super(ExcursionTravelItemView, self).get_context_data(**kwargs)
        travel = ExcursionCategory.objects.travel()

        if not travel or self.category != travel:
            raise Http404

        context.update({
            'price_headers': 'headers_travel',
            'meta': {
                'description': u"Путешествие: %s; Описание: %s" % (
                    self.excursion.title, self.excursion.short_description)
            }
        })

        return context


class ExcursionPreviewItemView(LoginRequiredMixin, ExcursionItemBaseView):
    def preview(self):
        return True

    def get_context_data(self, **kwargs):
        context = super(ExcursionPreviewItemView, self).get_context_data(**kwargs)
        context['gallery'] = context['gallery'].filter(hidden=False)
        if self.category and self.category.is_travel:
            context['price_headers'] = 'headers_travel'
        return context


class ExcursionIndexBaseView(TitledView):
    def get_category(self):
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        context = super(ExcursionIndexBaseView, self).get_context_data(**kwargs)

        category = self.get_category()

        context.update({
            'excursions': category.get_excursions(self.request).order_by("title") if category else [],
            'current_category': category
        })

        return context

@method_decorator(xframe_options_exempt, name='dispatch')
class ExcursionGalleryIndexView(ExcursionIndexBaseView):
    title = u'Галерея'
    template_name = "excursions/gallery/index.html"

    def get_category(self):
        gallery = ExcursionCategory.objects.gallery()
        if not gallery:
            raise Http404
        return gallery


class ExcursionTravelIndexView(CategoryView):
    template_name = "excursions/travel/index.html"

    def get_object(self, **kwargs):
        travel = ExcursionCategory.objects.travel()
        if not travel:
            raise Http404
        return travel

    def get_context_data(self, **kwargs):
        context = super(ExcursionTravelIndexView, self).get_context_data(**kwargs)
        context.update({
            'title': u'Путешествия'
        })
        return context


class ExcursionRemoveView(BaseModelDeleteView):
    model = Excursion


class ExcursionCategoryRemoveView(BaseModelDeleteView):
    model = ExcursionCategory


class ExcursionCalendarView(TitledView):
    title = u'Календарь'
    template_name = 'excursions/calendar/index.html'

    def months(self):
        return settings.MONTHS

    def month(self):
        verbose = dict(settings.MONTHS)[self.selected_month]

        return {
            'number': self.selected_month,
            'verbose': verbose,
        }

    def today(self):
        return datetime.today()

    def day(self):
        d = date.today().day
        return d

    def selected_year(self):
        return self.selected_year

    def selected_month(self):
        return self.selected_month

    @classmethod
    def actual_years(cls):
        rng = ExcursionCalendar.objects.aggregate(min_date=Min('date'), max_date=Max('date'))
        if rng:
            min_year = rng['min_date'].year
            max_year = rng['max_date'].year
        else:
            min_year = date.today().year
            max_year = min_year
        if hasattr(cls, 'request') and cls.request.user.is_authenticated():
            return [year for year in xrange(min_year - 1, max_year + 2)]
        else:
            return [year for year in xrange(min_year, max_year + 1)]

    def get_calendar_items(self):
        dates = list(Calendar().itermonthdates(self.selected_year, self.selected_month))

        calendar_items = ExcursionCalendar.objects.filter(
            date__in=dates
        )
        calendar_items = dict([(item.date, item) for item in calendar_items])
        exists = bool(calendar_items)

        out = [
            {
                'date': date,
                'current': date == date.today(),
                'item': calendar_items.get(date, None)
            } for date in dates
        ]
        return out, exists

    def calendar(self):
        days = self.calendar_items

        weeks = {}
        for d in days:
            weeks.setdefault(d['date'].weekday(), [])
            weeks[d['date'].weekday()].append(d)
        out = []
        for w in weeks.keys():
            days = []
            for d in weeks[w]:
                days.append(d)
            out.append(days)
        return out

    def days(self):
        if self.request.user.is_authenticated():
            out = self.calendar_items
        else:
            out = [item for item in self.calendar_items
                   if item['item'] and item['item'].comment and item['date'].month == self.selected_month]

        return out

    def events(self):
        ExcursionCalendar.objects.filter(date)

    def get_context_data(self, **kwargs):
        self.selected_year = int(self.request.GET.get('year', date.today().year))
        self.selected_month = int(self.request.GET.get('month', date.today().month))
        self.calendar_items, calendar_items_exists = self.get_calendar_items()
        # if not self.request.user.is_authenticated():
        #     if not calendar_items_exists:
        #         raise Http404()

        return super(ExcursionCalendarView, self).get_context_data(**kwargs)


class ExcursionCalendarUpdateView(LoginRequiredMixin, View):
    def post(self, request):
        items = json.loads(request.POST['items'])
        for item in items:
            dt = date(item['year'], item['month'], item['day'])
            mdl, created = ExcursionCalendar.objects.get_or_create(
                date=dt
            )
            mdl.comment = item['description']
            mdl.save()

        return HttpResponse()


class ExcursionAppointmentCreateView(View):
    def post(self, request):
        from excursions.forms import ExcursionAppointmentForm

        email = request.POST['email']
        phone = request.POST['phone']
        comment = request.POST['comment']
        full_name = request.POST['full_name']

        form = ExcursionAppointmentForm(request.POST)
        if form.is_valid():
            appointment = ExcursionAppointment.objects.create(
                email=email,
                full_name=full_name,
                phone=phone,
                comment=comment,
            )
            message = "Спасибо за оставленную заявку! " \
                      "Ваш запрос принят и отправлен оператору. " \
                      "Мы постараемся в кратчайшие сроки ответить Вам"
            success = True
            send_appointment.apply_async((appointment.pk,))
        else:
            message = "Возникли проблемы при создании заявки,\nпожалуйста, попробуйте еще раз."
            success = False

        if request.is_ajax():
            return HttpResponse(json.dumps({
                "message": message,
                "success": success
            }), content_type='json')
        else:
            return redirect(request.META['HTTP_REFERER'])


class ExcursionOffersList(View):
    def get(self, request):
        categories = ExcursionCategory.objects.all()
        excursion_categories = []
        travel_category = None

        for category in categories:
            if category.is_travel:
                travel_category = category
            elif not category.is_gallery:
                excursion_categories.append(category)

        offers = Excursion.objects.filter(
            category__in=excursion_categories,
            category__visible=True,
            published=True
        )

        return render(request, "offers.xml", {
            'categories': excursion_categories + [travel_category,],
            'offers': offers,
            'tours': Excursion.objects.filter(category=travel_category, published=True)
        }, content_type="text/xml; charset=utf-8")

@login_required
@permission_required("excursions.change_excursion")
@require_in_POST("category_id")
def excursion_save(request):
    _excursion_save(request)
    return redirect(request.META['HTTP_REFERER'])


@login_required
@require_in_POST("title")
@permission_required("excursions.change_excursioncategory")
def category_save(request):
    ajax.category_save(request)
    return redirect(request.META['HTTP_REFERER'])

