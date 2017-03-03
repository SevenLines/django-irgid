# coding=utf-8
import json

from custom_settings.models import Setting, TextSetting
from excursions.models import ExcursionCategory, Excursion, ExcursionAppointment, ExcursionImage
from tests import BaseTestCase


class ViewsTestCase(BaseTestCase):
    def test_index_page(self):
        r = self.api('index')


class CategoryViewsTestCase(BaseTestCase):
    def test_hidden_category(self):
        c = ExcursionCategory.objects.create(
            title=u'Название'
        )
        self.api('excursions:category', params={'pk': c.pk}, status_code=404)

        c = ExcursionCategory.objects.create(
            title=u'Название'
        )
        e = Excursion.objects.create()
        c.excursion_set.add(e)
        self.api('excursions:category', params={'pk': c.pk}, status_code=404)

        with self.login():
            self.api('excursions:category', params={'pk': c.pk}, status_code=200)

        c = ExcursionCategory.objects.create(
            title=u'Название',
            visible=True,
        )
        self.api('excursions:category', params={'pk': c.pk}, status_code=404)

        with self.login():
            self.api('excursions:category', params={'pk': c.pk}, status_code=200)

    def test_visible_category(self):
        c = ExcursionCategory.objects.create(
            title=u'Название',
            visible=True,
        )
        self.api('excursions:category', params={'pk': c.pk}, status_code=404)

    def test_it_should_display_gallery_category(self):
        c = ExcursionCategory.objects.create(
            title=u'Название',
            visible=True,
        )
        c.excursion_set.add(Excursion.objects.create(published=True))
        c.excursion_set.add(Excursion.objects.create(published=True))

        r = self.api('gallery:index', status_code=404)
        self.api('gallery:item', params={'pk': c.excursion_set.all()[0].pk}, status_code=404)

        gallery_setting = Setting.objects.get(key='gallery_id')
        gallery_setting.value = c.id
        gallery_setting.save()

        self.api('gallery:index')
        self.api('gallery:item', params={'pk': c.excursion_set.all()[0].pk})

    def test_it_should_display_travel_category(self):
        c = ExcursionCategory.objects.create(
            title=u'Название',
            visible=True,
        )
        c.excursion_set.add(Excursion.objects.create(published=True, title='title',
                                                     short_description='description'))
        c.excursion_set.add(Excursion.objects.create(published=True))

        r = self.api('travel:index', status_code=404)
        self.api('travel:item', params={'pk': c.excursion_set.all()[0].pk}, status_code=404)

        travel_setting = Setting.objects.get(key='travel_id')
        travel_setting.value = c.id
        travel_setting.save()

        self.api('travel:index')
        self.api('travel:item', params={'pk': c.excursion_set.all()[0].pk})

    def test_it_can_be_removed(self):
        c = ExcursionCategory.objects.create(
            title=u'Название',
            visible=True,
        )
        self.assertEqual(ExcursionCategory.objects.filter(pk=c.pk).count(), 1)
        self.api('excursions:category_remove', params={'pk': c.pk}, status_code=302)
        self.assertEqual(ExcursionCategory.objects.filter(pk=c.pk).count(), 1)

        with self.login():
            self.api('excursions:category_remove', params={'pk': c.pk}, post=True, ajax=True)
        self.assertEqual(ExcursionCategory.objects.filter(pk=c.pk).count(), 0)

    def test_category_create(self):
        with self.login():
            self.assertEqual(0, ExcursionCategory.objects.count())
            with open("tests/icon.png") as image:
                self.api("ajax_category_save", {
                    'title': "title",
                    'description': "description",
                    'visible': True,
                    'image': image,
                }, post=True, ajax=True)

                cat = ExcursionCategory.objects.first()
                self.assertEqual('title', cat.title)
                self.assertEqual('description', cat.description)
                self.assertTrue(cat.visible)
                self.assertIsNotNone(cat.image)

    def test_category_update(self):
        with self.login():
            c = ExcursionCategory.objects.create(
                title=u'Название',
                visible=True,
            )
            with open("tests/icon.png") as image:
                self.api("ajax_category_save", {
                    'id': c.pk,
                    'title': "title",
                    'description': "description",
                    'visible': True,
                    'image': image,
                }, post=True, ajax=True)

            cat = ExcursionCategory.objects.first()
            self.assertEqual('title', cat.title)
            self.assertEqual('description', cat.description)
            self.assertTrue(cat.visible)
            self.assertIsNotNone(cat.image)

    def test_set_cattery_order(self):
        c1 = ExcursionCategory.objects.create(
            title=u'Название',
            visible=True,
        )
        c2 = ExcursionCategory.objects.create(
            title=u'Название2',
            visible=True,
        )

        with self.login():
            self.api("ajax_set_categories_order", {
                "order": json.dumps({
                    c1.pk: 1,
                    c2.pk: 2,
                })
            }, ajax=True, post=True)
            self.assertEqual(ExcursionCategory.objects.order_by("order").first().pk, c1.pk)

            self.api("ajax_set_categories_order", {
                "order": json.dumps({
                    c1.pk: 2,
                    c2.pk: 1,
                })
            }, ajax=True, post=True)
            self.assertEqual(ExcursionCategory.objects.order_by("order").first().pk, c2.pk)

    def test_category_toggle(self):
        category = ExcursionCategory.objects.create(
            title=u'Название',
            visible=True,
        )
        with self.login():
            r = self.api("ajax_toggle_category", {
                'id': category.pk,
                'visible': False
            }, ajax=True)

            category = ExcursionCategory.objects.get(pk=category.pk)
            self.assertFalse(category.visible)

            r = self.api("ajax_toggle_category", {
                'id': category.pk,
                'visible': True
            }, ajax=True)

            category = ExcursionCategory.objects.get(pk=category.pk)
            self.assertTrue(category.visible)

    def test_set_and_remove_category_image(self):
        category = ExcursionCategory.objects.create(
            title=u'Название',
            visible=True,
        )
        with self.login():
            with open("tests/icon.png") as image:
                r = self.api("ajax_set_category_image", {
                    'id': category.pk,
                    'image': image
                }, post=True, ajax=True)
                category = ExcursionCategory.objects.get(pk=category.pk)
                self.assertEqual(r.content, category.image.url)

                r = self.api("ajax_remove_category_image", {
                    'id': category.pk,
                }, ajax=True)
                category = ExcursionCategory.objects.get(pk=category.pk)
                self.assertTrue(category.image.name == '')


