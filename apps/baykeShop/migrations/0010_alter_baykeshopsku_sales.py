# Generated by Django 4.1.5 on 2023-02-04 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baykeShop', '0009_baykeshopsku_sales'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baykeshopsku',
            name='sales',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='销量'),
        ),
    ]
