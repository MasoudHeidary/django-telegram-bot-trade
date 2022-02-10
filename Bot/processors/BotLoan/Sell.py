from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from django_tgbot.exceptions import ProcessFailure
from Bot.bot import state_manager, TelegramBot
from Bot.models import TelegramState, TelegramUser

from .Dialog import go_sell_loan_duration, go_sell_loan_price, loan_history, \
    loan_report_for_seller, loan_channel_for_seller, go_loan
# from ..BotDialog import go_home

# from Date.DateRequest import valid_days
from Loan.LoanRequest import make_sell_loan, loan_min_max_price


# from SiteSetting.SiteSettingRequest import loan_valid_day_long


@processor(
    state_manager,
    from_states='/Loan/Sell/Value',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def loan_sell_value(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    value = update.get_callback_query().get_data()

    state.reset_memory()
    state.update_memory({'loan_value': int(value)})

    go_sell_loan_duration(chat_id, bot)
    state.set_name('/Loan/Sell/Duration')


@processor(
    state_manager,
    from_states='/Loan/Sell/Duration',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def loan_sell_duration(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    value = update.get_callback_query().get_data()

    if value not in ['3', '6', '12']:
        bot.sendMessage(chat_id, '📌 لطفا یکی از گزینه های بالا را انتخاب نمایید.👆')
    else:
        state.update_memory({'loan_duration': value})

        # send loan history
        data = state.get_memory()
        loan_value = data.get('loan_value')
        loan_duration = data.get('loan_duration')
        loan_history(chat_id, loan_value, loan_duration, bot)

        # go_sell_loan_time(chat_id, bot)
        # state.set_name('/Loan/Sell/Time')
        go_sell_loan_price(chat_id, bot)
        state.set_name('/Loan/Sell/Price')


# back home
@processor(
    state_manager,
    from_states=['/Loan/Sell/Value', '/Loan/Sell/Duration'],
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def bacK_to_loan(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()

    go_loan(chat_id, bot)
    state.set_name('/Loan')


# @processor(
#     state_manager,
#     from_states='/Loan/Sell/Time',
#     update_types=update_types.CallbackQuery,
#     message_types=message_types.Text,
# )
# def loan_sell_time(bot: TelegramBot, update: Update, state: TelegramState):
#     chat_id = update.get_chat().get_id()
#     value = update.get_callback_query().get_data()
#
#     valid = valid_days(loan_valid_day_long())
#     if value not in valid:
#         bot.sendMessage(chat_id, '📌 لطفا یکی از گزینه های بالا را انتخاب نمایید.👆')
#     else:
#         state.update_memory({'loan_time': value})
#
#         # send loan history
#         data = state.get_memory()
#         loan_value = data.get('loan_value')
#         loan_duration = data.get('loan_duration')
#         loan_history(chat_id, loan_value, loan_duration, bot)
#
#         go_sell_loan_price(chat_id, bot)
#         state.set_name('/Loan/Sell/Price')


@processor(
    state_manager,
    from_states='/Loan/Sell/Price',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def loan_sell_price(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()

    user_id = update.get_user().get_id()
    user = TelegramUser.objects.get(telegram_id=user_id)

    if message_text == 'بازگشت':
        go_loan(chat_id, bot)
        state.set_name('/Loan')
        return

    if not message_text.isdigit():
        bot.sendMessage(chat_id, '📌 لطفا قیمت وام را با عدد لاتین و به تومان مشخص نمایید.')
    else:
        data = state.get_memory()
        min_price, max_price = loan_min_max_price(value=data.get('loan_value'), duration=data.get('loan_duration'))

        price = int(message_text)
        if price < min_price:
            bot.sendMessage(chat_id, '📌 این مبلغ از حداقل قیمت کمتر است.')
            raise ProcessFailure
        elif price > max_price:
            bot.sendMessage(chat_id, '📌 این مبلغ از حداکثر قیمت بیشتر است.')
            raise ProcessFailure

        state.update_memory({'loan_price': price})
        bot.sendMessage(chat_id, f"قیمت {price} با موفقت ثبت شد.")

        data = state.get_memory()
        loan = make_sell_loan(
            user=user,
            value=data.get('loan_value'),
            # time=data.get('loan_time'),
            duration=data.get('loan_duration'),
            price=data.get('loan_price'),
            sell_id=user_id,
            chat_id=chat_id
        )
        state.reset_memory()
        loan_report_for_seller(chat_id, loan, bot)
        loan_channel_for_seller(loan, bot)

        go_loan(chat_id, bot)
        state.set_name('/Loan')
        # go_home(chat_id, bot)
        # state.set_name('/Home')
