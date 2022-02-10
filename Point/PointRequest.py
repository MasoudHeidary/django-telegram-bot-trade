from .models import Point

from Bot.models import TelegramUser
from SiteSetting.SiteSettingRequest import point_fee
from WalletTransition.WalletRequest import make_buy_transition, make_sell_transition, \
    done_buy_transition, cancel_buy_transition, cancel_sell_transition


def point_buyer():
    qu = Point.objects.filter(SellID='0')
    return qu


def point_seller():
    qu = Point.objects.filter(BuyID='0')
    return qu


def get_point(id):
    point = Point.objects.filter(id=id)
    if not point:
        return False
    else:
        return point.first()


# ---------------------------------------------------------------------------------

def make_buy_point(name, family, club_code, number, price, buy_id, chat_id):
    fee = point_fee()
    cause = f"خرید " \
            f"{number}" \
            f" عدد امتیاز"
    tran = make_buy_transition(user_id=buy_id, value=price * number // 10, fee_percent=fee, cause=cause)
    if not tran:
        return False
    point = Point.objects.create(
        Name=name,
        Family=family,
        ClubCode=club_code,
        Number=number,
        Price=price,
        BuyID=buy_id,
        ChatID=chat_id,
        ChatIDBuyer=chat_id,
        BuyTransition=tran,
        Conf=False,
        BuyConf=False,
        SellConf=False
    )
    return point


def make_sell_point(user: TelegramUser, number, price, sell_id, chat_id):
    cause = f"فروش " \
            f"{number}" \
            f" امتباز"
    fee = point_fee()
    tran = make_sell_transition(user_id=sell_id, value=number * price // 10, fee_percent=fee, cause=cause)
    if not tran:
        return False
    point = Point.objects.create(
        Name=user.profile.Name,
        Family=user.profile.Family,
        ClubCode=user.profile.ClubCode,
        Number=number,
        Price=price,
        SellID=sell_id,
        ChatID=chat_id,
        ChatIDSeller=chat_id,
        SellTransition=tran,
        Conf=False,
        BuyConf=False,
        SellConf=False
    )
    return point


def cancel_point(point_id):
    point: Point = get_point(point_id)
    if not point:
        return False

    if point.BuyID == '0':
        # seller
        tran = cancel_sell_transition(point.SellTransition)
        if not tran:
            return False
        point.delete()
        return True
    elif point.SellID == '0':
        # buyer
        tran = cancel_buy_transition(point.BuyTransition)
        if not tran:
            return False
        point.delete()
        return True
    return False


def sell_point_to_buyer(point_id, seller_id, chat_id):
    point: Point = get_point(id=point_id)
    if not point:
        return False
    if point.SellID != '0' or point.Conf:
        return False

    cause = f"خرید " \
            f"{point.Number}" \
            f" تعداد امتیاز"
    fee = point_fee()
    tran = make_sell_transition(user_id=seller_id, value=point.Number * point.Price / 10, fee_percent=fee, cause=cause)
    if not tran:
        return False
    point.SellID = seller_id
    point.SellTransition = tran
    point.ChatIDSeller = chat_id
    point.save()
    return True


def buy_point_from_seller(point_id, buyer_id, chat_id):
    point: Point = get_point(id=point_id)
    if not point:
        return False
    if point.BuyID != '0' or point.Conf:
        return False

    cause = f"خرید " \
            f"{point.Number}" \
            f" امتیاز"
    fee = point_fee()
    tran = make_buy_transition(user_id=buyer_id, value=point.Number * point.Price / 10, fee_percent=fee, cause=cause)
    if not tran:
        return False
    point.BuyID = buyer_id
    point.BuyTransition = tran
    point.ChatIDBuyer = chat_id
    point.save()
    return True


# ----------------------------------------------------------------------- conf

def conf_point(user_id, point_id):
    point: Point = get_point(id=point_id)
    if not point:
        return False
    if point.BuyID == user_id:
        point.BuyConf = True
        point.save()
    if point.SellID == user_id:
        point.SellConf = True
        point.save()

    # if both conf
    if point.BuyConf and point.SellConf:
        done_buy_transition(point.BuyTransition, point.SellTransition)
        point.Conf = True
        point.save()
    return True
