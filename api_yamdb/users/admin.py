from api_yamdb.constant import ADDITIONAL_USER_FIELDS
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User


class UserAdmin(BaseUserAdmin):

    list_display = ('username', 'email', 'role', 'bio',)
    list_editable = ('role', 'bio')
    add_fieldsets = BaseUserAdmin.add_fieldsets + ADDITIONAL_USER_FIELDS
    fieldsets = BaseUserAdmin.fieldsets + ADDITIONAL_USER_FIELDS


admin.site.register(User, UserAdmin)
