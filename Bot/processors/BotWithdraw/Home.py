from json import dumps

from django.contrib.humanize.templatetags.humanize import intcomma
from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types
from django_tgbot.types.update import Update
from Bot.bot import state_manager, TelegramBot
from Bot.models import TelegramState, TelegramUser

from ..BotDialog import go_home
from .Dialog import go_withdraw_home
from Bot.BotSetting import AdminChannel

from WalletTransition.WalletRequest import withdraw_from_wallet


@processor(
    state_manager,
    from_states='/Withdraw',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def withdraw_home(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    user_id = update.get_user().get_id()
    # user = TelegramUser.objects.get(telegram_id=user_id)
    message_text = update.get_message().get_text()

    if message_text == 'صفحه اول':
        go_home(chat_id, bot)
        state.set_name('/Home')

    elif not message_text.isdigit():
        go_withdraw_home(chat_id, bot)

    else:
        value = int(message_text)

        tran = withdraw_from_wallet(user_id, value)
        if not tran:
            bot.sendMessage(chat_id, "متاسفانه مبلغ در خواستی از موجودی کیف پول بیشتر است")
        else:
            message_to_client = f"برداشت با موفقیت برای ادمین ارسال شد، به شما اطلاع رسانی خواهد شد."
            bot.sendMessage(chat_id, message_to_client)

            user_detail = {
                'user_id': user_id,
                'tran_id': tran,
                'cause': 'withdraw',
                'amount': value,
                'chat_id': chat_id,
            }
            message_to_admin = dumps(user_detail)
            bot.sendMessage(AdminChannel, message_to_admin)

        go_home(chat_id, bot)
        state.set_name('/Home')
