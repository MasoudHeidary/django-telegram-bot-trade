from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types
from django_tgbot.types.update import Update
from django_tgbot.exceptions import ProcessFailure
from Bot.bot import state_manager, TelegramBot
from Bot.models import TelegramState
from Date.DateRequest import valid_days
from SiteSetting.SiteSettingRequest import credit_valid_day_long

from ..BotProfile.CreateProfile import check_club_code

from .Dialog import seller_list_pager, go_sell_list_for, send_message_to_seller_for_me, \
    seller_detail, go_buy_credit_for_other_name, go_buy_credit_for_other_club_code, \
    send_message_to_seller_for_other, go_sell_credit_time, go_credit, go_seller_list_value

from CreditPack.CreditPackRequest import seller_by_month_value, get_credit, buy_credit_from_seller


@processor(
    state_manager,
    from_states='/Credit/SellerList',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def credit_seller_list(bot: TelegramBot, update: Update, state: TelegramState):
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
        go_credit(chat_id, bot)
        state.set_name('/Credit')
        return

    go_seller_list_value(chat_id, bot)
    state.set_name('/Credit/SellerList/Value')


@processor(
    state_manager,
    from_states='/Credit/SellerList/Value',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def credit_seller_list_value(bot: TelegramBot, update: Update, state: TelegramState):
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
    qu = seller_by_month_value(month, credit_value)
    if not qu:
        bot.sendMessage(chat_id, 'در حال حاضر بسته اعتباری با این مشخصات وجود ندارد')
    else:
        seller_list_pager(chat_id, qu, 0, show_len, bot)


@processor(
    state_manager,
    from_states='/Credit/SellerList/Value',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def credit_seller_list(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    value = update.get_callback_query().get_data()
    show_len = 3

    if 'more' in value:
        month = state.get_memory().get('month')
        credit_value = state.get_memory().get('value')
        qu = seller_by_month_value(month, credit_value)

        index = int(value.split('-')[1])
        seller_list_pager(chat_id, qu, index, show_len, bot)
    else:
        state.update_memory({'credit_id': value})
        # go_sell_list_for(chat_id, bot)
        # state.set_name('/Credit/SellerList/For')
        go_sell_credit_time(chat_id, bot)
        state.set_name('/Credit/SellerList/Time')


@processor(
    state_manager,
    from_states='/Credit/SellerList/Time',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def credit_sell_time(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    value = update.get_callback_query().get_data()

    valid = valid_days(credit_valid_day_long())
    if value not in valid:
        bot.sendMessage(chat_id, '📌 لطفا یکی از گزینه های بالا را انتخاب نمایید.👆')
    else:
        state.update_memory({'credit_time': value})

        go_sell_list_for(chat_id, bot)
        state.set_name('/Credit/SellerList/For')


@processor(
    state_manager,
    from_states='/Credit/SellerList/For',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def credit_seller_list_for(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()
    user_id = update.get_user().get_id()

    credit_id = state.get_memory().get('credit_id')
    time = state.get_memory().get('credit_time')

    if message_text == 'خودم':
        x = buy_credit_from_seller(credit_id=credit_id, time=time, buyer_id=user_id, chat_id=chat_id)
        if not x:
            message = "به نظر در خرید بسته اعتباری مشکلی وجود دارد:\n" \
                      "1) نسبت به شارژ کیف پول خود اقدام نمیایید\n" \
                      "2) بسته اعتباری جهت فروش حذف شده یا فروش رفته است\n" \
                      "با تشکر"
            bot.sendMessage(chat_id, message)
        else:
            credit = get_credit(credit_id)
            send_message_to_seller_for_me(user_id=user_id, credit=credit, bot=bot)
            seller_detail(chat_id, credit, bot)

        go_credit(chat_id, bot)
        state.set_name('/Credit')

    elif message_text == 'شخصی دیگر':
        go_buy_credit_for_other_name(chat_id, bot)
        state.set_name('/Credit/SellerList/For/Other/Name')
    else:
        go_credit(chat_id, bot)
        state.set_name('/Credit')


@processor(
    state_manager,
    from_states='/Credit/SellerList/For/Other/Name',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def credit_seller_list_for_other_name(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()

    try:
        name, family = message_text.split('-')
        state.update_memory({'name': name, 'family': family})
    except:
        go_buy_credit_for_other_name(chat_id, bot)
        raise ProcessFailure

    go_buy_credit_for_other_club_code(chat_id, bot)
    state.set_name('/Credit/SellerList/For/Other/ClubCode')


@processor(
    state_manager,
    from_states='/Credit/SellerList/For/Other/ClubCode',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def credit_seller_list_for_other_club_code(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    user_id = update.get_user().get_id()
    club_code = update.get_message().get_text()

    if not check_club_code(club_code):
        go_buy_credit_for_other_club_code(chat_id, bot)
    else:
        credit_id = state.get_memory().get('credit_id')
        time = state.get_memory().get('credit_time')

        x = buy_credit_from_seller(credit_id=credit_id, time=time, buyer_id=user_id, chat_id=chat_id)
        if not x:
            message = "به نظر در خرید بسته اعتباری مشکلی وجود دارد:\n" \
                      "1) نسبت به شارژ کیف پول خود اقدام نمیایید\n" \
                      "2) بسته اعتباری جهت فروش حذف شده یا فروش رفته است\n" \
                      "با تشکر"
            bot.sendMessage(chat_id, message)
        else:
            credit = get_credit(credit_id)
            data = state.get_memory()
            send_message_to_seller_for_other(
                name=data.get('name'),
                family=data.get('family'),
                club_code=club_code,
                credit=credit,
                bot=bot,
            )
            seller_detail(chat_id, credit=credit, bot=bot)
        go_credit(chat_id, bot)
        state.set_name('/Credit')
