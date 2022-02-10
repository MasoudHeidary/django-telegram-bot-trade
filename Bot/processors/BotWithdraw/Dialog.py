from Bot.bot import TelegramBot
from Bot.models import TelegramUser
from Profile.models import Profile

from ..BotComponent import ReplyKeyboardBackHome


def go_withdraw_home(chat_id, bot: TelegramBot):
    message = "💡 ثبت درخواست وجه همه روزه از ساعت 9الی 22 امکان پذیر می باشد.\n" \
              "💡 پرداختی ها به صورت پایا انجام می شود و همه روزه به درخواست ها رسیدگی خواهد شد.\n" \
              "💡 کارمزد انتقال وجه بین بانکی پایا هنگام واریز از مبلغ درخواستی کسر خواهد شد.\n" \
              "برای برداشت وجه، مبلغ خود را به تومان و با اعداد لاتین وارد نمایید."
    bot.sendMessage(chat_id, message, reply_markup=ReplyKeyboardBackHome)


def check_withdraw(user_id):
    profile: Profile = TelegramUser.objects.get(telegram_id=user_id).profile
    state = profile.BankName and \
            profile.BankAccount and \
            profile.Shaba

    return state
