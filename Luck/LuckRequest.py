from django.db.models.query import Q
from .models import Luck, LuckSetting
from random import randint, choice

from Loan.models import Loan
from CreditPack.models import CreditPack
from Point.models import Point
from SiteSetting.SiteSettingRequest import luck_price


def all_transition_value(user_id):
    loan = Loan.objects.filter(
        Q(Conf=True),
        Q(SellID=user_id) | Q(BuyID=user_id)
    )
    credit = CreditPack.objects.filter(
        Q(Conf=True),
        Q(SellID=user_id) | Q(BuyID=user_id)
    )
    point = Point.objects.filter(
        Q(Conf=True),
        Q(SellID=user_id) | Q(BuyID=user_id)
    )

    all_tran = 0
    for i in loan:
        all_tran += i.Price
    for i in credit:
        all_tran += i.Price
    for i in point:
        all_tran += (i.Number * i.Price // 10)

    return all_tran


def number_of_got_luck(user_id):
    num = Luck.objects.filter(UserID=user_id)
    return num.count()


def check_luck(user_id):
    min_tran = luck_price()
    if all_transition_value(user_id) >= (number_of_got_luck(user_id) + 1) * min_tran:
        return True
    return False


def generate_luck(user_id):
    degree = [
        range(61, 90),
        range(331, 360),
        range(241, 270),
        range(151, 180),
        range(1, 30),
        range(91, 121),
        range(181, 210),
        range(271, 300)
    ]
    available_reward = [
        'وجه نقد به ارزش 20هزار امتیاز',  # 0
        'وجه نقد به ارزش 30هزار امتیاز',  # 1
        'وجه نقد به ارزش 40هزار امتیاز',  # 2
        'وجه نقد به ارزش 50هزار امتیاز',  # 3
        'پوج',  # 4
        'پوج',  # 5
        'پوج',  # 6
        'پوج',  # 7
    ]
    if LuckSetting.objects.get(Name=2).Number:
        available_reward += ['وجه نقد به ارزش بسته 2میلیون یک ماهه ']  # 8
        degree += [range(121, 150)]
    if LuckSetting.objects.get(Name=3).Number:
        available_reward += ['وجه نقد به ارزش بسته 3میلیون یک ماهه ']  # 9
        degree += [range(211, 240)]
    if LuckSetting.objects.get(Name=5).Number:
        available_reward += ['وجه نقد به ارزش بسته 5میلیون یک ماهه ']  # 10
        degree += [range(301, 330)]

    num = randint(0, len(degree) - 1)

    if num == 8:
        q = LuckSetting.objects.get(Name=2)
        q.Number -= 1
        q.save()
    elif num == 9:
        q = LuckSetting.objects.get(Name=3)
        q.Number -= 1
        q.save()
    elif num == 10:
        q = LuckSetting.objects.get(Name=5)
        q.Number -= 1
        q.save()

    Luck.objects.create(
        UserID=user_id,
        Name=available_reward[num]
    )

    return choice(degree[num])
