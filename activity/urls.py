from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^check_notifications/$', views.check_notifications, name='check_notifications'),
    url(r'^last_notifications/$', views.last_notifications, name='last_notifications'),
]