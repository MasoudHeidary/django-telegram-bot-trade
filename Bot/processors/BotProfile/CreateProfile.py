from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from Bot.bot import state_manager, TelegramBot, TelegramUser
from Bot.models import TelegramState

from Profile.models import Profile

from ..BotDialog import go_home

from .Dialog import go_create_profile_family, go_create_profile_club_code, go_create_profile_phone_number, \
    go_create_profile_rule_1, go_create_profile_rule_2, go_create_profile_rule_3, go_create_profile_rule_4


# club-code is like AB1234
def check_club_code(code: str):
    if not len(code) == 6:
        return False
    if not code[0:2].isalpha():
        return False
    if not code[2:].isdigit():
        return False
    return True


# phone number should all be digits and 11digi
def check_phone_number(phone: str):
    if not phone.isdigit():
        return False
    if not len(phone) == 11:
        return False
    return True


@processor(
    state_manager,
    from_states='/Profile/Name',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def create_profile_name(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()

    if len(message_text) >= 100:
        bot.sendMessage(chat_id, 'نام کاربر نمیتواند اینقدر طولانی باشد.')
    else:
        state.reset_memory()
        state.update_memory({'name': message_text})
        go_create_profile_family(chat_id, bot)
        state.set_name('/Profile/Family')


@processor(
    state_manager,
    from_states='/Profile/Family',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def create_profile_family(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()

    if len(message_text) >= 100:
        bot.sendMessage(chat_id, 'فامیلی کاربر نمیتواند اینقدر طولانی باشد.')
    else:
        state.update_memory({'family': message_text})
        go_create_profile_club_code(chat_id, bot)
        state.set_name('/Profile/ClubCode')


@processor(
    state_manager,
    from_states='/Profile/ClubCode',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def create_profile_club_code(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()

    if not check_club_code(message_text):
        bot.sendMessage(chat_id, 'لطفا کد باشگاه خود را به صورت صحیح وارد نمایید.')
    else:
        state.update_memory({'club_code': message_text})
        go_create_profile_phone_number(chat_id, bot)
        state.set_name('/Profile/PhoneNumber')


@processor(
    state_manager,
    from_states='/Profile/PhoneNumber',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def create_profile_phone_number(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()

    user_id = update.get_user().get_id()
    user = TelegramUser.objects.get(telegram_id=user_id)

    if not check_phone_number(message_text):
        bot.sendMessage(chat_id, 'لطفا شماره موبایل را با فرمت صحیح وارد نمایید.')
    else:
        state.update_memory({'phone_number': message_text})

        # # create profile of user
        # data = state.get_memory()
        # Profile.objects.create(
        #     Name=data.get('name'),
        #     Family=data.get('family'),
        #     ClubCode=data.get('club_code'),
        #     PhoneNumber=data.get('phone_number'),
        #     ToTelegramUser=user,
        # )
        # bot.sendMessage(chat_id, 'پروفایل شما با موفقیت ساخته شد، از معامله لذت ببرید.')

        # go_home(chat_id, bot)
        # state.set_name('/Home')
        go_create_profile_rule_1(chat_id, bot)
        state.set_name('/Profile/Rule1')


@processor(
    state_manager,
    from_states='/Profile/Rule1',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def create_profile_rule_1(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    value = update.get_callback_query().get_data()

    if value == 'conf-rule':
        go_create_profile_rule_2(chat_id, bot)
        state.set_name('/Profile/Rule2')


@processor(
    state_manager,
    from_states='/Profile/Rule2',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def create_profile_rule_2(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    value = update.get_callback_query().get_data()

    if value == 'conf-rule':
        go_create_profile_rule_3(chat_id, bot)
        state.set_name('/Profile/Rule3')


@processor(
    state_manager,
    from_states='/Profile/Rule3',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def create_profile_rule_3(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    value = update.get_callback_query().get_data()

    if value == 'conf-rule':
        go_create_profile_rule_4(chat_id, bot)
        state.set_name('/Profile/Rule4')


@processor(
    state_manager,
    from_states='/Profile/Rule4',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def create_profile_rule_4(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    user_id = update.get_user().get_id()
    user = TelegramUser.objects.get(telegram_id=user_id)
    value = update.get_callback_query().get_data()

    if value == 'conf-rule':
        # create profile of user
        data = state.get_memory()
        Profile.objects.create(
            Name=data.get('name'),
            Family=data.get('family'),
            ClubCode=data.get('club_code'),
            PhoneNumber=data.get('phone_number'),
            ToTelegramUser=user,
            UserConf=True
        )

        bot.sendMessage(chat_id, "پروفایل شما با موفقیت ساخته شد")
        go_home(chat_id, bot)
        state.set_name('/Home')
