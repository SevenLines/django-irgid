# coding=utf-8
# Create your views here.
import json

from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect
from django.views.generic import DetailView, View
from django.views.generic.detail import SingleObjectMixin

from excursions.models import ExcursionCategory, Excursion, ExcursionImage
from excursions.utils import get_price_list
from excursions.views import ajax
from excursions.views.base import _excursion_save, _excursion_context
from irgid.utils import require_in_POST
from irgid.views import TitledView


class MainPageView(TitledView):
    title = u'Иргид - экскурсионное агентство'
    template_name = 'excursions/main-page/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)

        categories = ExcursionCategory.objects.common_with_all(self.request.user)

        context.update({
            'categories': categories,
            'gallery': ExcursionCategory.objects.gallery(),
            'travel': ExcursionCategory.objects.travel()
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

        context['price_headers'] = 'headers_excursions'
        context['current_excursion'] = self.excursion
        context['current_category'] = self.category
        context['excursions'] = self.category.get_excursions(self.request).order_by("title") if self.category else []
        context['categories'] = ExcursionCategory.objects.common(self.request.user)
        context['price_list'] = json.dumps(get_price_list(self.excursion.priceList))
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

