from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from Bot.bot import state_manager, TelegramBot, TelegramUser
from Bot.models import TelegramState

from .CreateProfile import check_club_code, check_phone_number
from ..BotDialog import go_home
from ..BotComponent import ReplyKeyboardBackHome


# check shaba number and
def check_shaba(shaba: str):
    shaba = shaba.upper()
    if not shaba[0:2] == 'IR':
        return False
    if not shaba[2:].isdigit():
        return False
    if not len(shaba) == 26:
        return False
    shaba = shaba.replace("I", "18")
    shaba = shaba.replace("R", "27")
    if not (int(shaba[6:] + shaba[0:6]) % 97 == 1):
        return False
    return True


@processor(
    state_manager,
    from_states='/EditProfile',
    update_types=update_types.CallbackQuery,
    message_types=message_types.Text,
)
def edit_profile(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    value = update.get_callback_query().get_data()

    if value == 'edit-name':
        bot.sendMessage(chat_id, 'اسم جدید را وارد نمایید:', reply_markup=ReplyKeyboardBackHome)
        state.set_name('/EditProfile/Name')

    elif value == 'edit-family':
        bot.sendMessage(chat_id, 'فامیلی جدید را وارد نمایید:', reply_markup=ReplyKeyboardBackHome)
        state.set_name('/EditProfile/Family')

    elif value == 'edit-club-code':
        state.set_name('/EditProfile/ClubCode')
        bot.sendMessage(chat_id, 'کد باشگاه جدید را وارد نمایید:', reply_markup=ReplyKeyboardBackHome)

    elif value == 'edit-phone-number':
        bot.sendMessage(chat_id, 'شماره موبایل جدید را وارد نمایید', reply_markup=ReplyKeyboardBackHome)
        state.set_name('/EditProfile/PhoneNumber')

    elif value == 'edit-bank-name':
        bot.sendMessage(chat_id, 'نام بانک را وارد نمایید', reply_markup=ReplyKeyboardBackHome)
        state.set_name('/EditProfile/BankName')

    elif value == 'edit-bank-number':
        bot.sendMessage(chat_id, 'شماره حساب را وارد نمایید', reply_markup=ReplyKeyboardBackHome)
        state.set_name('/EditProfile/BankNumber')

    elif value == 'edit-bank-shaba':
        bot.sendMessage(chat_id, 'شماره شبا را وارد نمایید', reply_markup=ReplyKeyboardBackHome)
        state.set_name('/EditProfile/BankShaba')


@processor(
    state_manager,
    from_states='/EditProfile',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def edit_profile_fail(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    go_home(chat_id, bot)
    state.set_name('/Home')


@processor(
    state_manager,
    from_states='/EditProfile/Name',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def edit_profile_name(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()
    user_id = update.get_user().get_id()
    user = TelegramUser.objects.get(telegram_id=user_id).profile

    if message_text == 'صفحه اول':
        state.set_name('/Home')
        go_home(chat_id, bot)
    elif len(message_text) >= 100:
        bot.sendMessage(chat_id, 'فکر کنم اشتباه وارد کردی، اسم نباید اینقدر طولانی باشه')
    else:
        user.Name = message_text
        user.save()
        bot.sendMessage(chat_id, 'اسم با موفقیت ثبت شد')
        state.set_name('/Home')
        go_home(chat_id, bot)


@processor(
    state_manager,
    from_states='/EditProfile/Family',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def edit_profile_family(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()
    user_id = update.get_user().get_id()
    user = TelegramUser.objects.get(telegram_id=user_id).profile

    if message_text == 'صفحه اول':
        state.set_name('/Home')
        go_home(chat_id, bot)
    elif len(message_text) >= 100:
        bot.sendMessage(chat_id, 'فکر کنم اشتباه وارد کردی، فامیلی نباید اینقدر طولانی باشه')
    else:
        user.Family = message_text
        user.save()
        bot.sendMessage(chat_id, 'فامیلی با موفقیت ثبت شد')
        state.set_name('/Home')
        go_home(chat_id, bot)


@processor(
    state_manager,
    from_states='/EditProfile/ClubCode',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def edit_profile_club_code(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()
    user_id = update.get_user().get_id()
    user = TelegramUser.objects.get(telegram_id=user_id).profile

    if message_text == 'صفحه اول':
        state.set_name('/Home')
        go_home(chat_id, bot)
    elif not check_club_code(message_text):
        bot.sendMessage(chat_id, 'فرمت کد باشگاهت به نظر درست نمیرسه، میتونی از توی سایت باشگاه آگاه برش داری')
    else:
        user.ClubCode = message_text
        user.save()
        bot.sendMessage(chat_id, 'کد باشگاه با موفقیت ثبت شد')
        state.set_name('/Home')
        go_home(chat_id, bot)


@processor(
    state_manager,
    from_states='/EditProfile/PhoneNumber',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def edit_profile_phone_number(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()
    user_id = update.get_user().get_id()
    user = TelegramUser.objects.get(telegram_id=user_id).profile

    if message_text == 'صفحه اول':
        state.set_name('/Home')
        go_home(chat_id, bot)
    elif not check_phone_number(message_text):
        bot.sendMessage(chat_id, 'لطفا شماره موبایل را به صورت صحیح وارد نمایید.')
    else:
        user.PhoneNumber = message_text
        user.save()
        bot.sendMessage(chat_id, 'شماره موبایل با موفقیت ثبت شد')
        state.set_name('/Home')
        go_home(chat_id, bot)


@processor(
    state_manager,
    from_states='/EditProfile/BankName',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def edit_profile_bank_name(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()
    user_id = update.get_user().get_id()
    user = TelegramUser.objects.get(telegram_id=user_id).profile

    if message_text == 'صفحه اول':
        state.set_name('/Home')
        go_home(chat_id, bot)
    else:
        user.BankName = message_text
        user.save()
        bot.sendMessage(chat_id, 'نام بانک با موفقیت ثبت شد')
        state.set_name('/Home')
        go_home(chat_id, bot)


@processor(
    state_manager,
    from_states='/EditProfile/BankNumber',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def edit_profile_bank_number(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()
    user_id = update.get_user().get_id()
    user = TelegramUser.objects.get(telegram_id=user_id).profile

    if message_text == 'صفحه اول':
        state.set_name('/Home')
        go_home(chat_id, bot)
    elif not message_text.isdigit():
        bot.sendMessage(chat_id, 'لطفا شماره حساب را به صورت صحیح وارد نمایید.')
    else:
        user.BankAccount = message_text
        user.save()
        bot.sendMessage(chat_id, 'شماره حساب با موفقیت ثبت شد')
        state.set_name('/Home')
        go_home(chat_id, bot)


@processor(
    state_manager,
    from_states='/EditProfile/BankShaba',
    update_types=update_types.Message,
    message_types=message_types.Text,
)
def edit_profile_bank_shaba(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    message_text = update.get_message().get_text()
    user_id = update.get_user().get_id()
    user = TelegramUser.objects.get(telegram_id=user_id).profile

    if message_text == 'صفحه اول':
        state.set_name('/Home')
        go_home(chat_id, bot)
    elif not check_shaba(message_text):
        bot.sendMessage(chat_id, 'لطفا شماره شبا را به صورت صحیح همراه با IR وارد نمایید.')
    else:
        user.Shaba = message_text
        user.save()
        bot.sendMessage(chat_id, 'شماره شبا با موفقیت ثبت شد')
        state.set_name('/Home')
        go_home(chat_id, bot)
