# coding=utf-8
from custom_settings.models import Setting, TextSetting
from excursions.models import ExcursionCategory, Excursion, ExcursionAppointment
from tests import BaseTestCase


class ViewsTestCase(BaseTestCase):
    def test_index_page(self):
        r = self.api('index')
        print r


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
        c.excursion_set.add(Excursion.objects.create(published=True, title='title', short_description='description'))
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
        e = Excursion.objects.create(title=u'Название', published=True, category=category)
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


class TestAppointment(BaseTestCase):
    def test_can_add_appointment(self):
        TextSetting.objects.filter(key='email_for_appointments')\
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




