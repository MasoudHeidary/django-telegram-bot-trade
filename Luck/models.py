from django.db import models


# Create your models here.

class Luck(models.Model):
    UserID = models.CharField(max_length=30, verbose_name='آیدی کاربر')
    Name = models.CharField(max_length=100, verbose_name='اسم جایزه')
    Paied = models.BooleanField(default=False, verbose_name='پرداخت شده')

    class Meta:
        verbose_name = 'جایزه'
        verbose_name_plural = 'جایزه ها'


class LuckSetting(models.Model):
    Name = models.CharField(max_length=100, verbose_name='اسم')
    Number = models.IntegerField(default=0, verbose_name='تعداد')
    Degree = models.IntegerField(default=0, verbose_name='درجه(تخصصی)')

    class Meta:
        verbose_name = 'تنظیمات جایزه'
        verbose_name_plural = 'تنظیمات جایزه ها'
