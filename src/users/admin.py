from django.contrib import admin
from django.contrib.auth.models import Group
from .models import UserProfile, User


class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'admin', 'staff')

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'name', 'surname', 'photo')


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)