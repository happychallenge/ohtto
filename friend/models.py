from django.db import models

from account.models import Profile
# Create your models here.
class FriendshipRequest(models.Model):
    """ Model to represent friendship requests """
    from_user = models.ForeignKey(Profile, related_name='friend_sent')
    to_user = models.ForeignKey(Profile, related_name='friend_received')

    message = models.TextField(_('Message'), blank=True)

    created = models.DateTimeField(default=timezone.now)
    rejected = models.DateTimeField(blank=True, null=True)
    viewed = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _('Friendship Request')
        verbose_name_plural = _('Friendship Requests')
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return "User #%s friendship requested #%s" % (self.from_user_id, self.to_user_id)
