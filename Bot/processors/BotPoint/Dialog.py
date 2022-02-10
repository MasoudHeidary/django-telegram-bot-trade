from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Q
from Bot.bot import TelegramBot
from Bot.BotSetting import ChannelName, ReportChannel
from Bot.models import TelegramUser

from WalletTransition.models import Transition
from SiteSetting.SiteSettingRequest import point_fee

from ..BotComponent import ReplyKeyboardBack

from .Component import ReplyKeyboardPoint, ReplyKeyboardPointBuyFor, inline_keyboard_buyer_list_detail, \
    inline_keyboard_seller_list_detail, inline_keyboard_conf, inline_keyboard_cancel
from Point.models import Point


# -------------------------------------------- home

def go_point(chat_id, bot: TelegramBot):
    message = "بخش امتیازها ➕"
    bot.sendMessage(chat_id, message, reply_markup=ReplyKeyboardPoint)


def fail_point(chat_id, bot: TelegramBot):
    message = "لطفا از دستورات زیر استفاده کنید." \
              "👇"
    bot.sendMessage(chat_id, message, reply_markup=ReplyKeyboardPoint)


# ------------------------------------------------------------------------------- buy
def go_buy_point_number(chat_id, bot: TelegramBot):
    back_message = "🔙 در تمامی مراحل قابلیت بازگشت وجود دارد"
    bot.sendMessage(chat_id, back_message, reply_markup=ReplyKeyboardBack)

    message = "📌 لطفا تعداد امتیاز مورد نظر را با عدد لاتین مشخص نمایید."
    bot.sendMessage(chat_id, message)


def go_buy_point_price(chat_id, bot: TelegramBot):
    message = "📌 لطفا قیمت هر امتیاز را با عدد لاتین و به ریال مشخص نمایید."
    bot.sendMessage(chat_id, message)


def go_buy_point_for(chat_id, bot: TelegramBot):
    message = "📌 آیا امتیازها برای کد باشگاه شما منتقل شود یا شخص دیگر؟"
    bot.sendMessage(chat_id, message, reply_markup=ReplyKeyboardPointBuyFor)


def go_buy_point_for_other_name(chat_id, bot: TelegramBot):
    message = "📌 لطفا نام و نام خانوادگی خریدار را با خط تیره وارد کنید." \
              "\n" \
              "👈 مثل: رضا-عطاری"
    bot.sendMessage(chat_id, message)


def go_buy_point_for_other_club_code(chat_id, bot: TelegramBot):
    message = "📌 لطفا کد باشگاه خریدار را وارد کنید.(6حرف)"
    bot.sendMessage(chat_id, message)


def point_report(chat_id, point: Point, bot: TelegramBot):
    tran = Transition.objects.get(Q(id=point.BuyTransition) | Q(id=point.SellTransition))
    message = f"📃 رسید مشتری(خریدار)" \
              f"\n" \
              f"💢 امتیاز: " \
              f"({point.id})\n" \
              f"🔆 تعداد: " \
              f"{intcomma(point.Number)} " \
              f"عدد\n" \
              f"❌ قیمت هر امتیاز: " \
              f"{point.Price} " \
              f"ریال\n" \
              f"💰 قیمت کل: " \
              f"{intcomma(point.Price * point.Number // 10)}" \
              f" تومان\n" \
              f"🛠 کارمزد: " \
              f"{intcomma(tran.Fee)}" \
              f" تومان\n" \
              f"💵 مبلغ نهایی: " \
              f"{intcomma(tran.Value + tran.Fee)}" \
              f" تومان\n" \
              f"📌 توجه کارمزد لحاظ شده بابت هزینه های نگهداری ربات  می باشد.\n" \
              f"👈 میتوانید در درخواست های من در منوی امتیازها نسبت به لغو درخواست خود اقدام نمایید."
    bot.sendMessage(chat_id, message)

    # admin report channel
    bot.sendMessage(ReportChannel, message)


def point_channel(point: Point, bot: TelegramBot):
    message = f"📃 (خریدار)" \
              f"\n" \
              f"💢 امتیاز: " \
              f"({point.id})\n" \
              f"🔆 تعداد: " \
              f"{intcomma(point.Number)} " \
              f"عدد\n" \
              f"❌ قیمت هر امتیاز: " \
              f"{point.Price} " \
              f"ریال\n" \
              f"💰 قیمت کل: " \
              f"{intcomma(point.Price * point.Number // 10)}" \
              f" تومان\n" \
              f"\n\n"
    message += point_history_com()
    message += "\n\n" \
               "💡 برای فروش به خریدار این امتیاز و اطلاع از خریداران دیگر،" \
               " داخل ربات معاملات از منو امتیاز سپس فروش به لیست  اقدام نمایید.\n" \
               "🤖 @bashgahagahtradebot"
    bot.sendMessage(ChannelName, message)


