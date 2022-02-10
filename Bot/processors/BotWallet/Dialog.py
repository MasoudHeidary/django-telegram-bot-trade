import datetime

from django.contrib.humanize.templatetags.humanize import intcomma
from persiantools.jdatetime import JalaliDate

from Bot.bot import state_manager, TelegramBot
from Bot.models import TelegramState, TelegramUser

from .Component import inline_keyboard_more_transition
from WalletTransition.models import Transition


def go_transition_list_pager(chat_id, user: TelegramUser, bot: TelegramBot):
    wallet = user.wallet
    message = f"میزان پول موجود:" \
              f"{intcomma(wallet.AvailableMoney)} 💲\n" \
              f"پول بلوکه شده:" \
              f"{intcomma(wallet.BlockedMoney)} 🚫"
    bot.sendMessage(chat_id, message)

    tran = wallet.transition_set.all()
    transition_list_pager(chat_id, tran, 0, 5, bot)


def transition_list_pager(chat_id, qu, index_start, index_len, bot: TelegramBot):
    counter = 0
    for i in qu[index_start:index_start + index_len]:
        i: Transition
        counter += 1

        time = JalaliDate.to_jalali(
            datetime.date(
                i.TranTime.year,
                i.TranTime.month,
                i.TranTime.day
            )
        )

        message = f"قبل: " \
                  f"{intcomma(i.Before)}" \
                  f" تومان\n" \
                  f"بعد: " \
                  f"{intcomma(i.Next)}" \
                  f" تومان\n" \
                  f"ارزش تراکنش: " \
                  f"{intcomma(i.Value)}" \
                  f" تومان\n" \
                  f"کارمزد تراکنش: " \
                  f"{intcomma(i.Fee)}" \
                  f" تومان\n" \
                  f"دلیل تراکنش: " \
                  f"{i.Cause}\n" \
                  f"تاریخ تراکنش: " \
                  f"{time.strftime('%Y/%m/%d')}"

        if counter != index_len:
            bot.sendMessage(
                chat_id,
                message
            )
        else:
            bot.sendMessage(
                chat_id,
                message,
                reply_markup=inline_keyboard_more_transition(more_id=index_start + index_len)
            )
