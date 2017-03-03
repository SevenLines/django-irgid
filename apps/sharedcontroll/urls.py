from django.conf.urls import include, url
import sharedcontroll.views

urlpatterns = [
    url(r'shareurl/$', sharedcontroll.views.share, name="share"),
]
