# Generated by Django 3.2.5 on 2021-12-19 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_delete_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart', models.AutoField(primary_key=True, serialize=False)),
                ('goods_name', models.CharField(default='', max_length=50, verbose_name='商品名称')),
                ('seller_name', models.CharField(max_length=25, verbose_name='店铺名称')),
                ('goods_number', models.IntegerField(default=0, verbose_name='数量')),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=20, null=True, verbose_name='单价')),
                ('status', models.IntegerField(default=0, verbose_name='状态')),
                ('cart_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
    ]
