from django.db import models


# Create your models here.
class Point(models.Model):
    Name = models.CharField(max_length=100, verbose_name='نام')
    Family = models.CharField(max_length=100, verbose_name='نام خانوادگی')
    ClubCode = models.CharField(max_length=6, verbose_name='کد باشگاه')

    Number = models.IntegerField(verbose_name='تعداد امتیازها')
    Price = models.IntegerField(verbose_name='قیمت(ریال)')

    SellID = models.CharField(default='0', max_length=20, verbose_name='آیدی فروشنده')
    SellTransition = models.IntegerField(null=True, verbose_name='تراکنش مربوط به فروش')

    BuyID = models.CharField(default='0', max_length=20, verbose_name='آیدی خریدار')
    BuyTransition = models.IntegerField(null=True, verbose_name='تراکنش مربوط به خرید')

    SellConf = models.BooleanField(default=False, verbose_name='تاییده ی فروشنده')
    BuyConf = models.BooleanField(default=False, verbose_name='تاییده ی خریدار')
    Conf = models.BooleanField(default=False, verbose_name='انجام شده')

    ChatID = models.CharField(max_length=20, verbose_name='چتی که درخواست ثبت کرده')
    ChatIDSeller = models.CharField(max_length=20, null=True, blank=True)
    ChatIDBuyer = models.CharField(max_length=20, null=True, blank=True)

    BuyerMessageID = models.IntegerField(null=True, blank=True)
    SellerMessageID = models.IntegerField(null=True, blank=True)

    # objects = LoanManager()

    class Meta:
        verbose_name = 'امتیاز'
        verbose_name_plural = 'امتیازها'
