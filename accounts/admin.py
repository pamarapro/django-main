from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Account, UserProfile
from django.utils.html import format_html
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login','date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    search_fields = ('username', 'first_name', 'last_name', 'email')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    def thumnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%";>'.format(object.profile_picture.url))
    thumnail.short_description = "Profile Picture"
    list_display = ['thumnail', 'user', 'state', 'city']


admin.site.register(Account,)
admin.site.register(UserProfile, UserProfileAdmin) 