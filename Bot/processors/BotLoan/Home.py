from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types
from django_tgbot.types.update import Update
from Bot.bot import state_manager, TelegramBot
from Bot.models import TelegramState
from Bot.BotSetting import ReportChannel
from Loan.models import Loan

from ..BotDialog import go_home
from .Dialog import fail_loan, go_buy_loan_Value, go_conf, go_sell_loan_value, go_seller_list_month, \
    go_my_request, go_buyer_list_month

from Loan.LoanRequest import conf_loan, cancel_loan, get_loan


@processor(
    state_manager,
    from_states='/Loan',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def loan_home(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    user_id = update.get_user().get_id()
    message_text = update.get_message().get_text()

    if message_text == 'درخواست خرید وام':
        go_buy_loan_Value(chat_id, bot)
        state.set_name('/Loan/Buy/Value')

    elif message_text == 'درخواست فروش وام':
        go_sell_loan_value(chat_id, bot)
        state.set_name('/Loan/Sell/Value')

    elif message_text == 'خرید وام از لیست':
        go_seller_list_month(chat_id, bot)
        state.set_name('/Loan/SellerList')

    elif message_text == 'فروش وام به لیست':
        go_buyer_list_month(chat_id, bot)
        state.set_name('/Loan/BuyerList')

    elif message_text == 'درخواست های من':
        go_my_request(chat_id, user_id, bot)

    elif message_text == 'لیست انتظار تایید':
        go_conf(chat_id, user_id, bot)

    elif message_text == 'صفحه اول':
        go_home(chat_id, bot)
        state.set_name('/Home')

    else:
        fail_loan(chat_id, bot)


@processor(
    state_manager,
    from_states='/Loan',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def loan_conf(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    user_id = update.get_user().get_id()
    value = update.get_callback_query().get_data()

    if 'cancel' in value:
        id = int(value.split('-')[1])
        res = cancel_loan(id)
        if res:
            bot.sendMessage(chat_id, 'درخواست شما با موفقیت حذف شد.')

            # admin report channel
            bot.sendMessage(ReportChannel,
                            f"لغو وام: "
                            f"{id}\n"
                            f"user_id: {user_id}"
                            )

        else:
            bot.sendMessage(chat_id,
                            'در حذف درخواست شما مشکلی وجود دارد، علل شایع: معامله صورت گرفته یا قبلا حذف شده است.')
    else:
        res = conf_loan(user_id, int(value))
        loan: Loan = get_loan(value)
        if res:
            message = f"وام شماره " \
                      f"({value})" \
                      f" توسط فروشنده به باشگاه اگاه شما انتقال یافت" \
                      f" لطفا در صورت صحیح بودن و صحت اعتبار وام توسط کارگزاری آگاه را در ربات تایید کنید"
            if loan.SellID == user_id:
                bot.sendMessage(loan.ChatIDBuyer, message)

                # admin report channel
                bot.sendMessage(ReportChannel, message)

            else:
                # admin report channel -> for buyer
                report_channel_message = f"وام شماره " \
                                         f"{value}" \
                                         f" توسط خریدار تایید شد"
                bot.sendMessage(ReportChannel, report_channel_message)

            bot.sendMessage(chat_id, 'با موفقیت درخواست تایید ثبت شد')
        else:
            bot.sendMessage(chat_id, 'متاسفانه به نظر در درخواست تایید مشکلی وجود دارد.')
