# Generated by Django 3.2 on 2021-05-03 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WalletTransition', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transition',
            name='Done',
            field=models.BooleanField(default=False, verbose_name='ترکانش انجام شده'),
        ),
    ]
