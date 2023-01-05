import string
from urllib import request
from django import forms
from django.utils import timezone
from captcha.fields import CaptchaField
from django.core.cache import cache
from web.settings import MEDIA_ROOT
from django.forms import Form, fields
from django.shortcuts import render, redirect, Http404, HttpResponse
from .models import *
from django.core.mail import send_mail
from django.conf import settings
import random, datetime, os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
import base64
# Create your views here.


def get(request):
    return render(request, 'get.html')


code_str = string.ascii_letters + string.digits


def gen_code(len=4):
    return ''.join(random.sample(code_str, len))


class RegisterForm1(Form):
    account = fields.CharField(max_length=16,
                                min_length=6,
                                required=True,
                                error_messages={
                                    'required': "用户名不能为空",
                                    'min_length': "太短了"
                                }
                                )
    password = fields.CharField(max_length=16, min_length=6, required=True, error_messages={
        "min_length": "密码过短，请重新输入",
        "max_length": "密码过长，请重新输入",
        "required": "请输入密码",
    })
    password2 = fields.CharField(max_length=16, min_length=6, required=True, error_messages={
        "min_length": "密码过短，请重新输入",
        "max_length": "密码过长，请重新输入",
        "required": "请输入密码",
    })
    email = fields.EmailField(error_messages={
        'required': "邮箱不能为空",
        'invalid': "邮箱格式不对",
    })
    phone = fields.CharField(max_length=16, min_length=6, required=True, error_messages={
        "min_length": "太短了，请重新输入",
        "max_length": "太长了，请重新输入",
        "required": '请输入联系方式',
    })
    user_name = fields.CharField(max_length=16, min_length=1, required=True, error_messages={
        "max_length": "太长了，请重新输入",
        "min_length": "太短了，请重新输入",
        "required": '请输入用户昵称',
    })



class RegisterForm2(Form):
    account = fields.CharField(max_length=16,
                                min_length=6,
                                required=True,
                                error_messages={
                                    'required': "用户名不能为空",
                                    'min_length': "太短了"
                                }
                                )
    password = fields.CharField(max_length=16, min_length=6, required=True, error_messages={
        "min_length": "密码过短，请重新输入",
        "max_length": "密码过长，请重新输入",
        "required": "请输入密码",
    })
    password2 = fields.CharField(max_length=16, min_length=6, required=True, error_messages={
        "min_length": "密码过短，请重新输入",
        "max_length": "密码过长，请重新输入",
        "required": "请输入密码",
    })
    email = fields.EmailField(error_messages={
        'required': "邮箱不能为空",
        'invalid': "邮箱格式不对",
    })
    store = fields.CharField(max_length=16, min_length=4, required=True, error_messages={
        'max_length': '店铺名过长',
        'min_length': '店铺名过短',
        'required': '请输入店铺名',
    })


def register1(request):
    m = request.method
    forbid = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=', '.']
    if m == 'GET':
        return render(request, 'reg1.html')
    else:
        obj = RegisterForm1(request.POST)
        rej = obj.is_valid()
        account = request.POST.get('account', '')
        pwd1 = request.POST.get('password', '')
        pwd2 = request.POST.get('password2', '')
        confirm_code = request.POST.get('email_code', '')
        phone = request.POST.get('phone', '')
        user_name = request.POST.get('user_name', '')
        email = request.POST.get('email', '')
        data = {'user_name': user_name, 'account': account, 'pwd1': pwd1, 'pwd2': pwd2, 'phone': phone, 'email': email}
        if rej:
            c = user_seller.objects.filter(account=account)
            e = user_seller.objects.filter(email=email)
            if c:
                data['error'] = '该用户名已被注册'
                return render(request, 'reg1.html', data)
            if e:
                data['error3'] = '该邮箱已被注册'
                return render(request, 'reg1.html', data)
            for i in account:
                if i in forbid:
                    data['error'] = '用户名含有非法字符'
                    return render(request, 'reg1.html', data)
            if pwd1 != pwd2:
                data['error2'] = '两次输入的密码不一致'
                return render(request, 'reg1.html', data)
            if confirm_code == '':
                code = random.choice([gen_code() for i in range(1000)])
                request.session['code'] = code
                msg = '帅哥发的验证码噢，请查收：' + code
                send_mail('邮箱验证', msg, settings.EMAIL_FROM, [email])
                return HttpResponse("<script>alert('验证码发送成功');window.history.back(-1);</script>")
            elif confirm_code != '':
                code = request.session.get('code')
                if code != confirm_code:
                    return HttpResponse("<script>alert('验证码输入错误');window.history.back(-1);</script>")
                else:
                    model1 = user_seller.objects.create(account=account, password=pwd1, email=email)
                    model2 = user(user_contact=phone, user_name=user_name, user_id_id=model1.user_seller_id)
                    model1.save()
                    model2.save()
                    return HttpResponse("<script>alert('注册成功！');window.location.href='/login/';</script>")
        else:
            data['obj'] = obj
            return render(request, 'reg1.html', data)


