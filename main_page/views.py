# coding=utf-8
from glob import glob
import json
import os
import re
from uuid import uuid4
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import storage
from django.contrib.staticfiles.finders import AppDirectoriesFinder, FileSystemFinder
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from app.utils import require_in_POST
from main_page.models import MainPageItem, MainPage


def main_page_context(data=None):
    if not data:
        data = {}
    obj = MainPage.solo()

    if 'item' not in data:
        data['item'] = obj.current_item.dictionary if obj.current_item else None
    if 'show_border' not in data:
        data['show_border'] = obj.show_border
    if 'img_bootstrap_cols' not in data:
        data['img_bootstrap_cols'] = obj.img_bootstrap_cols
    if 'desc_bootstrap_cols' not in data:
        data['desc_bootstrap_cols'] = 12 - obj.img_bootstrap_cols
    data['description'] = obj.description
    return data


def index(request):
    # context = RequestContext(request, main_page_context())
    return render(request, 'main_page/index.html', main_page_context())


@login_required
def item(request):
    try:
        if 'item_id' in request.POST:
            i = MainPageItem.objects.get(pk=request.POST['item_id'])
        elif 'item_id' in request.GET:
            i = MainPageItem.objects.get(pk=request.GET['item_id'])
        else:
            i = MainPage.solo().current_item
    except ObjectDoesNotExist as e:
        return HttpResponseBadRequest("can't get item with the item_id")
    context = main_page_context({
        'item': i.dictionary if i else None,
    })
    html = render_to_string('main_page/image.html', RequestContext(request, context))

    return HttpResponse(json.dumps(main_page_context({
        'item': i.dictionary if i else None,
        'html': html,
    })), content_type='json')


def list_items(request):
    main_page = MainPage.solo()
    main_item = main_page.current_item

    items = []
    items.extend(list(MainPageItem.objects.all().order_by("-pk")))
    if main_item is not None and main_item not in items:
        items.append(main_item)

    output = []
    for i in items:
        i_dict = i.dictionary
        i_dict.update({'active': main_item.id == i.id if main_item else False})
        output.append(i_dict)

    return HttpResponse(json.dumps(output), content_type='json')


@login_required
def list_themes(request):
    current_theme = MainPage.solo().current_theme_css

    out = []

    out.append({
        'name': 'без темы',
        'path': '',
        'current': current_theme == ''
    })

    _, files = storage.StaticFilesStorage().listdir("css")
    for f in files:
        fl = f.split(os.sep)[-1]
        m = re.match(r"theme_(.*?)\.css", fl)
        if m:
            theme_path = os.path.join(settings.STATIC_URL, 'css', f)
            out.append({
                'name': m.group(1),
                'path': theme_path,
                'current': theme_path == current_theme
            })

    return HttpResponse(json.dumps(out), content_type='json')


@login_required
@require_in_POST("css_path")
def set_current_theme(request):
    main_page = MainPage.solo()
    main_page.current_theme_css = request.POST['css_path']
    main_page.save()

    return HttpResponse()


@require_POST
@login_required
@require_in_POST("item_id")
def set_active(request):
    item_id = request.POST['item_id']

    try:
        item = MainPageItem.objects.get(pk=item_id)
    except BaseException as e:
        return HttpResponseBadRequest(e.message)

    main_page_settings = MainPage.solo()
    main_page_settings.current_item = item if item != main_page_settings.current_item else None
    main_page_settings.save()

    return render(request, 'main_page/image.html', main_page_context())


@login_required
@require_POST
@require_in_POST("item_id")
def save_item(request):
    item_id = request.POST['item_id']
    i = MainPageItem.objects.get(pk=item_id)

    if 'description' in request.POST:
        i.description = request.POST['description']

    if 'title' in request.POST:
        i.title = request.POST['title']

    # if 'item_url' in request.POST:
    # i.item_url = request.POST['item_url']

    i.save()

    return item(request)


@login_required
@require_POST
@require_in_POST("title", "description")
def add_item(request):
    it = MainPageItem()
    it.title = request.POST['title']
    it.description = request.POST['description']

    f = request.FILES['file']
    ext = f.name.split('.')[-1]
    it.img.save('%s.%s' % (uuid4(), ext), ContentFile(f.read()))
    it.save()

    if "activate" in request.POST:
        main_page = MainPage.solo()
        main_page.current_item = it
        main_page.save()

    mutable = request.POST._mutable
    request.POST._mutable = True
    request.POST['item_id'] = it.pk
    request.POST._mutable = mutable

    return item(request)


@login_required
@require_in_POST("item_id")
def remove_item(request):
    item_id = request.POST['item_id']
    it = MainPageItem.objects.get(pk=item_id)
    it.delete()

    return HttpResponse()


@login_required
@require_in_POST("show_border")
def toggle_border(request):
    f = request.POST['show_border']

    obj = MainPage.solo()
    obj.show_border = f != u"true"
    obj.save()

    return HttpResponse()

@login_required
@require_in_POST("img_bootstrap_cols")
def toggle_img_bootstrap_cols(request):
    img_bootstrap_cols = request.POST['img_bootstrap_cols']
    obj = MainPage.solo()
    obj._img_bootstrap_cols = img_bootstrap_cols
    obj.save()

    return HttpResponse(img_bootstrap_cols)

@login_required
@require_in_POST("description")
def update_description(request):
    description = request.POST['description']
    obj = MainPage.solo()
    obj.description = description
    obj.save()

    return HttpResponse(description)