from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from Bot.bot import state_manager, TelegramBot
from Bot.BotSetting import ReportChannel
from Bot.models import TelegramState, TelegramUser

from ..BotDialog import go_home
from .Dialog import fail_point, go_buy_point_number, go_sell_point_number
from .Dialog import buyer_list_pager, seller_list_pager, \
    go_conf, go_my_request

from Point.models import Point
from Point.PointRequest import point_buyer, point_seller, conf_point, cancel_point, get_point


@processor(
    state_manager,
    from_states='/Point',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def point_home(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()
    user_id = update.get_user().get_id()

    if message_text == 'درخواست خرید امتیاز':
        go_buy_point_number(chat_id, bot)
        state.set_name('/Point/Buy/Number')

    elif message_text == 'درخواست فروش امتیاز':
        go_sell_point_number(chat_id, bot)
        state.set_name('/Point/Sell/Number')

    elif message_text == 'خرید امتیاز از لیست':
        show_len = 5
        qu = point_seller()
        if not qu:
            bot.sendMessage(chat_id, 'در حال حاضر امتیازی برای معامله وجود ندارد')
        else:
            seller_list_pager(chat_id, qu, 0, show_len, bot)
            state.set_name('/Point/SellerList')

    elif message_text == 'فروش امتیاز به لیست':
        show_len = 5
        qu = point_buyer()
        if not qu:
            bot.sendMessage(chat_id, 'در حال حاضر امتیازی برای معامله وجود ندارد')
        else:
            buyer_list_pager(chat_id, qu, 0, show_len, bot)
            state.set_name('/Point/BuyerList')

    elif message_text == 'درخواست های من':
        go_my_request(chat_id, user_id, bot)

    elif message_text == 'لیست انتظار تایید':
        go_conf(chat_id, user_id, bot)

    elif message_text == 'صفحه اول':
        go_home(chat_id, bot)
        state.set_name('/Home')

    else:
        fail_point(chat_id, bot)


@processor(
    state_manager,
    from_states='/Point',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def point_conf(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    user_id = update.get_user().get_id()
    value = update.get_callback_query().get_data()

    if 'cancel' in value:
        id = int(value.split('-')[1])
        res = cancel_point(id)
        if res:
            bot.sendMessage(chat_id, 'درخواست شما با موفقیت حذف شد.')

            # admin report channel
            bot.sendMessage(ReportChannel,
                            f"لغو امتیاز: "
                            f"{id}\n"
                            f"user_id: {user_id}"
                            )
        else:
            bot.sendMessage(chat_id,
                            'در حذف درخواست شما مشکلی وجود دارد، علل شایع: معامله صورت گرفته یا قبلا حذف شده است.')
    else:
        res = conf_point(user_id, int(value))
        point: Point = get_point(value)
        if res:
            message = "امتیاز شماره " \
                      f"({value})" \
                      " توسط فروشنده به باشگاه اگاه شما انتقال یافت لطفا در صورت صحیح بودن آن را در ربات تایید کنید"
            if point.SellID == user_id:
                bot.sendMessage(point.ChatIDBuyer, message)

                # admin report channel
                bot.sendMessage(ReportChannel, message)

            else:
                # admin report channel -> for buyer
                report_channel_message = f"امتیاز شماره " \
                                         f"{value}" \
                                         f" توسط خریدار تایید شد"
                bot.sendMessage(ReportChannel, report_channel_message)

            bot.sendMessage(chat_id, 'با موفقیت درخواست تایید ثبت شد')
        else:
            bot.sendMessage(chat_id, 'متاسفانه به نظر در درخواست تایید مشکلی وجود دارد.')
