from django.contrib.humanize.templatetags.humanize import intcomma
from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from django_tgbot.exceptions import ProcessFailure
from Bot.bot import state_manager, TelegramBot
from Bot.models import TelegramState, TelegramUser

from .Dialog import go_sell_point_price, go_sell_point_number, point_report_for_seller, point_history, \
    point_channel_for_seller, go_point

from SiteSetting.SiteSettingRequest import point_min_max_number, point_min_max_price
from Point.PointRequest import make_sell_point


@processor(
    state_manager,
    from_states='/Point/Sell/Number',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def point_sell_number(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    number = update.get_message().get_text()
    min, max = point_min_max_number()

    if number == 'بازگشت':
        go_point(chat_id, bot)
        state.set_name('/Point')
        return

    # check be digit + check min, max
    if not number.isdigit():
        go_sell_point_number(chat_id, bot)
        raise ProcessFailure

    number = int(number)
    if number < min:
        bot.sendMessage(chat_id, '📌 این تعداد از حداقل تعداد کمتر است.')
        raise ProcessFailure
    elif number > max:
        bot.sendMessage(chat_id, '📌 این تعداد از حداکثر تعداد بیشتر است.')
        raise ProcessFailure

    state.reset_memory()
    state.update_memory({'point_number': number})
    bot.sendMessage(chat_id, f"تعداد {intcomma(number)} با موفقت ثبت شد.")

    # history
    point_history(chat_id, bot)

    go_sell_point_price(chat_id, bot)
    state.set_name('/Point/Sell/Price')


@processor(
    state_manager,
    from_states='/Point/Sell/Price',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def point_sell_price(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    price = update.get_message().get_text()
    min, max = point_min_max_price()

    user_id = update.get_user().get_id()
    user = TelegramUser.objects.get(telegram_id=user_id)

    if price == 'بازگشت':
        go_point(chat_id, bot)
        state.set_name('/Point')
        return

    # check be digit + check min, max
    if not price.isdigit():
        go_sell_point_price(chat_id, bot)
        raise ProcessFailure

    price = int(price)
    if price < min:
        bot.sendMessage(chat_id, '📌 این مبلغ از حداقل قیمت کمتر است.')
        raise ProcessFailure
    elif price > max:
        bot.sendMessage(chat_id, '📌 این مبلغ از حداکثر قیمت بیشتر است.')
        raise ProcessFailure

    state.update_memory({'point_price': price})
    bot.sendMessage(chat_id, f"قیمت {intcomma(price)} با موفقت ثبت شد.")

    data = state.get_memory()
    point = make_sell_point(
        user=user,
        number=data.get('point_number'),
        price=data.get('point_price'),
        sell_id=user_id,
        chat_id=chat_id
    )
    state.reset_memory()

    point_report_for_seller(chat_id, point, bot)
    point_channel_for_seller(point, bot)

    go_point(chat_id, bot)
    state.set_name('/Point')