def register2(request):
    m = request.method
    forbid = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=', '.']
    if m == 'GET':
        return render(request, 'reg2.html')
    else:
        obj = RegisterForm2(request.POST)
        rej = obj.is_valid()
        account = request.POST.get('account', '')
        pwd1 = request.POST.get('password', '')
        pwd2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')
        confirm_code = request.POST.get("email_code", '')
        store = request.POST.get('store', '')
        data = {'store': store, 'account': account, 'pwd1': pwd1, 'pwd2': pwd2, 'email': email}
        if rej:
            c = user_seller.objects.filter(account=account)
            e = user_seller.objects.filter(email=email)
            s = seller.objects.filter(store_name=store)
            if c:
                data['error'] = '该用户名已被注册'
                return render(request, 'reg2.html', data)
            if e:
                data['error3'] = '该邮箱已被注册'
                return render(request, 'reg2.html', data)
            if s:
                data['error4'] = '该店铺名已被注册'
                return render(request, 'reg2.html', data)
            for i in account:
                if i in forbid:
                    data['error'] = '用户名含有非法字符'
                    return render(request, 'reg2.html', data)
            if pwd1 != pwd2:
                data['error2'] = '两次输入的密码不一致'
                return render(request, 'reg2.html', data)
            if confirm_code == '':
                code = random.choice([gen_code() for i in range(1000)])
                request.session['code'] = code
                msg = '帅哥发的验证码噢，请查收：' + code
                send_mail('邮箱验证', msg, settings.EMAIL_FROM, [email])
                return HttpResponse("<script>alert('验证码发送成功');window.history.back(-1);</script>")
            elif confirm_code != '':
                code = request.session.get('code')
                if code != confirm_code:
                    return HttpResponse("<script>alert('验证码输入错误');window.history.back(-1);</script>")
                else:
                    model1 = user_seller.objects.create(account=account, password=pwd1, email=email)
                    model2 = seller(store_name=store, seller_id_id=model1.user_seller_id)
                    model1.save()
                    model2.save()
                    return HttpResponse("<script>alert('注册成功！');window.location.href='/login/';</script>")
        else:
            data['obj'] = obj
            return render(request, 'reg2.html', data)


def index_view(request):
    #request.session.flush()
    tps = types.objects.all().order_by('type_id')  #商品分类
    num = goods.objects.all().count()
    a = random.randint(1, num)
    b = random.randint(1, num)
    while a == b:
        a = random.randint(1, num)
    try:
        good1 = goods.objects.get(pk=a)
        good2 = goods.objects.get(pk=b)
    except:
        good1 = goods.objects.get(pk=1)
        good2 = goods.objects.get(pk=2)
    data = {'tps': tps, 'good1': good1, 'good2': good2}
    if request.session.get("is_login"):
        user1 = user.objects.get(pk=request.session.get('u_id'))
        data['user_name'] = user1.user_name
        data['is_login'] = True
        data['id'] = request.session.get('u_id')
        return render(request, 'index.html', data)
    elif request.session.get('seller_login'):
        seller1 = seller.objects.get(seller_id_id=request.session.get('s_id'))
        data['store_name'] = seller1.store_name
        data['seller_login'] = True
        data['id'] = request.session.get('s_id')
        return render(request, 'index.html', data)
    else:
        return render(request, 'index.html', data)


class AddressForm(Form):
    receiver1 = fields.CharField(max_length=16, min_length=1, required=True, error_messages={
        'max_length': '收件人姓名过长，请重新输入',
        'min_length': '收件人姓名过短，请重新输入',
        'required': '收件人不能为空',
    })
    address1 = fields.CharField(max_length=16, min_length=2, required=True, error_messages={
        'max_length': '地址过长，请重新输入',
        'min_length': '地址过短，请重新输入',
        'required': '地址不能为空',
    })
    phone_number1 = fields.CharField(required=True, max_length=16, min_length=2, error_messages={
        'max_length': '电话过长，请重新输入',
        'min_length': '电话过短，请重新输入',
        'required': '电话不能为空',
    })
    post1 = fields.CharField(required=True, max_length=16, min_length=2, error_messages={
        'max_length': '邮编过长，请重新输入',
        'min_length': '邮编过短，请重新输入',
        'required': '邮编不能为空',
    })


def address_show(request):
    data = {}
    id = request.session.get('u_id')
    adress = address.objects.filter(fk_address_id=id)
    if adress.count() == 0:
        data['error_message'] = '当前无地址信息'
    else:
        data['adress'] = adress
    if request.method == 'GET':
        return render(request, 'address.html', data)
    elif request.method == 'POST':
        ad = AddressForm(request.POST)
        if ad.is_valid():
            receiver1 = request.POST.get('receiver1', '')
            address1 = request.POST.get('address1', '')
            post1 = request.POST.get('post1', '')
            phone_number1 = request.POST.get('phone_number1', '')
            is_default = request.POST.get('is_default1', '')
            defaults = address.objects.filter(fk_address_id=id).filter(is_default=1)
            num = defaults.count()     ##如果有默认地址，则把其改为非默认地址
            if num == 0:
                address_de = address.objects.create(receiver=receiver1, address=address1,
                post=post1, phone_number=phone_number1, fk_address_id=id, is_default=is_default)
            elif num == 1:
                defaults.update(is_default=0)
                address_de = address.objects.create(receiver=receiver1, address=address1, post=post1,
                phone_number=phone_number1, fk_address_id=id, is_default=is_default)
            adress = address.objects.filter(fk_address_id=id)
            data['adress'] = adress
            return render(request, 'address.html', data)
        else:
            data['ad'] = ad
            return render(request, 'address.html', data)



def address_change(request, address_id):
    id = request.session.get('u_id')
    the_address = address.objects.get(pk=address_id)
    data = {'adress': the_address}
    if request.method == 'GET':
        return render(request, 'address_change.html', data)
    elif request.method == 'POST':
        receiver1 = request.POST.get('receiver1', '')
        address1 = request.POST.get('address1', '')
        post1 = request.POST.get('post1', '')
        phone_number1 = request.POST.get('phone_number1', '')
        is_default1 = request.POST.get('is_default1', '')
        defaults = address.objects.filter(fk_address_id=id).filter(is_default=1)
        num = defaults.count()                   ##如果有默认地址，则把其改为非默认地址
        if num == 1 and is_default1 == 1:
            defaults.is_default = 0
            defaults.save()
            the_address.is_default = 1
            the_address.save()
        else:
            the_address.is_default = is_default1
            the_address.save()
        if receiver1:
            the_address.receiver = receiver1
            the_address.save()
        if address1:
            the_address.address = address1
            the_address.save()
        if post1:
            the_address.post = post1
            the_address.save()
        if phone_number1:
            the_address.phone_number = phone_number1
            the_address.save()
        the_address = address.objects.get(pk=address_id)
        data['adress'] = the_address
        return render(request, 'address_change.html', data)



