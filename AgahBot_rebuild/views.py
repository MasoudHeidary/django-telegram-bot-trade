from django.contrib.humanize.templatetags.humanize import intcomma
from django.shortcuts import render
from WalletTransition.models import Transition


def all_and_fee(request):
    tran = Transition.objects.filter(Done=True)

    all = 0
    fee = 0
    for i in tran:
        i: Transition
        all += i.Value
        fee += i.Fee

    context = \
        {
            'All': intcomma(all),
            'Fee': intcomma(fee)
        }

    return render(request, 'PriceAndFee.html', context)
