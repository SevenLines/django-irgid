import os

from django.db import models
from django.db.models.base import Model
from django.dispatch import receiver
from easy_thumbnails.alias import aliases
from easy_thumbnails.fields import ThumbnailerImageField


class MainPageItem(Model):
    # create thumbnailer alias
    if not aliases.get('main_page_thumb'):
        aliases.set('main_page_thumb', {'size': (160, 100)})

    title = models.CharField(max_length=50)
    img = ThumbnailerImageField(upload_to='main_page_items')
    description = models.TextField(blank=True, null=True)

    @property
    def dictionary(self):
        """
        return dictionary copy of object suitable for json response
        :return:
        """
        exists = os.path.exists(self.img.path)
        return {
            'id': self.pk,
            'title': self.title,
            # 'description': self.description,
            'item_url': self.img.url if self.img.name and exists else "",
            'item_thumb_url': self.img['main_page_thumb'].url if self.img.name and exists else ""
        }


class MainPage(Model):
    current_item = models.ForeignKey(MainPageItem, null=True, on_delete=models.SET_NULL)
    current_theme_css = models.TextField(default="")
    _img_bootstrap_cols = models.IntegerField(default=0)
    show_border = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True, default="")

    @property
    def img_bootstrap_cols(self):
        return min(max(self._img_bootstrap_cols, -1), 12)


    @staticmethod
    def solo():
        """
        returns singleton MainPage object, create it in db if necessary
        :return: MainPage
        """
        if MainPage.objects.count() == 0:
            mp = MainPage()
            mp.save()
        return MainPage.objects.first()


@receiver(models.signals.post_delete, sender=MainPageItem)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MainPageItem` object is deleted.
    """
    if instance.img:
        instance.img.delete(False)


@receiver(models.signals.pre_save, sender=MainPageItem)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MainPageItem` object is changed.
    """
    if not instance.pk:
        return False

    try:
        old_file = MainPageItem.objects.get(pk=instance.pk).img
    except MainPageItem.DoesNotExist:
        return False

    new_file = instance.img
    if not old_file.path == new_file.path:
        if os.path.isfile(old_file.path):
            old_file.delete()