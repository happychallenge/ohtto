from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from activity.models import Notification
# Create your models here.
class Profile(models.Model):
    """docstring for Person"""
    """ 기억할 인물에 대한 설명 """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    birthdate = models.DateTimeField(_('Birth Date'), null=True, blank=True)
    picture = models.ImageField('', upload_to='person_profile/%Y/%m/',
                     null=True, blank=True)
    friend_set = models.ManyToManyField('self',
                                    blank=True,
                                    through='Relation',
                                    symmetrical=False, )
    num = models.IntegerField(_('UID'), null=True, blank=True)
    create_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname

    @property
    def get_follower(self):
        return [i.from_user for i in self.follower_user.all()]

    @property
    def get_following(self):
        return [i.to_user for i in self.follow_user.all()]

    @property
    def follower_count(self):
        return len(self.get_follower) - 1

    @property
    def following_count(self):
        return len(self.get_following) - 1

    def is_follower(self, user):
        return user in self.get_follower

    def is_following(self, user):
        return user in self.get_following

    @property
    def get_bucket_list(self):
        return [i.post for i in self.user.buckets.all()]

    @property
    def bucket_count(self):
        return self.user.buckets.count()

    @property
    def get_post_list(self):
        user = self.user
        return [i.post for i in user.posts.all()]

    @property
    def get_invited_theme(self):
        user = self.user
        return [i.theme for i in user.invitee_set.all()]

    @property
    def post_count(self):
        user = self.user
        return user.posts.count()

    def get_theme_list(self):
        user = self.user
        return user.themes.all()

    def notify_post_liked(self, post):
        if self.user != post.author:
            Notification(notification_type=Notification.LIKED, 
                from_user=self.user, to_user=post.author,
                post=post).save()

    def notify_post_unliked(self, post):
        if self.user != post.author:
            Notification.objects.filter(notification_type=Notification.LIKED,
                from_user=self.user, to_user=post.author,post=post).delete()

    def notify_post_commented(self, post):
        if self.user != post.author:
            Notification(notification_type=Notification.COMMENTED, 
                from_user=self.user, to_user=post.author,
                post=post).save()

    def notify_post_bucketed(self, post):
        if self.user != post.author:
            Notification(notification_type=Notification.BUCKET, 
                from_user=self.user, to_user=post.author,
                post=post).save()

    def notify_post_unbucketed(self, post):
        if self.user != post.author:
            Notification(notification_type=Notification.BUCKET, 
                from_user=self.user, to_user=post.author,
                post=post).delete()

    def notify_theme_invited(self, theme, to_user):
        if self.user != theme.author:
            Notification(notification_type=Notification.INVITED,
                    from_user=self.user, to_user=to_user, 
                    theme=theme).save()


class Relation(models.Model):
    FRIEND = 'F'
    BREAK = 'B'
    REJECT = 'R'
    STATUS = (
        (FRIEND, 'Friend'),
        (BREAK, 'Break'),
        (REJECT, 'Reject'),
    )
    from_user = models.ForeignKey(Profile, related_name='follow_user')
    to_user = models.ForeignKey(Profile, related_name='follower_user')
    status = models.CharField(max_length=1, choices=STATUS, default=FRIEND)
    create_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} -> {}".format(self.from_user, self.to_user)

    class Meta:
        unique_together = (
            ('from_user', 'to_user')
        )



def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, nickname=instance.first_name)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)
post_save.connect(save_user_profile, sender=settings.AUTH_USER_MODEL)