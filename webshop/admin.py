from django.contrib import admin
from .models import Products_Order, Product_OrderItem

# Register your models here.
admin.site.register(Products_Order)
admin.site.register(Product_OrderItem)