from cms.models.pagemodel import Page
from cms.models.pluginmodel import CMSPlugin
from django.db import models


# Create your models here.
class TextPage(CMSPlugin):
    text = models.TextField(default="")
