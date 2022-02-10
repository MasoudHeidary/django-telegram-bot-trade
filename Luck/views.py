from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import LuckSetting
from .LuckRequest import check_luck, generate_luck


# Create your views here.

def luck_page(request):
    if request.GET:
        user_id = request.GET.get('user_id')
        if not user_id:
            return HttpResponseNotFound("<h1>access denied!</h1>")
        luck = check_luck(user_id)
        if not luck:
            return HttpResponseNotFound("<h1>access denied!</h1>")
    else:
        return HttpResponseNotFound("<h1>access denied!</h1>")

    context = \
        {
            'Degree': generate_luck(user_id),
        }

    return render(request, 'LuckyRound.html', context)
