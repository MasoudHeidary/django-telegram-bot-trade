from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from ..bot import state_manager, TelegramBot
from ..models import TelegramState
from ..BotSetting import BotName, ChannelName

from .BotDialog import go_home

state_manager.set_default_update_types(update_types.Message)


@processor(
    state_manager,
    from_states=state_types.Reset,
    success='/Home',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def start(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    user_name = update.get_chat().get_username()

    message = f"سلام " \
              f"{user_name}" \
              f" به ربات " \
              f"{BotName}" \
              f" خوش اومدی" \
              f"\n" \
              f"یادت نره که قوانین رو برای معاملات بخونی، چون اگه متضرر بشی ما هیچ مسئولیتی نداریم" \
              f"\n" \
              f"در آخر برای استفاده از ربات باید در کانال عضو بشی " \
              f"{ChannelName}" \
              f" و یک پروفایل هم بسازی"

    bot.sendMessage(chat_id, message)
    go_home(chat_id, bot)
