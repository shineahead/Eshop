# Generated by Django 3.2.5 on 2021-12-20 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_cart_goods_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='order',
        ),
    ]
