from django.contrib import admin
from .models import Wallet, Transition


# Register your models here.

class WalletAdmin(admin.ModelAdmin):
    list_display = ['id', 'telegram_id', 'AvailableMoney', 'BlockedMoney']
    search_fields = ['id', 'ToTelegramUser__telegram_id']

    @admin.display(ordering='ToTelegramUser__telegram_id')
    def telegram_id(self, obj: Wallet):
        try:
            return obj.ToTelegramUser.telegram_id
        except:
            return 'no telegram id'

    class Meta:
        object = Wallet


class TransitionAdmin(admin.ModelAdmin):
    list_display = ['id', 'telegram_id', 'wallet_id', 'Value', 'Fee', 'Time', 'Cause']
    search_fields = ['id', 'ToWallet__ToTelegramUser__telegram_id', 'ToWallet__id', 'Cause', 'Value']
    list_filter = ['Done']

    @admin.display(ordering='ToWallet__id')
    def wallet_id(self, obj: Transition):
        try:
            return obj.ToWallet.id
        except:
            return 'no wallet id'

    @admin.display(ordering='ToWallet__ToTelegramUser__telegram_id')
    def telegram_id(self, obj: Transition):
        try:
            return obj.ToWallet.ToTelegramUser.telegram_id
        except:
            return 'no telegram id'

    class Meta:
        object = Transition


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transition, TransitionAdmin)
