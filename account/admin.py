from django.contrib import admin

from .models import Profile, Relation
# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = Profile
    list_display = ['user', 'birthdate']


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    class Meta:
        model = Relation
    list_display = ['from_user', 'to_user']
