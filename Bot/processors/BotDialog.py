from Bot.models import TelegramUser
from Profile.models import Profile
from ..bot import TelegramBot
from .BotComponent import ReplyKeyboardHome

from Bot.BotSetting import ChannelName


# Home
def go_home(chat_id, bot: TelegramBot):
    message = "صفحه اول " \
              "🏠"
    bot.sendMessage(chat_id, message, reply_markup=ReplyKeyboardHome)


def fail_home(chat_id, bot: TelegramBot):
    message = "لطفا از دستورات زیر استفاده کنید." \
              "👇"
    bot.sendMessage(chat_id, message, reply_markup=ReplyKeyboardHome)


def join_channel(chat_id, user_id, bot: TelegramBot):
    user_status_in_channel = bot.getChatMember(chat_id=ChannelName, user_id=user_id)
    if user_status_in_channel.status == 'left':
        message = f"لطفا قبل از انجام ترکانش ها، در کانال زیر عضو شوید\n" \
                  f"{ChannelName}"
        bot.sendMessage(chat_id, message, reply_markup=ReplyKeyboardHome)
        return False
    return True


def check_profile(user: TelegramUser):
    try:
        profile: Profile = user.profile

        state = profile.Name and \
                profile.Family and \
                profile.ClubCode and \
                profile.PhoneNumber and \
                profile.UserConf
        return state
    except:
        return False


def go_wallet_charge(chat_id, bot: TelegramBot):
    message = "💵 برای شارژ کیف پول خود لطفا مبلغ مورد نظر را به شماره حساب زیر واریز نمایید.\n\n" \
              "🏦 بانک: آینده\n\n" \
              "👤 صاحب حساب مشترک: محمد امین احمدی و حسین لاوری منفرد\n\n" \
              "شماره کارت: \n" \
              "6362141121991930\n\n" \
              "کد شبا: \n" \
              "IR970620000000302950973001\n\n" \
              "شماره حساب:\n" \
              "0302950973001\n\n" \
              "سپس در همین قسمت عکس مربوط به تراکنش را ارسال نمایید، تا به صورت اتومات برای ادمین ارسال شود و کیف پول شما نیز شارژ شود .\n" \
              "با تشکر 🌹"
    bot.sendMessage(chat_id, message, parse_mode="HTML")
