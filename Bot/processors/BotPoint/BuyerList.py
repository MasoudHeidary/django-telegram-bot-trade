from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types
from django_tgbot.types.update import Update
from Bot.bot import state_manager, TelegramBot
from Bot.models import TelegramState

from .Dialog import go_point, buyer_list_pager, send_message_to_buyer, buyer_detail

from Point.models import Point
from Point.PointRequest import get_point, sell_point_to_buyer


@processor(
    state_manager,
    from_states='/Point/BuyerList',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def point_buyer_list(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    go_point(chat_id, bot)
    state.set_name('/Point')


@processor(
    state_manager,
    from_states='/Point/BuyerList',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def point_buyer_list(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    user_id = update.get_user().get_id()
    value = update.get_callback_query().get_data()
    show_len = 5

    if 'more' in value:
        qu = Point.objects.all()

        index = int(value.split('-')[1])
        buyer_list_pager(chat_id, qu, index, show_len, bot)
    else:
        sell = sell_point_to_buyer(point_id=int(value), seller_id=user_id, chat_id=chat_id)
        if not sell:
            bot.sendMessage(chat_id, '📌 این امتیاز دیگر در دسترس نمی باشد، لطفا لیست خود را به روز کنید.')
        else:
            point = get_point(int(value))
            send_message_to_buyer(point, bot)
            buyer_detail(chat_id, point, bot)

            go_point(chat_id, bot)
            state.set_name('/Point')
