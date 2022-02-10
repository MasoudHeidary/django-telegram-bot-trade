from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types
from django_tgbot.types.update import Update
from Bot.bot import state_manager, TelegramBot
from Bot.models import TelegramState

from Loan.LoanRequest import buyer_by_month_value, sell_loan_to_buyer, get_loan
from .Dialog import buyer_list_pager, buyer_detail, send_message_to_buyer, go_loan, \
    go_buyer_list_value


@processor(
    state_manager,
    from_states='/Loan/BuyerList',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def loan_buyer_list(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()
    state.reset_memory()

    if message_text == '3 ماهه':
        state.update_memory({'month': 3})

    elif message_text == '6 ماهه':
        state.update_memory({'month': 6})

    elif message_text == 'یک ساله':
        state.update_memory({'month': 12})

    else:
        go_loan(chat_id, bot)
        state.set_name('/Loan')
        return

    go_buyer_list_value(chat_id, bot)
    state.set_name('/Loan/BuyerList/Value')


@processor(
    state_manager,
    from_states='/Loan/BuyerList/Value',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def loan_buyer_list_value(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()

    if message_text == 'پنج میلیون':
        state.update_memory({'value': 5})
    elif message_text == 'ده میلیون':
        state.update_memory({'value': 10})
    elif message_text == 'بیست میلیون':
        state.update_memory({'value': 20})
    elif message_text == 'پنجاه میلیون':
        state.update_memory({'value': 50})
    elif message_text == 'صد میلیون':
        state.update_memory({'value': 100})
    else:
        go_loan(chat_id, bot)
        state.set_name('/Loan')
        return

    month = state.get_memory().get('month')

    show_len = 3
    qu = buyer_by_month_value(month, state.get_memory().get('value'))
    if not qu:
        bot.sendMessage(chat_id, 'در حال حاضر وامی با این مشخصات وجود ندارد')
    else:
        buyer_list_pager(chat_id, qu, 0, show_len, bot)


@processor(
    state_manager,
    from_states='/Loan/BuyerList/Value',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def loan_buyer_list(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    user_id = update.get_user().get_id()
    value = update.get_callback_query().get_data()
    loan_value = state.get_memory().get('value')
    month = state.get_memory().get('month')

    show_len = 3
    if 'more' in value:
        qu = buyer_by_month_value(month, loan_value)

        index = int(value.split('-')[1])
        buyer_list_pager(chat_id, qu, index, show_len, bot)
    else:
        sell = sell_loan_to_buyer(loan_id=int(value), seller_id=user_id, chat_id=chat_id)
        if not sell:
            bot.sendMessage(chat_id, '📌 این وام دیگر در دسترس نمی باشد، لطفا لیست خود را به روز کنید.')
        else:
            loan = get_loan(int(value))
            send_message_to_buyer(loan, bot)
            buyer_detail(chat_id, loan, bot)
