from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Q
from Bot.bot import TelegramBot
from Bot.BotSetting import ChannelName, ReportChannel
from Bot.models import TelegramUser

from .Component import ReplyKeyboardCredit, InlineKeyboardCreditValue, InlineKeyboardCreditDuration, \
    ReplyKeyboardCreditBuyFor, ReplyKeyboardBuyListMonth, \
    inline_keyboard_buyer_list_detail, inline_keyboard_seller_list_detail, \
    inline_keyboard_conf, inline_keyboard_cancel, inline_keyboard_valid_days, ReplyKeyboardBuyListValue

from ..BotComponent import ReplyKeyboardBack

from CreditPack.models import CreditPack
from CreditPack.CreditPackRequest import credit_real_price
from WalletTransition.models import Transition
# from SiteSetting.SiteSettingRequest import credit_pack_fee
from CreditPack.CreditPackRequest import credit_packet_fee_percent


# -------------------------------------------- home

def go_credit(chat_id, bot: TelegramBot):
    message = "📌 جهت درخواست خرید یا فروش بسته اعتباری یکی از موارد را انتخاب نمایید."
    bot.sendMessage(chat_id, message, reply_markup=ReplyKeyboardCredit)


def fail_credit(chat_id, bot: TelegramBot):
    message = "لطفا از دستورات زیر استفاده کنید." \
              "👇"
    bot.sendMessage(chat_id, message, reply_markup=ReplyKeyboardCredit)


# ------------------------------------------------------------------------------- buy
def go_buy_credit_value(chat_id, bot: TelegramBot):
    back_message = "🔙 در تمامی مراحل قابلیت بازگشت وجود دارد"
    bot.sendMessage(chat_id, back_message, reply_markup=ReplyKeyboardBack)

    message = "📌 لطفا یکی از بسته های اعتباری زیر را انتخاب نمایید."
    bot.sendMessage(chat_id, message, reply_markup=InlineKeyboardCreditValue)


def go_buy_credit_duration(chat_id, bot: TelegramBot):
    message = "📌 لطفا مدت زمان بسته اعتباری را انتخاب نمایید."
    bot.sendMessage(chat_id, message, reply_markup=InlineKeyboardCreditDuration)


def go_buy_credit_time(chat_id, bot: TelegramBot):
    message = "📌 لطفا تاریخ اعمال بسته اعتباری را انتخاب نمایید."
    bot.sendMessage(chat_id, message, reply_markup=inline_keyboard_valid_days())


def go_buy_credit_price(chat_id, bot: TelegramBot):
    message = "📌 لطفا قیمت بسته اعتباری را با عدد لاتین و به تومان مشخص نمایید."
    bot.sendMessage(chat_id, message)


def go_buy_credit_for(chat_id, bot: TelegramBot):
    message = "📌 آیا بسته اعتباری برای کد باشگاه شما منتقل شود یا شخص دیگر؟"
    bot.sendMessage(chat_id, message, reply_markup=ReplyKeyboardCreditBuyFor)


def go_buy_credit_for_other_name(chat_id, bot: TelegramBot):
    message = "📌 لطفا نام و نام خانوادگی خریدار را با خط تیره وارد کنید." \
              "\n" \
              "👈 مثل: رضا-عطاری"
    bot.sendMessage(chat_id, message)


def go_buy_credit_for_other_club_code(chat_id, bot: TelegramBot):
    message = "📌 لطفا کد باشگاه خریدار را وارد کنید.(6حرف)"
    bot.sendMessage(chat_id, message)


def credit_report(chat_id, credit: CreditPack, bot: TelegramBot):
    tran = Transition.objects.get(Q(id=credit.BuyTransition) | Q(id=credit.SellTransition))
    message = f"📃 رسید مشتری(خریدار)" \
              f"\n" \
              f"💢 بسته اعتباری: " \
              f"({credit.id})\n" \
              f"💹 ارزش بسته اعتباری: " \
              f"{credit.Value} " \
              f"میلیون تومان\n" \
              f"💰 مبلغ تعیین شده: " \
              f"{intcomma(credit.Price)}" \
              f"تومان\n" \
              f"🗓 مدت زمان: " \
              f"{credit.Duration} " \
              f"ماه\n" \
              f"📆 تاریخ اعمال بسته اعتباری: " \
              f"{credit.Time}\n" \
              f"🛠 کارمزد: " \
              f"{intcomma(tran.Fee)}" \
              f" تومان\n" \
              f"💵 مبلغ نهایی: " \
              f"{intcomma(credit.Price + tran.Fee)}" \
              f" تومان\n" \
              f"📌 توجه کارمزد لحاظ شده بابت هزینه های نگهداری ربات  می باشد.\n" \
              f"👈 میتوانید در درخواست های من در منوی بسته های اعتباری نسبت به لغو درخواست خود اقدام نمایید."
    bot.sendMessage(chat_id, message)

    # admin report channel
    bot.sendMessage(ReportChannel, message)


