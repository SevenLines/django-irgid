# coding=utf-8
# Create your views here.
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404

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
            'categories': categories
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


class ExcursionItemView(TitledView):
    template_name = "excursions/excursion/index.html"

    def get_context_data(self, **kwargs):
        context = super(ExcursionItemView, self).get_context_data(**kwargs)

        pk = kwargs.get('pk', None)

        e = get_object_or_404(Excursion, pk=pk)
        category = e.category

        context.update({
            'current_excursion': e,
            'current_category': category,
            'categories': ExcursionCategory.objects.common(self.request.user),
            'excursions': category.excursions(self.request).order_by("title"),
            'gallery': ExcursionImage.objects.filter(excursion_id=pk).order_by("order"),
            'title': e.title,
            'meta': {
                'description': u"Экскурсия: %s; Описание: %s" % (e.title, e.short_description)
            },
            'price_list': json.dumps(get_price_list(e.priceList))
        })

        return context


class ExcursionGalleryIndexView(TitledView):
    title = u'Галерея'
    template_name = "excursions/gallery/index.html"

    def get_context_data(self, **kwargs):
        context = super(ExcursionGalleryIndexView, self).get_context_data(**kwargs)
        c = ExcursionCategory.objects.gallery()

        context.update({
            'excursions': c.excursions(self.request).order_by("title") if c else [],
            'current_category': c
        })
        return context


class ExcursionGalleryItemView(TitledView):
    template_name = "excursions/gallery/excursion/index.html"

    def get_context_data(self, **kwargs):
        context = super(ExcursionGalleryItemView, self).get_context_data(**kwargs)
        pk = kwargs.get('pk')

        e = get_object_or_404(Excursion, pk=pk)
        category = e.category

        context.update({
            'current_excursion': e,
            'current_category': category,
            'excursions': category.excursions(self.request).order_by("title"),
            'gallery': ExcursionImage.objects.filter(excursion=e).order_by("order"),
            'meta': {
                'description': u"Галерея: %s; Описание: %s" % (e.title, e.short_description)
            }
        })

        return context


class ExcursionTravelIndexView(TitledView):
    title = u'Путешествия'
    template_name = "excursions/travel/index.html"

    def get_context_data(self, **kwargs):
        context = super(ExcursionTravelIndexView, self).get_context_data(**kwargs)
        c = ExcursionCategory.objects.travel()

        context.update({
            'excursions': c.excursions(self.request).order_by("title") if c else [],
            'current_category': c
        })
        return context


class ExcursionTravelItemView(TitledView):
    template_name = "excursions/travel/excursion/index.html"

    def get_context_data(self, **kwargs):
        context = super(ExcursionTravelItemView, self).get_context_data(**kwargs)
        pk = kwargs.get('pk')

        e = get_object_or_404(Excursion, pk=pk)
        category = e.category

        context.update({
            'current_excursion': e,
            'current_category': category,
            'excursions': category.excursions(self.request).order_by("title"),
            'gallery': ExcursionImage.objects.filter(excursion=e).order_by("order"),
            'meta': {
                'description': u"Путешествие: %s; Описание: %s" % (e.title, e.short_description)
            }
        })

        return context


@login_required
@permission_required("excursions.delete_excursioncategory")
def category_remove(request, id):
    try:
        ExcursionCategory.objects.get(pk=id).delete()
    except Exception as e:
        messages.warning(request, e.message)

    return redirect(request.META['HTTP_REFERER'])


@login_required
@permission_required("excursions.delete_excursion")
def excursion_remove(request, id):
    try:
        Excursion.objects.get(pk=id).delete()
    except Exception as e:
        messages.warning(request, e.message)

    return redirect(request.META['HTTP_REFERER'])


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

