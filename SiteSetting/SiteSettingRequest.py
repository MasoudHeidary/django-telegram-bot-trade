from .models import SiteSetting


# ------------------------------------------------------ loan
# def loan_fee():
#     fee = SiteSetting.objects.filter(Name='LoanFee')
#     if not fee:
#         return 1.5
#     return fee.first().Value


def loan_min_max():
    min = SiteSetting.objects.filter(Name='LoanMin')
    if not min:
        min = 0
    min = min.first().Value
    max = SiteSetting.objects.filter(Name='LoanMax')
    if not max:
        max = 0
    max = max.first().Value
    return int(min), int(max)


def loan_valid_day_long():
    days = SiteSetting.objects.filter(Name='LoanValidDay')
    if not days:
        return 1
    return int(days.first().Value)


# ------------------------------------------------------ credit pack
# def credit_pack_fee():
#     fee = SiteSetting.objects.filter(Name='CreditPackFee')
#     if not fee:
#         return 1.5
#     return fee.first().Value


def credit_min_max():
    min = SiteSetting.objects.filter(Name='CreditMin')
    if not min:
        min = 0
    min = min.first().Value
    max = SiteSetting.objects.filter(Name='CreditMax')
    if not max:
        max = 200
    max = max.first().Value
    return int(min), int(max)


def credit_valid_day_long():
    days = SiteSetting.objects.filter(Name='CreditPackValidDay')
    if not days:
        return 1
    return int(days.first().Value)


# ------------------------------------------------------ point
def point_fee():
    fee = SiteSetting.objects.filter(Name='PointFee')
    if not fee:
        return 1.5
    return fee.first().Value


def point_min_max_price():
    min = SiteSetting.objects.filter(Name='PointMinPrice')
    if not min:
        min = 0
    min = min.first().Value
    max = SiteSetting.objects.filter(Name='PointMaxPrice')
    if not max:
        max = 200
    max = max.first().Value
    return int(min), int(max)


def point_min_max_number():
    min = SiteSetting.objects.filter(Name='PointMinNumber')
    if not min:
        min = 10_000
    min = min.first().Value
    max = SiteSetting.objects.filter(Name='PointMaxNumber')
    if not max:
        max = 1_000_000
    max = max.first().Value
    return int(min), int(max)


# ------------------------------------------------------ luck
def luck_price():
    price = SiteSetting.objects.filter(Name='LuckPrice')
    if not price:
        return False
    return int(price.first().Value)
