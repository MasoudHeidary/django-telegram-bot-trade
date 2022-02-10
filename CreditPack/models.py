from django.db import models


class CreditPack(models.Model):
    Name = models.CharField(max_length=100, verbose_name='نام')
    Family = models.CharField(max_length=100, verbose_name='نام خانوادگی')
    ClubCode = models.CharField(max_length=6, verbose_name='کد باشگاه')
    Value = models.IntegerField(verbose_name='ارزش')
    Price = models.IntegerField(verbose_name='قیمت')
    Duration = models.IntegerField(verbose_name='مدت')
    Time = models.CharField(null=True, blank=True, max_length=10, verbose_name='تاریخ اعمال')

    SellID = models.CharField(default='0', max_length=20, verbose_name='آیدی فروشنده')
    SellTransition = models.IntegerField(null=True, verbose_name='تراکنش مربوط به فروش')

    BuyID = models.CharField(default='0', max_length=20, verbose_name='آیدی خریدار')
    BuyTransition = models.IntegerField(null=True, verbose_name='تراکنش مربوط به خرید')

    SellConf = models.BooleanField(default=False, verbose_name='تاییده ی فروشنده')
    BuyConf = models.BooleanField(default=False, verbose_name='تاییده ی خریدار')
    Conf = models.BooleanField(default=False, verbose_name='انجام شده')

    ChatID = models.CharField(max_length=20, verbose_name='چتی که درخواست ثبت کرده')
    ChatIDSeller = models.CharField(max_length=20, null=True, blank=True)
    ChatIDBuyer = models.CharField(max_length=20, null=False, blank=True)

    BuyerMessageID = models.IntegerField(null=True, blank=True)
    SellerMessageID = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'بسته اعتباری'
        verbose_name_plural = 'بسته های اعتباری'


class CreditPackSiteSetting(models.Model):
    Value = models.IntegerField(verbose_name='ارزش')
    Duration = models.IntegerField(verbose_name='مدت زمان')
    Price = models.IntegerField(verbose_name='قیمت در سایت')
    FeePercent = models.DecimalField(verbose_name='درصد کارمزد', null=True, decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = 'تنظیم بسته اعتباری'
        verbose_name_plural = 'تنظیمات بسته های اعتباری'
