# Generated by Django 4.1.7 on 2023-03-22 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baykeshop', '0003_baykeipaddress_baykestats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baykeipaddress',
            name='browser',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
    ]
