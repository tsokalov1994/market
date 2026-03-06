from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Products_Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num_order = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=32, default='cart')
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True)
    date_pay = models.DateField(auto_now_add=True, null=True)
    objects = models.Manager

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return f"{self.user} - {self.amount}"


class Product_OrderItem(models.Model):
    order = models.ForeignKey(Products_Order, on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, help_text="Change quantity", verbose_name="Product quantity in "
                                                                                                "order")
    price = models.DecimalField(max_digits=20, decimal_places=2)
    user_id = models.PositiveIntegerField(blank=True, null=True)

    objects = models.Manager

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.order} - {self.product}'