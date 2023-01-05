# coding = utf-8
from django.urls import path
from django.conf.urls.static import static
from . import views
from web import settings


urlpatterns = [
    path('', views.get, name='get'),
    path('index/', views.index_view, name='index'),
    path('login/', views.login, name='login'),
    path('login1/', views.login1, name='login1'),
    path('register1/', views.register1, name='register1'),
    path('register2/', views.register2, name='register2'),
    path('reply_post/<int:post_id>/', views.reply_post, name="reply_post"),
    path('user_info/', views.user_info, name='user_info'),
    path('seller_info/', views.seller_info, name='seller_info'),
    path('logout/', views.logout, name='logout'),
    path('change/', views.change, name='change'),
    path('goods_change/<int:goods_id>/', views.goods_change, name='goods_change'),
    path('goods_delete/<int:goods_id>/', views.goods_delete, name='goods_delete'),
    path('seller_change/', views.seller_change, name='seller_change'),
    path('find_pwd/', views.find_pwd, name='find_pwd'),
    path('balance/', views.balance, name='balance'),
    path('order_show/', views.order_show, name='order_show'),
    path('order_manage/', views.order_manage, name='order_manage'),
    path('order_operate/<int:order_id>/', views.order_operate, name='order_operate'),
    path('order_pre/', views.order_pre, name='order_pre'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('search_goods/', views.search_goods, name='search_goods'),
    path('create_order/<int:goods_id>/<int:cart>/', views.create_order, name='create_order'),
    path('create_order2/<int:goods_id>/', views.create_order2, name='create_order2'),
    path('put_goods/', views.put_goods, name='put_goods'),
    path('goods_info/<int:goods_id>/', views.goods_info, name='goods_info'),
    path('add_cart/<int:goods_id>/', views.add_cart, name='add_cart'),
    path('delete_cart/<int:cart>/', views.delete_cart, name='delete_cart'),
    path('cart/<int:user_id_id>/', views.cart, name='cart'),
    path('address_show/', views.address_show, name='address_show'),
    path('address_change/<int:address_id>/', views.address_change, name='address_change'),
    path('address_delete/<int:address_id>/', views.address_delete, name='address_delete'),
    path('create_posts/<int:goods_id>/', views.create_posts, name='create_posts'),
    path('goods_post/<int:goods_id>/', views.goods_post, name='goods_post'),
    path('goods_post_detail/<int:post_id>/', views.goods_post_detail, name='goods_post_detail'),
    path('category/<int:type_id>/', views.category, name='category'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

