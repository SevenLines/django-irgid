from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns


urlpatterns = i18n_patterns('textpage.views',
    url(r'save/$', 'save'),
    url(r'$', 'index'),
)