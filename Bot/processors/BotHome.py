from json import dumps

from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from django_tgbot.exceptions import ProcessFailure
from ..bot import state_manager, TelegramBot
from ..models import TelegramState, TelegramUser
from ..BotSetting import AdminChannel

from .BotDialog import fail_home, go_wallet_charge, join_channel, check_profile
from .BotProfile.Dialog import go_profile, go_create_profile_name
from .BotLoan.Dialog import go_loan
from .BotWallet.Dialog import go_transition_list_pager, transition_list_pager
from .BotCreditPack.Dialog import go_credit
from .BotPoint.Dialog import go_point
from .BotLuck.Dialog import go_luck
from .BotWithdraw.Dialog import go_withdraw_home, check_withdraw

from .BotComponent import ReplyKeyboardHome

from WalletTransition.WalletRequest import check_have_wallet


@processor(
    state_manager,
    from_states='/Home',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def home(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()

    user_id = update.get_user().get_id()
    user = TelegramUser.objects.get(telegram_id=user_id)

    # check join channel
    # if not join_channel(chat_id, user_id, bot):
    #     raise ProcessFailure

    # check wallet
    check_have_wallet(user_id)

    if message_text == 'پروفایل 🎫':
        # check make profile or edit it
        pr = go_profile(chat_id, user_id, bot)

        if pr:
            # edit
            state.set_name('/EditProfile')
        else:
            # create
            state.set_name('/Profile/Name')
            go_create_profile_name(chat_id, bot)

        return

        # check profile
    if not check_profile(user):
        bot.sendMessage(chat_id, "لطفا ابتدا پروفایل خود را تکمیل نمایید.", reply_markup=ReplyKeyboardHome)
        raise ProcessFailure

    if message_text == 'وام 🏦':
        go_loan(chat_id, bot)
        state.set_name('/Loan')

    elif message_text == 'بسته اعتباری 💰':
        go_credit(chat_id, bot)
        state.set_name('/Credit')

    elif message_text == 'کیف پول و تراکنش ها 🗃':
        go_transition_list_pager(chat_id, user, bot)

    elif message_text == 'شارژ کیف پول 💵':
        go_wallet_charge(chat_id, bot)

    elif message_text == 'امتیاز 🧩':
        go_point(chat_id, bot)
        state.set_name('/Point')

    elif message_text == 'گردونه شگفت انگیز 🏵':
        go_luck(chat_id, user_id, bot)

    elif message_text == 'درخواست وجه 💸':
        if not check_withdraw(user_id):
            bot.sendMessage(chat_id, 'لطفا نسبت به تکمیل اطلاعات بانکی خود در قسمت پروفایل اقدام نمایید')
            raise ProcessFailure
        go_withdraw_home(chat_id, bot)
        state.set_name('/Withdraw')

    else:
        fail_home(chat_id, bot)


# wallet and transitions
@processor(
    state_manager,
    from_states='/Home',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def wallet_and_transitions(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    value = update.get_callback_query().get_data()

    if value == 'conf-rule':
        return

    user_id = update.get_user().get_id()
    user = TelegramUser.objects.get(telegram_id=user_id)
    tran = user.wallet.transition_set.all()

    index = int(value.split('-')[1])
    index_len = 5
    transition_list_pager(chat_id, tran, index, index_len, bot)


# send photo to admin channel
@processor(
    state_manager,
    from_states='/Home',
    update_types=update_types.Message,
    message_types=message_types.Photo,
)
def wallet_and_transitions(bot: TelegramBot, update: Update, state: TelegramState):
    message_id = update.get_message().get_message_id()
    chat_id = update.get_chat().get_id()
    user_id = update.get_user().get_id()
    # user = TelegramUser.objects.get(telegram_id=user_id)

    # message_to_admin = f"wallet_id= {user.wallet.id}\n" \
    #                    f"profile_name= {user.profile.Name}\n" \
    #                    f"profile_family= {user.profile.Family}\n" \
    #                    f"profile_clubcode= {user.profile.ClubCode}"

    user_detail = {
        'user_id': user_id,
        'chat_id': chat_id,
        'cause': 'charge',
    }
    message_to_admin = dumps(user_detail)

    bot.forwardMessage(from_chat_id=chat_id, chat_id=AdminChannel, message_id=message_id)
    bot.sendMessage(AdminChannel, message_to_admin)

    message_to_user = "عکس تراکنش شما برای تایید با موفقیت به ادمین فرستاده شد."
    bot.sendMessage(chat_id, message_to_user)
