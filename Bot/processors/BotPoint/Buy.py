from django.contrib.humanize.templatetags.humanize import intcomma
from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types
from django_tgbot.types.update import Update
from django_tgbot.exceptions import ProcessFailure
from Bot.bot import state_manager, TelegramBot
from Bot.models import TelegramState, TelegramUser

from ..BotProfile.CreateProfile import check_club_code

from .Dialog import go_buy_point_price, go_buy_point_for, go_buy_point_for_other_name, \
    go_buy_point_for_other_club_code, go_buy_point_number, point_report, point_history, \
    point_channel, go_point

from SiteSetting.SiteSettingRequest import point_min_max_number, point_min_max_price
from Point.PointRequest import make_buy_point


@processor(
    state_manager,
    from_states='/Point/Buy/Number',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def point_buy_number(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    number = update.get_message().get_text()
    min, max = point_min_max_number()

    if number == 'بازگشت':
        go_point(chat_id, bot)
        state.set_name('/Point')
        return

    # check be digit + check min, max
    if not number.isdigit():
        go_buy_point_number(chat_id, bot)
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

    go_buy_point_price(chat_id, bot)
    state.set_name('/Point/Buy/Price')


@processor(
    state_manager,
    from_states='/Point/Buy/Price',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def point_buy_price(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    price = update.get_message().get_text()
    min, max = point_min_max_price()

    if price == 'بازگشت':
        go_point(chat_id, bot)
        state.set_name('/Point')
        return

    # check be digit + check min, max
    if not price.isdigit():
        go_buy_point_price(chat_id, bot)
        raise ProcessFailure

    price = int(price)
    if price < min:
        bot.sendMessage(chat_id, '📌 این مبلغ از حداقل قیمت کمتر است.')
        raise ProcessFailure
    elif price > max:
        bot.sendMessage(chat_id, '📌 این مبلغ از حداکثر قیمت بیشتر است.')
        raise ProcessFailure

    state.update_memory({'point_price': price})
    bot.sendMessage(chat_id, f"قیمت {intcomma(price)} ریال با موفقت ثبت شد.")

    go_buy_point_for(chat_id, bot)
    state.set_name('/Point/Buy/For')


@processor(
    state_manager,
    from_states='/Point/Buy/For',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def point_buy_for(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()

    user_id = update.get_user().get_id()
    user = TelegramUser.objects.get(telegram_id=user_id)

    if message_text == 'خودم':
        data = state.get_memory()
        point = make_buy_point(
            name=user.profile.Name,
            family=user.profile.Family,
            club_code=user.profile.ClubCode,
            number=data.get('point_number'),
            price=data.get('point_price'),
            buy_id=user_id,
            chat_id=chat_id,
        )
        state.reset_memory()

        if not point:
            bot.sendMessage(chat_id, 'لطفا نسبت به شارژ کیف پول خود اقدام نمایید، با تشکر')
        else:
            point_report(chat_id, point, bot)
            point_channel(point, bot)
        go_point(chat_id, bot)
        state.set_name('/Point')

    elif message_text == 'شخصی دیگر':
        go_buy_point_for_other_name(chat_id, bot)
        state.set_name('/Point/Buy/For/Other/Name')

    else:
        go_buy_point_for(chat_id, bot)


@processor(
    state_manager,
    from_states='/Point/Buy/For/Other/Name',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def point_buy_for_other_name(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()
    try:
        name, family = message_text.split('-')
        state.update_memory({'name': name, 'family': family})
    except:
        go_buy_point_for_other_name(chat_id, bot)
        raise ProcessFailure

    go_buy_point_for_other_club_code(chat_id, bot)
    state.set_name('/Point/Buy/For/Other/ClubCode')


@processor(
    state_manager,
    from_states='/Point/Buy/For/Other/ClubCode',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def point_buy_for_other_clubcode(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    club_code = update.get_message().get_text()
    user_id = update.get_user().get_id()

    if not check_club_code(club_code):
        go_buy_point_for_other_club_code(chat_id, bot)
    else:
        data = state.get_memory()
        point = make_buy_point(
            name=data.get('name'),
            family=data.get('family'),
            club_code=club_code,
            number=data.get('point_number'),
            price=data.get('point_price'),
            buy_id=user_id,
            chat_id=chat_id,
        )
        state.reset_memory()

        if not point:
            bot.sendMessage(chat_id, 'لطفا نسبت به شارژ کیف پول خود اقدام نمایید، با تشکر')
        else:
            point_report(chat_id, point, bot)
            point_channel(point, bot)

        go_point(chat_id, bot)
        state.set_name('/Point')