def credit_channel(credit: CreditPack, bot: TelegramBot):
    message = f"📃 (خریدار)" \
              f"\n" \
              f"💢 بسته اعتباری: " \
              f"({credit.id})\n" \
              f"💹 ارزش بسته اعتباری: " \
              f"{credit.Value} " \
              f"میلیون تومان\n" \
              f"💰 مبلغ تعیین شده: " \
              f"{intcomma(credit.Price)}" \
              f"تومان\n" \
              f"🗓 مدت زمان: " \
              f"{credit.Duration} " \
              f"ماه\n" \
              f"📆 تاریخ اعمال بسته اعتباری: " \
              f"{credit.Time}\n\n\n"

    message += credit_history_com(credit.Value, credit.Duration)

    message += "\n\n" \
               "💡 برای فروش به خریدار این بسته اعتباری و اطلاع از خریداران دیگر،" \
               " داخل ربات معاملات از منو بسته اعتباری سپس فروش به لیست  اقدام نمایید.\n" \
               "🤖 @bashgahagahtradebot"

    bot.sendMessage(ChannelName, message)


# ------------------------------------------------------------------------------- sell

def go_sell_credit_value(chat_id, bot: TelegramBot):
    back_message = "🔙 در تمامی مراحل قابلیت بازگشت وجود دارد"
    bot.sendMessage(chat_id, back_message, reply_markup=ReplyKeyboardBack)

    message = "📌 لطفا یکی از بسته های اعتباری زیر را انتخاب نمایید."
    bot.sendMessage(chat_id, message, reply_markup=InlineKeyboardCreditValue)


def go_sell_credit_duration(chat_id, bot: TelegramBot):
    message = "📌 لطفا مدت زمان بسته اعتباری را انتخاب نمایید."
    bot.sendMessage(chat_id, message, reply_markup=InlineKeyboardCreditDuration)


def go_sell_credit_time(chat_id, bot: TelegramBot):
    message = "📌 لطفا تاریخ اعمال بسته اعتباری را انتخاب نمایید."
    bot.sendMessage(chat_id, message, reply_markup=inline_keyboard_valid_days())


def go_sell_credit_price(chat_id, bot: TelegramBot):
    message = "📌 لطفا قیمت بسته اعتباری را با عدد لاتین و به تومان مشخص نمایید."
    bot.sendMessage(chat_id, message)


def credit_report_for_seller(chat_id, credit: CreditPack, bot: TelegramBot):
    tran = Transition.objects.get(Q(id=credit.BuyTransition) | Q(id=credit.SellTransition))
    message = f"📃(فروشنده)" \
              f"\n" \
              f"💢 بسته اعتباری: " \
              f"({credit.id})\n" \
              f"💹 ارزش بسته اعتباری: " \
              f"{credit.Value} " \
              f"میلیون تومان\n" \
              f"💰 مبلغ تعیین شده: " \
              f"{intcomma(credit.Price)}" \
              f"تومان\n" \
              f"🗓 مدت زمان: " \
              f"{credit.Duration} " \
              f"ماه\n" \
              f"📆 تاریخ اعمال بسته اعتباری: " \
              f"{credit.Time}\n" \
              f"🛠 کارمزد: " \
              f"{intcomma(tran.Fee)}" \
              f" تومان\n" \
              f"💵 مبلغ نهایی: " \
              f"{intcomma(credit.Price - tran.Fee)}" \
              f" تومان\n" \
              f"📌 توجه کارمزد لحاظ شده بابت هزینه های نگهداری ربات  می باشد.\n" \
              f"👈 میتوانید در درخواست های من در منوی بسته های اعتباری نسبت به لغو درخواست خود اقدام نمایید." \
              f"\n" \
              f"⚠️ درصورت فروش بسته اعتباری در جایی غیر از ربات بسته اعتباری مربوطه را حذف نمایید."
    bot.sendMessage(chat_id, message)

    # admin report channel
    bot.sendMessage(ReportChannel, message)


