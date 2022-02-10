from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types
from django_tgbot.types.update import Update
from django_tgbot.exceptions import ProcessFailure
from Bot.bot import state_manager, TelegramBot
from Bot.models import TelegramState, TelegramUser

from .Dialog import go_buy_loan_duration, go_buy_loan_time, go_buy_loan_price, go_buy_loan_for, \
    go_buy_loan_for_other_name, go_buy_loan_for_other_club_code, loan_history, loan_report, \
    loan_report_channel, go_loan

# from ..BotDialog import go_home
from ..BotProfile.CreateProfile import check_club_code

from Loan.LoanRequest import make_buy_loan, loan_min_max_price
from Date.DateRequest import valid_days
from SiteSetting.SiteSettingRequest import loan_valid_day_long


@processor(
    state_manager,
    from_states='/Loan/Buy/Value',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def loan_buy_value(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    value = update.get_callback_query().get_data()

    state.reset_memory()
    state.update_memory({'loan_value': int(value)})

    go_buy_loan_duration(chat_id, bot)
    state.set_name('/Loan/Buy/Duration')


@processor(
    state_manager,
    from_states='/Loan/Buy/Duration',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def loan_buy_duration(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    value = update.get_callback_query().get_data()

    if value not in ['3', '6', '12']:
        bot.sendMessage(chat_id, '📌 لطفا یکی از گزینه های بالا را انتخاب نمایید.👆')
    else:
        state.update_memory({'loan_duration': value})

        go_buy_loan_time(chat_id, bot)
        state.set_name('/Loan/Buy/Time')


@processor(
    state_manager,
    from_states='/Loan/Buy/Time',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def loan_buy_time(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    value = update.get_callback_query().get_data()

    valid = valid_days(loan_valid_day_long())
    if value not in valid:
        bot.sendMessage(chat_id, '📌 لطفا یکی از گزینه های بالا را انتخاب نمایید.👆')
    else:
        state.update_memory({'loan_time': value})

        # send loan history
        data = state.get_memory()
        loan_value = data.get('loan_value')
        loan_duration = data.get('loan_duration')
        loan_history(chat_id, loan_value, loan_duration, bot)

        go_buy_loan_price(chat_id, bot)
        state.set_name('/Loan/Buy/Price')


# back home
@processor(
    state_manager,
    from_states=['/Loan/Buy/Time', '/Loan/Buy/Value', '/Loan/Buy/Duration'],
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def bacK_to_loan(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()

    go_loan(chat_id, bot)
    state.set_name('/Loan')


@processor(
    state_manager,
    from_states='/Loan/Buy/Price',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def loan_buy_price(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()

    if message_text == 'بازگشت':
        go_loan(chat_id, bot)
        state.set_name('/Loan')

    elif not message_text.isdigit():
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

        go_buy_loan_for(chat_id, bot)
        state.set_name('/Loan/Buy/For')


@processor(
    state_manager,
    from_states='/Loan/Buy/For',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def loan_buy_for(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()

    user_id = update.get_user().get_id()
    user = TelegramUser.objects.get(telegram_id=user_id)

    if message_text == 'بازگشت':
        go_loan(chat_id, bot)
        state.set_name('/Loan')

    elif message_text == 'خودم':
        data = state.get_memory()
        loan = make_buy_loan(
            name=user.profile.Name,
            family=user.profile.Family,
            club_code=user.profile.ClubCode,
            value=data.get('loan_value'),
            price=data.get('loan_price'),
            duration=data.get('loan_duration'),
            time=data.get('loan_time'),
            buy_id=user_id,
            chat_id=chat_id,
        )
        state.reset_memory()

        if not loan:
            bot.sendMessage(chat_id, 'لطفا نسبت به شارژ کیف پول خود اقدام نمایید، با تشکر')
        else:
            loan_report(chat_id, loan, bot)
            loan_report_channel(loan, bot)

        go_loan(chat_id, bot)
        state.set_name('/Loan')
        # go_home(chat_id, bot)
        # state.set_name('/Home')
    elif message_text == 'شخصی دیگر':
        go_buy_loan_for_other_name(chat_id, bot)
        state.set_name('/Loan/Buy/For/Other/Name')
    else:
        go_buy_loan_for(chat_id, bot)


@processor(
    state_manager,
    from_states='/Loan/Buy/For/Other/Name',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def loan_buy_for_other_name(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()

    if message_text == 'بازگشت':
        go_loan(chat_id, bot)
        state.set_name('/Loan')
        return

    try:
        name, family = message_text.split('-')
        state.update_memory({'name': name, 'family': family})
    except:
        message = "📌 لطفا نام و نام خانوادگی خریدار را با خط تیره وارد کنید." \
                  "\n" \
                  "👈 مثل: رضا-عطاری"
        bot.sendMessage(chat_id, message)
        raise ProcessFailure

    go_buy_loan_for_other_club_code(chat_id, bot)
    state.set_name('/Loan/Buy/For/Other/ClubCode')


@processor(
    state_manager,
    from_states='/Loan/Buy/For/Other/ClubCode',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def loan_buy_for_other_club_code(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    user_id = update.get_user().get_id()
    club_code = update.get_message().get_text()

    message_text = update.get_message().get_text()
    if message_text == 'بازگشت':
        go_loan(chat_id, bot)
        state.set_name('/Loan')
        return

    if not check_club_code(club_code):
        bot.sendMessage(chat_id, '📌 لطفا کد باشگاه خریدار را وارد کنید.(6حرف)')
    else:
        data = state.get_memory()
        loan = make_buy_loan(
            name=data.get('name'),
            family=data.get('family'),
            club_code=club_code,
            value=data.get('loan_value'),
            price=data.get('loan_price'),
            duration=data.get('loan_duration'),
            time=data.get('loan_time'),
            buy_id=user_id,
            chat_id=chat_id,
        )
        state.reset_memory()

        if not loan:
            bot.sendMessage(chat_id, 'لطفا نسبت به شارژ کیف پول خود اقدام نمایید، با تشکر')
        else:
            loan_report(chat_id, loan, bot)
            loan_report_channel(loan, bot)

        go_loan(chat_id, bot)
        state.set_name('/Loan')
        # go_home(chat_id, bot)
        # state.set_name('/Home')
