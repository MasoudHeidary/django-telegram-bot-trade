from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Q
from Bot.bot import TelegramBot
from Bot.BotSetting import ChannelName, ReportChannel
from Bot.models import TelegramUser

from Loan.LoanRequest import loan_real_price, loan_fee_percent
from Loan.models import Loan
from WalletTransition.models import Transition

from .Component import ReplyKeyboardLoan, InlineKeyboardLoanValue, InlineKeyboardLoanDuration, \
    ReplyKeyboardLoanBuyFor, ReplyKeyboardBuyListMonth, \
    inline_keyboard_buyer_list_detail, inline_keyboard_conf, inline_keyboard_seller_list_detail, \
    inline_keyboard_cancel, inline_keyboard_valid_days, ReplyKeyboardBuyListValue

from ..BotComponent import ReplyKeyboardBack


# ------------------------------------------------------------------------------- home
def go_loan(chat_id, bot: TelegramBot):
    message = "📌 جهت درخواست خرید یا فروش وام یکی از موارد را انتخاب نمایید."
    bot.sendMessage(chat_id, message, reply_markup=ReplyKeyboardLoan)


def fail_loan(chat_id, bot: TelegramBot):
    message = "لطفا از دستورات زیر استفاده کنید." \
              "👇"
    bot.sendMessage(chat_id, message, reply_markup=ReplyKeyboardLoan)


# ------------------------------------------------------------------------------- buy
def go_buy_loan_Value(chat_id, bot: TelegramBot):
    back_message = "🔙 در تمامی مراحل قابلیت بازگشت وجود دارد"
    bot.sendMessage(chat_id, back_message, reply_markup=ReplyKeyboardBack)

    message = "📌 لطفا یکی از وام های زیر را انتخاب نمایید."
    bot.sendMessage(chat_id, message, reply_markup=InlineKeyboardLoanValue)


def go_buy_loan_duration(chat_id, bot: TelegramBot):
    message = "📌 لطفا مدت زمان وام را انتخاب نمایید."
    bot.sendMessage(chat_id, message, reply_markup=InlineKeyboardLoanDuration)


def go_buy_loan_time(chat_id, bot: TelegramBot):
    message = "📌 لطفا تاریخ اعمال وام را انتخاب نمایید."
    bot.sendMessage(chat_id, message, reply_markup=inline_keyboard_valid_days())


def go_buy_loan_price(chat_id, bot: TelegramBot):
    message = "📌 لطفا قیمت وام را با عدد لاتین و به تومان مشخص نمایید."
    bot.sendMessage(chat_id, message)


def go_buy_loan_for(chat_id, bot: TelegramBot):
    message = "📌 آیا وام برای کد باشگاه شما منتقل شود یا شخص دیگر؟"
    bot.sendMessage(chat_id, message, reply_markup=ReplyKeyboardLoanBuyFor)


def go_buy_loan_for_other_name(chat_id, bot: TelegramBot):
    message = "📌 لطفا نام و نام خانوادگی خریدار را با خط تیره وارد کنید." \
              "\n" \
              "👈 مثل: رضا-عطاری"
    bot.sendMessage(chat_id, message)


def go_buy_loan_for_other_club_code(chat_id, bot: TelegramBot):
    message = "📌 لطفا کد باشگاه خریدار را وارد کنید.(6حرف)"
    bot.sendMessage(chat_id, message)


def loan_report(chat_id, loan: Loan, bot: TelegramBot):
    tran = Transition.objects.get(Q(id=loan.BuyTransition) | Q(id=loan.SellTransition))
    message = f"📃 رسید مشتری(خریدار)" \
              f"\n" \
              f"💢 وام: " \
              f"({loan.id})\n" \
              f"💹 ارزش وام: " \
              f"{loan.Value} " \
              f"میلیون تومان\n" \
              f"💰 مبلغ تعیین شده: " \
              f"{intcomma(loan.Price)}" \
              f"تومان\n" \
              f"🗓 مدت زمان: " \
              f"{loan.Duration} " \
              f"ماه\n" \
              f"📆 تاریخ اعمال وام: " \
              f"{loan.Time}\n" \
              f"🛠 کارمزد: " \
              f"{intcomma(tran.Fee)}" \
              f" تومان\n" \
              f"💵 مبلغ نهایی: " \
              f"{intcomma(loan.Price + tran.Fee)}" \
              f" تومان\n" \
              f"📌 توجه کارمزد لحاظ شده بابت هزینه های نگهداری ربات  می باشد.\n" \
              f"👈 میتوانید در منوی درخواست های من نسبت به لغو درخواست خود اقدام نمایید."
    bot.sendMessage(chat_id, message)

    # admin report channel
    bot.sendMessage(ReportChannel, message)


