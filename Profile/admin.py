from django.contrib import admin
from django.utils.html import format_html

from .models import Profile


# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'telegram_id', 'telegram_id_url', 'Name', 'Family', 'ClubCode', 'ToTelegramUser']
    list_filter = ['UserConf']
    search_fields = ['id', 'ClubCode', 'ToTelegramUser__telegram_id', 'Name', 'Family', 'PhoneNumber']

    @admin.display(ordering='ToTelegramUser__telegram_id')
    def telegram_id(self, obj: Profile):
        try:
            return obj.ToTelegramUser.telegram_id
        except:
            return 'no telegram id'

    @admin.display(description="تلگرام")
    def telegram_id_url(self, obj):
        obj: Profile

        try:
            username = obj.ToTelegramUser.username
            url = f'<a href="https://t.me/{username}">{username}</a>'
            return format_html(url)
        except:
            return "NOT SUPPORT"

    class Meta:
        object = Profile


admin.site.register(Profile, ProfileAdmin)
