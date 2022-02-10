from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types
from django_tgbot.types.update import Update
from Bot.bot import state_manager, TelegramBot
from Bot.models import TelegramState
from Bot.BotSetting import ReportChannel
from CreditPack.models import CreditPack

from ..BotDialog import go_home
from .Dialog import fail_credit, go_buy_credit_value, go_sell_credit_value, go_buyer_list_month, go_seller_list_month, \
    go_conf, go_my_request

from CreditPack.CreditPackRequest import conf_loan, cancel_credit, get_credit


@processor(
    state_manager,
    from_states='/Credit',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def credit_home(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()
    user_id = update.get_user().get_id()

    if message_text == 'درخواست خرید بسته اعتباری':
        go_buy_credit_value(chat_id, bot)
        state.set_name('/Credit/Buy/Value')

    elif message_text == 'درخواست فروش بسته اعتباری':
        go_sell_credit_value(chat_id, bot)
        state.set_name('/Credit/Sell/Value')

    elif message_text == 'خرید بسته اعتباری از لیست':
        go_seller_list_month(chat_id, bot)
        state.set_name('/Credit/SellerList')

    elif message_text == 'فروش بسته اعتباری به لیست':
        go_buyer_list_month(chat_id, bot)
        state.set_name('/Credit/BuyerList')

    elif message_text == 'درخواست های من':
        go_my_request(chat_id, user_id, bot)

    elif message_text == 'لیست انتظار تایید':
        go_conf(chat_id, user_id, bot)

    elif message_text == 'صفحه اول':
        go_home(chat_id, bot)
        state.set_name('/Home')

    else:
        fail_credit(chat_id, bot)


@processor(
    state_manager,
    from_states='/Credit',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def loan_conf(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    user_id = update.get_user().get_id()
    value = update.get_callback_query().get_data()

    if 'cancel' in value:
        id = int(value.split('-')[1])
        res = cancel_credit(id)
        if res:
            bot.sendMessage(chat_id, 'درخواست شما با موفقیت حذف شد.')

            # admin report channel
            bot.sendMessage(ReportChannel,
                            f"لغو بسته اعتباری: "
                            f"{id}\n"
                            f"user_id:{user_id}"
                            )

        else:
            bot.sendMessage(chat_id,
                            'در حذف درخواست شما مشکلی وجود دارد، علل شایع: معامله صورت گرفته یا قبلا حذف شده است.')
    else:
        res = conf_loan(user_id, int(value))
        credit: CreditPack = get_credit(value)
        if res:
            message = f"بسته اعتباری شماره " \
                      f"({value})" \
                      f" توسط فروشنده به باشگاه اگاه شما انتقال یافت" \
                      f" لطفا در صورت صحیح بودن و صحت اعتبار بسته اعتباری توسط کارگزاری آگاه را در ربات تایید کنید"
            if credit.SellID == user_id:
                bot.sendMessage(credit.ChatIDBuyer, message)

                # admin channel report
                bot.sendMessage(ReportChannel, message)

            else:
                # admin channel report -> for buyer
                report_channel_message = f"بسته اعتباری " \
                                         f"{value}" \
                                         f" توسط خریدار تایید شد."
                bot.sendMessage(ReportChannel, report_channel_message)

            bot.sendMessage(chat_id, 'با موفقیت درخواست تایید ثبت شد')
        else:
            bot.sendMessage(chat_id, 'متاسفانه به نظر در درخواست تایید مشکلی وجود دارد.')
