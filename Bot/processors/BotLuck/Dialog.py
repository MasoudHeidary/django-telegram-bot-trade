from Bot.bot import TelegramBot
from django_tgbot.types.inlinekeyboardmarkup import InlineKeyboardMarkup
from django_tgbot.types.inlinekeyboardbutton import InlineKeyboardButton

from Luck.LuckRequest import check_luck
from Luck.models import Luck
from Bot.BotSetting import DomainName


def go_luck(chat_id, user_id, bot: TelegramBot):
    all_my_luck = Luck.objects.filter(UserID=user_id)
    if not all_my_luck:
        bot.sendMessage(chat_id, "تا به حال در گردونه شانس شرکت نکرده اید.")
    else:
        message = "🎁 جوایزی که تا الان برنده شده اید\n"
        for i in all_my_luck:
            message += f"💯 {i.Name}\n"
        message += "برای دریافت جایز های خود با ادمین در ارتباط باشید.\n" \
                   "admin: @BOTAGAHSERVICES"
        bot.sendMessage(chat_id, message)

    luck = check_luck(user_id)
    if not luck:
        message = "🏆 مشتری گرامی در صورتی که  معاملات شما در ربات به مبلغ 5 میلیون" \
                  " تومان برسد گردونه شگفت انگیز برای شما فعال خواهد شد  در ضمن " \
                  "به ازای هر 5 میلیون تومان معامله  یکبار گردونه برای شما فعال " \
                  "خواهد شد و شانس دریافت  جوایز نفیس را خواهید داشت ."
        bot.sendMessage(chat_id, message)
    else:
        message = "با زدن روی دکمه زیر گردونه شگفت انگیز برای شما باز میشود." \
                  "\n" \
                  "گردونه قابل زوم کردن است.\n" \
                  "توجه: اگر صفحه گردونه را باز کنید و اقدام به چرخاندن گردونه نکنید" \
                  "سیستم به صورت اتومات برای شما گردونه را خواهد چرخاند."
        url = f"{DomainName}/luck/?user_id={user_id}"
        inline_keyboard = InlineKeyboardMarkup.a(inline_keyboard=[
            [InlineKeyboardButton.a('باز کردن گردونه شگفت انگیز', url=url)],
        ])
        bot.sendMessage(chat_id, message, reply_markup=inline_keyboard)
