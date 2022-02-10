from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup
from django_tgbot.types.keyboardbutton import KeyboardButton
from django_tgbot.types.inlinekeyboardmarkup import InlineKeyboardMarkup
from django_tgbot.types.inlinekeyboardbutton import InlineKeyboardButton

from SiteSetting.SiteSettingRequest import credit_valid_day_long
from Date.DateRequest import valid_days

# --------------------------------------------------------------------------------- general

# def grouper(iter, n):
#     res = list()
#     for i in range(len(iter)):
#         q = list(iter[i * n:(i + 1) * n])
#         if not q:
#             return res
#         res += [q]
#
#
# # return valid days based on DB
# def inline_keyboard_valid_days():
#     days = credit_valid_day_long()
#
#     inline_days = []
#     for i in grouper(valid_days(days), 3):
#         temp = []
#         for j in i:
#             temp += [InlineKeyboardButton.a(j, callback_data=j)]
#         inline_days += [temp]
#     return InlineKeyboardMarkup.a(inline_keyboard=inline_days)


# --------------------------------------------------------------------------------------- home

ReplyKeyboardPoint = ReplyKeyboardMarkup.a(keyboard=[
    [KeyboardButton.a(text='درخواست فروش امتیاز'), KeyboardButton.a(text='درخواست خرید امتیاز')],
    [KeyboardButton.a(text='فروش امتیاز به لیست'), KeyboardButton.a(text='خرید امتیاز از لیست')],
    [KeyboardButton.a(text='لیست انتظار تایید'), KeyboardButton.a(text='درخواست های من')],
    [KeyboardButton.a(text='صفحه اول')],
], resize_keyboard=True, one_time_keyboard=True)

# --------------------------------------------------------------------------------------- buy
ReplyKeyboardPointBuyFor = ReplyKeyboardMarkup.a(keyboard=[
    [KeyboardButton.a(text='شخصی دیگر'), KeyboardButton.a(text='خودم')],
    [KeyboardButton.a(text='بازگشت')],
], resize_keyboard=True, one_time_keyboard=True)


# -------------------------------------------------------------------------------------- buy list

def inline_keyboard_buyer_list_detail(id,show, more):
    inline_keyboard = []
    if show:
        inline_keyboard = [[InlineKeyboardButton.a('فروش به خریدار', callback_data=f"{id}")]]
    if more:
        inline_keyboard += [[InlineKeyboardButton.a('بیشتر', callback_data=f"more-{more}")]]
    buyer_detail = InlineKeyboardMarkup.a(inline_keyboard=inline_keyboard)
    return buyer_detail


# -------------------------------------------------------------------------------------- sell list

def inline_keyboard_seller_list_detail(id,show, more):
    inline_keyboard = []
    if show:
        inline_keyboard = [[InlineKeyboardButton.a('خرید از فروشنده', callback_data=f"{id}")]]
    if more:
        inline_keyboard += [[InlineKeyboardButton.a('بیشتر', callback_data=f"more-{more}")]]
    seller_detail = InlineKeyboardMarkup.a(inline_keyboard=inline_keyboard)
    return seller_detail


# -------------------------------------------------------------------------------------- Cancel

def inline_keyboard_cancel(id):
    inline_keyboard = [[InlineKeyboardButton.a('لغو درخواست', callback_data=f"cancel-{id}")]]
    cancel = InlineKeyboardMarkup.a(inline_keyboard=inline_keyboard)
    return cancel

# -------------------------------------------------------------------------------------- Conf

def inline_keyboard_conf(id):
    inline_keyboard = [[InlineKeyboardButton.a('تایید', callback_data=f"{id}")]]
    buyer_detail = InlineKeyboardMarkup.a(inline_keyboard=inline_keyboard)
    return buyer_detail