def loan_report_channel(loan: Loan, bot: TelegramBot):
    message = f"📃(خریدار)" \
              f"\n" \
              f"💢 وام: " \
              f"({loan.id})\n" \
              f"💹 ارزش وام: " \
              f"{loan.Value} " \
              f"میلیون تومان\n" \
              f"💰 مبلغ تعیین شده: " \
              f"{intcomma(loan.Price)}" \
              f"تومان\n" \
              f"🗓 مدت زمان: " \
              f"{loan.Duration} " \
              f"ماه\n" \
              f"📆 تاریخ اعمال وام: " \
              f"{loan.Time}\n\n\n"
    message += loan_history_com(loan.Value, loan.Duration)
    message += "\n\n" \
               "💡 برای فروش به خریدار این وام و اطلاع از خریداران دیگر،" \
               " داخل ربات معاملات از منو وام سپس فروش به لیست  اقدام نمایید.\n" \
               "🤖 @bashgahagahtradebot"

    bot.sendMessage(ChannelName, message)


# ------------------------------------------------------------------------------- sell
def go_sell_loan_value(chat_id, bot: TelegramBot):
    back_message = "🔙 در تمامی مراحل قابلیت بازگشت وجود دارد"
    bot.sendMessage(chat_id, back_message, reply_markup=ReplyKeyboardBack)

    message = "📌 لطفا یکی از وام های زیر را انتخاب نمایید."
    bot.sendMessage(chat_id, message, reply_markup=InlineKeyboardLoanValue)


def go_sell_loan_duration(chat_id, bot: TelegramBot):
    message = "📌 لطفا مدت زمان وام را انتخاب نمایید."
    bot.sendMessage(chat_id, message, reply_markup=InlineKeyboardLoanDuration)


def go_sell_loan_time(chat_id, bot: TelegramBot):
    message = "📌 لطفا تاریخ اعمال وام را انتخاب نمایید."
    bot.sendMessage(chat_id, message, reply_markup=inline_keyboard_valid_days())


def go_sell_loan_price(chat_id, bot: TelegramBot):
    message = "📌 لطفا قیمت وام را با عدد لاتین و به تومان مشخص نمایید."
    bot.sendMessage(chat_id, message)


def loan_report_for_seller(chat_id, loan: Loan, bot: TelegramBot):
    tran = Transition.objects.get(Q(id=loan.BuyTransition) | Q(id=loan.SellTransition))
    message = f"📃 رسید مشتری(فروشنده)" \
              f"\n" \
              f"💢 وام: " \
              f"({loan.id})\n" \
              f"💹 ارزش وام: " \
              f"{loan.Value} " \
              f"میلیون تومان\n" \
              f"💰 مبلغ تعیین شده: " \
              f"{intcomma(loan.Price)}" \
              f"تومان\n" \
              f"🗓 مدت زمان: " \
              f"{loan.Duration} " \
              f"ماه\n" \
              f"📆 تاریخ اعمال وام: " \
              f"{loan.Time}\n" \
              f"🛠 کارمزد: " \
              f"{intcomma(tran.Fee)}" \
              f" تومان\n" \
              f"💵 مبلغ نهایی: " \
              f"{intcomma(loan.Price - tran.Fee)}" \
              f" تومان\n" \
              f"📌 توجه کارمزد لحاظ شده بابت هزینه های نگهداری ربات  می باشد.\n" \
              f"👈 میتوانید در منوی درخواست های من نسبت به لغو درخواست خود اقدام نمایید." \
              f"\n" \
              f"⚠️ درصورت فروش وام در جایی غیر از ربات وام مربوطه را حذف نمایید."
    bot.sendMessage(chat_id, message)

    # admin report channel
    bot.sendMessage(ReportChannel, message)


def loan_channel_for_seller(loan: Loan, bot: TelegramBot):
    message = f"📃(فروشنده)" \
              f"\n" \
              f"💢 وام: " \
              f"({loan.id})\n" \
              f"💹 ارزش وام: " \
              f"{loan.Value} " \
              f"میلیون تومان\n" \
              f"💰 مبلغ تعیین شده: " \
              f"{intcomma(loan.Price)}" \
              f"تومان\n" \
              f"🗓 مدت زمان: " \
              f"{loan.Duration} " \
              f"ماه\n" \
              f"\n\n"
    message += loan_history_com(loan.Value, loan.Duration)
    message += "\n\n" \
               "💡 برای خرید این وام و اطلاع از وام های موجود،" \
               " داخل ربات معاملات از منو وام سپس خرید از لیست  اقدام نمایید.\n" \
               "🤖 @bashgahagahtradebot"
    bot.sendMessage(ChannelName, message)


