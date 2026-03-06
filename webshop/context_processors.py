from django.apps import apps
from django.contrib.auth.models import User
from django.db.models import Sum


# Create your views here.
def genre_m(request):
    genre = apps.get_model("catalog", "Genre_m")
    return {'genre_m': genre.objects.all()}

def num_products_m(request):
    product_model = apps.get_model("catalog", "Product")
    num_products_m = product_model.objects.all().count()
    return {'num_products_m': num_products_m}

def cart_kol_m(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        my_order = apps.get_model('webshop', 'Products_Order')
        my_order_item = apps.get_model('webshop', "Product_OrderItem")

        try:
            order = my_order.objects.get(user_id=user_id, status='cart')
            id_cart_m = order.id
            order_item = my_order_item.objects.filter(order_id=order.id)
            cart_kol_m = len(order_item)
        except my_order.DoesNotExist:
            cart_kol_m = 0
            id_cart_m = None
    else:
        cart_kol_m = 0
        id_cart_m = None
    return {'cart_kol_m': cart_kol_m, 'id_cart_m': id_cart_m}

def cart_sum_zak_m(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        my_order = apps.get_model('webshop', "Products_Order")

        try:

            order = my_order.objects.get(user_id=user_id, status="for_payment")
            id_zak_m = order.id
            sum_cart_m = order.amount
        except my_order.DoesNotExist:
            sum_cart_m = 0
            id_zak_m = None
    else:
        sum_cart_m = 0
        id_zak_m = None
    context = {"sum_cart_m": sum_cart_m, 'id_zak_m': id_zak_m}
    return context

def sum_buy_order_m(request):
    if request.user.is_authenticated:
        user = request.user
        user_id = request.user.id
        my_order = apps.get_model('webshop', "Products_Order")
        orders = my_order.objects.filter(user_id=user_id, status="paid")
        total = orders.aggregate(Sum('amount'))
        sum_my_buy_m = total["amount__sum"] or 0

    else:
        sum_my_buy_m = 0

    context = {'sum_my_buy_m': sum_my_buy_m}
    return context