def credit_channel_for_seller(credit: CreditPack, bot: TelegramBot):
    message = f"📃 (فروشنده)" \
              f"\n" \
              f"💢 بسته اعتباری: " \
              f"({credit.id})\n" \
              f"💹 ارزش بسته اعتباری: " \
              f"{credit.Value} " \
              f"میلیون تومان\n" \
              f"💰 مبلغ تعیین شده: " \
              f"{intcomma(credit.Price)}" \
              f"تومان\n" \
              f"🗓 مدت زمان: " \
              f"{credit.Duration} " \
              f"ماه\n" \
              f"\n\n"

    message += credit_history_com(credit.Value, credit.Duration)

    message += "\n\n" \
               "💡 برای خرید این بسته اعتباری و اطلاع از بسته های اعتباری موجود،" \
               " داخل ربات معاملات از منو بسته اعتباری سپس خرید از لیست  اقدام نمایید.\n" \
               "🤖 @bashgahagahtradebot"

    bot.sendMessage(ChannelName, message)


# ------------------------------------------------------------------------------- buyer list


def go_buyer_list_month(chat_id, bot: TelegramBot):
    message_text = '📌 لطفا مدت زمان بسته اعتباری را انتخاب نمایید.'
    bot.sendMessage(chat_id, message_text, reply_markup=ReplyKeyboardBuyListMonth)


def go_buyer_list_value(chat_id, bot: TelegramBot):
    message_text = '📌 لطفا ارزش بسته اعتباری را انتخاب نمایید.'
    bot.sendMessage(chat_id, message_text, reply_markup=ReplyKeyboardBuyListValue)


def buyer_list_pager(chat_id, qu, index_start, index_len, bot: TelegramBot):
    counter = 0
    for i in qu[index_start:index_start + index_len]:
        counter += 1
        i: CreditPack
        per = credit_real_price(value=i.Value, duration=i.Duration)
        if not per:
            per = 0
        else:
            per = ((i.Price - per) * 100) // per

        message = f"🔸 خریدار\n" \
                  f"💳 بسته اعتباری " \
                  f"({i.id})\n" \
                  f"💰 ارزش: " \
                  f"{i.Value}" \
                  f" میلیون تومان\n" \
                  f"🗓 مدت: " \
                  f"{i.Duration}" \
                  f" ماهه" \
                  f"\n" \
                  f"💵 قیمت: " \
                  f"{intcomma(i.Price)}" \
                  f"تومان" \
                  f" (+{per}%)\n" \
                  f"✍️تاریخ اعمال: " \
                  f"{i.Time}"

        bot.sendMessage(
            chat_id,
            message,
            reply_markup=inline_keyboard_buyer_list_detail(
                i.id,
                i.ChatID != chat_id,
                index_start + index_len if counter == index_len else False
            )
        )


def buyer_detail(chat_id, credit: CreditPack, bot: TelegramBot):
    tran = Transition.objects.get(id=credit.SellTransition)
    message = f"📃 رسید مشتری" \
              f"\n" \
              f"💢 بسته اعتباری: " \
              f"({credit.id})\n" \
              f"💹 ارزش بسته اعتباری: " \
              f"{credit.Value} " \
              f"میلیون تومان\n" \
              f"💰 مبلغ تعیین شده: " \
              f"{intcomma(credit.Price)}" \
              f"تومان\n" \
              f"🗓 مدت زمان: " \
              f"{credit.Duration} " \
              f"ماه\n" \
              f"📆 تاریخ اعمال بسته اعتباری: " \
              f"{credit.Time}\n" \
              f"🛠 کارمزد: " \
              f"{intcomma(tran.Fee)}" \
              f" تومان\n" \
              f"💵 مبلغ نهایی: " \
              f"{intcomma(credit.Price - tran.Fee)}" \
              f" تومان\n" \
              f"مشخصات خریدار به شرح زیر است\n" \
              f"{credit.Name} - {credit.Family} - {credit.ClubCode}\n" \
              f"📌 توجه کارمزد لحاظ شده بابت هزینه های نگهداری ربات  می باشد.\n" \
              f"پس از انتقال بسته اعتباری به باشگاه آگاه خریدار، در لیست انتظار تایید، نسبت به تایید آن اقدام نمایید."

    sent_message = bot.sendMessage(chat_id, message)

    # save message that sent to seller
    credit.SellerMessageID = sent_message.get_message_id()
    credit.save()


