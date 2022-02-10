from django.db import models

from Bot.models import TelegramUser


# Create your models here.

class Profile(models.Model):
    Name = models.CharField(max_length=100, verbose_name='نام')
    Family = models.CharField(max_length=100, verbose_name='نام خانوادگی')
    ClubCode = models.CharField(max_length=6, verbose_name='کد باشگاه آگاه')
    PhoneNumber = models.CharField(max_length=11, verbose_name='شماره تلفن')
    BankName = models.CharField(max_length=50, null=True, verbose_name='نام بانک')
    BankAccount = models.CharField(max_length=100, null=True, verbose_name='شماره حساب بانکی')
    Shaba = models.CharField(max_length=26, null=True, verbose_name='شماره شبا')
    UserConf = models.BooleanField(default=False, null=True)

    ToTelegramUser = models.OneToOneField(TelegramUser, on_delete=models.CASCADE, verbose_name='کاربر مرتبط')

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'