from custom_settings.models import Setting, IntegerSetting
from excursions.models import ExcursionCategory
from tests import BaseTestCase


class TestCustomSettings(BaseTestCase):
    def test_options_list(self):
        ex1 = ExcursionCategory.objects.create(
            title="exc1"
        )
        ex2 = ExcursionCategory.objects.create(
            title="exc2"
        )

        options = IntegerSetting.objects.get(key="gallery_id").options
        self.assertEqual({'pk': ex1.pk, 'title': ex1.title}, options[0])
        self.assertEqual({'pk': ex2.pk, 'title': ex2.title}, options[1])

    def test_list(self):
        with self.login():
            self.api("settings", follow=True)

    def test_update(self):
        with self.login():
            obj = IntegerSetting.objects.first()
            new_value = obj.value or 0 + 2
            self.api("settings-update",
                     data = {'value': new_value},
                     params={'pk': obj.pk},
                     post=True, ajax=True)
            obj = IntegerSetting.objects.get(pk=obj.pk)
            self.assertEqual(new_value, obj.value)

            new_value = obj.value + 2
            self.api("settings-update-by-key",
                     data={'value': new_value},
                     params={'slug': obj.key},
                     post=True, ajax=True)
            obj = IntegerSetting.objects.get(pk=obj.pk)
            self.assertEqual(new_value, obj.value)