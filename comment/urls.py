from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^post_comment$', views.post_comment, name='post_comment'),
]