# ------------------------------------------------------------------------------- buyer list

def go_buyer_list_month(chat_id, bot: TelegramBot):
    message_text = '📌 لطفا مدت زمان وام را انتخاب نمایید.'
    bot.sendMessage(chat_id, message_text, reply_markup=ReplyKeyboardBuyListMonth)


def go_buyer_list_value(chat_id, bot: TelegramBot):
    message_text = '📌 لطفا ارزش وام را انتخاب نمایید.'
    bot.sendMessage(chat_id, message_text, reply_markup=ReplyKeyboardBuyListValue)


def buyer_list_pager(chat_id, qu, index_start, index_len, bot: TelegramBot):
    counter = 0
    for i in qu[index_start:index_start + index_len]:
        counter += 1
        per = loan_real_price(value=i.Value, duration=i.Duration)
        if not per:
            per = 0
        else:
            per = ((i.Price - per) * 100) // per

        message = f"🔸 خریدار\n" \
                  f"💳 وام " \
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
                  f" (+{per})\n" \
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


def buyer_detail(chat_id, loan: Loan, bot: TelegramBot):
    tran = Transition.objects.get(id=loan.SellTransition)
    message = f"📃 رسید مشتری" \
              f"\n" \
              f"💢 وام: " \
              f"({loan.id})\n" \
              f"💹 ارزش وام: " \
              f"{loan.Value} " \
              f"میلیون تومان\n" \
              f"💰 مبلغ تعیین شده: " \
              f"{intcomma(loan.Price)}" \
              f"تومان\n" \
              f"🗓 مدت زمان: " \
              f"{loan.Duration} " \
              f"ماه\n" \
              f"📆 تاریخ اعمال وام: " \
              f"{loan.Time}\n" \
              f"🛠 کارمزد: " \
              f"{intcomma(tran.Fee)}" \
              f" تومان\n" \
              f"💵 مبلغ نهایی: " \
              f"{intcomma(loan.Price - tran.Fee)}" \
              f" تومان\n" \
              f"مشخصات خریدار به شرح زیر است\n" \
              f"{loan.Name} - {loan.Family} - {loan.ClubCode}\n" \
              f"📌 توجه کارمزد لحاظ شده بابت هزینه های نگهداری ربات  می باشد.\n" \
              f"پس از انتقال وام به باشگاه آگاه خریدار" \
              f"، در لیست انتظار تایید در منوی وام، نسبت به تایید آن اقدام نمایید."
    sent_message = bot.sendMessage(chat_id, message)

    # add message id that want to sell
    loan.SellerMessageID = int(sent_message.get_message_id())
    loan.save()


def send_message_to_buyer(loan: Loan, bot: TelegramBot):
    seller = TelegramUser.objects.get(telegram_id=loan.SellID)
    message = f"یک فروشنده با مشخصات زیر قصد انتقال وام با مشخصات زیر را " \
              f"\n" \
              f"💢 وام: " \
              f"({loan.id})\n" \
              f"💹 ارزش وام: " \
              f"{loan.Value} " \
              f"میلیون تومان\n" \
              f"💰 مبلغ تعیین شده: " \
              f"{intcomma(loan.Price)}" \
              f"تومان\n" \
              f"🗓 مدت زمان: " \
              f"{loan.Duration} " \
              f"ماه\n" \
              f"📆 تاریخ اعمال وام: " \
              f"{loan.Time}\n" \
              f"ماهه\n" \
              f"\n{seller.profile.Name} - {seller.profile.Family} - {seller.profile.ClubCode}\n" \
              f" به شما دارد ، لطفا وارد باشگاه خود شده و وام را در صورت صحیح بودن تایید کنید" \
              f" و بعد از اینکه وام توسط کارگزاری تایید و در حساب معاملاتی شما اعمال شد" \
              f" ، آنرا در  ربات در لیست انتظار تایید کنید تا پول بحساب فروشنده واریز شود."

    sent_message = bot.sendMessage(loan.ChatID, message)

    # admin report channel
    bot.sendMessage(ReportChannel, message)

    # add message id that to buyer
    loan.BuyerMessageID = sent_message.get_message_id()
    loan.save()


# ------------------------------------------------------------------------------- seller list

