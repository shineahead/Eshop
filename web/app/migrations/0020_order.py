# Generated by Django 3.2.5 on 2021-12-20 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_delete_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='order',
            fields=[
                ('order', models.AutoField(primary_key=True, serialize=False)),
                ('goods_number', models.PositiveBigIntegerField(default=1, verbose_name='商品数量')),
                ('money', models.DecimalField(decimal_places=3, max_digits=8, verbose_name='订单总金额')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('state', models.IntegerField(default=0, verbose_name='订单状态')),
                ('address_id', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='app.address')),
                ('order_goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods', to='app.user')),
                ('order_seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to='app.user')),
                ('order_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ouser', to='app.user')),
            ],
        ),
    ]