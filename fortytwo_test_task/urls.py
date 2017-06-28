from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.contrib import admin
from apps.hello import views
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^requests/$', TemplateView.as_view(template_name="requests.html")),
    url(r'^help/$', views.help, name='help'),
)

urlpatterns += staticfiles_urlpatterns()
