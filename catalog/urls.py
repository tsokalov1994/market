from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path('', views.redirect_to_catalog, name='home'),
    path('catalog/', views.show_products, name="show_products"),
    path('catalog_tree/', views.catalog_tree, name='catalog_tree'),
    path('product_tree/<int:id>/', views.product_tree, name='product_tree'),
    path('cart_edit/', views.cart_edit, name='cart_edit'),
    path('my_order/', views.my_order, name='my_order'),
    path('my_buy/', views.my_buy, name='my_buy'),
    path('cart/<int:id>/', views.cart, name='cart'),
    path('product_detail/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('order-del/<int:id>/<int:id_zak>/', views.order_del, name='order_del'),
    path('update-quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('create-order/', views.create_order, name='create_order'),
]