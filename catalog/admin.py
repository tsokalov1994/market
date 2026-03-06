from django.contrib import admin
from .models import Genre_m, Product
from django_mptt_admin.admin import DjangoMpttAdmin

# Register your models here.
class CategoryAdmin(DjangoMpttAdmin):
    name = {"slug": ("name",)}

admin.site.register(Genre_m, CategoryAdmin)
admin.site.register(Product)
