from django.contrib import admin
from django.utils.html import format_html

from .models import Loan, LoanSiteSetting

from Bot.bot import bot
from Bot.models import TelegramUser
from Loan.LoanRequest import cancel_buy_transition, cancel_sell_transition, loan_fee_percent
from WalletTransition.models import Transition


@admin.action(description='لغو خرید و برگشت به لیست')
def cancel_loan_for_buyer(modeladmin, request, queryset):
    for loan in queryset:
        loan: Loan

        # sign as not sell
        loan.BuyID = '0'
        loan.SellConf = False
        loan.BuyConf = False
        loan.Conf = False
        loan.Time = None
        loan.save()

        # relate to seller
        bot.deleteMessage(loan.ChatID, loan.SellerMessageID)

        cancel_message = "خریدار وام از خرید خود منصرف شده است" \
                         " پیام مربوط به خریدار به صورت اتومات پاک شد، لطفا از انتقال وام به خریدار" \
                         " خودداری بفرمایید." \
                         "\n" \
                         "با عرض معذرت و تشکر، پشیبانی ربات معاملاتی"
        bot.sendMessage(loan.ChatID, cancel_message)

        # relate to buyer
        bot.deleteMessage(loan.ChatIDBuyer, loan.BuyerMessageID)
        bot.sendMessage(loan.ChatIDBuyer, "خرید وام شما توسط پشتیبانی لغو شد.")

        cancel_buy_transition(loan.BuyTransition)


@admin.action(description='لغو فروش وام و برگشت به لیست')
def cancel_loan_for_seller(modeladmin, request, queryset):
    for loan in queryset:
        loan: Loan

        # sign as noy bought
        loan.SellID = '0'
        loan.SellConf = False
        loan.BuyConf = False
        loan.Conf = False
        loan.save()

        # relate to seller
        bot.deleteMessage(loan.ChatIDSeller, loan.SellerMessageID)
        bot.sendMessage(loan.ChatIDSeller, "فروش وام شما توسط پشتیبانی لغو شد.")

        # relate to buyer
        bot.deleteMessage(loan.ChatIDBuyer, loan.BuyerMessageID)

        cancel_message = "فروشنده وام از فروش خود منصرف شده است" \
                         "\n" \
                         " پیام مربوط به فروشنده به صورت اتومات پاک شد، " \
                         "وام شما دوباره در صف خریداران قرار گرفت" \
                         "\n" \
                         "با عرض معذرت و تشکر، پشیبانی ربات معاملاتی"
        bot.sendMessage(loan.ChatIDBuyer, cancel_message)

        cancel_sell_transition(loan.SellTransition)


@admin.action(description='حذف کلی وام')
def delete_loan(modeladmin, request, queryset):
    for loan in queryset:
        loan: Loan

        if loan.Conf:
            # return money
            sell_tran = Transition.objects.get(id=loan.SellTransition)
            buy_tran = Transition.objects.get(id=loan.BuyTransition)

            # cancel seller side
            sell_tran.ToWallet.AvailableMoney -= (sell_tran.Value - sell_tran.Fee)
            sell_tran.ToWallet.save()
            sell_tran.delete()

            # cancel buyer side
            buy_tran.ToWallet.AvailableMoney += (buy_tran.Value + buy_tran.Fee)
            buy_tran.ToWallet.save()
            buy_tran.delete()

        else:
            cancel_buy_transition(loan.BuyTransition)
            cancel_sell_transition(loan.SellTransition)

        # messaging side
        bot.deleteMessage(
            loan.ChatIDSeller,
            loan.SellerMessageID
        )
        bot.sendMessage(
            loan.ChatIDSeller,
            "فروش وام شما توسط پشتیبانی لغو گردید."
        )

        bot.deleteMessage(
            loan.ChatIDBuyer,
            loan.BuyerMessageID
        )
        bot.sendMessage(
            loan.ChatIDBuyer,
            "خرید وام شما توسط پشتیبانی لغو گردید."
        )

        # delete loan
        loan.delete()


class LoanAdmin(admin.ModelAdmin):
    list_display = ['id', 'Value', 'Duration', 'Price', 'Time', 'profit', 'buyer_id', 'seller_id', 'Conf']
    list_filter = ['Value', 'Duration', 'Conf']
    search_fields = ['id', 'SellID', 'BuyID', 'ClubCode']
    actions = [cancel_loan_for_buyer, cancel_loan_for_seller, delete_loan]

    @admin.display(description='میزان سود')
    def profit(self, obj):
        obj: Loan
        if not obj.Conf:
            return 0

        fee_percent = loan_fee_percent(obj.Value, obj.Duration)
        return obj.Price * fee_percent * 2 // 100

    @admin.display(description='خریدار')
    def buyer_id(self, obj):
        obj: Loan
        try:
            user = TelegramUser.objects.get(telegram_id=obj.BuyID)
            url = f'<a href="https://t.me/{user.username}">{user.username}</a>'
            return format_html(url)
        except:
            return "NONE"

    @admin.display(description="فروشنده")
    def seller_id(self, obj):
        obj: Loan
        try:
            user = TelegramUser.objects.get(telegram_id=obj.SellID)
            url = f'<a href="https://t.me/{user.username}">{user.username}</a>'
            return format_html(url)
        except:
            return "NONE"

    class Meta:
        object = Loan


class LoanSiteSettingAdmin(admin.ModelAdmin):
    list_display = ['Value', 'Duration', 'Price', 'FeePercent']

    class Meta:
        object = LoanSiteSetting


admin.site.register(Loan, LoanAdmin)
admin.site.register(LoanSiteSetting, LoanSiteSettingAdmin)
