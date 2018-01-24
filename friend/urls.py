from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.friend_list, name='friend_list'),
]
