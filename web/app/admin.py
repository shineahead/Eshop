from __future__ import unicode_literals
from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(seller)
admin.site.register(goods)
admin.site.register(types)
admin.site.register(user_seller)
admin.site.register(address)
admin.site.register(user)

admin.site.register(Cart)
admin.site.register(post)
admin.site.register(post_reply)


