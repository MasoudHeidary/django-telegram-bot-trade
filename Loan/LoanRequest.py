from .models import Loan, LoanSiteSetting
from Bot.models import TelegramUser
from WalletTransition.WalletRequest import make_buy_transition, make_sell_transition, done_buy_transition, \
    cancel_buy_transition, cancel_sell_transition
from SiteSetting.SiteSettingRequest import loan_min_max


def loan_real_price(value, duration):
    loan = LoanSiteSetting.objects.filter(Value=value, Duration=duration)
    if not loan:
        return False
    return loan.first().Price


def loan_min_max_price(value, duration):
    loan = LoanSiteSetting.objects.filter(Value=value, Duration=duration)
    if not loan:
        return 0, 100000000
    loan = loan.first()
    min, max = loan_min_max()
    min_price = loan.Price * min / 100
    max_price = loan.Price * max / 100
    return min_price, max_price


def loan_fee_percent(value, duration):
    loan = LoanSiteSetting.objects.filter(Value=value, Duration=duration)
    if not loan:
        return 0
    else:
        loan: LoanSiteSetting = loan.first()
        return float(loan.FeePercent)


def get_loan(id):
    loan = Loan.objects.filter(id=id)
    if not loan:
        return False
    else:
        return loan.first()


# -------------------------------------------------------------------------------- buy
def buyer_by_month_value(month, value):
    qu = Loan.objects.filter(SellID='0', Duration=month, Value=value)
    return qu


def seller_by_month_value(month, value):
    qu = Loan.objects.filter(BuyID='0', Duration=month, Value=value)
    return qu


def make_buy_loan(name, family, club_code, value, price, duration, time, buy_id, chat_id):
    fee = loan_fee_percent(value, duration)
    cause = f"خرید وام با مشخصات اختصاری زیر:" \
            f"\n{value}M ,{price}T, {duration}, {time}"
    tran = make_buy_transition(user_id=buy_id, value=price, fee_percent=fee, cause=cause)
    if not tran:
        return False
    loan = Loan.objects.create(
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
    return loan


def make_sell_loan(user: TelegramUser, value, price, duration, sell_id, chat_id):
    fee = loan_fee_percent(value, duration)
    cause = f"فروش وام با مشخصات اختصاری زیر:" \
            f"\n{value}M ,{price}T, {duration}"
    tran = make_sell_transition(user_id=sell_id, value=price, fee_percent=fee, cause=cause)
    if not tran:
        return False
    loan = Loan.objects.create(
        Name=user.profile.Name,
        Family=user.profile.Family,
        ClubCode=user.profile.ClubCode,
        Value=value,
        Price=price,
        Duration=duration,
        # Time=time,
        SellID=sell_id,
        ChatID=chat_id,
        ChatIDSeller=chat_id,
        SellTransition=tran,
        Conf=False,
        BuyConf=False,
        SellConf=False
    )
    return loan


def cancel_loan(loan_id):
    loan: Loan = get_loan(loan_id)
    if not loan:
        return False

    if loan.BuyID == '0':
        # seller
        tran = cancel_sell_transition(loan.SellTransition)
        if not tran:
            return False
        loan.delete()
        return True
    elif loan.SellID == '0':
        # buyer
        tran = cancel_buy_transition(loan.BuyTransition)
        if not tran:
            return False
        loan.delete()
        return True
    return False


def sell_loan_to_buyer(loan_id, seller_id, chat_id):
    loan: Loan = get_loan(id=loan_id)
    if not loan:
        return False
    if loan.SellID != '0' or loan.Conf:
        return False

    cause = f"فروش وام با مشخصات اختصاری زیر:" \
            f"\n{loan.Value}M ,{loan.Price}T, {loan.Duration}, {loan.Time}"

    fee = loan_fee_percent(loan.Value, loan.Duration)
    tran = make_sell_transition(user_id=seller_id, value=loan.Price, fee_percent=fee, cause=cause)
    if not tran:
        return False
    loan.SellID = seller_id
    loan.SellTransition = tran
    loan.ChatIDSeller = chat_id
    loan.save()
    return True


def buy_loan_from_seller(loan_id, time, buyer_id, chat_id):
    loan: Loan = get_loan(id=loan_id)
    if not loan:
        return False
    if loan.BuyID != '0' or loan.Conf:
        return False

    cause = f"خرید وام با مشخصات اختصاری زیر:" \
            f"\n{loan.Value}M ,{loan.Price}T, {loan.Duration}, {time}"
    fee = loan_fee_percent(loan.Value, loan.Duration)
    tran = make_buy_transition(user_id=buyer_id, value=loan.Price, fee_percent=fee, cause=cause)
    if not tran:
        return False
    loan.BuyID = buyer_id
    loan.BuyTransition = tran
    loan.Time = time
    loan.ChatIDBuyer = chat_id
    loan.save()
    return True


# ----------------------------------------------------------------------- conf

def conf_loan(user_id, loan_id):
    loan: Loan = get_loan(id=loan_id)
    if not loan:
        return False
    if loan.BuyID == user_id:
        loan.BuyConf = True
        loan.save()
    if loan.SellID == user_id:
        loan.SellConf = True
        loan.save()

    # if both conf
    if loan.BuyConf and loan.SellConf:
        done_buy_transition(loan.BuyTransition, loan.SellTransition)
        loan.Conf = True
        loan.save()
    return True
