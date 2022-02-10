# Generated by Django 3.2.3 on 2021-06-24 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Point', '0002_point_chatidbuyer'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='BuyerMessageID',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='point',
            name='ChatIDSeller',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='point',
            name='SellerMessageID',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
