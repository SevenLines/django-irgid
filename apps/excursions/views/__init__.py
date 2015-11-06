# coding=utf-8
# Create your views here.
import json

from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView

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

        categories = ExcursionCategory.objects.common_with_gallery(self.request.user)

        context.update({
            'categories': categories,
            'gallery': ExcursionCategory.objects.gallery(),
            'travel': ExcursionCategory.objects.travel()
        })
        return context


class CategoryView(TitledView):
    template_name = 'excursions/category/index.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)

        c = get_object_or_404(ExcursionCategory, pk=kwargs.get('pk', None))

        categories = ExcursionCategory.objects.common(self.request.user)

        context.update({
            'current_category': c,
            'excursions': c.excursions(self.request).order_by("title"),
            'title': c.title,
            'categories': categories,
            'meta': {
                'description': u"Категория: %s; Описание: %s"
                               % (c.title, c.description.strip())
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

        context['title'] = self.excursion.title
        context['current_excursion'] = self.excursion
        context['current_category'] = self.category
        context['excursions'] = self.category.excursions(self.request).order_by("title")
        context['categories'] = ExcursionCategory.objects.common(self.request.user)
        context['price_list'] = json.dumps(get_price_list(self.excursion.priceList))
        context['gallery'] = ExcursionImage.objects.filter(excursion=self.excursion).order_by("order")
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
        context.update({
            'meta': {
                'description': u"Галерея: %s; Описание: %s" % (e.title, e.short_description)
            }
        })

        return context


class ExcursionTravelItemView(ExcursionItemBaseView):
    template_name = "excursions/travel/excursion/index.html"

    def get_context_data(self, **kwargs):
        context = super(ExcursionTravelItemView, self).get_context_data(**kwargs)

        context.update({
            'meta': {
                'description': u"Путешествие: %s; Описание: %s" % (e.title, e.short_description)
            }
        })

        return context


class ExcursionIndexBaseView(TitledView):
    def get_category(self):
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        context = super(ExcursionIndexBaseView, self).get_context_data(**kwargs)

        category = self.get_category()

        context.update({
            'excursions': category.excursions(self.request).order_by("title") if category else [],
            'current_category': category
        })

        return context


class ExcursionGalleryIndexView(ExcursionIndexBaseView):
    title = u'Галерея'
    template_name = "excursions/gallery/index.html"

    def get_category(self):
        return ExcursionCategory.objects.gallery()


class ExcursionTravelIndexView(TitledView):
    title = u'Путешествия'
    template_name = "excursions/travel/index.html"

    def get_category(self):
        return ExcursionCategory.objects.travel()


class CategoryRemove(LoginRequiredMixin, DeleteView):
    model = ExcursionCategory


class ExcursionRemove(LoginRequiredMixin, DeleteView):
    model = Excursion


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