def send_message_to_buyer(credit: CreditPack, bot: TelegramBot):
    seller = TelegramUser.objects.get(telegram_id=credit.SellID)
    message = f"یک فروشنده با مشخصات زیر قصد انتقال بسته اعتباری با مشخصات زیر را " \
              f"\n" \
              f"💢 بسته اعتباری: " \
              f"({credit.id})\n" \
              f"💹 ارزش بسته اعتباری: " \
              f"{credit.Value} " \
              f"میلیون تومان\n" \
              f"💰 مبلغ تعیین شده: " \
              f"{intcomma(credit.Price)}" \
              f"تومان\n" \
              f"🗓 مدت زمان: " \
              f"{credit.Duration} " \
              f"ماه\n" \
              f"📆 تاریخ اعمال بسته اعتباری: " \
              f"{credit.Time}\n" \
              f"ماهه\n" \
              f"\n{seller.profile.Name} - {seller.profile.Family} - {seller.profile.ClubCode}" \
              f" به شما دارد ، لطفا وارد باشگاه خود شده و بسته اعتباری را در صورت صحیح بودن تایید کنید" \
              f" و بعد از اینکه بسته اعتباری توسط کارگزاری تایید و در حساب معاملاتی شما اعمال شد" \
              f" ، آنرا در  ربات در قسمت لیست انتظار تایید کنید تا پول بحساب فروشنده واریز شود."
    sent_message = bot.sendMessage(credit.ChatID, message)

    # admin report channel
    bot.sendMessage(ReportChannel, message)

    # save message that sent to buyer
    credit.BuyerMessageID = sent_message.get_message_id()
    credit.save()


# ------------------------------------------------------------------------------- seller list

def go_seller_list_month(chat_id, bot: TelegramBot):
    message_text = '📌 لطفا مدت زمان بسته اعتباری را انتخاب نمایید.'
    bot.sendMessage(chat_id, message_text, reply_markup=ReplyKeyboardBuyListMonth)


def go_seller_list_value(chat_id, bot: TelegramBot):
    message_text = '📌 لطفا ارزش بسته اعتباری را انتخاب نمایید.'
    bot.sendMessage(chat_id, message_text, reply_markup=ReplyKeyboardBuyListValue)


def seller_list_pager(chat_id, qu, index_start, index_len, bot: TelegramBot):
    counter = 0
    for i in qu[index_start:index_start + index_len]:
        i: CreditPack
        counter += 1
        i: CreditPack
        per = credit_real_price(value=i.Value, duration=i.Duration)
        if not per:
            per = 0
        else:
            per = ((i.Price - per) * 100) // per

        message = f"🔸 فروشنده\n" \
                  f"💳 بسته اعتباری " \
                  f"({i.id})\n" \
                  f"💰 ارزش: " \
                  f"{i.Value}" \
                  f" میلیون تومان\n" \
                  f"🗓 مدت: " \
                  f"{i.Duration}" \
                  f" ماهه" \
                  f"\n" \
                  f"💵 قیمت: " \
                  f"{intcomma(int(i.Price * (100 + credit_packet_fee_percent(i.Value, i.Duration)) // 100))}" \
                  f"تومان" \
                  f" (+{per})\n"

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
    message = "📌 آیا بسته اعتباری برای کد باشگاه شما منتقل شود یا شخص دیگر؟"
    bot.sendMessage(chat_id, message, reply_markup=ReplyKeyboardCreditBuyFor)


def seller_detail(chat_id, credit: CreditPack, bot: TelegramBot):
    tran = Transition.objects.get(id=credit.BuyTransition)
    message = f"📃 رسید مشتری" \
              f"\n" \
              f"💢 بسته اعتباری: " \
              f"({credit.id})\n" \
              f"💹 ارزش بسته اعتباری: " \
              f"{credit.Value} " \
              f"میلیون تومان\n" \
              f"💰 مبلغ تعیین شده: " \
              f"{intcomma(credit.Price)}" \
              f"تومان\n" \
              f"🗓 مدت زمان: " \
              f"{credit.Duration} " \
              f"ماه\n" \
              f"📆 تاریخ اعمال بسته اعتباری: " \
              f"{credit.Time}\n" \
              f"🛠 کارمزد: " \
              f"{intcomma(tran.Fee)}" \
              f" تومان\n" \
              f"💵 مبلغ نهایی: " \
              f"{intcomma(credit.Price + tran.Fee)}" \
              f" تومان\n" \
              f"مشخصات فروشنده به شرح زیر است\n" \
              f"{credit.Name} - {credit.Family} - {credit.ClubCode}\n" \
              f"📌 توجه کارمزد لحاظ شده بابت هزینه های نگهداری ربات  می باشد.\n" \
              f"پس از دریافت بسته اعتباری و تایید توسط باشگاه آگاه،" \
              f" در لیست انتظار تایید در منوی بسته اعتباری، نسبت به تایید آن اقدام نمایید."

    sent_message = bot.sendMessage(chat_id, message)

    # save message that sent to buyer
    credit.BuyerMessageID = sent_message.get_message_id()
    credit.save()


