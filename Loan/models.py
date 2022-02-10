from django.db import models


class Loan(models.Model):
    Name = models.CharField(max_length=100, verbose_name='نام')
    Family = models.CharField(max_length=100, verbose_name='نام خانوادگی')
    ClubCode = models.CharField(max_length=6, verbose_name='کد باشگاه')
    Value = models.IntegerField(verbose_name='ارزش')
    Price = models.IntegerField(verbose_name='قیمت')
    Duration = models.IntegerField(verbose_name='مدت')
    Time = models.CharField(null=True, max_length=10, verbose_name='تاریخ اعمال')

    SellID = models.CharField(default='0', max_length=20, verbose_name='آیدی فروشنده')
    SellTransition = models.IntegerField(null=True, verbose_name='ترکنش مربوط به فروش')

    BuyID = models.CharField(default='0', max_length=20, verbose_name='آیدی خریدار')
    BuyTransition = models.IntegerField(null=True, verbose_name='تراکنش مربوط به خریدار')

    SellConf = models.BooleanField(default=False, verbose_name='تاییده ی فروشنده')
    BuyConf = models.BooleanField(default=False, verbose_name='تاییده خریدار')
    Conf = models.BooleanField(default=False, verbose_name='انجام شده')

    ChatID = models.CharField(max_length=20, verbose_name='چتی که درخواست ثبت کرده')
    ChatIDSeller = models.CharField(max_length=20, null=True, blank=True)
    ChatIDBuyer = models.CharField(max_length=20, null=True, blank=True)

    BuyerMessageID = models.IntegerField(null=True, blank=True)
    SellerMessageID = models.IntegerField(null=True, blank=True)

    # objects = LoanManager()

    class Meta:
        verbose_name = 'وام'
        verbose_name_plural = 'وام ها'


class LoanSiteSetting(models.Model):
    Value = models.IntegerField(verbose_name='ارزش')
    Duration = models.IntegerField(verbose_name='مدت زمان')
    Price = models.IntegerField(verbose_name='قیمت در سایت')
    FeePercent = models.DecimalField(verbose_name='درصد کارمزد', null=True, decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = 'تنظیم وام'
        verbose_name_plural = 'تنظیمات وام ها'