def address_delete(request, address_id):
    the_address = address.objects.get(address_id=address_id)
    the_address.delete()
    data = {}
    user_id = request.session.get('u_id')
    adress = address.objects.filter(fk_address_id=user_id)
    if adress.count() == 0:
        data['error_message'] = '当前无地址信息'
    else:
        data['adress'] = adress
    return render(request, 'address.html', data)



def category(request, type_id):
    is_login = request.session.get('is_login')
    type1 = types.objects.get(pk=type_id)
    request.session['type_id'] = type_id
    data = {'type': type1, 'is_login': is_login, 'type_id': type_id}
    goods = types.objects.get(pk=type_id).goods_set.all()
    num = request.GET.get('num', 1)
    n = int(num)
    pager = Paginator(goods, 3)
    try:
        perpage_data = pager.page(n)
    except PageNotAnInteger:
        perpage_data = pager.page(1)
    except EmptyPage:
        perpage_data = pager.page(pager.num_pages)
    data['pager'] = pager
    data['perpage_data'] = perpage_data
    count = types.objects.get(pk=type_id).goods_set.all().count()
    if count == 0:
        data['error_message'] = '该分类无商品信息'
    else:
        data['goods'] = goods
    return  render(request, 'types.html', data)



class LoginForm(forms.Form):
    account = forms.CharField(max_length=16,
                                min_length=6,
                                required=True,
                                error_messages={
                                    'required': "用户名不能为空",
                                    'max_length': '用户名错误',
                                    'min_length': '用户名错误',
                                }
                                )
    password = forms.CharField(max_length=16, min_length=6, required=True,
                                error_messages={
                                    'required': '密码错误',
                                    'max_length': '密码错误',
                                    'min_length': '密码错误',
    })
    captcha = CaptchaField(error_messages={
        'invalid': '验证码错误'
    })


def login(request):
    m = request.method
    if m == 'GET':
        return render(request, 'login.html', locals())
    else:
        obj = LoginForm(request.POST)
        data = {'obj': obj}
        log = obj.is_valid()
        account = request.POST.get('account')
        try:
            user_seller.objects.get(account=account)
        except user_seller.DoesNotExist:
            data['error_message'] = '该账号不存在'
            data['user_verify'] = 1
            return render(request, 'login.html', data)
        if log:
            account = request.POST.get('account')
            password = request.POST.get('password')
            buyer = user_seller.objects.get(account=account, password=password)
            try:
                iid = buyer.user_seller_id
            except:
                iid = 0
            try:
                ssid = seller.objects.get(seller_id_id=iid)
                sid = ssid.seller_id_id
            except:
                sid = 0
            if iid and not sid:
                request.session['is_login'] = True
                request.session['u_id'] = buyer.user_seller_id
                return redirect("/index/")
            elif iid and sid:
                data = {'error_message': '此账号为卖家号，请换个登录口', 'obj': obj, 'user_verify': 1}
                return render(request, 'login.html', data)
            else:
                print(iid)
                print(sid)
                data = {'error_message': '密码错误', 'obj': obj, 'user_verify': 1}
                return render(request, 'login.html', data)
        print("5ds")
        data = {"obj": obj, 'user_verify': 1}
        return render(request, 'login.html', data)


def login1(request):
    m = request.method
    obj = LoginForm()
    if m == 'GET':
        return render(request, 'login.html', locals())
    else:
        obj = LoginForm(request.POST)
        data = {'obj': obj}
        log = obj.is_valid()
        account = request.POST.get('account')
        try:
            user_seller.objects.get(account=account)
        except user_seller.DoesNotExist:
            data['error_message'] = '该账号不存在'
            data['seller_verify'] = 1
            return render(request, 'login.html', data)
        if log:
            account = request.POST.get('account')
            password = request.POST.get('password')
            seller1 = user_seller.objects.get(account=account, password=password)
            try:
                sid = seller1.user_seller_id
            except:
                sid = 0
            try:
                iiid = user.objects.get(user_id_id=sid)
                iid = ssid.user_id_id
            except:
                iid = 0
            if sid and not iid:
                request.session['seller_login'] = True
                request.session['s_id'] = seller1.user_seller_id
                return redirect("/index/")
            elif iid and sid:
                data = {'error_message': '此账号为买家号，请换个登录口', 'obj': obj, 'seller_verify': 1}
                return render(request, 'login.html', data)
            else:
                data = {'error_message': '密码错误', 'obj': obj, 'seller_verify': 1}
                return render(request, 'login.html', data)
        data = {"obj": obj, 'seller_verify': 1}
        return render(request, 'login.html', data)


