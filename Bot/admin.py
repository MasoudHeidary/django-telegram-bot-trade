from django.contrib import admin
from .models import TelegramUser, TelegramChat, TelegramState


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'telegram_id', 'username', 'first_name', 'last_name']
    search_fields = ['id', 'telegram_id', 'username']

    class Meta:
        object = TelegramUser


class TelegramStateAdmin(admin.ModelAdmin):
    list_display = ['id', 'telegram_user_username', 'telegram_user_telegram_id', 'name']
    search_fields = ['id', 'telegram_user__telegram_id']

    @admin.display(ordering='telegram_user__telegram_id')
    def telegram_user_telegram_id(self, obj):
        try:
            return obj.telegram_user.telegram_id
        except:
            return "no telegram id"

    @admin.display(ordering='telegram_user__username')
    def telegram_user_username(self, obj):
        try:
            return obj.telegram_user.username
        except:
            return 'none'

    class Meta:
        obj = TelegramState


admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(TelegramChat)
admin.site.register(TelegramState, TelegramStateAdmin)
