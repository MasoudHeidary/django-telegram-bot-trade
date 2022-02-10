from django.contrib import admin
from django.utils.html import format_html

from Bot.bot import bot
from Bot.models import TelegramUser
from WalletTransition.WalletRequest import cancel_buy_transition, cancel_sell_transition
from SiteSetting.SiteSettingRequest import point_fee
from WalletTransition.models import Transition

from .models import Point


@admin.action(description='لغو خرید امتیاز و برگشت به لیست')
def cancel_point_for_buyer(modeladmin, request, queryset):
    for point in queryset:
        point: Point

        # sign as not sell
        point.BuyID = '0'
        point.SellConf = False
        point.BuyConf = False
        point.Conf = False
        point.Time = None
        point.save()

        # relate to seller
        bot.deleteMessage(point.ChatID, point.SellerMessageID)

        cancel_message = "خریدار امتیاز از خرید خود منصرف شده است" \
                         "\n" \
                         " پیام مربوط به خریدار به صورت اتومات پاک شد، لطفا از انتقال امتیاز به خریدار" \
                         " خودداری بفرمایید." \
                         "\n" \
                         "با عرض معذرت و تشکر، پشیبانی ربات معاملاتی"
        bot.sendMessage(point.ChatID, cancel_message)

        # relate to buyer
        bot.deleteMessage(point.ChatIDBuyer, point.BuyerMessageID)
        bot.sendMessage(point.ChatIDBuyer, "خرید امتیاز شما توسط پشتیبانی لغو شد.")

        cancel_buy_transition(point.BuyTransition)


@admin.action(description='لغو فروش امتیاز و برگشت به لیست')
def cancel_point_for_seller(modeladmin, request, queryset):
    for point in queryset:
        point: Point

        # sign as noy bought
        point.SellID = '0'
        point.SellConf = False
        point.BuyConf = False
        point.Conf = False
        point.save()

        # relate to seller
        bot.deleteMessage(point.ChatIDSeller, point.SellerMessageID)
        bot.sendMessage(point.ChatIDSeller, "فروش امتیاز شما توسط پشتیبانی لغو شد.")

        # relate to buyer
        bot.deleteMessage(point.ChatIDBuyer, point.BuyerMessageID)

        cancel_message = "فروشنده امتیاز از فروش خود منصرف شده است" \
                         "\n" \
                         " پیام مربوط به فروشنده به صورت اتومات پاک شد، " \
                         "امتیازهای شما دوباره در صف خریداران قرار گرفت" \
                         "\n" \
                         "با عرض معذرت و تشکر، پشیبانی ربات معاملاتی"
        bot.sendMessage(point.ChatIDBuyer, cancel_message)

        cancel_sell_transition(point.SellTransition)


@admin.action(description='حذف کلی امتیاز')
def delete_point(modeladmin, request, queryset):
    for point in queryset:
        point: Point

        if point.Conf:
            # return money
            sell_tran = Transition.objects.get(id=point.SellTransition)
            buy_tran = Transition.objects.get(id=point.BuyTransition)

            # cancel seller side
            sell_tran.ToWallet.AvailableMoney -= (sell_tran.Value - sell_tran.Fee)
            sell_tran.ToWallet.save()
            sell_tran.delete()

            # cancel buyer side
            buy_tran.ToWallet.AvailableMoney += (buy_tran.Value + buy_tran.Fee)
            buy_tran.ToWallet.save()
            buy_tran.delete()

        else:
            cancel_buy_transition(point.BuyTransition)
            cancel_sell_transition(point.SellTransition)

        # messaging side
        bot.deleteMessage(
            point.ChatIDSeller,
            point.SellerMessageID
        )
        bot.sendMessage(
            point.ChatIDSeller,
            "فروش بسته امتیاز شما توسط پشتیبانی لغو گردید."
        )

        bot.deleteMessage(
            point.ChatIDBuyer,
            point.BuyerMessageID
        )
        bot.sendMessage(
            point.ChatIDBuyer,
            "خرید امتیاز شما توسط پشتیبانی لغو گردید."
        )

        # delete loan
        point.delete()


class PointAdmin(admin.ModelAdmin):
    list_display = ['id', 'Number', 'Price', 'profit', 'buyer_id', 'seller_id', 'Conf']
    list_filter = ['Price', 'Conf']
    search_fields = ['id', 'SellID', 'BuyID', 'ClubCode']
    actions = [cancel_point_for_buyer, cancel_point_for_seller, delete_point]

    @admin.display(description='میزان سود')
    def profit(self, obj):
        obj: Point
        if not obj.Conf:
            return 0

        fee_percent = float(point_fee())
        return (obj.Number * obj.Price / 10 * fee_percent * 2) // 100

    @admin.display(description='خریدار')
    def buyer_id(self, obj):
        obj: Point
        try:
            user = TelegramUser.objects.get(telegram_id=obj.BuyID)
            url = f'<a href="https://t.me/{user.username}">{user.username}</a>'
            return format_html(url)
        except:
            return "NONE"

    @admin.display(description="فروشنده")
    def seller_id(self, obj):
        obj: Point
        try:
            user = TelegramUser.objects.get(telegram_id=obj.SellID)
            url = f'<a href="https://t.me/{user.username}">{user.username}</a>'
            return format_html(url)
        except:
            return "NONE"

    class Meta:
        object = Point


admin.site.register(Point, PointAdmin)
