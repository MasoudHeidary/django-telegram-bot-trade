from django.contrib.humanize.templatetags.humanize import intcomma

from .models import Wallet, Transition
from Bot.models import TelegramUser


# ----------------------------------------------------------------- wallet
# return wallet if wallet exist else, return false
def check_have_wallet(user_id):
    user = TelegramUser.objects.filter(telegram_id=user_id)
    if not user:
        return False
    try:
        user = user.first()
        wallet = user.wallet
        return wallet
    except:
        wallet = make_new_wallet(user_id=user_id)
        return wallet


# return maked wallet
def make_new_wallet(user_id):
    user = TelegramUser.objects.filter(telegram_id=user_id)
    if not user:
        return False
    user = user.first()
    Wallet.objects.create(
        ToTelegramUser=user
    )
    return user.wallet


# ----------------------------------------------------------------- charge and withdraw

def charge_wallet(user_id, amount):
    wallet: Wallet = check_have_wallet(user_id)
    if not wallet:
        return False

    cause = f"شارژ کیف پول به مبلغ" \
            f" {amount}"
    Transition.objects.create(
        Before=wallet.AvailableMoney,
        Value=amount,
        Fee=0,
        Next=wallet.AvailableMoney + amount,
        Cause=cause,
        ToWallet=wallet,
        Done=True
    )

    wallet.AvailableMoney += amount
    wallet.save()

    return True


def withdraw_from_wallet(user_id, amount: int):
    wallet: Wallet = check_have_wallet(user_id)
    if not wallet:
        return False

    if wallet.AvailableMoney < amount:
        return False

    cause = f"برداشت از کیف پول به مبلغ " \
            f"{intcomma(amount)}"
    tran = Transition.objects.create(
        Before=wallet.AvailableMoney,
        Value=amount,
        Next=wallet.AvailableMoney - amount,
        Fee=0,
        Cause=cause,
        ToWallet=wallet,
        Done=True
    )

    wallet.AvailableMoney -= amount
    wallet.BlockedMoney += amount
    wallet.save()

    return tran.id


def admin_withdraw_from_wallet(tran_id, amount: int, fee: int):
    try:
        tran = Transition.objects.get(id=tran_id)
    except:
        return False

    tran.Next -= fee
    tran.Fee = fee
    tran.save()

    tran.ToWallet.BlockedMoney -= amount
    tran.ToWallet.AvailableMoney -= fee
    tran.ToWallet.save()

    return True


# ----------------------------------------------------------------- transition

# value + fee -> blocked
# return tran id
def make_buy_transition(user_id, value, fee_percent, cause):
    wallet: Wallet = check_have_wallet(user_id=user_id)
    if not wallet:
        return False

    fee_percent = float(fee_percent)
    if wallet.AvailableMoney < value + value * fee_percent / 100:
        return False

    wallet.AvailableMoney -= (value + value * fee_percent / 100)
    wallet.BlockedMoney += (value + value * fee_percent / 100)
    wallet.save()

    tran = Transition.objects.create(
        Before=wallet.AvailableMoney + value + value * fee_percent / 100,
        Value=value,
        Fee=value * fee_percent / 100,
        Next=wallet.AvailableMoney,
        Cause=cause,
        ToWallet=wallet,
    )
    return tran.id


def cancel_buy_transition(transition_id):
    tran = Transition.objects.filter(id=transition_id)
    if not tran:
        return False
    transition = tran.first()
    wallet = transition.ToWallet
    wallet.AvailableMoney += transition.Value + transition.Fee
    wallet.BlockedMoney -= (transition.Value + transition.Fee)
    wallet.save()
    transition.delete()
    return True


def make_sell_transition(user_id, value, fee_percent, cause):
    wallet: Wallet = check_have_wallet(user_id=user_id)
    if not wallet:
        return False

    fee_percent = float(fee_percent)
    tran = Transition.objects.create(
        Before=wallet.AvailableMoney,
        Value=value,
        Fee=value * fee_percent / 100,
        Next=wallet.AvailableMoney + value - value * fee_percent / 100,
        Cause=cause,
        ToWallet=wallet,
    )
    return tran.id


def cancel_sell_transition(transition_id):
    tran = Transition.objects.filter(id=transition_id)
    if not tran:
        return False
    tran.first().delete()
    return True


def done_buy_transition(buy_tran_id, sell_tran_id):
    buy_tran: Transition = Transition.objects.get(id=buy_tran_id)
    sell_tran: Transition = Transition.objects.get(id=sell_tran_id)

    # money from buyer -> seller
    buy_tran.ToWallet.BlockedMoney -= (sell_tran.Value + sell_tran.Fee)
    buy_tran.Done = True
    buy_tran.ToWallet.save()
    buy_tran.save()
    sell_tran.ToWallet.AvailableMoney += (buy_tran.Value - buy_tran.Fee)
    sell_tran.Done = True
    sell_tran.ToWallet.save()
    sell_tran.save()
