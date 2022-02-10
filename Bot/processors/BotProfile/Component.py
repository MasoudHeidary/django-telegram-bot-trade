from django_tgbot.types.inlinekeyboardmarkup import InlineKeyboardMarkup
from django_tgbot.types.inlinekeyboardbutton import InlineKeyboardButton


InlineKeyboardEditProfile = InlineKeyboardMarkup.a(inline_keyboard=[
    [InlineKeyboardButton.a('نام', callback_data='edit-name')],
    [InlineKeyboardButton.a('نام خانوادگی', callback_data='edit-family')],
    [InlineKeyboardButton.a('کد باشگاه', callback_data='edit-club-code')],
    [InlineKeyboardButton.a('شماره موبایل', callback_data='edit-phone-number')],
    [InlineKeyboardButton.a('نام بانک', callback_data='edit-bank-name')],
    [InlineKeyboardButton.a('شماره حساب', callback_data='edit-bank-number')],
    [InlineKeyboardButton.a('شماره شبا', callback_data='edit-bank-shaba')],
])


InlineKeyboardRule = InlineKeyboardMarkup.a(inline_keyboard=[
    [InlineKeyboardButton.a('تایید قوانین', callback_data='conf-rule')],
])