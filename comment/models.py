from django.conf import settings
from django.db import models


# Create your models here.
from blog.models import Post

class Comment(models.Model):
    """docstring for Comment"""
    """ 설명 """
    post = models.ForeignKey(Post, related_name='comments', null=True, blank=True)
    comment = models.CharField(max_length=256)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True)
    create_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ( '-id', )

    def __str__(self):
        return "{}".format(self.id)