# ------------------------------------------------------------------------------- sell

def go_sell_point_number(chat_id, bot: TelegramBot):
    back_message = "🔙 در تمامی مراحل قابلیت بازگشت وجود دارد"
    bot.sendMessage(chat_id, back_message, reply_markup=ReplyKeyboardBack)

    message = "📌 لطفا تعداد امتیاز مورد نظر را با عدد لاتین مشخص نمایید."
    bot.sendMessage(chat_id, message)


def go_sell_point_price(chat_id, bot: TelegramBot):
    message = "📌 لطفا قیمت هر امتیاز را با عدد لاتین و به ریال مشخص نمایید."
    bot.sendMessage(chat_id, message)


def point_report_for_seller(chat_id, point: Point, bot: TelegramBot):
    tran = Transition.objects.get(Q(id=point.BuyTransition) | Q(id=point.SellTransition))
    message = f"📃 رسید مشتری(فروشنده)" \
              f"\n" \
              f"💢 امتیاز: " \
              f"({point.id})\n" \
              f"🔆 تعداد: " \
              f"{intcomma(point.Number)} " \
              f"عدد\n" \
              f"❌ قیمت هر امتیاز: " \
              f"{point.Price} " \
              f"ریال\n" \
              f"💰 قیمت کل: " \
              f"{intcomma(point.Price * point.Number // 10)}" \
              f" تومان\n" \
              f"🛠 کارمزد: " \
              f"{intcomma(tran.Fee)}" \
              f" تومان\n" \
              f"💵 مبلغ نهایی: " \
              f"{intcomma(tran.Value - tran.Fee)}" \
              f" تومان\n" \
              f"📌 توجه کارمزد لحاظ شده بابت هزینه های نگهداری ربات  می باشد.\n" \
              f"👈 میتوانید در درخواست های من در منوی امتیازها نسبت به لغو درخواست خود اقدام نمایید." \
              f"\n" \
              f"⚠️ درصورت فروش امتیازها در جایی غیر از ربات امتیازهای مربوطه را حذف نمایید."
    bot.sendMessage(chat_id, message)

    # admin report channel
    bot.sendMessage(ReportChannel, message)


def point_channel_for_seller(point: Point, bot: TelegramBot):
    message = f"📃 (فروشنده)" \
              f"\n" \
              f"💢 امتیاز: " \
              f"({point.id})\n" \
              f"🔆 تعداد: " \
              f"{intcomma(point.Number)} " \
              f"عدد\n" \
              f"❌ قیمت هر امتیاز: " \
              f"{point.Price} " \
              f"ریال\n" \
              f"💰 قیمت کل: " \
              f"{intcomma(point.Price * point.Number // 10)}" \
              f" تومان\n" \
              f"\n\n"
    message += point_history_com()
    message += "\n\n" \
               "💡 برای خرید این امتیاز و اطلاع از امتیازهای موجود،" \
               " داخل ربات معاملات از منو امتیاز سپس خرید از لیست  اقدام نمایید.\n" \
               "🤖 @bashgahagahtradebot"

    bot.sendMessage(ChannelName, message)


# ------------------------------------------------------------------------------- buyer list

def buyer_list_pager(chat_id, qu, index_start, index_len, bot: TelegramBot):
    counter = 0
    for i in qu[index_start:index_start + index_len]:
        i: Point
        counter += 1

        message = f"💢 خریدار\n" \
                  f"امتیاز " \
                  f"({i.id})\n" \
                  f"🔆 تعداد: " \
                  f"{intcomma(i.Number)} " \
                  f"عدد\n" \
                  f"❌ قیمت هر امتیاز: " \
                  f"{i.Price} " \
                  f"ریال\n" \
                  f"💰 قیمت کل: " \
                  f"{intcomma((i.Price * i.Number // 10))}" \
                  f" تومان"

        bot.sendMessage(
            chat_id,
            message,
            reply_markup=inline_keyboard_buyer_list_detail(
                i.id,
                i.ChatID != chat_id,
                index_start + index_len if counter == index_len else False
            )
        )


