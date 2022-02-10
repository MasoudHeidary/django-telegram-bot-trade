from Bot.bot import state_manager, TelegramBot
from Profile.ProfileRequest import check_user
from .Component import InlineKeyboardEditProfile, InlineKeyboardRule


# Profile

# return true(if user have profile) otherwise return false
def go_profile(chat_id, user_id, bot: TelegramBot):
    user = check_user(user_id)
    if not user:
        message = "ابتدا باید یک پروفایل بسازیم"
        bot.sendMessage(chat_id, message)
        return False
    else:
        message = f"اطلاعات شما به شرح زیر است." \
                  f"\n" \
                  f"{user.Name} - {user.Family} - {user.ClubCode}" \
                  f"\n" \
                  f"شماره موبایل: " \
                  f"{user.PhoneNumber}\n" \
                  f" اطلاعات بانکی:\n" \
                  f"{user.BankName}: {user.BankAccount}\n" \
                  f"شبا: " \
                  f"{user.Shaba}\n" \
                  f"برای تغییر هر کدام روی گزینه مربوطه کلیک کنید" \
                  f"\n" \
                  f"*برای برگشت به صفحه قبلی میتوانید یک کلمه تایپ کنید*"
        bot.sendMessage(chat_id, message, reply_markup=InlineKeyboardEditProfile)
        return True


# ---------------------------------------------------------------------- create profile
def go_create_profile_name(chat_id, bot: TelegramBot):
    message = "لطفا نام خود در باشگاه آگاه را وارد نمایید."
    bot.sendMessage(chat_id, message)


def go_create_profile_family(chat_id, bot: TelegramBot):
    message = "لطفا فامیلی خود در باشگاه آکاه را وارد نمایید."
    bot.sendMessage(chat_id, message)


def go_create_profile_club_code(chat_id, bot: TelegramBot):
    message = "لطفا کد باشگاه آگاه خود را وارد نمایید"
    bot.sendMessage(chat_id, message)


def go_create_profile_phone_number(chat_id, bot: TelegramBot):
    message = "لطفا شماره موبایل خود را وارد نمایید."
    bot.sendMessage(chat_id, message)


def go_create_profile_rule_1(chat_id, bot: TelegramBot):
    message = "📌 قابل توجه #خریداران بسته های اعتباری\n" \
              "بمنظور کمتر شدن مشکلات رد شدن بسته های اعتباری و پیگیری بسته ها و انتقال مجدد آن\n" \
              "⚡️خریداران قبل از خرید بسته اعتباری باید از سقف قرارداد امضا شده در کارگزاری اطلاع داشته و از میزان ارزش تضمین خود آگاهی کامل داشته باشند.\n" \
              "⚡️بعد از انتقال بسته توسط فروشنده تا زمانی که کارگزاری بسته اعتباری را داخل باشگاه تایید نکرده مجاز به تایید بسته داخل ربات نیستید. \n" \
              "⚠ ️در صورت رعایت نکردن این موارد عواقب بعدی به عهده خریدار می باشد.\n"
    bot.sendMessage(chat_id, message, reply_markup=InlineKeyboardRule)


def go_create_profile_rule_2(chat_id, bot: TelegramBot):
    message = " شباهت ها و تفاوت های #وام و #بسته_اعتباری\n" \
              "برای دریافت وام یا بسته باید قرارداد مربوطه را به صورت حضوری امضا کرده باشید.\n" \
              "سقف قرارداد و ارزش تضمین هم باید رعایت کنید که در غیر اینصورت بسته توسط کارگزاری رد خواهد شد.\n" \
              "نحوه تسویه وام یا بسته تفاوتی باهم ندارد.\n" \
              "برای دریافت وام باید حداقل سطح ۵ باشگاه باشید اما برای بسته سطح باشگاه ملاک نیست.\n" \
              "تعیین «بازگشت اعتبار استفاده نشده» برای بسته وجود دارد اما برای وام این مورد وجود ندارد.\n" \
              "بسته را میشود به صورت ۱ ماهه گرفت (جمعا ۲۰ میلیون) اما وام کمتر از ۳ ماهه نمیشود درخواست کرد.\n" \
              "وام را میشود ۱۰۰ میلیون به صورت یکجا گرفت اما بسته بیشتر از ۵۰ میلیون یکجا نمیشود گرفت.\n"
    bot.sendMessage(chat_id, message, reply_markup=InlineKeyboardRule)


def go_create_profile_rule_3(chat_id, bot: TelegramBot):
    message = "💡 قابل توجه #خریداران #بسته_اعتباری\n" \
              "📌قبل از خرید بسته به موارد زیر توجه داشته باشید\n" \
              "۱- حتما در کارگزاری قرارداد مربوط به دریافت اعتبار رو امضا کرده باشید.\n" \
              "۲- سقف تعهد و ارزش تضامین پرتفو را در نظر گرفته  تا بعد از دریافت اعتبار توسط کارگزاری رد نشود.\n" \
              "✅ اگر شرایط بالا رعایت شده بود میتوانید داخل ربات بسته مورد نظر را خریداری کرده و پس از اینکه فروشنده بسته را برای شما منتقل کرد\n" \
              "👈 اول باید پنل باشگاه را چک کرده و از منو گزارش گزینه اعتبارات، بسته انتقالی مورد نظر را تایید نمایید و سپس داخل ربات آن بسته را تایید کنید.\n" \
              "⚠️ به هیچ عنوان قبل از تایید بسته داخل پنل باشگاه داخل ربات بسته را تایید نکنید.\n"
    bot.sendMessage(chat_id, message, reply_markup=InlineKeyboardRule)


def go_create_profile_rule_4(chat_id, bot: TelegramBot):
    message = "👈 #توجه\n" \
              "▫️لطفا فقط در مواقع ضروری با پشتیبانی ربات در تماس باشید و اصلا لازم نیست وقتی بسته یا امتیازی را انتقال دادید به پشتیبانی پیام بدهید یا وقتی درخواست وجه زدید به پشتیبانی پیام دهید.\n" \
              "▫️توجه داشته باشید اگر بسته یا امتیازی را ثبت کردید برای فروش درصورتی که خریدار برای آن پیدا شد دیگه قادر به حذف آن نیستید و قبل از اینکه خریدار پیدا بشه قادر به حذف خواهید بود.\n" \
              "▫️درصورتی که با ربات معاملات آشنا نیستید حتما  کلیپ آموزش  معامله کردن در ربات را  که در داخل کانال معاملات مشتریان باشگاه آگاه قرا داده شده  تماشا کنید . \n" \
              " ⚠️ تذکر جدی : فروشندگانی که بسته یا امتیازی را برای خریدار منتقل نمی کنند و یا منتقل کرده و سپس داخل باشگاه حذف میکنن متخلف تلقی شده و اکانت ربات آنها بلاک و قادر به معامله نخواهند بود.\n"
    bot.sendMessage(chat_id, message,  reply_markup=InlineKeyboardRule)
# ---------------------------------------------------------------------- done create profile
