from django.contrib.humanize.templatetags.humanize import intcomma
from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types
from django_tgbot.types.update import Update
from django_tgbot.exceptions import ProcessFailure
from Bot.bot import state_manager, TelegramBot
from Bot.models import TelegramState, TelegramUser

from ..BotProfile.CreateProfile import check_club_code
from .Dialog import go_buy_credit_duration, go_buy_credit_time, go_buy_credit_price, go_buy_credit_for, \
    go_buy_credit_for_other_name, go_buy_credit_for_other_club_code, credit_report, credit_history, \
    credit_channel, go_credit

from SiteSetting.SiteSettingRequest import credit_valid_day_long
from Date.DateRequest import valid_days
from CreditPack.CreditPackRequest import make_buy_credit, credit_min_max_price


@processor(
    state_manager,
    from_states='/Credit/Buy/Value',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def credit_buy_value(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    value = update.get_callback_query().get_data()

    state.reset_memory()
    state.update_memory({'credit_value': int(value)})

    go_buy_credit_duration(chat_id, bot)
    state.set_name('/Credit/Buy/Duration')


@processor(
    state_manager,
    from_states='/Credit/Buy/Duration',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def credit_buy_duration(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    value = update.get_callback_query().get_data()

    if state.get_memory().get('credit_value') == 50:
        if value == '1':
            bot.sendMessage(chat_id, 'دوره یک ماهه، برای بسته پنجاه میلیون تومانی در دسترس نمی باشد.')
            raise ProcessFailure

    if value not in ['1', '3', '6', '12']:
        bot.sendMessage(chat_id, '📌 لطفا یکی از گزینه های بالا را انتخاب نمایید.👆')
    else:
        state.update_memory({'credit_duration': value})

        go_buy_credit_time(chat_id, bot)
        state.set_name('/Credit/Buy/Time')


@processor(
    state_manager,
    from_states='/Credit/Buy/Time',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def credit_buy_time(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    value = update.get_callback_query().get_data()

    valid = valid_days(credit_valid_day_long())
    if value not in valid:
        bot.sendMessage(chat_id, '📌 لطفا یکی از گزینه های بالا را انتخاب نمایید.👆')
    else:
        state.update_memory({'credit_time': value})

        # send credit history
        data = state.get_memory()
        credit_value = data.get('credit_value')
        credit_duration = data.get('credit_duration')
        credit_history(chat_id, credit_value, credit_duration, bot)

        go_buy_credit_price(chat_id, bot)
        state.set_name('/Credit/Buy/Price')


# back
@processor(
    state_manager,
    from_states=['/Credit/Buy/Value', '/Credit/Buy/Duration', '/Credit/Buy/Time'],
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def back(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()

    go_credit(chat_id, bot)
    state.set_name('/Credit')


@processor(
    state_manager,
    from_states='/Credit/Buy/Price',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def credit_buy_price(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()

    if message_text == 'بازگشت':
        go_credit(chat_id, bot)
        state.set_name('/Credit')
        return

    if not message_text.isdigit():
        go_buy_credit_price(chat_id, bot)
    else:
        data = state.get_memory()
        min_price, max_price = credit_min_max_price(value=data.get('credit_value'),
                                                    duration=data.get('credit_duration'))

        price = int(message_text)
        if price < min_price:
            bot.sendMessage(chat_id, '📌 این مبلغ از حداقل قیمت کمتر است.')
            raise ProcessFailure
        elif price > max_price:
            bot.sendMessage(chat_id, '📌 این مبلغ از حداکثر قیمت بیشتر است.')
            raise ProcessFailure

        state.update_memory({'credit_price': price})
        bot.sendMessage(chat_id, f"قیمت {intcomma(price)} با موفقت ثبت شد.")

        go_buy_credit_for(chat_id, bot)
        state.set_name('/Credit/Buy/For')


@processor(
    state_manager,
    from_states='/Credit/Buy/For',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def credit_buy_for(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()

    user_id = update.get_user().get_id()
    user = TelegramUser.objects.get(telegram_id=user_id)

    if message_text == 'خودم':
        data = state.get_memory()
        credit = make_buy_credit(
            name=user.profile.Name,
            family=user.profile.Family,
            club_code=user.profile.ClubCode,
            value=data.get('credit_value'),
            price=data.get('credit_price'),
            duration=data.get('credit_duration'),
            time=data.get('credit_time'),
            buy_id=user_id,
            chat_id=chat_id,
        )
        state.reset_memory()

        if not credit:
            bot.sendMessage(chat_id, 'لطفا نسبت به شارژ کیف پول خود اقدام نمایید، با تشکر')
        else:
            credit_report(chat_id, credit, bot)
            credit_channel(credit, bot)
        go_credit(chat_id, bot)
        state.set_name('/Credit')

    elif message_text == 'شخصی دیگر':
        go_buy_credit_for_other_name(chat_id, bot)
        state.set_name('/Credit/Buy/For/Other/Name')

    else:
        go_buy_credit_for(chat_id, bot)


@processor(
    state_manager,
    from_states='/Credit/Buy/For/Other/Name',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def credit_buy_for_other_name(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()
    try:
        name, family = message_text.split('-')
        state.update_memory({'name': name, 'family': family})
    except:
        go_buy_credit_for_other_name(chat_id, bot)
        raise ProcessFailure

    go_buy_credit_for_other_club_code(chat_id, bot)
    state.set_name('/Credit/Buy/For/Other/ClubCode')


@processor(
    state_manager,
    from_states='/Credit/Buy/For/Other/ClubCode',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def credit_buy_for_other_club_code(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    club_code = update.get_message().get_text()
    user_id = update.get_user().get_id()

    if not check_club_code(club_code):
        go_buy_credit_for_other_club_code(chat_id, bot)
    else:
        data = state.get_memory()
        credit = make_buy_credit(
            name=data.get('name'),
            family=data.get('family'),
            club_code=club_code,
            value=data.get('credit_value'),
            price=data.get('credit_price'),
            duration=data.get('credit_duration'),
            time=data.get('credit_time'),
            buy_id=user_id,
            chat_id=chat_id,
        )
        state.reset_memory()

        if not credit:
            bot.sendMessage(chat_id, 'لطفا نسبت به شارژ کیف پول خود اقدام نمایید، با تشکر')
        else:
            credit_report(chat_id, credit, bot)
            credit_channel(credit, bot)

        go_credit(chat_id, bot)
        state.set_name('/Credit')
