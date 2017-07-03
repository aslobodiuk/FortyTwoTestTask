from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import login
from django.contrib import admin
from django.conf.urls.static import static
from fortytwo_test_task import settings
from apps.hello import views
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^requests/$', views.requests, name='requests'),
    url(r'^help/$', views.help, name='help'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^accounts/login', login, name='login'),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
