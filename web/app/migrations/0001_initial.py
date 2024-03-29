# Generated by Django 3.2.5 on 2021-12-19 14:03

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='goods',
            fields=[
                ('goods_id', models.AutoField(primary_key=True, serialize=False)),
                ('goods_name', models.CharField(max_length=50, verbose_name='商品名')),
                ('item_img', models.ImageField(default='g_image/default.jpg', upload_to='g_images/', verbose_name='图片')),
                ('goods_introduction', models.CharField(default='商品简介ya', max_length=50, verbose_name='简介')),
                ('price', models.DecimalField(decimal_places=3, max_digits=8, verbose_name='售价')),
                ('stock', models.IntegerField(default=0, verbose_name='库存')),
                ('state', models.IntegerField(default=0, verbose_name='商品状态')),
            ],
        ),
        migrations.CreateModel(
            name='types',
            fields=[
                ('type_id', models.AutoField(primary_key=True, serialize=False)),
                ('sort', models.CharField(max_length=16, verbose_name='商品种类')),
            ],
        ),
        migrations.CreateModel(
            name='user_seller',
            fields=[
                ('user_seller_id', models.AutoField(primary_key=True, serialize=False)),
                ('account', models.CharField(max_length=16, unique=True, verbose_name='账号')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('email', models.EmailField(max_length=16, verbose_name='邮箱')),
            ],
        ),
        migrations.CreateModel(
            name='goods_detail',
            fields=[
                ('goods_detail_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.goods')),
                ('photo', models.ImageField(upload_to='', verbose_name='图片')),
                ('detail', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='seller',
            fields=[
                ('seller_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.user_seller')),
                ('store_name', models.CharField(max_length=50, unique=True, verbose_name='店铺名')),
                ('avatar', models.ImageField(default='s_image/default.jpg', upload_to='u_images/', verbose_name='店铺头像')),
                ('detail', models.CharField(default='此商家很懒，没有简介', max_length=50, verbose_name='店铺简介')),
                ('goods_number', models.IntegerField(default=0, verbose_name='商品数量')),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.user_seller')),
                ('user_name', models.CharField(default=250, max_length=16, verbose_name='用户昵称')),
                ('user_contact', models.CharField(max_length=16, verbose_name='联系方式')),
                ('avatar', models.ImageField(default='u_image/default.jpg', upload_to='u_images/', verbose_name='头像')),
                ('state', models.IntegerField(default=1, verbose_name='状态')),
                ('balance', models.DecimalField(decimal_places=3, max_digits=8, verbose_name='用户余额')),
            ],
        ),
        migrations.CreateModel(
            name='post_reply',
            fields=[
                ('reply_id', models.AutoField(primary_key=True, serialize=False)),
                ('reply_context', models.TextField(max_length=200, verbose_name='回复内容')),
                ('reply_time', models.DateTimeField(verbose_name='回复时间')),
                ('seller_name', models.CharField(max_length=16, verbose_name='回复商家')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.goods')),
            ],
        ),
        migrations.CreateModel(
            name='post',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('post_context', models.TextField(max_length=500, verbose_name='评论内容')),
                ('user_name', models.CharField(max_length=10, verbose_name='评论人')),
                ('post_time', models.DateTimeField(verbose_name='发布时间')),
                ('post_goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.goods')),
            ],
        ),
        migrations.AddField(
            model_name='goods',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app.types'),
        ),
        migrations.CreateModel(
            name='order',
            fields=[
                ('order_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.goods')),
                ('addressee', models.CharField(max_length=16, verbose_name='收件人')),
                ('good_number', models.PositiveBigIntegerField(default=1, verbose_name='商品数量')),
                ('money', models.DecimalField(decimal_places=3, max_digits=8, verbose_name='订单总金额')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('state', models.IntegerField(default=0, verbose_name='订单状态')),
                ('fk_order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
        migrations.AddField(
            model_name='goods',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.seller'),
        ),
        migrations.AddField(
            model_name='goods',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app.user'),
        ),
        migrations.CreateModel(
            name='address',
            fields=[
                ('address_id', models.AutoField(primary_key=True, serialize=False)),
                ('receiver', models.CharField(max_length=20, verbose_name='收件人')),
                ('address', models.CharField(max_length=50, verbose_name='地址')),
                ('post', models.CharField(max_length=32, verbose_name='邮编')),
                ('is_default', models.IntegerField(default=0, verbose_name='是否默认')),
                ('phone_number', models.CharField(max_length=32, verbose_name='电话')),
                ('fk_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
    ]
