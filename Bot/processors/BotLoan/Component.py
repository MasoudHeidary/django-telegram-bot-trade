from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup
from django_tgbot.types.keyboardbutton import KeyboardButton
from django_tgbot.types.inlinekeyboardmarkup import InlineKeyboardMarkup
from django_tgbot.types.inlinekeyboardbutton import InlineKeyboardButton

from Date.DateRequest import valid_days
from SiteSetting.SiteSettingRequest import loan_valid_day_long


# ------------------------------------------------------------------------------------

def grouper(iter, n):
    res = list()
    for i in range(len(iter)):
        q = list(iter[i * n:(i + 1) * n])
        if not q:
            return res
        res += [q]


# return valid days based on DB
def inline_keyboard_valid_days():
    days = loan_valid_day_long()
    if not days or days == 0:
        no_day = InlineKeyboardMarkup.a(
            inline_keyboard=[[InlineKeyboardButton.a('در حال حاضر امکان معامله وحود ندارد', callback_data='-')]])
        return no_day

    inline_days = []
    for i in grouper(valid_days(days), 3):
        temp = []
        for j in i:
            temp += [InlineKeyboardButton.a(j, callback_data=j)]
        inline_days += [temp]
    return InlineKeyboardMarkup.a(inline_keyboard=inline_days)


# ------------------------------------------------------------------------------------

ReplyKeyboardLoan = ReplyKeyboardMarkup.a(keyboard=[
    [KeyboardButton.a(text='درخواست فروش وام'), KeyboardButton.a(text='درخواست خرید وام')],
    [KeyboardButton.a(text='فروش وام به لیست'), KeyboardButton.a(text='خرید وام از لیست')],
    [KeyboardButton.a(text='لیست انتظار تایید'), KeyboardButton.a(text='درخواست های من')],
    [KeyboardButton.a(text='صفحه اول')],
], resize_keyboard=True, one_time_keyboard=True)

ReplyKeyboardLoanBuyFor = ReplyKeyboardMarkup.a(keyboard=[
    [KeyboardButton.a(text='شخصی دیگر'), KeyboardButton.a(text='خودم')],
    [KeyboardButton.a(text='بازگشت')],
], resize_keyboard=True, one_time_keyboard=True)

InlineKeyboardLoanDuration = InlineKeyboardMarkup.a(inline_keyboard=[
    [InlineKeyboardButton.a('3 ماهه', callback_data='3')],
    [InlineKeyboardButton.a('6 ماهه', callback_data='6')],
    [InlineKeyboardButton.a('یک ساله', callback_data='12')],
])

InlineKeyboardLoanValue = InlineKeyboardMarkup.a(inline_keyboard=[
    [InlineKeyboardButton.a('ده میلیون', callback_data='10'),
     InlineKeyboardButton.a('پنج میلیون', callback_data='5')],
    [InlineKeyboardButton.a('پنجاه میلیون', callback_data='50'),
     InlineKeyboardButton.a('بیست میلیون', callback_data='20')],
    [InlineKeyboardButton.a('صد میلیون', callback_data='100')],
])

# ------------------------------------------------------------------------------------
ReplyKeyboardBuyListMonth = ReplyKeyboardMarkup.a(keyboard=[
    [KeyboardButton.a(text='6 ماهه'), KeyboardButton.a(text='3 ماهه')],
    [KeyboardButton.a(text='یک ساله')],
    [KeyboardButton.a(text='صفحه اول')],
], resize_keyboard=True)

ReplyKeyboardBuyListValue = ReplyKeyboardMarkup.a(keyboard=[
    [KeyboardButton.a(text='ده میلیون'), KeyboardButton.a(text='پنج میلیون')],
    [KeyboardButton.a(text='پنجاه میلیون'), KeyboardButton.a(text='بیست میلیون')],
    [KeyboardButton.a(text='صد میلیون')],
    [KeyboardButton.a(text='صفحه اول')],
], resize_keyboard=True)

def inline_keyboard_buyer_list_detail(id, show, more):
    inline_keyboard = []
    if show:
        inline_keyboard = [[InlineKeyboardButton.a('فروش به خریدار', callback_data=f"{id}")]]
    if more:
        inline_keyboard += [[InlineKeyboardButton.a('بیشتر', callback_data=f"more-{more}")]]
    buyer_detail = InlineKeyboardMarkup.a(inline_keyboard=inline_keyboard)
    return buyer_detail


# -------------------------------------------------------------------------------------- sell list

def inline_keyboard_seller_list_detail(id, show, more):
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