def buyer_detail(chat_id, point: Point, bot: TelegramBot):
    tran = Transition.objects.get(id=point.SellTransition)
    message = f"📃 رسید مشتری\n" \
              f"مشخصات امتیاز برای انتقال \n" \
              f"💢 امتیاز " \
              f"({point.id})\n" \
              f"🔆 تعداد: " \
              f"{intcomma(point.Number)} " \
              f"عدد\n" \
              f"❌ قیمت هر امتیاز: " \
              f"{point.Price} " \
              f"ریال\n" \
              f"💰 قیمت کل: " \
              f"{intcomma(point.Price * point.Number // 10)}" \
              f" تومان\n" \
              f"🛠 کارمزد: " \
              f"{intcomma(tran.Fee)} " \
              f"تومان\n" \
              f"💵 مبلغ نهایی: " \
              f"{intcomma(tran.Value - tran.Fee)} " \
              f"تومان\n" \
              f"مشخصات خریدار\n" \
              f"{point.Name} - {point.Family} - {point.ClubCode}\n" \
              f"پس از انتقال امتیاز در باشگاه آگاه،" \
              f" در لیست انتظار تایید در منوی امتیازها، نسبت به تایید آن اقدام نمایید."

    sent_message = bot.sendMessage(chat_id, message)

    # save message that sent to seller
    point.SellerMessageID = sent_message.get_message_id()
    point.save()


def send_message_to_buyer(point: Point, bot: TelegramBot):
    seller = TelegramUser.objects.get(telegram_id=point.SellID)
    message = f"یک فروشنده با مشخصات زیر قصد انتقال امتیاز با مشخصات زیر را،" \
              f"\n" \
              f"امتیاز: " \
              f"({point.id})\n" \
              f"🔆 تعداد: " \
              f"{intcomma(point.Number)} " \
              f"عدد\n" \
              f"❌ قیمت هر امتیاز: " \
              f"{point.Price} " \
              f"ریال\n" \
              f"💰 قیمت کل: " \
              f"{intcomma(point.Price * point.Number // 10)}" \
              f" تومان\n" \
              f"{seller.profile.Name} - {seller.profile.Family} - {seller.profile.ClubCode}\n" \
              f" به شما دارد ، لطفا وارد باشگاه خود شده و امتیازها را در صورت صحیح بودن" \
              f" ، در  ربات در قسمت لیست انتظار تایید" \
              f"در منوی امتیازها  تایید کنید تا پول بحساب فروشنده واریز شود."

    sent_message = bot.sendMessage(point.ChatID, message)

    # admin report channel
    bot.sendMessage(ReportChannel, message)

    # save message that sent to buyer
    point.BuyerMessageID = sent_message.get_message_id()
    point.save()


# ------------------------------------------------------------------------------- seller list

def seller_list_pager(chat_id, qu, index_start, index_len, bot: TelegramBot):
    counter = 0
    for i in qu[index_start:index_start + index_len]:
        i: Point
        counter += 1

        message = f"💢 فروشنده\n" \
                  f"امتیاز " \
                  f"({i.id})\n" \
                  f"🔆 تعداد: " \
                  f"{intcomma(i.Number)} " \
                  f"عدد\n" \
                  f"❌ قیمت هر امتیاز: " \
                  f"{i.Price} " \
                  f"ریال\n" \
                  f"💰 قیمت کل: " \
                  f"{intcomma(int((i.Price * i.Number // 10) * (100 + point_fee()) // 100))}" \
                  f" تومان"
        bot.sendMessage(
            chat_id,
            message,
            reply_markup=inline_keyboard_seller_list_detail(
                i.id,
                i.ChatID != chat_id,
                index_start + index_len if counter == index_len else False
            )
        )


def go_sell_list_for(chat_id, bot: TelegramBot):
    message = "📌 آیا امتیازها برای کد باشگاه شما منتقل شود یا شخص دیگر؟"
    bot.sendMessage(chat_id, message, reply_markup=ReplyKeyboardPointBuyFor)


