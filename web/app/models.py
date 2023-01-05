from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.



class types(models.Model):
    type_id = models.AutoField(primary_key=True)
    sort = models.CharField(u'商品种类', max_length=16, blank=False, )


class user_seller(models.Model):
    user_seller_id = models.AutoField(primary_key=True)
    account = models.CharField(u'账号', max_length=20, unique=True)
    password = models.CharField(u'密码', max_length=32)
    email = models.EmailField(u'邮箱', max_length=32)


class seller(models.Model):
    seller_id = models.OneToOneField(user_seller, primary_key=True, on_delete=models.CASCADE)
    store_name = models.CharField(u'店铺名', max_length=50, unique=True)
    avatar = models.ImageField('店铺头像', upload_to='u_images/', default='s_image/default.jpg')
    detail = models.CharField(u'店铺简介', max_length=50, default='此商家很懒，没有简介')
    goods_number = models.IntegerField(u'商品数量', default=0)


class user(models.Model):
    user_id = models.OneToOneField(user_seller, primary_key=True, on_delete=models.CASCADE)
    user_name = models.CharField(u'用户昵称', max_length=16, default=250)
    user_contact = models.CharField(u'联系方式', max_length=16)
    avatar = models.ImageField(u'头像',  upload_to='u_images/', default='u_image/default.jpg')
    state = models.IntegerField(u'状态', default=1)  #0是被冻结，1是正常状态
    balance = models.DecimalField(u'用户余额', max_digits=8, decimal_places=3, default=0)


class Cart(models.Model):
    cart = models.AutoField(primary_key=True)
    goods_name = models.CharField(max_length=50, verbose_name='商品名称', default='')
    seller_name = models.CharField(max_length=25, verbose_name="店铺名称")
    goods_number = models.IntegerField(default=0, verbose_name="数量")
    img = models.ImageField(u'商品图片', default='')
    goods_id = models.IntegerField(u'商品ID', default=0)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0.0, null=True, blank=True,
                                    verbose_name="单价")
    status = models.IntegerField(default=0, verbose_name="状态")  # 0是未下单，1是已下单
    cart_user = models.ForeignKey(user, on_delete=models.CASCADE, null=True)



class goods(models.Model):
    goods_id = models.AutoField(primary_key=True)
    goods_name = models.CharField(u'商品名', max_length=50)
    item_img = models.ImageField(u'图片',  upload_to='g_images/', default='item_images/default.jpg')
    goods_introduction = RichTextUploadingField(u'简介', max_length=50, default='商品简介ya')
    price = models.DecimalField(u'售价', max_digits=8, decimal_places=3)
    stock = models.IntegerField(u'库存', default=0)
    state = models.IntegerField(u'商品状态', default=0)  #0是未上架，1是已上架
    category = models.ForeignKey(types, on_delete=models.CASCADE, default='')
    store = models.ForeignKey(seller, on_delete=models.CASCADE, )
    user = models.ForeignKey(user, on_delete=models.CASCADE, null=True, blank=True, related_name='user')


class post(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_context = models.TextField(u'评论内容', max_length=500)
    user_name = models.CharField(u'评论人', max_length=10)
    post_time = models.DateTimeField(u'发布时间')
    goods_name = models.CharField(u'评论商品名称', max_length=50)
    post_goods = models.ForeignKey(goods, on_delete=models.CASCADE)
    post_user = models.ForeignKey(user, on_delete=models.CASCADE)


class post_reply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    reply_context = models.TextField(u'回复内容', max_length=200)
    reply_time = models.DateTimeField("回复时间")
    seller_name = models.CharField(u'回复商家',  max_length=16)
    post = models.ForeignKey(goods, on_delete=models.CASCADE)


class goods_detail(models.Model):
    goods_detail_id = models.OneToOneField(goods, primary_key=True, on_delete=models.CASCADE)
    photo = models.ImageField(u'图片', upload_to='')
    detail = RichTextUploadingField(null=True, blank=True)


class address(models.Model):
    address_id = models.AutoField(primary_key=True)
    receiver = models.CharField(u'收件人', max_length=20, blank=False)
    address = models.CharField(u'地址', max_length=50, blank=False)
    post = models.CharField(u'邮编', blank=False, max_length=32)
    is_default = models.IntegerField(u'是否默认', default=0)   #1为默认， 0为非默认
    phone_number = models.CharField(u'电话',  blank=False, max_length=32)
    fk_address = models.ForeignKey(user, on_delete=models.CASCADE)


class order(models.Model):
    order_id = models.AutoField(primary_key=True)
    address = models.OneToOneField(address, on_delete=models.CASCADE, default='')
    goods_number = models.PositiveBigIntegerField('商品数量', blank=False, default=1)
    money = models.DecimalField('订单总金额', max_digits=8, decimal_places=3)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    state = models.IntegerField('订单状态', default=0)            #0是下单未处理，1是接受订单，2是拒绝订单
    order_user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='ouser')
    order_seller = models.ForeignKey(seller, on_delete=models.CASCADE, related_name='seller')
    order_goods = models.ForeignKey(goods, on_delete=models.CASCADE, related_name='goods')