def send_message_to_seller_for_me(user_id, credit: CreditPack, bot: TelegramBot):
    user = TelegramUser.objects.get(telegram_id=user_id)
    message = f"📌 یک خریدار با مشخصات زیر قصد خرید بسته اعتباری شما را دارد،" \
              f"مشخصات بسته اعتباری به شرح زیر است\n" \
              f"💢 بسته اعتباری: " \
              f"({credit.id})\n" \
              f"💹 ارزش: " \
              f"{credit.Value}" \
              f" میلیون تومان\n" \
              f"💰 قیمت: " \
              f"{intcomma(credit.Price)}" \
              f" تومان\n" \
              f"📆 تاریخ اعمال: " \
              f"{credit.Time}\n" \
              f"🗓 دوره: " \
              f"{credit.Duration} " \
              f"ماهه\n" \
              f"مشخصات خریدار" \
              f"\n{user.profile.Name} - {user.profile.Family} - {user.profile.ClubCode}\n" \
              f"پس از انتقال بسته اعتباری به باشگاه آگاه خریدار،" \
              f" در لیست انتظار تایید در منوی بسته اعتباری، نسبت به تایید آن اقدام نمایید."
    sent_message = bot.sendMessage(credit.ChatID, message)

    # admin channel report
    bot.sendMessage(ReportChannel, message)

    # save message that sent to seller
    credit.SellerMessageID = sent_message.get_message_id()
    credit.save()


def send_message_to_seller_for_other(name, family, club_code, credit: CreditPack, bot: TelegramBot):
    message = f"📌 یک خریدار با مشخصات زیر قصد خرید بسته اعتباری شما را دارد،" \
              f"مشخصات بسته اعتباری به شرح زیر است\n" \
              f"💢 بسته اعتباری: " \
              f"({credit.id})\n" \
              f"💹 ارزش: " \
              f"{credit.Value}" \
              f" میلیون تومان\n" \
              f"💰 قیمت: " \
              f"{intcomma(credit.Price)}" \
              f" تومان\n" \
              f"📆 تاریخ اعمال: " \
              f"{credit.Time}\n" \
              f"🗓 دوره: " \
              f"{credit.Duration} " \
              f"ماهه\n" \
              f"مشخصات خریدار" \
              f"\n{name} - {family} - {club_code}\n" \
              f"پس از انتقال بسته اعتباری به باشگاه آگاه خریدار،" \
              f" در لیست انتظار تایید در منوی بسته اعتباری، نسبت به تایید آن اقدام نمایید."
    sent_message = bot.sendMessage(credit.ChatID, message)

    # admin channel report
    bot.sendMessage(ReportChannel, message)

    # save message that sent to seller
    credit.SellerMessageID = sent_message.get_message_id()
    credit.save()


# ------------------------------------------------------------------------------- Request

def go_my_request(chat_id, user_id, bot: TelegramBot):
    as_buyer = CreditPack.objects.filter(BuyID=user_id)
    bot.sendMessage(chat_id, 'درخواست های خرید:')
    if not as_buyer:
        bot.sendMessage(chat_id, 'درخواست خریدی نداشته اید!')
    else:
        for i in as_buyer:
            i: CreditPack
            message = f"💢 بسته اعتباری " \
                      f"({i.id})\n" \
                      f"💹 ارزش: " \
                      f"{i.Value}" \
                      f" میلیون تومان\n" \
                      f"💰 قیمت: " \
                      f"{intcomma(i.Price)}" \
                      f" تومان\n" \
                      f"📆 تاریخ اعمال: " \
                      f"{i.Time}\n" \
                      f"🗓 دوره: " \
                      f"{i.Duration} " \
                      f"ماهه\n"

            if i.SellID == '0':
                bot.sendMessage(chat_id, message, reply_markup=inline_keyboard_cancel(i.id))
            else:
                bot.sendMessage(chat_id, message)

    as_seller = CreditPack.objects.filter(SellID=user_id)
    bot.sendMessage(chat_id, 'درخواست های فروش:')
    if not as_seller:
        bot.sendMessage(chat_id, 'درخواست فروشی نداشته اید!')
    else:
        for i in as_seller:
            i: CreditPack
            message = f"💢 بسته اعتباری " \
                      f"({i.id})\n" \
                      f"💹 ارزش: " \
                      f"{i.Value}" \
                      f" میلیون تومان\n" \
                      f"💰 قیمت: " \
                      f"{intcomma(i.Price)}" \
                      f" تومان\n" \
                      f"📆 تاریخ اعمال: " \
                      f"{i.Time}\n" \
                      f"🗓 دوره: " \
                      f"{i.Duration} " \
                      f"ماهه\n"

            if i.BuyID == '0':
                bot.sendMessage(chat_id, message, reply_markup=inline_keyboard_cancel(i.id))
            else:
                bot.sendMessage(chat_id, message)