def user_info(request):
    if request.method == 'GET':
        if request.session.get("is_login"):
            uid = request.session.get("u_id")
            is_login = request.session.get("is_login")
            user1 = user.objects.get(user_id_id=uid)
            user2 = user_seller.objects.get(user_seller_id=uid)
            user_name = user1.user_name
            email = user2.email
            phone = user1.user_contact
            user_account = user2.account
            user_password = user2.password
            data = {"id": uid, "is_login": is_login, "user_name": user_name,
                    "user_email": email, "user_password": user_password, "user_phone": phone,
                    "user_account": user_account, 'user_avatar': user1.avatar, 'user_id_id': uid}
            return render(request, "user_info.html", data)
    elif request.method == 'POST':
        avatar = request.FILES.get("avatar", None)
        if avatar:
            img_list = avatar.name.split(".")
            user1 = user.objects.filter(pk=request.session.get('u_id'))
            if str(user1.first().avatar) != 'u_image/default.jpg':
                os.remove(MEDIA_ROOT + '/' + str(user1.first().avatar))
            item_img = "u_image/{}.{}".format(request.session.get("u_id"), img_list[1])
            i = 0
            while os.path.exists(MEDIA_ROOT + "/" + item_img):
                i +=1
                item_img = "u_image/{}({}).{}".format(request.session.get("u_id"), i, img_list[1])
            default_storage.save(MEDIA_ROOT + "/" + item_img, ContentFile(avatar.read()))
            user1.update(avatar=item_img)
            return HttpResponse("<script>alert('上传成功!');window.location.href='/user_info/';</script>")
        return HttpResponse("<script>alert('上传失败!');window.location.href='/user_info/';</script>")


def create_order(request, **dic):
    if request.method == 'GET':
        id = dic['goods_id']
        cart = dic['cart']
        if request.session.get('is_login'):
            the_cart = Cart.objects.get(pk=cart)
            goods_number = the_cart.goods_number
            uid = request.session.get('u_id')
            buyer = user.objects.get(pk=uid)
            state = buyer.state
            if not state:
                return HttpResponse("<script>alert('账号被冻结，无法购买商品');window.history.back(-1);</script>")
            the_address = address.objects.filter(fk_address=uid)
            the_good = goods.objects.get(pk=id)
            data = {'the_good': the_good, 'address': the_address, 'goods_number': goods_number, 'cart': cart}
            return render(request, 'create_order.html', data)
        else:
            return HttpResponse("<script>alert('仅有买家可以购买商品');window.history.back(-1);</script>")
    elif request.method == 'POST':
        cart = dic['cart']
        id = dic['goods_id']
        uid = request.session.get('u_id')
        buyer = user.objects.get(pk=uid)
        user_money = buyer.balance
        the_good = goods.objects.get(pk=id)
        the_seller = the_good.store_id
        good_stock = the_good.stock
        the_address_id = request.POST.get('the_address', '')
        goods_number = int(request.POST.get('goods_number'))
        if not goods_number:
            return HttpResponse("<script>alert('请选择商品的数量');window.history.back(-1);</script>")
        else:
            if goods_number > good_stock:
                return HttpResponse("<script>alert('该商品库存不足，请选择其他商品');window.history.back(-1);</script>")
            else:
                money = the_good.price * goods_number
                if user_money < money:
                    return HttpResponse("<script>alert('余额不足，请及时充值');window.history.back(-1);</script>")
                else:
                    user_money = user_money - money
                    buyer.balance = user_money
                    buyer.save()
                    good_stock = good_stock - goods_number
                    the_good.stock = good_stock
                    the_good.save()
                the_order = order.objects.create(goods_number=goods_number, money=money, address_id=the_address_id,
                                                 order_seller_id=the_seller, order_goods_id=id, order_user_id=uid)
                the_cart = Cart.objects.get(pk=cart)
                the_cart.status = 1
                the_cart.save()
                return HttpResponse("<script>alert('下单成功!');window.location.href='/user_info/';</script>")


def create_order2(request, goods_id):
    if request.method == 'GET':
        if request.session.get('is_login'):
            id = goods_id
            uid = request.session.get('u_id')
            buyer = user.objects.get(pk=uid)
            state = buyer.state
            if not state:
                return HttpResponse("<script>alert('账号被冻结，无法购买商品');window.history.back(-1);</script>")
            the_address = address.objects.filter(fk_address=uid)
            the_good = goods.objects.get(pk=id)
            data = {'the_good': the_good, 'address': the_address}
            return render(request, 'create_order2.html', data)
        else:
            return HttpResponse("<script>alert('仅有买家可以购买商品');window.history.back(-1);</script>")
    elif request.method == 'POST':
        id = goods_id
        uid = request.session.get('u_id')
        buyer = user.objects.get(pk=uid)
        user_money = buyer.balance
        the_good = goods.objects.get(pk=id)
        the_seller = the_good.store_id
        good_stock = the_good.stock
        the_address_id = request.POST.get('the_address', '')
        goods_number = int(request.POST.get('goods_number'))
        if not goods_number:
            return HttpResponse("<script>alert('请选择商品的数量');window.history.back(-1);</script>")
        else:
            if goods_number > good_stock:
                return HttpResponse("<script>alert('该商品库存不足，请选择其他商品');window.history.back(-1);</script>")
            else:
                money = the_good.price * goods_number
                if user_money < money:
                    return HttpResponse("<script>alert('余额不足，请及时充值');window.history.back(-1);</script>")
                else:
                    user_money = user_money - money
                    buyer.balance = user_money
                    buyer.save()
                    good_stock = good_stock - goods_number
                    the_good.stock = good_stock
                    the_good.save()
                the_order = order.objects.create(goods_number=goods_number, money=money, address_id=the_address_id,
                 order_seller_id=the_seller, order_goods_id=id, order_user_id=uid)
                return HttpResponse("<script>alert('下单成功!');window.location.href='/user_info/';</script>")


def order_show(request):
    uid = request.session.get('u_id')
    user1 = user.objects.get(pk=uid)
    print(user1)
    try:
        order_form = user1.ouser.all()
    except:
        order_form = ''
    if not order_form:
        return HttpResponse("<script>alert('目前您暂无订单');window.history.back(-1);</script>")
    else:
        data = {'order_form': order_form}
        return render(request, 'order_show.html', data)


