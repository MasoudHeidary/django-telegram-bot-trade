from django.db import models


# Create your models here.

class SiteSetting(models.Model):
    Name = models.CharField(max_length=50, verbose_name='نام پارامتر')
    Value = models.DecimalField(decimal_places=1, max_digits=20, verbose_name='مقدار پارامتر')
    PersianName = models.CharField(max_length=100, verbose_name='نام فارسی پارامتر')

    class Meta:
        verbose_name = 'تنظیم'
        verbose_name_plural = 'تنظیمات'

# SiteSetting.objects.create(Name='CreditPackFee', Value=1.5, PersianName=' ')
# SiteSetting.objects.create(Name='CreditPackValidDay', Value=10, PersianName=' ')
# SiteSetting.objects.create(Name='LoanFee', Value=1.5, PersianName=' ')
# SiteSetting.objects.create(Name='LoanValidDay', Value=10, PersianName=' ')
# SiteSetting.objects.create(Name='LoanMin', Value=110, PersianName=' ')
# SiteSetting.objects.create(Name='LoanMax', Value=250, PersianName=' ')
# SiteSetting.objects.create(Name='CreditMin', Value=110, PersianName=' ')
# SiteSetting.objects.create(Name='CreditMax', Value=250, PersianName=' ')
# SiteSetting.objects.create(Name='PointMinNumber', Value=50000, PersianName=' ')
# SiteSetting.objects.create(Name='PointMaxNumber', Value=1000000, PersianName=' ')
# SiteSetting.objects.create(Name='PointMinPrice', Value=1, PersianName=' ')
# SiteSetting.objects.create(Name='PointMaxPrice', Value=10, PersianName=' ')
# SiteSetting.objects.create(Name='PointFee', Value=1.5, PersianName=' ')
# SiteSetting.objects.create(Name='LuckPrice', Value=5000000, PersianName=' ')
