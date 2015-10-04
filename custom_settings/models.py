from django.db import models


# Create your models here.
class Setting(models.Model):
    key = models.CharField(max_length=128, null=False, blank=True, unique=True)
    title = models.CharField(max_length=128, null=False, blank=True)


class TextSetting(Setting):
    value = models.TextField()