def order_pre(request):
    uid = request.session.get('u_id')
    user1 = user.objects.get(pk=uid)
    try:
        order_form = user1.ouser.all()
        order_form = order_form.filter(state=1 or 2)
        count = order_form.count()
    except:
        order_form = ''
        count = 0
    data = {'order_form': order_form, 'count': count}
    return render(request, 'order_pre.html', data)


def order_manage(request):
    sid = request.session.get('s_id')
    the_seller = seller.objects.get(pk=sid)
    try:
        order_form = the_seller.seller.all()   ##通过related_name来查询的外键
    except:
        order_form = ''
    data = {'order_form': order_form}
    return render(request, 'order_manage.html', data)



def order_operate(request, order_id):
    if request.method == 'GET':
        the_order = order.objects.get(pk=order_id)
        a = the_order.order_goods.goods_name
        print(a)
        data = {'the_order': the_order, 'order_id': order_id}
        return render(request, 'order_operate.html', data)
    elif request.method == 'POST':
        state = request.POST.get('state', '')
        the_order = order.objects.get(pk=order_id)
        the_order.state = state
        the_order.save()
        return HttpResponse("<script>alert('确认成功，请尽快发货！');window.location.href='/order_manage/';</script>")


def order_detail(request, order_id):
    id = order_id
    the_order = order.objects.get(pk=id)
    the_good = goods.objects.get(pk=the_order.order_goods_id)
    the_store = seller.objects.get(pk=the_order.order_seller_id)
    data = {'the_good': the_good, 'the_store': the_store, 'the_order': the_order}
    return render(request, 'order_detail.html', data)


def search_goods(request):
    data = {}
    if request.method == 'GET':
        return render(request, 'search_goods.html', )
    elif request.method == 'POST':
        name = request.POST.get('the_name', '')
        store = request.POST.get('the_store', '')
        if not name and not store:
            return HttpResponse("<script>alert('请输入查询信息');window.history.back(-1);</script>")
        if name != '':
            the_goods = goods.objects.filter(goods_name__contains=name)
        else:
            the_goods = ''
        try:
            the_store = seller.objects.get(store_name=store)
        except:
            the_store = 0
        if not the_goods and not the_store:
            return HttpResponse("<script>alert('未查询到商品信息');window.history.back(-1);</script>")
        if the_store and name:
            return HttpResponse("<script>alert('请勿同时输入商品和店铺信息');window.history.back(-1);</script>")
        try:
            the_goods2 = the_store.goods_set.all()
        except:
            the_goods2 = ''
        if the_goods and not the_goods2:
            number = the_goods.count()
            num = request.GET.get('num', 1)
            n = int(num)
            pager = Paginator(the_goods, 3)
            try:
                perpage_data = pager.page(n)
            except PageNotAnInteger:
                perpage_data = pager.page(1)
            except EmptyPage:
                perpage_data = pager.page(pager.num_pages)
            data['pager'] = pager
            data['perpage_data'] = perpage_data
            data['number'] = number
            return render(request, 'search_goods.html', data)
        elif the_goods2 and not the_goods:
            number = the_goods2.count()
            num = request.GET.get('num', 1)
            n = int(num)
            pager = Paginator(the_goods2, 3)
            try:
                perpage_data = pager.page(n)
            except PageNotAnInteger:
                perpage_data = pager.page(1)
            except EmptyPage:
                perpage_data = pager.page(pager.num_pages)
            data['pager'] = pager
            data['perpage_data'] = perpage_data
            data['number'] = number
            return render(request, 'search_goods.html', data)
        elif not the_goods2 and not the_goods:
            return HttpResponse("<script>alert('请输入查询信息');window.history.back(-1);</script>")
        else:
            return HttpResponse("<script>alert('请勿同时输入商品和店铺信息');window.history.back(-1);</script>")



def goods_info(request, goods_id):
    id = goods_id
    is_login = request.session.get('is_login')
    try:
        the_good = goods.objects.get(pk=id, state=1)
    except:
        the_good = ''
    if not the_good:
        return HttpResponse("<script>alert('该商品不存在或已下架！');window.location.href='/index/';</script>")
    posts =post.objects.filter(post_goods_id=id)
    user1 = user.objects.filter(pk=request.session.get('u_id')).first()
    category = goods.objects.get(goods_id=goods_id).category.sort
    data = {'the_good': the_good, 'posts': posts, 'user': user1, 'is_login': is_login,
            'type_id': request.session.get('type_id', ''), 'category': category}
    return render(request, 'goods_info.html', data)



def add_cart(request, goods_id):
    if request.method == 'GET':
        the_good = goods.objects.get(pk=goods_id)
        store_name = the_good.store.store_name
        return render(request, 'add_cart.html', {'the_good': the_good, 'store_name': store_name})
    elif request.method == 'POST':
        id = goods_id
        uid = request.session.get('u_id')
        the_good = goods.objects.get(pk=id)
        store_name = the_good.store.store_name
        price = the_good.price
        img = the_good.item_img
        goods_number = request.POST.get('goods_number')
        if not goods_number:
            return HttpResponse("<script>alert('请输入商品数量');window.history.back(-1);</script>")
        else:
            cart = Cart.objects.create(seller_name=store_name, price=price, cart_user_id=uid, goods_id=id,
                                       goods_number=goods_number, goods_name=the_good.goods_name, img=img)
            return HttpResponse("<script>alert('添加成功');window.location.href='/index/';</script>")



