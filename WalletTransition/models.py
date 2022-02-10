from django.db import models

from Bot.models import TelegramUser


# Create your models here.

class Wallet(models.Model):
    AvailableMoney = models.IntegerField(default=0, verbose_name='پول موجود')
    BlockedMoney = models.IntegerField(default=0, verbose_name='پول بلوکه شده')

    ToTelegramUser = models.OneToOneField(TelegramUser, on_delete=models.CASCADE, verbose_name='کاربر مرتبط')

    class Meta:
        verbose_name = 'کیف پول'
        verbose_name_plural = 'کیف پول ها'


class Transition(models.Model):
    Before = models.IntegerField(verbose_name='موجودی قبل از تراکنش')
    Value = models.IntegerField(verbose_name='ارزش ترکانش')
    Fee = models.IntegerField(verbose_name='کارمزد تراکنش')
    Next = models.IntegerField(verbose_name='موجودی بعد از تراکنش')
    Cause = models.CharField(max_length=200, verbose_name='توضیحات تراکنش')
    Time = models.DateTimeField(auto_now_add=True, verbose_name='زمان تراکنش')
    Done = models.BooleanField(default=False, verbose_name='تراکنش انجام شده')
    TranTime = models.DateField(auto_now=True, null=True, verbose_name='تاریخ تراکنش')

    ToWallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, verbose_name='کیف پول مربوطه')

    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش ها'