class ExcursionViewsTestCase(BaseTestCase):
    def test_it_can_be_dont_visible_for_guest(self):
        e = Excursion.objects.create(title=u'Название')
        self.api('excursions:item', params={'pk': e.id}, status_code=404)

        e = Excursion.objects.create(title=u'Название', published=True)
        self.api('excursions:item', params={'pk': e.id}, status_code=404)

        with self.login():
            e = Excursion.objects.create(title=u'Название')
            self.api('excursions:item', params={'pk': e.id})

            e = Excursion.objects.create(title=u'Название', published=True)
            self.api('excursions:item', params={'pk': e.id})

    def test_it_with_category_and_if_published_should_be_visible(self):
        category = ExcursionCategory.objects.create(visible=True)
        e = Excursion.objects.create(
            title=u'Название',
            published=True,
            category=category,
            priceList=u"1-10|100/200/300\n11-20 | 100/300\n21 |100\n50|400 на всех"
        )
        self.api('excursions:item', params={'pk': e.id})

        with self.login():
            self.api('excursions:item', params={'pk': e.id})

    def test_it_can_be_removed(self):
        e = Excursion.objects.create(
            title=u'Название',
            published=True,
        )
        self.assertEqual(Excursion.objects.filter(pk=e.pk).count(), 1)
        self.api('excursions:remove', params={'pk': e.pk}, status_code=302)
        self.assertEqual(Excursion.objects.filter(pk=e.pk).count(), 1)

        with self.login():
            self.api('excursions:remove', params={'pk': e.pk}, post=True, ajax=True)
        self.assertEqual(Excursion.objects.filter(pk=e.pk).count(), 0)

    def test_preview(self):
        e = Excursion.objects.create(
            title=u'Название',
        )
        self.api('excursions:item_preview', params={'pk': e.pk}, status_code=302)

        with self.login():
            self.api('excursions:item_preview', params={'pk': e.pk})

    def test_price_list_rendered(self):
        e = Excursion.objects.create(
            title=u'Название',
            published=True,
            priceList=
            "1-10 | 100/200/300\n"
            "11-20 | 400/500/600"
        )

        data = e.price_list_rendered()
        lines = data['lines']
        data = data['data']
        self.assertEqual('100', data[0]['default_price'])
        self.assertEqual("1-10", data[0]['header'])
        self.assertEqual(0, data[0]['span'])
        self.assertEqual({0: '300', 1: '200', 2: '100'}, data[0]['price_line'])

        self.assertEqual('400', data[1]['default_price'])
        self.assertEqual("11-20", data[1]['header'])
        self.assertEqual(0, data[1]['span'])
        self.assertEqual({0: '600', 1: '500', 2: '400'}, data[1]['price_line'])

        self.assertEqual([0, 1, 2], lines)

    def test_excursions_save(self):
        with self.login():
            with open("tests/icon.png") as image:
                c = ExcursionCategory.objects.create(
                    title="category_title"
                )

                ex = Excursion.objects.create(
                    title="exc1",
                    description="description",
                    short_description="short_description",
                )

                data = {
                    'id': ex.pk,
                    'title': "exc1_new",
                    'description': "description_new",
                    'short_description': "short_description_new",
                    'yandex_map_script': 'yandex_map_script',
                    'category_id': c.pk,
                    'price_list': '1-10|100\n11-20|200',
                    'time_length': 2,
                    'min_age': 3,
                    'published': True,
                    'small_image': image,
                    'gallery[]': [
                        image,
                        image,
                    ]
                }

                r = self.api("ajax_save", data, post=True, follow=True)
                ex = Excursion.objects.get(pk=ex.pk)

                for key, item in data.items():
                    if key == 'small_image':
                        self.assertTrue(ex.img_preview.name is not None and ex.img_preview.name != "")
                    elif key == 'gallery[]':
                        self.assertEqual(2, ex.images.count())
                    elif key == 'price_list':
                        self.assertEqual(item, ex.priceList)
                    else:
                        self.assertEqual(item, ex.__dict__[key],
                                         "{}: {} != {}".format(key, item, ex.__dict__[key]))

    def test_upload_image(self):
        with self.login():
            ex = Excursion.objects.create(title=u"название")
            with open("tests/icon.png") as image:
                self.api('image_add', {
                    'excursion_id': ex.pk,
                    'image': image
                }, ajax=True, post=True)

                ex = Excursion.objects.get(pk=ex.pk)
                self.assertEqual(1, ex.images.count())

    def test_excursion_image_remove(self):
        with self.login():
            ex = Excursion.objects.create(title=u"название")
            im = ExcursionImage.objects.create(excursion_id=ex.pk)
            r = self.api("ajax_image_remove", params={
                "pk": im.pk
            }, ajax=True)
            self.assertEqual(0, ExcursionImage.objects.count())

    def test_excursion_image_toggle(self):
        with self.login():
            ex = Excursion.objects.create(title=u"название")
            im = ExcursionImage.objects.create(excursion_id=ex.pk, hidden=False)
            r = self.api("ajax_image_toggle", params={
                "pk": im.pk
            }, ajax=True)
            im = ExcursionImage.objects.get(pk=im.pk)
            self.assertTrue(im.hidden)

            r = self.api("ajax_image_toggle", params={
                "pk": im.pk
            }, ajax=True)
            im = ExcursionImage.objects.get(pk=im.pk)
            self.assertFalse(im.hidden)

class TestAppointment(BaseTestCase):
    def test_can_add_appointment(self):
        TextSetting.objects.filter(key='email_for_appointments') \
            .update(value='some_mail@some_mail.com')

        self.assertEqual(0, ExcursionAppointment.objects.count())
        data = {
            "email": "mail@mail.ru",
            "phone": "2128506",
            "full_name": "sardanapal",
            "comment": "ohm mane padme hum",
        }
        r = self.api("appointment_create", data, post=True, ajax=True)
        appointment = ExcursionAppointment.objects.first()
        self.assertEqual(1, ExcursionAppointment.objects.count())
        self.assertEqual(appointment.email, data['email'])
        self.assertEqual(appointment.phone, data['phone'])
        self.assertEqual(appointment.full_name, data['full_name'])
        self.assertEqual(appointment.comment, data['comment'])
        self.assertTrue(appointment.sended)