# ------------------------------------------------------------------------------- Conf

def go_conf(chat_id, user_id, bot: TelegramBot):
    message = "اگر فروشنده هستید، و بسته اعتباری را منتقل کرده اید، آن را تایید کنید\n" \
              "اگر خریدار هستید، و بسته اعتباری به حساب باشگاه شما آمده و توسط کارگزاری نیز تایید شده است، آن را تایید کنید\n" \
              "⭐ در غیر این صورت مراقب باشید که در صورت تایید اشتباه، ربات معاملاتی باشگاه، مسئولیتی ندارد."

    bot.sendMessage(chat_id, message)

    as_buyer = CreditPack.objects.filter(BuyID=user_id, Conf=False).filter(~Q(SellID='0'))
    for i in as_buyer:
        message = f"✅ خریدار بوده اید\n" \
                  f"بسته اعتباری " \
                  f"({i.id})\n" \
                  f"ارزش: " \
                  f"{i.Value}" \
                  f" میلیون تومان\n" \
                  f"قیمت: " \
                  f"{intcomma(i.Price)}" \
                  f" تومان\n" \
                  f"تاریخ اعمال: " \
                  f"{i.Time}\n" \
                  f"دوره: " \
                  f"{i.Duration} " \
                  f"ماهه\n" \
                  f"وضعیت تایید فروشنده: " \
                  f"{'تایید شده' if i.SellConf else 'در انتظار تایید'}\n" \
                  f"وضعیت تایید خریدار: " \
                  f"{'تایید شده' if i.BuyConf else 'در انتظار تایید'}"
        bot.sendMessage(chat_id, message, reply_markup=inline_keyboard_conf(i.id))

    as_seller = CreditPack.objects.filter(SellID=user_id, Conf=False).filter(~Q(BuyID='0'))
    for i in as_seller:
        message = f"✅ فروشنده بوده اید\n" \
                  f"بسته اعتباری " \
                  f"({i.id})\n" \
                  f"ارزش: " \
                  f"{i.Value}" \
                  f" میلیون تومان\n" \
                  f"قیمت: " \
                  f"{intcomma(i.Price)}" \
                  f" تومان\n" \
                  f"تاریخ اعمال: " \
                  f"{i.Time}\n" \
                  f"دوره: " \
                  f"{i.Duration} " \
                  f"ماهه\n" \
                  f"وضعیت تایید فروشنده: " \
                  f"{'تایید شده' if i.SellConf else 'در انتظار تایید'}\n" \
                  f"وضعیت تایید خریدار: " \
                  f"{'تایید شده' if i.BuyConf else 'در انتظار تایید'}"
        bot.sendMessage(chat_id, message, reply_markup=inline_keyboard_conf(i.id))


# ------------------------------------------------------------------------------- history

def credit_history(chat_id, credit_value, credit_duration, bot: TelegramBot):
    message = credit_history_com(credit_value, credit_duration)
    bot.sendMessage(chat_id, message)


def credit_history_com(credit_value, credit_duration):
    credit = CreditPack.objects.filter(Value=credit_value, Duration=credit_duration, Conf=True)
    message = "📊 رنج های قیمتی معامله شده به ترتیب:" \
              "\n"

    price = set()
    for i in credit:
        price.add(i.Price)

    for i in price:
        counter = CreditPack.objects.filter(Value=credit_value, Duration=credit_duration, Price=i, Conf=True).count()

        per = credit_real_price(value=credit_value, duration=credit_duration)
        if not per:
            per = 0
        else:
            per = ((i - per) * 100) // per

        message += f"✅ {intcomma(i)}" \
                   f"تومان" \
                   f"- {counter}" \
                   f" مرتبه" \
                   f" (+{per}%)" \
                   f"\n"
    return message
