from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from django_tgbot.exceptions import ProcessFailure
from Bot.bot import state_manager, TelegramBot
from Bot.models import TelegramState

from ..BotProfile.CreateProfile import check_club_code
from .Dialog import seller_list_pager, go_sell_list_for, seller_detail, send_message_to_seller_for_me, \
    send_message_to_seller_for_other, go_buy_point_for_other_name, go_buy_point_for_other_club_code, go_point

from Point.models import Point
from Point.PointRequest import get_point, buy_point_from_seller


@processor(
    state_manager,
    from_states='/Point/SellerList',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def point_seller_list(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    go_point(chat_id, bot)
    state.set_name('/Point')


@processor(
    state_manager,
    from_states='/Point/SellerList',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def point_seller_list(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    # user_id = update.get_user().get_id()
    value = update.get_callback_query().get_data()
    show_len = 5

    if 'more' in value:
        qu = Point.objects.all()

        index = int(value.split('-')[1])
        seller_list_pager(chat_id, qu, index, show_len, bot)
    else:
        state.update_memory({'point_id': value})
        go_sell_list_for(chat_id, bot)
        state.set_name('/Point/SellerList/For')


@processor(
    state_manager,
    from_states='/Point/SellerList/For',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def point_seller_list_for(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()
    user_id = update.get_user().get_id()

    point_id = state.get_memory().get('point_id')

    if message_text == 'خودم':
        x = buy_point_from_seller(point_id=point_id, buyer_id=user_id, chat_id=chat_id)
        if not x:
            message = "به نظر در خرید امتیاز مشکلی وجود دارد:\n" \
                      "1) نسبت به شارژ کیف پول خود اقدام نمیایید\n" \
                      "2) امتیاز جهت فروش حذف شده یا فروش رفته است\n" \
                      "با تشکر"
            bot.sendMessage(chat_id, message)
        else:
            point = get_point(point_id)
            send_message_to_seller_for_me(user_id=user_id, point=point, bot=bot)
            seller_detail(chat_id, point, bot)

        go_point(chat_id, bot)
        state.set_name('/Point')

    elif message_text == 'شخصی دیگر':
        go_buy_point_for_other_name(chat_id, bot)
        state.set_name('/Point/SellerList/For/Other/Name')

    else:
        go_point(chat_id, bot)
        state.set_name('/Point')


@processor(
    state_manager,
    from_states='/Point/SellerList/For/Other/Name',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def point_seller_list_for_other_name(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()

    try:
        name, family = message_text.split('-')
        state.update_memory({'name': name, 'family': family})
    except:
        go_buy_point_for_other_name(chat_id, bot)
        raise ProcessFailure

    go_buy_point_for_other_club_code(chat_id, bot)
    state.set_name('/Point/SellerList/For/Other/ClubCode')


@processor(
    state_manager,
    from_states='/Point/SellerList/For/Other/ClubCode',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def point_seller_list_for_other_club_code(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    user_id = update.get_user().get_id()
    club_code = update.get_message().get_text()

    if not check_club_code(club_code):
        go_buy_point_for_other_club_code(chat_id, bot)
    else:
        point_id = state.get_memory().get('point_id')
        x = buy_point_from_seller(point_id=point_id, buyer_id=user_id, chat_id=chat_id)
        if not x:
            message = "به نظر در خرید امتیاز مشکلی وجود دارد:\n" \
                      "1) نسبت به شارژ کیف پول خود اقدام نمیایید\n" \
                      "2) امتیاز جهت فروش حذف شده یا فروش رفته است\n" \
                      "با تشکر"
            bot.sendMessage(chat_id, message)
        else:
            point = get_point(point_id)
            data = state.get_memory()
            send_message_to_seller_for_other(
                name=data.get('name'),
                family=data.get('family'),
                club_code=club_code,
                point=point,
                bot=bot,
            )
            seller_detail(chat_id, point=point, bot=bot)
        go_point(chat_id, bot)
        state.set_name('/Point')
