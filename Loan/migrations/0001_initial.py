# Generated by Django 3.2 on 2021-05-03 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100, verbose_name='نام')),
                ('Family', models.CharField(max_length=100, verbose_name='نام خانوادگی')),
                ('ClubCode', models.CharField(max_length=6, verbose_name='کد باشگاه')),
                ('Value', models.IntegerField(verbose_name='ارزش')),
                ('Price', models.IntegerField(verbose_name='قیمت')),
                ('Duration', models.IntegerField(verbose_name='مدت')),
                ('Time', models.CharField(max_length=10, verbose_name='تاریخ اعمال')),
                ('ToSell', models.BooleanField(verbose_name='فروشنده است؟')),
                ('SellID', models.CharField(default=None, max_length=20, verbose_name='آیدی فروشنده')),
                ('SellTransition', models.IntegerField(default=None, verbose_name='ترکنش مربوط به فروش')),
                ('BuyID', models.CharField(default=None, max_length=20, verbose_name='آیدی خریدار')),
                ('BuyTransition', models.IntegerField(default=None, verbose_name='تراکنش مربوط به خریدار')),
            ],
            options={
                'verbose_name': 'وام',
                'verbose_name_plural': 'وام ها',
            },
        ),
        migrations.CreateModel(
            name='LoanSiteSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Value', models.IntegerField(verbose_name='')),
                ('Duration', models.IntegerField(verbose_name='')),
                ('Price', models.IntegerField(verbose_name='')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': '',
            },
        ),
    ]