def go_seller_list_month(chat_id, bot: TelegramBot):
    message_text = '📌 لطفا مدت زمان وام را انتخاب نمایید.'
    bot.sendMessage(chat_id, message_text, reply_markup=ReplyKeyboardBuyListMonth)


def go_seller_list_value(chat_id, bot: TelegramBot):
    message_text = '📌 لطفا ارزش وام را انتخاب نمایید.'
    bot.sendMessage(chat_id, message_text, reply_markup=ReplyKeyboardBuyListValue)


def seller_list_pager(chat_id, qu, index_start, index_len, bot: TelegramBot):
    counter = 0
    for i in qu[index_start:index_start + index_len]:
        i: Loan
        counter += 1

        per = loan_real_price(value=i.Value, duration=i.Duration)
        if not per:
            per = 0
        else:
            per = ((i.Price - per) * 100) // per

        message = f"🔸 فروشنده\n" \
                  f"💳 وام " \
                  f"({i.id})\n" \
                  f"💰 ارزش: " \
                  f"{i.Value}" \
                  f" میلیون تومان\n" \
                  f"🗓 مدت: " \
                  f"{i.Duration}" \
                  f" ماهه" \
                  f"\n" \
                  f"💵 قیمت: " \
                  f"{intcomma(int(i.Price * (100 + loan_fee_percent(i.Value, i.Duration)) // 100))}" \
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
    message = "📌 آیا وام برای کد باشگاه شما منتقل شود یا شخص دیگر؟"
    bot.sendMessage(chat_id, message, reply_markup=ReplyKeyboardLoanBuyFor)


def seller_detail(chat_id, loan: Loan, bot: TelegramBot):
    tran = Transition.objects.get(id=loan.BuyTransition)
    message = f"📃 رسید مشتری" \
              f"\n" \
              f"💢 وام: " \
              f"({loan.id})\n" \
              f"💹 ارزش وام: " \
              f"{loan.Value} " \
              f"میلیون تومان\n" \
              f"💰 مبلغ تعیین شده: " \
              f"{intcomma(loan.Price)}" \
              f"تومان\n" \
              f"🗓 مدت زمان: " \
              f"{loan.Duration} " \
              f"ماه\n" \
              f"📆 تاریخ اعمال وام: " \
              f"{loan.Time}\n" \
              f"🛠 کارمزد: " \
              f"{intcomma(tran.Fee)}" \
              f" تومان\n" \
              f"💵 مبلغ نهایی: " \
              f"{intcomma(loan.Price + tran.Fee)}" \
              f" تومان\n" \
              f"مشخصات فروشنده به شرح زیر است\n" \
              f"{loan.Name} - {loan.Family} - {loan.ClubCode}\n" \
              f"📌 توجه کارمزد لحاظ شده بابت هزینه های نگهداری ربات  می باشد.\n" \
              f"پس از دریافت وام و تایید توسط باشگاه آکاه،" \
              f" در لیست انتظار تایید در منوی وام، نسبت به تایید آن اقدام نمایید."

    sent_message = bot.sendMessage(chat_id, message)

    # save seller detail that sent to buyer
    loan.BuyerMessageID = int(sent_message.get_message_id())
    loan.save()


def send_message_to_seller_for_me(user_id, loan: Loan, bot: TelegramBot):
    user = TelegramUser.objects.get(telegram_id=user_id)
    message = f"📌 یک خریدار با مشخصات زیر قصد خرید وام شما را دارد،" \
              f"مشخصات وام به شرح زیر است\n" \
              f"💢 وام: " \
              f"({loan.id})\n" \
              f"💹 ارزش: " \
              f"{loan.Value}" \
              f" میلیون تومان\n" \
              f"💰 قیمت: " \
              f"{intcomma(loan.Price)}" \
              f" تومان\n" \
              f"📆 تاریخ اعمال: " \
              f"{loan.Time}\n" \
              f"🗓 دوره: " \
              f"{loan.Duration} " \
              f"ماهه\n" \
              f"مشخصات خریدار" \
              f"\n{user.profile.Name} - {user.profile.Family} - {user.profile.ClubCode}\n" \
              f"پس از انتقال وام به باشگاه آگاه خریدار،" \
              f" در لیست انتظار تایید در منوی وام، نسبت به تایید آن اقدام نمایید."
    sent_message = bot.sendMessage(loan.ChatID, message)

    # admin report channel
    bot.sendMessage(ReportChannel, message)

    # add message id that sent to seller
    loan.SellerMessageID = int(sent_message.get_message_id())
    loan.save()


