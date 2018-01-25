from django.contrib import admin

# Register your models here.
from .models import FriendshipRequest

@admin.register(FriendshipRequest)
class FriendshipRequestAdmin(admin.ModelAdmin):
    class Meta:
        model = FriendshipRequest
    list_display = ['from_user', 'to_user', 'rejected', 'rejected_dt', 'create_dt']
    list_editable = ['rejected']
