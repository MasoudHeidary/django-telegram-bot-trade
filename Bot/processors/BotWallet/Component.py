from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup
from django_tgbot.types.keyboardbutton import KeyboardButton
from django_tgbot.types.replykeyboardremove import ReplyKeyboardRemove
from django_tgbot.types.inlinekeyboardmarkup import InlineKeyboardMarkup
from django_tgbot.types.inlinekeyboardbutton import InlineKeyboardButton
from Bot.bot import state_manager, TelegramBot
from Bot.models import TelegramState


def inline_keyboard_more_transition(more_id):
    return InlineKeyboardMarkup.a(inline_keyboard=[
        [InlineKeyboardButton.a('تراکنش بیشتر', callback_data=f"more-{more_id}")]
    ])
