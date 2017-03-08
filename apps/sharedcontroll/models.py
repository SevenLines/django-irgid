from django.db import models


class SharedURL(models.Model):
    url = models.URLField(default="", null=True, max_length=1000)
    service = models.TextField(default="")