# Generated by Django 4.1.5 on 2023-02-09 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baykeShop', '0013_baykeshopingcart_baykeshopingcart_unique_owner_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baykeshopingcart',
            name='num',
            field=models.PositiveIntegerField(default=0, verbose_name='数量'),
        ),
    ]