def send_message_to_seller_for_other(name, family, club_code, loan: Loan, bot: TelegramBot):
    message = f"📌 یک خریدار با مشخصات زیر قصد خرید وام شما را دارد،" \
              f"مشخصات وام به شرح زیر است\n" \
              f"💢 وام: " \
              f"({loan.id})\n" \
              f"💹 ارزش: " \
              f"{loan.Value}" \
              f" میلیون تومان\n" \
              f"💰 قیمت: " \
              f"{intcomma(loan.Price)}" \
              f" تومان\n" \
              f"📆 تاریخ اعمال: " \
              f"{loan.Time}\n" \
              f"🗓 دوره: " \
              f"{loan.Duration} " \
              f"ماهه\n" \
              f"مشخصات خریدار\n" \
              f"\n{name} - {family} - {club_code}\n" \
              f"پس از انتقال وام به باشگاه آگاه خریدار،" \
              f" در لیست انتظار تایید در منوی وام، نسبت به تایید آن اقدام نمایید."
    sent_message = bot.sendMessage(loan.ChatID, message)

    # admin report channel
    bot.sendMessage(ReportChannel, message)

    # add message id that sent to seller
    loan.SellerMessageID = int(sent_message.get_message_id())
    loan.save()


# ------------------------------------------------------------------------------- Request

def go_my_request(chat_id, user_id, bot: TelegramBot):
    as_buyer = Loan.objects.filter(BuyID=user_id)
    bot.sendMessage(chat_id, 'درخواست های خرید:')
    if not as_buyer:
        bot.sendMessage(chat_id, 'در حال حاضر درخواست خریدی نداشته اید.')
    else:
        for i in as_buyer:
            i: Loan
            message = f"💢 وام " \
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

    as_seller = Loan.objects.filter(SellID=user_id)
    bot.sendMessage(chat_id, 'درخواست های فروش:')
    if not as_seller:
        bot.sendMessage(chat_id, 'در حال حاظر درخواست فروشی نداشته اید.')
    else:
        for i in as_seller:
            i: Loan
            message = f"💢 وام " \
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
    message = "اگر فروشنده هستید، و وام را منتقل کرده اید، آن را تایید کنید\n" \
              "اگر خریدار هستید، و وام به حساب باشگاه شما آمده و توسط کارگزاری نیز تایید شده است، آن را تایید کنید\n" \
              "⭐ در غیر این صورت مراقب باشید که در صورت تایید اشتباه، ربات معاملاتی باشگاه، مسئولیتی ندارد."

    bot.sendMessage(chat_id, message)

    as_buyer = Loan.objects.filter(BuyID=user_id, Conf=False).filter(~Q(SellID='0'))
    for i in as_buyer:
        message = f"✅ خریدار بوده اید\n" \
                  f"💢 وام " \
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
                  f"ماهه\n" \
                  f"وضعیت تایید فروشنده: " \
                  f"{'تایید شده' if i.SellConf else 'در انتظار تایید'}\n" \
                  f"وضعیت تایید خریدار: " \
                  f"{'تایید شده' if i.BuyConf else 'در انتظار تایید'}"
        bot.sendMessage(chat_id, message, reply_markup=inline_keyboard_conf(i.id))

    as_seller = Loan.objects.filter(SellID=user_id, Conf=False).filter(~Q(BuyID='0'))
    for i in as_seller:
        message = f"✅ فروشنده بوده اید\n" \
                  f"💢 وام " \
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
                  f"ماهه\n" \
                  f"وضعیت تایید فروشنده: " \
                  f"{'تایید شده' if i.SellConf else 'در انتظار تایید'}\n" \
                  f"وضعیت تایید خریدار: " \
                  f"{'تایید شده' if i.BuyConf else 'در انتظار تایید'}"
        bot.sendMessage(chat_id, message, reply_markup=inline_keyboard_conf(i.id))


# ------------------------------------------------------------------------------- history

def loan_history(chat_id, loan_value, loan_duration, bot: TelegramBot):
    message = loan_history_com(loan_value, loan_duration)
    bot.sendMessage(chat_id, message)


def loan_history_com(loan_value, loan_duration):
    loan = Loan.objects.filter(Value=loan_value, Duration=loan_duration, Conf=True)
    message = "📊 رنج های قیمتی معامله شده به ترتیب:" \
              "\n"

    price = set()
    for i in loan:
        price.add(i.Price)

    for i in price:
        counter = Loan.objects.filter(Value=loan_value, Duration=loan_duration, Price=i, Conf=True).count()

        per = loan_real_price(value=loan_value, duration=loan_duration)
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
