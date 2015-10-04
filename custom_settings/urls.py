from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

import custom_settings.views

urlpatterns = patterns('',
   url(r'update/(?P<pk>\d+)/$', custom_settings.views.SettingEditView.as_view(),
       name='settings-update'),
   url(r'$', login_required(custom_settings.views.SettingsListView.as_view()), name='settings'),
)