def seller_detail(chat_id, point: Point, bot: TelegramBot):
    tran = Transition.objects.get(id=point.BuyTransition)
    message = f"📃 رسید مشتری" \
              f"\n" \
              f"💢 امتیاز: " \
              f"({point.id})\n" \
              f"🔆 تعداد: " \
              f"{intcomma(point.Number)} " \
              f"عدد\n" \
              f"❌ قیمت هر امتیاز: " \
              f"{point.Price} " \
              f"ریال\n" \
              f"💰 قیمت کل: " \
              f"{intcomma(point.Price * point.Number // 10)}" \
              f" تومان\n" \
              f"🛠 کارمزد: " \
              f"{intcomma(tran.Fee)}" \
              f" تومان\n" \
              f"💵 مبلغ نهایی: " \
              f"{intcomma(tran.Value + tran.Fee)}" \
              f" تومان\n" \
              f"مشخصات فروشنده به شرح زیر است\n" \
              f"{point.Name} - {point.Family} - {point.ClubCode}\n" \
              f"📌 توجه کارمزد لحاظ شده بابت هزینه های نگهداری ربات  می باشد.\n" \
              f"پس از دریافت امتیاز در باشگاه آگاه،" \
              f" در لیست انتظار تایید در منوی امتیازها، نسبت به تایید آن اقدام نمایید."
    sent_message = bot.sendMessage(chat_id, message)

    # save message that sent to buyer
    point.BuyerMessageID = sent_message.get_message_id()
    point.save()


def send_message_to_seller_for_me(user_id, point: Point, bot: TelegramBot):
    user = TelegramUser.objects.get(telegram_id=user_id)
    message = f"📌 یک خریدار با مشخصات زیر قصد خرید امتیازهای شما را دارد،" \
              f"مشخصات امتیاز به شرح زیر است\n" \
              f"💢 امتیاز: " \
              f"({point.id})\n" \
              f"🔆 تعداد: " \
              f"{intcomma(point.Number)} " \
              f"عدد\n" \
              f"❌ قیمت هر امتیاز: " \
              f"{point.Price} " \
              f"ریال\n" \
              f"💰 قیمت کل: " \
              f"{intcomma(point.Price * point.Number // 10)}" \
              f" تومان\n" \
              f"مشخصات خریدار" \
              f"\n{user.profile.Name} - {user.profile.Family} - {user.profile.ClubCode}\n" \
              f"پس از انتقال امتیاز به باشگاه آگاه خریدار،" \
              f" در لیست انتظار تایید در منوی امتیازها، نسبت به تایید آن اقدام نمایید."
    sent_message = bot.sendMessage(point.ChatID, message)

    # admin report channel
    bot.sendMessage(ReportChannel, message)

    # save message that sent to seller
    point.SellerMessageID = sent_message.get_message_id()
    point.save()


def send_message_to_seller_for_other(name, family, club_code, point: Point, bot: TelegramBot):
    message = f"📌 یک خریدار با مشخصات زیر قصد خرید امتیازهای شما را دارد،" \
              f"مشخصات امتیاز به شرح زیر است\n" \
              f"💢 امتیاز: " \
              f"({point.id})\n" \
              f"🔆 تعداد: " \
              f"{intcomma(point.Number)} " \
              f"عدد\n" \
              f"❌ قیمت هر امتیاز: " \
              f"{point.Price} " \
              f"ریال\n" \
              f"💰 قیمت کل: " \
              f"{intcomma(point.Price * point.Number // 10)}" \
              f"\n تومان" \
              f"مشخصات خریدار" \
              f"\n{name} - {family} - {club_code}\n" \
              f"پس از انتقال امتیاز به باشگاه آگاه خریدار،" \
              f" در لیست انتظار تایید در منوی امتیازها، نسبت به تایید آن اقدام نمایید."
    sent_message = bot.sendMessage(point.ChatID, message)

    # admin report channel
    bot.sendMessage(ReportChannel, message)

    # save message that sent to seller
    point.SellerMessageID = sent_message.get_message_id()
    point.save()


# ------------------------------------------------------------------------------- Request

