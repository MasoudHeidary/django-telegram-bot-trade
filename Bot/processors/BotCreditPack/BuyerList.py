from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types
from django_tgbot.types.update import Update
from Bot.bot import state_manager, TelegramBot
from Bot.models import TelegramState

from .Dialog import buyer_list_pager, send_message_to_buyer, buyer_detail, go_credit, go_buyer_list_value

from CreditPack.CreditPackRequest import buyer_by_month_value, sell_loan_to_buyer, get_credit


@processor(
    state_manager,
    from_states='/Credit/BuyerList',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def credit_buyer_list(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()
    state.reset_memory()

    if message_text == '1 ماهه':
        state.update_memory({'month': 1})
    elif message_text == '3 ماهه':
        state.update_memory({'month': 3})
    elif message_text == '6 ماهه':
        state.update_memory({'month': 6})
    elif message_text == 'یک ساله':
        state.update_memory({'month': 12})
    else:
        # state.set_name('/Home')
        # go_home(chat_id, bot)
        go_credit(chat_id, bot)
        state.set_name('/Credit')
        return

    go_buyer_list_value(chat_id, bot)
    state.set_name('/Credit/BuyerList/Value')


@processor(
    state_manager,
    from_states='/Credit/BuyerList/Value',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def credit_buyer_list_value(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()

    if message_text == 'دو میلیون':
        state.update_memory({'value': 2})
    elif message_text == 'سه میلیون':
        state.update_memory({'value': 3})
    elif message_text == 'پنج میلیون':
        state.update_memory({'value': 5})
    elif message_text == 'ده میلیون':
        state.update_memory({'value': 10})
    elif message_text == 'بیست میلیون':
        state.update_memory({'value': 20})
    elif message_text == 'پنجاه میلیون':
        state.update_memory({'value': 50})
    else:
        go_credit(chat_id, bot)
        state.set_name('/Credit')
        return

    month = state.get_memory().get('month')
    credit_value = state.get_memory().get('value')

    show_len = 3
    qu = buyer_by_month_value(month, credit_value)
    if not qu:
        bot.sendMessage(chat_id, 'در حال حاضر بسته اعتباری با این مشخصات وجود ندارد')
    else:
        buyer_list_pager(chat_id, qu, 0, show_len, bot)


@processor(
    state_manager,
    from_states='/Credit/BuyerList/Value',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def credit_buyer_list(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    user_id = update.get_user().get_id()
    value = update.get_callback_query().get_data()
    show_len = 3

    if 'more' in value:
        month = state.get_memory().get('month')
        credit_value = state.get_memory().get('value')
        qu = buyer_by_month_value(month, credit_value)

        index = int(value.split('-')[1])
        buyer_list_pager(chat_id, qu, index, show_len, bot)
    else:
        sell = sell_loan_to_buyer(loan_id=int(value), seller_id=user_id, chat_id=chat_id)
        if not sell:
            bot.sendMessage(chat_id, '📌 این بسته اعتباری دیگر در دسترس نمی باشد، لطفا لیست خود را به روز کنید.')
        else:
            credit = get_credit(int(value))
            send_message_to_buyer(credit, bot)
            buyer_detail(chat_id, credit, bot)
