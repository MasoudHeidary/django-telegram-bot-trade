from json import loads

from django.contrib.humanize.templatetags.humanize import intcomma
from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from Bot.bot import state_manager, TelegramBot
from Bot.models import TelegramState

from Bot.BotSetting import AdminChannel

from WalletTransition.WalletRequest import charge_wallet, admin_withdraw_from_wallet


@processor(
    state_manager,
    from_states=state_types.All,
    update_types=update_types.ChannelPost,
    message_types=message_types.Text,
)
def wallet_reply(bot: TelegramBot, update: Update, state: TelegramState):
    if not int(update.get_chat().get_id()) == AdminChannel:
        return

    try:
        # to indicate false message in admin channel
        chat_id = update.get_chat().get_id()
        reply_detail = loads(update.get_message().get_reply_to_message().get_text())
        try:
            amount, fee = update.get_message().get_text().split(',')
            amount = int(amount)
            fee = int(fee)
        except:
            amount = int(update.get_message().get_text())
            fee = 0

        message_id = int(update.get_message().get_message_id())

        if amount > 0:
            # charge wallet
            charge_wallet(reply_detail.get('user_id'), amount)

            message_to_client = f"کیف پول شما به مبلغ " \
                                f"{intcomma(amount)}" \
                                f" تومان با موفقیت شارژ شد."
            bot.sendMessage(reply_detail.get('chat_id'), message_to_client)

            # ack to admin
            bot.sendMessage(chat_id, "OK", reply_to_message_id=message_id)

        elif amount < 0:
            amount = abs(amount)
            check = admin_withdraw_from_wallet(
                reply_detail.get('tran_id'),
                amount,
                fee
            )

            if not check:
                bot.sendMessage(chat_id, "ERROR", reply_to_message_id=message_id)
                return

            message_to_client = f"برداشت مبلغ " \
                                f"{intcomma(amount)}" \
                                f" تومان" \
                                f" با میزان کارمزد " \
                                f"{intcomma(fee)}" \
                                f" تومان" \
                                f" از کیف پول شما در حال انجام است، و به زودی برای شما ارسال میشود."
            bot.sendMessage(reply_detail.get('chat_id'), message_to_client)

            # ack to admin
            bot.sendMessage(chat_id, "OK", reply_to_message_id=message_id)

    except:
        # a false message in admin channel
        pass