def go_my_request(chat_id, user_id, bot: TelegramBot):
    as_buyer = Point.objects.filter(BuyID=user_id)
    bot.sendMessage(chat_id, 'درخواست های خرید:')
    if not as_buyer:
        bot.sendMessage(chat_id, 'درخواست خریدی نداشته اید!')
    else:
        for i in as_buyer:
            message = f"امتیاز " \
                      f"({i.id})\n" \
                      f"🔆 تعداد: " \
                      f"{intcomma(i.Number)} " \
                      f"عدد\n" \
                      f"❌ قیمت هر امتیاز: " \
                      f"{i.Price} " \
                      f"ریال\n" \
                      f"💰 قیمت کل: " \
                      f"{intcomma(i.Price * i.Number // 10)}" \
                      f" تومان"
            if i.SellID == '0':
                bot.sendMessage(chat_id, message, reply_markup=inline_keyboard_cancel(i.id))
            else:
                bot.sendMessage(chat_id, message)

    as_seller = Point.objects.filter(SellID=user_id)
    bot.sendMessage(chat_id, 'درخواست های فروش:')
    if not as_seller:
        bot.sendMessage(chat_id, 'درخواست فروشی نداشته اید!')
    else:
        for i in as_seller:
            message = f"امتیاز " \
                      f"({i.id})\n" \
                      f"🔆 تعداد: " \
                      f"{intcomma(i.Number)} " \
                      f"عدد\n" \
                      f"❌ قیمت هر امتیاز: " \
                      f"{i.Price} " \
                      f"ریال\n" \
                      f"💰 قیمت کل: " \
                      f"{intcomma(i.Price * i.Number // 10)}" \
                      f" تومان"
            if i.BuyID == '0':
                bot.sendMessage(chat_id, message, reply_markup=inline_keyboard_cancel(i.id))
            else:
                bot.sendMessage(chat_id, message)


# ------------------------------------------------------------------------------- Conf

def go_conf(chat_id, user_id, bot: TelegramBot):
    message = "اگر فروشنده هستید، و امتیاز را منتقل کرده اید، آن را تایید کنید\n" \
              "اگر خریدار هستید، و امتیاز به حساب باشگاه شما آمده و توسط کارگزاری نیز تایید شده است، آن را تایید کنید\n" \
              "⭐ در غیر این صورت مراقب باشید که در صورت تایید اشتباه، ربات معاملاتی باشگاه، مسئولیتی ندارد."

    bot.sendMessage(chat_id, message)

    as_buyer = Point.objects.filter(BuyID=user_id, Conf=False).filter(~Q(SellID='0'))
    for i in as_buyer:
        message = f"خریدار بوده اید\n" \
                  f"امتیاز " \
                  f"({i.id})\n" \
                  f"🔆 تعداد: " \
                  f"{intcomma(i.Number)} " \
                  f"عدد\n" \
                  f"❌ قیمت هر امتیاز: " \
                  f"{i.Price} " \
                  f"ریال\n" \
                  f"💰 قیمت کل: " \
                  f"{intcomma(i.Price * i.Number // 10)}" \
                  f" تومان\n" \
                  f"وضعیت تایید فروشنده: " \
                  f"{'تایید شده' if i.SellConf else 'در انتظار تایید'}\n" \
                  f"وضعیت تایید خریدار: " \
                  f"{'تایید شده' if i.BuyConf else 'در انتظار تایید'}"
        bot.sendMessage(chat_id, message, reply_markup=inline_keyboard_conf(i.id))

    as_seller = Point.objects.filter(SellID=user_id, Conf=False).filter(~Q(BuyID='0'))
    for i in as_seller:
        message = f"فروشنده بوده اید\n" \
                  f"امتیاز " \
                  f"({i.id})\n" \
                  f"🔆 تعداد: " \
                  f"{intcomma(i.Number)} " \
                  f"عدد\n" \
                  f"❌ قیمت هر امتیاز: " \
                  f"{i.Price} " \
                  f"ریال\n" \
                  f"💰 قیمت کل: " \
                  f"{intcomma(i.Price * i.Number // 10)}" \
                  f" تومان\n" \
                  f"وضعیت تایید فروشنده: " \
                  f"{'تایید شده' if i.SellConf else 'در انتظار تایید'}\n" \
                  f"وضعیت تایید خریدار: " \
                  f"{'تایید شده' if i.BuyConf else 'در انتظار تایید'}"
        bot.sendMessage(chat_id, message, reply_markup=inline_keyboard_conf(i.id))


# ------------------------------------------------------- history
def point_history(chat_id, bot: TelegramBot):
    message = point_history_com()
    bot.sendMessage(chat_id, message)


def point_history_com():
    point = Point.objects.filter(Conf=True)
    message = "📊 رنج های قیمتی معامله شده به ترتیب:" \
              "\n"

    price = set()
    for i in point:
        price.add(i.Price)

    for i in price:
        counter = 0
        point_list = Point.objects.filter(Price=i, Conf=True)
        for obj in point_list:
            counter += obj.Number

        message += f"✅ {intcomma(i)}" \
                   f"ریال" \
                   f"- {intcomma(counter)}" \
                   f" امتیاز" \
                   f"\n"
    return message
