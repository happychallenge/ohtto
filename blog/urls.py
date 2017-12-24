from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.post_add, name='post_add'),
    url(r'^like/$', views.post_like, name='post_like'),
    url(r'^bucket/$', views.post_bucket, name='post_bucket'),
    url(r'^bucket_list/$', views.my_bucket_list, name='my_bucket_list'),

    url(r'^(?P<username>[\w@-_\.]+)/(?P<id>\d+)/$', views.user_theme_list, 
            name='user_theme_list'),

    url(r'^detail/$', views.post_detail, name='post_detail'),
    url(r'^current_location/$', views.current_location, name='current_location'),
    url(r'^myhistory/$', views.my_history, name='my_history'),
]
