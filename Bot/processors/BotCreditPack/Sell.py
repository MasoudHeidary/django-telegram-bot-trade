from django.contrib.humanize.templatetags.humanize import intcomma
from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from django_tgbot.exceptions import ProcessFailure
from Bot.bot import state_manager, TelegramBot
from Bot.models import TelegramState, TelegramUser

from .Dialog import go_sell_credit_duration, go_sell_credit_price, \
    credit_history, credit_report_for_seller, credit_channel_for_seller, go_credit

# from Date.DateRequest import valid_days
from CreditPack.CreditPackRequest import make_sell_credit, credit_min_max_price


# from SiteSetting.SiteSettingRequest import credit_valid_day_long


@processor(
    state_manager,
    from_states='/Credit/Sell/Value',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def credit_sell_value(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    value = update.get_callback_query().get_data()

    state.reset_memory()
    state.update_memory({'credit_value': int(value)})

    go_sell_credit_duration(chat_id, bot)
    state.set_name('/Credit/Sell/Duration')


@processor(
    state_manager,
    from_states='/Credit/Sell/Duration',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def credit_sell_duration(bot: TelegramBot, update: Update, state: TelegramState):
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

        # send credit history
        data = state.get_memory()
        credit_value = data.get('credit_value')
        credit_duration = data.get('credit_duration')
        credit_history(chat_id, credit_value, credit_duration, bot)

        # go_sell_credit_time(chat_id, bot)
        # state.set_name('/Credit/Sell/Time')
        go_sell_credit_price(chat_id, bot)
        state.set_name('/Credit/Sell/Price')


# back
@processor(
    state_manager,
    from_states=['/Credit/Sell/Value', '/Credit/Sell/Duration'],
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def back(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()

    go_credit(chat_id, bot)
    state.set_name('/Credit')


# @processor(
#     state_manager,
#     from_states='/Credit/Sell/Time',
#     update_types=update_types.CallbackQuery,
#     message_types=message_types.Text,
# )
# def credit_sell_time(bot: TelegramBot, update: Update, state: TelegramState):
#     chat_id = update.get_chat().get_id()
#     value = update.get_callback_query().get_data()
#
#     valid = valid_days(credit_valid_day_long())
#     if value not in valid:
#         bot.sendMessage(chat_id, '📌 لطفا یکی از گزینه های بالا را انتخاب نمایید.👆')
#     else:
#         state.update_memory({'credit_time': value})
#
#         # send credit history
#         data = state.get_memory()
#         credit_value = data.get('credit_value')
#         credit_duration = data.get('credit_duration')
#         credit_history(chat_id, credit_value, credit_duration, bot)
#
#         go_sell_credit_price(chat_id, bot)
#         state.set_name('/Credit/Sell/Price')


@processor(
    state_manager,
    from_states='/Credit/Sell/Price',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def credit_sell_price(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()

    user_id = update.get_user().get_id()
    user = TelegramUser.objects.get(telegram_id=user_id)

    if message_text == 'بازگشت':
        go_credit(chat_id, bot)
        state.set_name('/Credit')
        return

    if not message_text.isdigit():
        go_sell_credit_price(chat_id, bot)
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

        data = state.get_memory()
        credit = make_sell_credit(
            user=user,
            value=data.get('credit_value'),
            # time=data.get('credit_time'),
            duration=data.get('credit_duration'),
            price=data.get('credit_price'),
            sell_id=user_id,
            chat_id=chat_id
        )
        state.reset_memory()
        credit_report_for_seller(chat_id, credit, bot)
        credit_channel_for_seller(credit, bot)

        go_credit(chat_id, bot)
        state.set_name('/Credit')
