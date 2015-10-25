from django.db import models


class SharedURL(models.Model):
    url = models.URLField(default="")
    service = models.CharField(max_length=100, default="")