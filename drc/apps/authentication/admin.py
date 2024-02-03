from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from . import models


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.User
        fields = ('email', 'username', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm

    list_display = ('email', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'username','password')}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )
    ordering = () 

admin.site.register(models.User, UserAdmin)
