# Generated by Django 3.2 on 2021-05-03 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Loan', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='BuyID',
            field=models.CharField(max_length=20, null=True, verbose_name='آیدی خریدار'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='BuyTransition',
            field=models.IntegerField(null=True, verbose_name='تراکنش مربوط به خریدار'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='SellID',
            field=models.CharField(max_length=20, null=True, verbose_name='آیدی فروشنده'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='SellTransition',
            field=models.IntegerField(null=True, verbose_name='ترکنش مربوط به فروش'),
        ),
    ]