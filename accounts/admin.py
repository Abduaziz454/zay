from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from . import models


@admin.register(models.Customer)
class CustomerAdmin(UserAdmin):
    list_display = ("pk", "username", "first_name", "last_name", "email")
    list_display_links = ("username", )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email', "country", "city", "address")}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
