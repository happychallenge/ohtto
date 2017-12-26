from django.db import models
from django.conf import settings
from django.utils.html import escape

from blog.models import Post, Theme

# Create your models here.
class Notification(models.Model):
    LIKED = 'PL'
    COMMENTED = 'PC'
    BUCKET = 'PC'
    THEME = 'TM'
    INVITED = 'IV'

    NOTIFICATION_TYPES = (
        (LIKED, 'Liked'),
        (COMMENTED, 'Commented'),
        (BUCKET, 'Bucket'),
        (THEME, 'Theme'),
        (INVITED, 'Invited'),
    )

    _LIKED_TEMPLATE = '<a href="/user/{0}/">{1}</a> liked your post: <a href="/post/{2}/">{3}</a>' 
    _COMMENTED_TEMPLATE = '<a href="/user/{0}/">{1}</a> commented on your post: <a href="/post/{2}/">{3}</a>' 
    _BUCKET_TEMPLATE = '<a href="/user/{0}/">{1}</a> favorited your question: <a href="/post/{2}/">{3}</a>'

    _THEME_TEMPLATE = '<a href="/user/{0}/">{1}</a> invited you for his a theme: <a href="/blog/{2}/{3}/">{4}</a>' 

    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    post = models.ForeignKey(Post, null=True, blank=True)
    theme = models.ForeignKey(Theme, null=True, blank=True)
    notification_type = models.CharField(max_length=2, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    create_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-create_dt',)

    def __str__(self):
        if self.notification_type == self.LIKED:
            return self._LIKED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.first_name),
                self.post.pk,
                escape(self.post.pk)
                )
        elif self.notification_type == self.COMMENTED:
            return self._COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.first_name),
                self.post.pk,
                escape(self.post.pk)
                )
        elif self.notification_type == self.BUCKET:
            return self._BUCKET_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.first_name),
                self.post.pk,
                escape(self.post.pk)
                )
        elif self.notification_type == self.THEME:
            return self._THEME_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.first_name),
                escape(self.from_user.username),
                self.theme.pk,
                escape(self.theme.name)
                )
        else:
            return 'Ooops! Something went wrong.'

