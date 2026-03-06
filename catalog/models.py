from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from webshop.models import Products_Order, Product_OrderItem
import os
from uuid import uuid4


def rename_prod(instance, filename):
    upload_to = 'products'
    ext = filename.split('.')[-1]
    n_rec = len(Product.objects.all())
    if n_rec == 0:
        max_rec = 0
    else:
        max_rec = Product.objects.all().last().id

    max_id = max_rec + 1
    photo = 'img_' + str(max_id)
    if instance.pk:
        filename = '{}{}.{}'.format('img_', instance.pk, ext)
    elif photo:
        filename = '{}.{}'.format(photo, ext)
    else:
        filename = '{}{}.{}'.format('img_', uuid4().hex, ext)

    return os.path.join(upload_to, filename)
class Genre_m(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Product(models.Model):
    genre = models.ForeignKey(Genre_m, on_delete=models.CASCADE,
                              blank=True, null=True,
                              verbose_name="Product category")
    name = models.CharField(max_length=150,
                            verbose_name="Product name")
    description = models.TextField(blank=True, verbose_name="Product description")

    price = models.DecimalField(max_digits=10,decimal_places=2, verbose_name="Price")

    image = models.ImageField(upload_to=rename_prod, blank=True, verbose_name="Product photo")

    ostat = models.SmallIntegerField(default=0, help_text="Change quantity",
                                     verbose_name="On storage")

    objects = models.Manager

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)