def cart(request, user_id_id):
    id = user_id_id
    data = {}
    form = Cart.objects.filter(cart_user_id=id)
    num = request.GET.get('num', 1)
    n = int(num)
    pager = Paginator(form, 3)
    try:
        perpage_data = pager.page(n)
    except PageNotAnInteger:
        perpage_data = pager.page(1)
    except EmptyPage:
        perpage_data = pager.page(pager.num_pages)
    data['pager'] = pager
    data['perpage_data'] = perpage_data
    data['user_id_id'] = user_id_id
    return render(request, 'cart.html', data)


def delete_cart(request, cart):
    the_cart = Cart.objects.get(cart=cart).delete()
    if the_cart:
        return HttpResponse("<script>alert('删除成功');window.location.href='/cart/';</script>")
    else:
        return HttpResponse("<script>alert('删除失败');window.location.href='/cart/';</script>")


def seller_change(request):
    if request.method == 'GET':
        id = request.session.get('s_id')
        the_seller = seller.objects.get(pk=id)
        data = {'the_seller': the_seller}
        return render(request, 'seller_change.html', data)
    elif request.method == 'POST':
        word = 0
        sid = request.session.get('s_id')
        seller1 = user_seller.objects.get(pk=sid)
        seller2 = seller.objects.get(pk=sid)
        account = request.POST.get('account', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')
        store_name = request.POST.get('store_name', '')
        detail = request.POST.get('detail', '')
        if account:
            seller1.account = account
            seller1.save()
            word = 1
        if password:
            seller1.password = password
            seller1.save()
            word = 1
        if email:
            seller1.email = email
            seller1.save()
            word = 1
        if store_name:
            seller2.store_name = store_name
            seller2.save()
            word = 1
        if detail:
            seller2.detail = detail
            seller2.save()
            word = 1
        if word:
            return HttpResponse("<script>alert('修改成功!');window.location.href='/seller_change/';</script>")
        else:
            return HttpResponse("<script>alert('请输入修改内容！！');window.history.back(-1);</script>")


def seller_info(request):
    if request.method == 'GET':
        if request.session.get('seller_login'):
            data = {'seller_login': request.session.get('seller_login')}
            sid = request.session.get('s_id')
            the_goods = goods.objects.filter(store_id=sid)
            data['the_goods'] = the_goods
            seller1 = seller.objects.get(pk=request.session.get('s_id'))
            store_name = seller1.store_name
            avatar = seller1.avatar
            try:
                goods_number = goods.objects.filter(store_id=sid).count()
            except:
                goods_number = 0
            try:
                detail = seller1.detail
            except:
                detail = '此商家很懒，没有简介'
            seller1.goods_number = goods_number
            seller1.save()
            num = request.GET.get('num', 1)
            n = int(num)
            pager = Paginator(the_goods, 3)
            try:
                perpage_data = pager.page(n)
            except PageNotAnInteger:
                perpage_data = pager.page(1)
            except EmptyPage:
                perpage_data = pager.page(pager.num_pages)
            data['pager'] = pager
            data['perpage_data'] = perpage_data
            data['store_name'] = store_name
            data['detail'] = detail
            data['goods_number'] = goods_number
            data['avatar'] = avatar
            return render(request, 'seller_info.html', data)
    elif request.method == 'POST':
        avatar = request.FILES.get("avatar", None)
        if avatar:
            img_list = avatar.name.split(".")
            seller1 = seller.objects.filter(pk=request.session.get('s_id'))
            if str(seller1.first().avatar) != 's_image/default.jpg':
                os.remove(MEDIA_ROOT + '/' + str(seller1.first().avatar))
            item_img = "s_image/{}.{}".format(request.session.get("s_id"), img_list[1])
            i = 1
            while os.path.exists(MEDIA_ROOT + "/" + item_img):
                i += 1
                item_img = "s_image/{}({}).{}".format(request.session.get("s_id"), i, img_list[1])
            default_storage.save(MEDIA_ROOT + "/" + item_img, ContentFile(avatar.read()))
            seller1.update(avatar=item_img)
            return HttpResponse("<script>alert('上传成功!');window.location.href='/seller_info/';</script>")
        else:
            return HttpResponse("<script>alert('上传失败!');window.location.href='/seller_info/';</script>")


def put_goods(request):
    if request.method == 'GET':
        return render(request, 'put_goods.html')
    elif request.method == 'POST':
        #if request.POST.get('goods_id') == 0:
        goods_name = request.POST.get('goods_name', '')
        goods_introduction = request.POST.get('item_introduction', '')
        price = request.POST.get('price', '')
        stock = request.POST.get('stock', '')
        state = request.POST.get('state', '')
        category_id = request.POST.get('category', '')
        item_img1 = request.FILES.get("item_img", None)
        if not goods_name:
            return HttpResponse("<script>alert('请输入商品名称');window.history.back(-1)</script>")
        if not goods_introduction:
            return HttpResponse("<script>alert('请输入商品简介');window.history.back(-1)</script>")
        if not price:
            return HttpResponse("<script>alert('请输入商品价格');window.history.back(-1)</script>")
        if not item_img1:
            return HttpResponse("<script>alert('请上传图片');window.history.back(-1)</script>")
        if not stock:
            return HttpResponse("<script>alert('请输入商品库存');window.history.back(-1)</script>")
        if not state:
            return HttpResponse("<script>alert('请选择商品状态');window.history.back(-1)</script>")
        if not category_id:
            return HttpResponse("<script>alert('请选择商品分类');window.history.back(-1)</script>")
        img_list = item_img1.name.split(".")
        item_img = "item_img/{}.{}".format(request.session.get("s_id"), img_list[1])
        i = 0
        print(MEDIA_ROOT + "/" + item_img)
        while os.path.exists(MEDIA_ROOT + "/" + item_img):
            i += 1
            item_img = "item_img/{}({}).{}".format(request.session.get("id"), i, img_list[1])
        default_storage.save(MEDIA_ROOT + "/" + item_img, ContentFile(item_img1.read()))
        goods.objects.create(goods_name=goods_name, goods_introduction=goods_introduction,
                             store_id=request.session.get("s_id"), price=price, item_img=item_img1,
                             stock=stock, category_id=category_id, state=state)
        return HttpResponse("<script>alert('发布商品成功！');window.location.href='/index/'</script>")


def goods_change(request, goods_id):
    id = goods_id
    word = 0
    the_good = goods.objects.get(pk=id)
    data = {'the_good': the_good}
    if request.method == 'GET':
        return render(request, 'goods_change.html', data)
    elif request.method == 'POST':
        goods_name = request.POST.get('goods_name')
        goods_introduction = request.POST.get('goods_introduction')
        stock = request.POST.get('stock')
        price = request.POST.get('price')
        state = request.POST.get('state')
        the_item_img = request.FILES.get('item_img')
        if goods_name:
            the_good.goods_name = goods_name
            the_good.save()
            word = 1
        if stock:
            the_good.stock = stock
            the_good.save()
            word = 1
        if price:
            the_good.price = price
            the_good.save()
            word = 1
        if goods_introduction:
            the_good.goods_introduction = goods_introduction
            the_good.save()
            word = 1
        if state:
            the_good.state = state
            the_good.save()
            word = 1
        if the_item_img:
            img_list = the_item_img.name.split(".")
            the_good = goods.objects.filter(pk=id)
            if str(the_good.first().item_img) != 'item_img/default.jpg':
                os.remove(MEDIA_ROOT + '/' + str(the_good.first().item_img))
            item_img = "item_img/{}.{}".format(id, img_list[1])
            i = 0
            while os.path.exists(MEDIA_ROOT + "/" + item_img):
                i += 1
                item_img = "item_img/{}({}).{}".format(id, i, img_list[1])
            default_storage.save(MEDIA_ROOT + "/" + item_img, ContentFile(the_item_img.read()))
            the_good.update(item_img=item_img)
            return HttpResponse("<script>alert('上传成功!');window.location.href='/seller_info/';</script>")
        elif word == 1:
            return HttpResponse("<script>alert('修改成功');window.history.back(-1);</script>")
        else:
            return HttpResponse("<script>alert('请输入修改信息');window.history.back(-1);</script>")



def goods_delete(request, goods_id):
    id = goods_id
    the_goods = goods.objects.get(pk=id).delete()
    if the_goods:
        return HttpResponse("<script>alert('>删除成功!');window.location.href='/seller_info/';</script")
    else:
        return HttpResponse("<script>alert('删除失败!');window.location.href='/seller_info/';</script>")


def logout(request):
    if (request.session.get("is_login")) or (request.session.get('seller_login')):
        request.session.flush()
        return HttpResponse("<script>alert('登出成功!');window.location.href='/index/';</script>")
    else:
        return HttpResponse("<script>alert('请先登录!');window.location.href='/login/';</script>")


def change(request):
    if request.session.get("is_login"):
        user1 = user.objects.get(pk=request.session.get("u_id"))
        user2 = user_seller.objects.get(pk=request.session.get("u_id"))
        if request.method == 'GET':
            return render(request, 'change.html')
        elif request.method == "POST":
            obj = RegisterForm1(request.POST)
            rej = obj.is_valid()
            account = request.POST.get('account', '')
            pwd1 = request.POST.get('password', '')
            pwd2 = request.POST.get('password2', '')
            phone = request.POST.get('phone', '')
            user_name = request.POST.get('user_name', '')
            email = request.POST.get('email', '')
            if user_seller.objects.filter(account=account).count() == 1:
                return HttpResponse("<script>alert('该账号已被占用！');window.history.back(-1);</script>")
            elif user_seller.objects.filter(email=email).count() == 1:
                return HttpResponse("<script>alert('该邮箱已被注册！');window.history.back(-1);</script>")
            else:
                if pwd1 != pwd2:
                    return HttpResponse("<script>alert('两次输入密码不同请检查');window.history.back(-1);</script>")
                elif rej:
                    user1.user_name = user_name
                    user2.password = pwd1
                    user2.email = email
                    user2.account = account
                    user1.user_contact = phone
                    user1.save()
                    user2.save()
                    return HttpResponse("<script>alert('修改成功！！');window.history.back(-1);</script>")
                else:
                    form = {"obj": obj}
                    return render(request, "change.html", form)
        form = {
            "user_name": user1.user_name,
            "user_password": user2.password,
            "user_email": user2.email,
            "user_phone": user1.user_contact,
            "user_account": user2.account
        }
        return render(request, "change.html", form)
    else:
        return HttpResponse("<script>alert('请先登录!');window.location.href='/login/';</script>")


def goods_post(request, goods_id):
    form = goods.objects.get(goods_id=goods_id).post_set.all()
    data = {"form": form, 'goods_id': goods_id}
    request.session['goods_id'] = goods_id
    if request.session.get("is_login"):
        user1 = user.objects.get(user_id_id=request.session.get("u_id"))
        goods_name = goods.objects.get(pk=goods_id).goods_name
        data["is_login"] = request.session.get("is_login")
        data["user_name"] = user1.user_name
        data["post_id"] = request.session.get("u_id")
        data["goods_name"] = goods_name
    return render(request, "goods_post.html", data)


def goods_post_detail(request, post_id):
    if request.method == "GET":
        goods_id = request.session.get('goods_id')
        form = post.objects.get(post_id=post_id)
        reply = post_reply.objects.filter(post_id=post_id)
        data = {"form": form, "reply_form": reply, 'post_id': post_id, 'seller_login': request.session.get('seller_login'),
                'is_login': request.session.get('is_login'), 'goods_id': goods_id}
        return render(request, "goods_post_detail.html", data)


def create_posts(request, goods_id):
    if request.method == "POST" and request.session.get("is_login"):
        post_time = datetime.datetime.now()
        user1 = user.objects.get(user_id_id=request.session.get("u_id"))
        user_name = user1.user_name
        the_good = goods.objects.get(pk=goods_id)
        goods_name = the_good.goods_name
        post_context = request.POST.get("post_context")
        if len(post_context) == 0:
            return HttpResponse("<script>alert('请输入内容！');window.history.back(-1);</script>")
        post1 = post.objects.create(post_context=post_context, user_name=user_name, goods_name=goods_name,
        post_user_id=request.session.get('u_id'), post_time=post_time, post_goods_id=goods_id)
        post1.save()
        return HttpResponse("<script>alert('评论成功');window.history.back(-1);</script>")
    else:
        return HttpResponse("<script>alert('仅有买家可以进行再评论');window.location.href='/login/';</script>")


def reply_post(request, post_id):
    if request.method == "POST" and request.session.get("seller_login"):
        reply_time = datetime.datetime.now()
        seller1 = seller.objects.get(seller_id_id=request.session.get("s_id"))
        store_name = seller1.store_name
        reply_context = request.POST.get("reply_context")
        if len(reply_context) == 0:
            return HttpResponse("<script>alert('请输入内容！');window.history.back(-1);</script>")
        reply = post_reply.objects.create(reply_context=reply_context, seller_name=store_name, reply_time=reply_time, post_id=post_id)
        reply.save()
        return HttpResponse("<script>alert('回复成功');window.history.back(-1);</script>")
    else:
        return HttpResponse("<script>alert('仅商家可以进行回复!');window.location.href='/login/';</script>")


def balance(request):
    id = request.session.get('u_id')
    user1 = user.objects.get(user_id_id=id)
    user_balance = float(user1.balance)
    data = {'user_balance': user_balance}
    if request.method == 'GET':
        return render(request, 'balance.html', data)
    else:
        b = (request.POST.get('balance_add'))
        print(b)
        if ('&' or '=' or '!' or '@' or '#' or '$' or '%' or '^' or '(' or ')' or '=' or '+' or '-' or ',' or '.' or '?' or ';') in b:
            data['error_message'] = '输入的金额不合规范,请重新输入'
            return render(request, 'balance.html', data)
        else:
            try:
                balance_add = float(request.POST.get('balance_add'))
            except:
                balance_add = 0
            if balance_add <= 0:
                data['error_message'] = '充值的金额必须大于零'
                return render(request, 'balance.html', data)
            elif 0.1 > balance_add > 0:
                data['error_message'] = '充值的金额太少了'
                return render(request, 'balance.html', data)
            else:
                user_balance = user_balance + balance_add
                a = user.objects.get(user_id_id=id)
                a.balance = user_balance
                a.save()
                return HttpResponse("<script>alert('充值成功！');window.location.href='/balance/';</script>")


def find_pwd(request):
    global get_email, code
    if request.session.get('is_login'):
        if request.method == 'GET':
            return render(request, 'find_pwd.html', {'is_login': True})
        elif request.method == 'POST':
            if request.is_ajax():
                get_email = request.POST.get('email')
                id = request.session.get('u_id')
                user1 = user_seller.objects.get(pk=id)
                email_verify = user1.email
                if get_email == email_verify:
                    code = random.choice([gen_code() for i in range(1000)])
                    msg = '验证码：' + code
                    send_mail('邮箱验证', msg, settings.EMAIL_FROM, [get_email])
                    print(65656)
                    return HttpResponse('发送成功')
                else:
                    return HttpResponse('该邮箱与用户不匹配！')
            else:
                email_code = request.POST.get('email_code')
                if len(email_code) == 0:
                    return HttpResponse("<script>alert('请输入验证码');window.history.back(-1);</script>")
                elif code == email_code:
                    if request.session.get('is_login'):
                        id = request.session.get('u_id')
                        user1 = user_seller.objects.get(pk=id)
                        user_password = user1.password
                        data = {"verify": 1, 'user_password': user_password, 'user_login': True}
                        return  render(request, 'find_pwd.html', data)
                else:
                    return HttpResponse("<script>alert('请输入正确的验证码！');window.history.back(-1);</script>")
    elif request.session.get('seller_login'):
        if request.method == 'GET':
            return render(request, 'find_pwd.html', {'seller_login': True})
        elif request.method == 'POST':
            if request.is_ajax():
                get_email = request.POST.get('email')
                id = request.session.get('s_id')
                seller1 = user_seller.objects.get(pk=id)
                email_verify = seller1.email
                if get_email == email_verify:
                    code = random.choice([gen_code() for i in range(1000)])
                    msg = '验证码：' + code
                    send_mail('邮箱验证', msg, settings.EMAIL_FROM, [get_email])
                    print(65656)
                    return HttpResponse('发送成功')
                else:
                    return HttpResponse('该邮箱与用户不匹配！')
            else:
                email_code = request.POST.get('email_code')
                if len(email_code) == 0:
                    return HttpResponse("<script>alert('请输入验证码');window.history.back(-1);</script>")
                elif code == email_code:
                    if request.session.get('seller_login'):
                        id = request.session.get('s_id')
                        seller1 = user_seller.objects.get(pk=id)
                        seller_password = seller1.password
                        data = {"verify": 1, 'user_password': seller_password, 'seller_login': True}
                        return  render(request, 'find_pwd.html', data)
                else:
                    return HttpResponse("<script>alert('请输入正确的验证码！');window.history.back(-1);</script>")




