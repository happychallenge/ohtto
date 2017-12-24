from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^profile_edit/$', views.profile_edit, name='profile_edit'),
    url(r'^checkemail/$', views.checkemail, name='checkemail'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]