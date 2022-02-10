from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup
from django_tgbot.types.keyboardbutton import KeyboardButton

# Home
ReplyKeyboardHome = ReplyKeyboardMarkup.a(keyboard=[
    [KeyboardButton.a(text='بسته اعتباری 💰'), KeyboardButton.a(text='وام 🏦')],
    [KeyboardButton.a(text='شارژ کیف پول 💵'), KeyboardButton.a(text='امتیاز 🧩')],
    [KeyboardButton.a(text='درخواست وجه 💸'), KeyboardButton.a(text='کیف پول و تراکنش ها 🗃')],
    [KeyboardButton.a(text='پروفایل 🎫'), KeyboardButton.a(text='گردونه شگفت انگیز 🏵')],
], resize_keyboard=True, one_time_keyboard=True)

ReplyKeyboardBackHome = ReplyKeyboardMarkup.a(keyboard=[
    [KeyboardButton.a(text='صفحه اول')],
], resize_keyboard=True, one_time_keyboard=True)

ReplyKeyboardBack = ReplyKeyboardMarkup.a(keyboard=[
    [KeyboardButton.a(text='بازگشت')]
], resize_keyboard=True)