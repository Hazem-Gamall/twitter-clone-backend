from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.unregister(User)


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "id")
    readonly_fields = ("id",)


admin.site.register(User, CustomUserAdmin)

admin.site.register(UserProfile)
