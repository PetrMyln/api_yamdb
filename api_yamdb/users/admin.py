from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'bio',)
    list_editable = ('role', 'bio')


admin.site.register(User, UserAdmin)
