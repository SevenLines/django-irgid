from cms.models.pagemodel import Page
from cms.models.pluginmodel import CMSPlugin
from django.db import models


# Create your models here.
from easy_thumbnails.fields import ThumbnailerImageField
from filer.fields.image import FilerImageField


class TextPage(CMSPlugin):
    text = models.TextField(default="")


class TextPageImage(models.Model):
    image = ThumbnailerImageField(upload_to="textpage")