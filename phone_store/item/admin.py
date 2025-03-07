from django.contrib import admin

from .models import Category, item, Cart, CartItem

admin.site.register(Category)
admin.site.register(item)
admin.site.register(Cart)
admin.site.register(CartItem)