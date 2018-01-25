from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.friend_list, name='friend_list'),
    url(r'^ask_friend/$', views.ask_friend, name='ask_friend'),
    url(r'^accept_friend/$', views.accept_friend, name='accept_friend'),
    url(r'^reject_friend/$', views.reject_friend, name='reject_friend'),
]
