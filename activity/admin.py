from django.contrib import admin

# Register your models here.
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    class Meta:
        model = Notification

    list_display = [ 'from_user', 'to_user', 'notification_type', 'is_read']
    list_editable = ['is_read']