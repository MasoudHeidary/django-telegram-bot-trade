from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from django_tgbot.exceptions import ProcessFailure
from Bot.bot import state_manager, TelegramBot
from Bot.models import TelegramState, TelegramUser
from Date.DateRequest import valid_days
from SiteSetting.SiteSettingRequest import loan_valid_day_long

# from ..BotDialog import go_home

from Loan.LoanRequest import seller_by_month_value, buy_loan_from_seller, get_loan
from .Dialog import seller_list_pager, buyer_detail, send_message_to_buyer, go_sell_list_for, \
    go_buy_loan_for_other_name, go_buy_loan_for_other_club_code, send_message_to_seller_for_me, \
    send_message_to_seller_for_other, seller_detail, loan_report, go_sell_loan_time, go_loan, go_buy_loan_Value, \
    go_seller_list_value

from ..BotProfile.CreateProfile import check_club_code


@processor(
    state_manager,
    from_states='/Loan/SellerList',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def loan_seller_list(bot: TelegramBot, update: Update, state: TelegramState):
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
        # state.set_name('/Home')
        # go_home(chat_id, bot)

    go_seller_list_value(chat_id, bot)
    state.set_name('/Loan/SellerList/Value')


@processor(
    state_manager,
    from_states='/Loan/SellerList/Value',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def loan_seller_list_value(bot: TelegramBot, update: Update, state: TelegramState):
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
    qu = seller_by_month_value(month, state.get_memory().get('value'))
    if not qu:
        bot.sendMessage(chat_id, 'در حال حاضر وامی با این مشخصات وجود ندارد')
    else:
        seller_list_pager(chat_id, qu, 0, show_len, bot)


@processor(
    state_manager,
    from_states='/Loan/SellerList/Value',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def loan_seller_list(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    # user_id = update.get_user().get_id()
    value = update.get_callback_query().get_data()
    show_len = 3

    if 'more' in value:
        month = state.get_memory().get('month')
        loan_value = state.get_memory().get('value')
        qu = seller_by_month_value(month, loan_value)

        index = int(value.split('-')[1])
        seller_list_pager(chat_id, qu, index, show_len, bot)
    else:
        state.update_memory({'loan_id': value})

        go_sell_loan_time(chat_id, bot)
        state.set_name('/Loan/SellerList/Time')
        # go_sell_list_for(chat_id, bot)
        # state.set_name('/Loan/SellerList/For')


@processor(
    state_manager,
    from_states='/Loan/SellerList/Time',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def loan_sell_time(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    value = update.get_callback_query().get_data()

    valid = valid_days(loan_valid_day_long())
    if value not in valid:
        bot.sendMessage(chat_id, '📌 لطفا یکی از گزینه های بالا را انتخاب نمایید.👆')
    else:
        state.update_memory({'loan_time': value})
        go_sell_list_for(chat_id, bot)
        state.set_name('/Loan/SellerList/For')


# back
@processor(
    state_manager,
    from_states='/Loan/SellerList/Time',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def loan_back(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()

    go_loan(chat_id, bot)
    state.set_name('/Loan')


@processor(
    state_manager,
    from_states='/Loan/SellerList/For',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def loan_seller_list_for(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()
    user_id = update.get_user().get_id()

    loan_id = state.get_memory().get('loan_id')
    time = state.get_memory().get('loan_time')

    if message_text == 'خودم':
        x = buy_loan_from_seller(loan_id=loan_id, time=time, buyer_id=user_id, chat_id=chat_id)
        if not x:
            message = "به نظر در خرید وام مشکلی وجود دارد:\n" \
                      "1) نسبت به شارژ کیف پول خود اقدام نمیایید\n" \
                      "2) وام جهت فروش حذف شده یا فروش رفته است\n" \
                      "با تشکر"
            bot.sendMessage(chat_id, message)
        else:
            loan = get_loan(loan_id)
            send_message_to_seller_for_me(user_id=user_id, loan=loan, bot=bot)
            seller_detail(chat_id, loan, bot)

        go_loan(chat_id, bot)
        state.set_name('/Loan')
        # go_home(chat_id, bot)
        # state.set_name('/Home')

    elif message_text == 'شخصی دیگر':
        go_buy_loan_for_other_name(chat_id, bot)
        state.set_name('/Loan/SellerList/For/Other/Name')
    else:
        go_loan(chat_id, bot)
        state.set_name('/Loan')
        # go_home(chat_id, bot)
        # state.set_name('/Home')


@processor(
    state_manager,
    from_states='/Loan/SellerList/For/Other/Name',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def loan_seller_list_for_other_name(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()

    try:
        name, family = message_text.split('-')
        state.update_memory({'name': name, 'family': family})
    except:
        go_buy_loan_for_other_name(chat_id, bot)
        raise ProcessFailure

    go_buy_loan_for_other_club_code(chat_id, bot)
    state.set_name('/Loan/SellerList/For/Other/ClubCode')


@processor(
    state_manager,
    from_states='/Loan/SellerList/For/Other/ClubCode',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def loan_seller_list_for_other_club_code(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    user_id = update.get_user().get_id()
    club_code = update.get_message().get_text()
    time = state.get_memory().get('loan_time')

    if not check_club_code(club_code):
        go_buy_loan_for_other_club_code(chat_id, bot)
    else:
        loan_id = state.get_memory().get('loan_id')
        x = buy_loan_from_seller(loan_id=loan_id, time=time, buyer_id=user_id, chat_id=chat_id)
        if not x:
            message = "به نظر در خرید وام مشکلی وجود دارد:\n" \
                      "1) نسبت به شارژ کیف پول خود اقدام نمیایید\n" \
                      "2) وام جهت فروش حذف شده یا فروش رفته است\n" \
                      "با تشکر"
            bot.sendMessage(chat_id, message)
        else:
            loan = get_loan(loan_id)
            data = state.get_memory()
            send_message_to_seller_for_other(
                name=data.get('name'),
                family=data.get('family'),
                club_code=club_code,
                loan=loan,
                bot=bot,
            )
            # loan_report(chat_id, loan, bot) -> bug -> dont need
            seller_detail(chat_id, loan=loan, bot=bot)
        go_loan(chat_id, bot)
        state.set_name('/Loan')
        # go_home(chat_id, bot)
        # state.set_name('/Home')
