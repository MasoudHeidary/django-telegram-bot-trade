from django.contrib import admin
from django.utils.html import format_html

from .models import CreditPack, CreditPackSiteSetting

from Bot.bot import bot
from Bot.models import TelegramUser
from CreditPack.CreditPackRequest import cancel_buy_transition, cancel_sell_transition
from .CreditPackRequest import credit_packet_fee_percent
from WalletTransition.models import Transition


@admin.action(description='لغو خرید بسته و برگشت به لیست')
def cancel_credit_for_buyer(modeladmin, request, queryset):
    for credit in queryset:
        credit: CreditPack

        # sign as not sell
        credit.BuyID = '0'
        credit.SellConf = False
        credit.BuyConf = False
        credit.Conf = False
        credit.Time = None
        credit.save()

        # relate to seller
        bot.deleteMessage(credit.ChatID, credit.SellerMessageID)

        cancel_message = "خریدار بسته اعتباری از خرید خود منصرف شده است" \
                         "\n" \
                         " پیام مربوط به خریدار به صورت اتومات پاک شد، لطفا از انتقال بسته اعتباری به خریدار" \
                         " خودداری بفرمایید." \
                         "\n" \
                         "با عرض معذرت و تشکر، پشیبانی ربات معاملاتی"
        bot.sendMessage(credit.ChatID, cancel_message)

        # relate to buyer
        bot.deleteMessage(credit.ChatIDBuyer, credit.BuyerMessageID)
        bot.sendMessage(credit.ChatIDBuyer, "خرید بسته اعتباری شما توسط پشتیبانی لغو شد.")

        cancel_buy_transition(credit.BuyTransition)


@admin.action(description='لغو فروش بسته و برگشت به لیست')
def cancel_credit_for_seller(modeladmin, request, queryset):
    for credit in queryset:
        credit: CreditPack

        # sign as noy bought
        credit.SellID = '0'
        credit.SellConf = False
        credit.BuyConf = False
        credit.Conf = False
        credit.save()

        # relate to seller
        bot.deleteMessage(credit.ChatIDSeller, credit.SellerMessageID)
        bot.sendMessage(credit.ChatIDSeller, "فروش بسته اعتباری شما توسط پشتیبانی لغو شد.")

        # relate to buyer
        bot.deleteMessage(credit.ChatIDBuyer, credit.BuyerMessageID)

        cancel_message = "فروشنده بسته اعتباری از فروش خود منصرف شده است" \
                         "\n" \
                         " پیام مربوط به فروشنده به صورت اتومات پاک شد، " \
                         "بسته اعتباری شما دوباره در صف خریداران قرار گرفت" \
                         "\n" \
                         "با عرض معذرت و تشکر، پشیبانی ربات معاملاتی"
        bot.sendMessage(credit.ChatIDBuyer, cancel_message)

        cancel_sell_transition(credit.SellTransition)

@admin.action(description='حذف کلی بسته اعتباری')
def delete_credit(modeladmin, request, queryset):
    for credit in queryset:
        credit: CreditPack

        if credit.Conf:
            # return money
            sell_tran = Transition.objects.get(id=credit.SellTransition)
            buy_tran = Transition.objects.get(id=credit.BuyTransition)

            # cancel seller side
            sell_tran.ToWallet.AvailableMoney -= (sell_tran.Value - sell_tran.Fee)
            sell_tran.ToWallet.save()
            sell_tran.delete()

            # cancel buyer side
            buy_tran.ToWallet.AvailableMoney += (buy_tran.Value + buy_tran.Fee)
            buy_tran.ToWallet.save()
            buy_tran.delete()

        else:
            cancel_buy_transition(credit.BuyTransition)
            cancel_sell_transition(credit.SellTransition)

        # messaging side
        bot.deleteMessage(
            credit.ChatIDSeller,
            credit.SellerMessageID
        )
        bot.sendMessage(
            credit.ChatIDSeller,
            "فروش بسته اعتباری شما توسط پشتیبانی لغو گردید."
        )

        bot.deleteMessage(
            credit.ChatIDBuyer,
            credit.BuyerMessageID
        )
        bot.sendMessage(
            credit.ChatIDBuyer,
            "خرید بسته اعتباری شما توسط پشتیبانی لغو گردید."
        )

        # delete loan
        credit.delete()

class CreditPackAdmin(admin.ModelAdmin):
    list_display = ['id', 'Value', 'Price', 'Duration', 'profit', 'Time', 'buyer_id', 'seller_id', 'Conf']
    search_fields = ['id', 'SellID', 'BuyID', 'ClubCode']
    list_filter = ['Value', 'Time', 'Conf']
    actions = [cancel_credit_for_buyer, cancel_credit_for_seller, delete_credit]

    @admin.display(description='میزان سود')
    def profit(self, obj):
        obj: CreditPack
        if not obj.Conf:
            return 0

        fee_percent = credit_packet_fee_percent(obj.Value, obj.Duration)
        return (obj.Price * fee_percent * 2) // 100

    @admin.display(description='خریدار')
    def buyer_id(self, obj):
        obj: CreditPack
        try:
            user = TelegramUser.objects.get(telegram_id=obj.BuyID)
            url = f'<a href="https://t.me/{user.username}">{user.username}</a>'
            return format_html(url)
        except:
            return "NONE"

    @admin.display(description="فروشنده")
    def seller_id(self, obj):
        obj: CreditPack
        try:
            user = TelegramUser.objects.get(telegram_id=obj.SellID)
            url = f'<a href="https://t.me/{user.username}">{user.username}</a>'
            return format_html(url)
        except:
            return "NONE"

    class Meta:
        object = CreditPack


class CreditPackSiteSettingAdmin(admin.ModelAdmin):
    list_display = ['Value', 'Duration', 'Price', 'FeePercent']

    class Meta:
        object = CreditPackSiteSetting


admin.site.register(CreditPack, CreditPackAdmin)
admin.site.register(CreditPackSiteSetting, CreditPackSiteSettingAdmin)
