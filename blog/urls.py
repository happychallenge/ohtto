from django.conf.urls import url
from . import views, view_tm

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search_tag/(?P<tag>\w+)/$', views.index, name='tag_list'),

    url(r'^search_persons/$', views.search_persons, name='search_persons'),
    url(r'^invite_persons/(?P<theme_id>\d+)/$', views.invite_persons, name='invite_persons'),

    url(r'^add/$', views.post_add, name='post_add'),
    url(r'^edit/(?P<id>\d+)/$', view_tm.post_edit, name='post_edit'),
    url(r'^like/$', views.post_like, name='post_like'),
    url(r'^bucket/$', views.post_bucket, name='post_bucket'),
    url(r'^bucket_list/$', views.my_bucket_list, name='my_bucket_list'),

    url(r'^(?P<id>\d+)/$', views.user_theme_list, name='user_theme_list'),

    url(r'^detail/$', views.post_detail, name='post_detail'),

    url(r'^current_location/$', views.current_location, name='current_location'),
    url(r'^search/current/(?P<tag>\w+)/$', views.current_location, name='cur_tag_list'),

    url(r'^myhistory/$', views.my_history, name='my_history'),
    url(r'^friend_profile/(?P<username>[\w@-_\.]+)/$', views.friend_profile, name='friend_profile'),

    url(r'^theme_add/$', view_tm.theme_add, name='theme_add'),
]
