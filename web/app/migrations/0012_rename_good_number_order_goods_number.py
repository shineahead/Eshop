# Generated by Django 3.2.5 on 2021-12-19 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='good_number',
            new_name='goods_number',
        ),
    ]