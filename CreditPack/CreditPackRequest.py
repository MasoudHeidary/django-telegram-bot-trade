from .models import CreditPack, CreditPackSiteSetting
from Bot.models import TelegramUser
from SiteSetting.SiteSettingRequest import credit_min_max
from WalletTransition.WalletRequest import make_buy_transition, make_sell_transition, done_buy_transition, \
    cancel_buy_transition, cancel_sell_transition


def credit_real_price(value, duration):
    credit = CreditPackSiteSetting.objects.filter(Value=value, Duration=duration)
    if not credit:
        return False
    return credit.first().Price


def credit_min_max_price(value, duration):
    credit = CreditPackSiteSetting.objects.filter(Value=value, Duration=duration)
    if not credit:
        return 0, 100000000
    credit = credit.first()
    min, max = credit_min_max()
    min_price = credit.Price * min / 100
    max_price = credit.Price * max / 100
    return min_price, max_price


def credit_packet_fee_percent(value, duration):
    credit = CreditPackSiteSetting.objects.filter(Value=value, Duration=duration)
    if not credit:
        return 0
    else:
        credit: CreditPackSiteSetting = credit.first()
        return float(credit.FeePercent)


def get_credit(id):
    credit = CreditPack.objects.filter(id=id)
    if not credit:
        return False
    else:
        return credit.first()


# -------------------------------------------------------------------------------

def buyer_by_month_value(month, value):
    qu = CreditPack.objects.filter(SellID='0', Duration=month, Value=value)
    return qu


def seller_by_month_value(month, value):
    qu = CreditPack.objects.filter(BuyID='0', Duration=month, Value=value)
    return qu


def make_buy_credit(name, family, club_code, value, price, duration, time, buy_id, chat_id):
    fee = credit_packet_fee_percent(value, duration)
    cause = f"خرید بسته اعتباری با مشخصات اختصاری زیر:" \
            f"\n{value}M ,{price}T, {duration}, {time}"
    tran = make_buy_transition(user_id=buy_id, value=price, fee_percent=fee, cause=cause)
    if not tran:
        return False
    credit = CreditPack.objects.create(
        Name=name,
        Family=family,
        ClubCode=club_code,
        Value=value,
        Price=price,
        Duration=duration,
        Time=time,
        BuyID=buy_id,
        ChatID=chat_id,
        ChatIDBuyer=chat_id,
        BuyTransition=tran,
        Conf=False,
        BuyConf=False,
        SellConf=False
    )
    return credit


def make_sell_credit(user: TelegramUser, value, price, duration, sell_id, chat_id):
    fee = credit_packet_fee_percent(value, duration)
    cause = f"فروش بسته اعتباری با مشخصات اختصاری زیر:" \
            f"\n{value}M ,{price}T, {duration}"
    tran = make_sell_transition(user_id=sell_id, value=price, fee_percent=fee, cause=cause)
    if not tran:
        return False
    credit = CreditPack.objects.create(
        Name=user.profile.Name,
        Family=user.profile.Family,
        ClubCode=user.profile.ClubCode,
        Value=value,
        Price=price,
        Duration=duration,
        SellID=sell_id,
        ChatID=chat_id,
        ChatIDSeller=chat_id,
        SellTransition=tran,
        Conf=False,
        BuyConf=False,
        SellConf=False
    )
    return credit


def cancel_credit(credit_id):
    credit: CreditPack = get_credit(credit_id)
    if not credit:
        return False

    if credit.BuyID == '0':
        # seller
        tran = cancel_sell_transition(credit.SellTransition)
        if not tran:
            return False
        credit.delete()
        return True
    elif credit.SellID == '0':
        # buyer
        tran = cancel_buy_transition(credit.BuyTransition)
        if not tran:
            return False
        credit.delete()
        return True
    return False


def sell_loan_to_buyer(loan_id, seller_id, chat_id):
    credit: CreditPack = get_credit(id=loan_id)
    if not credit:
        return False
    if credit.SellID != '0' or credit.Conf:
        return False

    cause = f"فروش بسته اعتباری با مشخصات اختصاری زیر:" \
            f"\n{credit.Value}M ,{credit.Price}T, {credit.Duration}, {credit.Time}"
    fee = credit_packet_fee_percent(credit.Value, credit.Duration)
    tran = make_sell_transition(user_id=seller_id, value=credit.Price, fee_percent=fee, cause=cause)
    if not tran:
        return False
    credit.SellID = seller_id
    credit.SellTransition = tran
    credit.ChatIDSeller = chat_id
    credit.save()
    return True


def buy_credit_from_seller(credit_id, time, buyer_id, chat_id):
    credit: CreditPack = get_credit(id=credit_id)
    if not credit:
        return False
    if credit.BuyID != '0' or credit.Conf:
        return False

    cause = f"خرید بسته اعتباری با مشخصات اختصاری زیر:" \
            f"\n{credit.Value}M ,{credit.Price}T, {credit.Duration}, {time}"
    fee = credit_packet_fee_percent(credit.Value, credit.Duration)
    tran = make_buy_transition(user_id=buyer_id, value=credit.Price, fee_percent=fee, cause=cause)
    if not tran:
        return False
    credit.BuyID = buyer_id
    credit.BuyTransition = tran
    credit.Time = time
    credit.ChatIDBuyer = chat_id
    credit.save()
    return True


# ----------------------------------------------------------------------- conf

def conf_loan(user_id, loan_id):
    credit: CreditPack = get_credit(id=loan_id)
    if not credit:
        return False
    if credit.BuyID == user_id:
        credit.BuyConf = True
        credit.save()
    if credit.SellID == user_id:
        credit.SellConf = True
        credit.save()

    # if both conf
    if credit.BuyConf and credit.SellConf:
        done_buy_transition(credit.BuyTransition, credit.SellTransition)
        credit.Conf = True
        credit.save()
    return True
