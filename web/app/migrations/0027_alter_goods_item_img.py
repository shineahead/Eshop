# Generated by Django 3.2.5 on 2021-12-20 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20211220_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='item_img',
            field=models.ImageField(default='item_images/default.jpg', upload_to='g_images/', verbose_name='图片'),
        ),
    ]
