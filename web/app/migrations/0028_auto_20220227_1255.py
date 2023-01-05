# Generated by Django 3.2.5 on 2022-02-27 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_alter_goods_item_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_seller',
            name='account',
            field=models.CharField(max_length=20, unique=True, verbose_name='账号'),
        ),
        migrations.AlterField(
            model_name='user_seller',
            name='email',
            field=models.EmailField(max_length=32, verbose_name='邮箱'),
        ),
    ]
