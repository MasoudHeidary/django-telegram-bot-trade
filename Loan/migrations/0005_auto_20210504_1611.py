# Generated by Django 3.2 on 2021-05-04 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Loan', '0004_auto_20210504_0025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='ToSell',
        ),
        migrations.AddField(
            model_name='loan',
            name='Done',
            field=models.BooleanField(default=False, verbose_name='انجام شده'),
        ),
    ]