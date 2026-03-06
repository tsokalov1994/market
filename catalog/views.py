from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from .models import Product, Genre_m, Products_Order, Product_OrderItem
from django.core.paginator import Paginator
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

many = settings.MANY
# Create your views here.
def redirect_to_catalog(request):
    return redirect("catalog/")

def show_products(request):
    return render(request, 'catalog/catalog_products.html', {'user': request.user})

def catalog_tree(request):
    user = request.user

    name_cat = "All products"

    request.session['tip_cat'] = 'tree'
    products = Product.objects.all()

    paginator = Paginator(products, per_page=30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'products': products, 'page_obj': page_obj, 'name_cat': name_cat, 'user': user}
    return render(request, 'catalog/catalog_tree.html', context)

def product_tree(request, id=0):
    user = request.user

    if id == 0:
        id_cat = request.session['id_cat']
    else:
        id_cat = id

    request.session['id_cat'] = id_cat

    select_cat = Genre_m.objects.get(id=id_cat)
    opened_ids = select_cat.get_ancestors(include_self=True).values_list("id", flat=True)
    id_rod_cat = select_cat.parent_id

    if id_rod_cat is None:
        id_rod_cat = 1

    select_rod_cat = Genre_m.objects.all()
    categories = select_cat.get_descendants(include_self=True)

    if id != 0:
        products = Product.objects.filter(genre__in=categories).distinct().order_by('name')
        name_cat = select_cat.name
    else:
        products = Product.objects.all()
        name_cat = "All products"

    paginator = Paginator(products, per_page=10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'products': products, 'opened_ids': opened_ids, 'page_obj': page_obj,
               'name_cat': name_cat, 'id_cat': id_cat, 'user': user,
               'select_rod_cat': select_rod_cat, 'id_rod_cat': id_rod_cat}

    return render(request, 'catalog/catalog_tree.html', context)


class ProductDetail(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'

def cart_edit(request):
    user_id = request.user.id

    order = Products_Order.objects.filter(user_id=user_id, status='cart')
    if len(order) == 1:
        order = Products_Order.objects.get(user_id=user_id, status="cart")
        sum_order = order.amount
        order_item = Product_OrderItem.objects.filter(order_id=order.id)
        s = []
        for item in order_item:
            s.append(item.quantity * item.price)

    else:
        return render(request, 'catalog/cart_edit.html')

    request.session['order_item'] = order.id

    products = Product_OrderItem.objects.filter(order_id=order.id)
    my_list = zip(products, s)

    context = {'order': order, 'products': products, 'sum_order': sum_order, 'many': many, 'my_list': my_list}

    return render(request, 'catalog/cart_edit.html', context=context)


@login_required
def update_quantity(request, item_id):
    if request.method == 'POST':
        try:
            item = get_object_or_404(Product_OrderItem, id=item_id, order__user=request.user)
            new_quantity = int(request.POST.get('quantity', 1))

            if new_quantity > 0:
                item.quantity = new_quantity
                item.save()

                # Обновляем общую сумму заказа
                order = item.order
                order_items = Product_OrderItem.objects.filter(order=order)
                order.amount = sum(i.quantity * i.price for i in order_items)
                order.save()

                messages.success(request, 'Количество обновлено')
            else:
                messages.error(request, 'Количество должно быть больше 0')

        except (ValueError, Product_OrderItem.DoesNotExist):
            messages.error(request, 'Ошибка при обновлении')

    return redirect('catalog:cart_edit')


@login_required
def remove_from_cart(request, item_id):
    try:
        item = get_object_or_404(Product_OrderItem, id=item_id, order__user=request.user)
        order = item.order
        item.delete()

        # Обновляем сумму заказа
        order_items = Product_OrderItem.objects.filter(order=order)
        if order_items.exists():
            order.amount = sum(i.quantity * i.price for i in order_items)
        else:
            order.amount = 0
        order.save()

        messages.success(request, 'Товар удален из корзины')

    except Product_OrderItem.DoesNotExist:
        messages.error(request, 'Товар не найден')

    return redirect('catalog:cart_edit')


@login_required
def create_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = get_object_or_404(Products_Order, id=order_id, user=request.user, status='cart')

            # Проверяем, что в корзине есть товары
            if not Product_OrderItem.objects.filter(order=order).exists():
                messages.error(request, 'Корзина пуста')
                return redirect('catalog:cart_edit')

            # Меняем статус заказа
            order.status = 'pending'  # или 'ordered'
            order.save()

            messages.success(request, 'Заказ успешно создан!')
            return redirect('catalog:my_order')  # перенаправляем на страницу заказов

        except Products_Order.DoesNotExist:
            messages.error(request, 'Заказ не найден')

    return redirect('catalog:cart_edit')

def my_order(request):
    return HttpResponse("Order edit")

def my_buy(request):
    return HttpResponse("Buys edit")

@login_required
def cart(request, id):
    product = get_object_or_404(Product, id=id)
    user = request.user
    order, created = Products_Order.objects.get_or_create(user=user, status="cart")

    num_order = order.num_order
    if num_order is None:
        d = order.creation_date
        d = d.strftime('%d/%m/%Y')
        num_order = str(order.id) + "_" + str(user.id) + "_" + d
        order.num_order = num_order
        order.save()

    order_item = Product_OrderItem.objects.filter(order_id=order.id, product_id = id)
    if len(order_item) == 0:
        order_item, created = Product_OrderItem.objects.get_or_create(order_id=order.id,
                                                                      product_id=id,
                                                                      price=product.price,
                                                                      quantity=1,
                                                                      user_id=user.id)

    else:
        messages.success(request, "Item is already in cart")

    order_items = Product_OrderItem.objects.filter(order=order)
    s = 0
    for item in order_items:
        s = s + item.quantity * item.price


    order.amount = s
    order.save()

    return redirect(reverse("catalog:catalog_tree"))


def order_del(request, id, id_zak):
    """
    Очистка корзины только по ID заказа
    """
    try:
        # Получаем корзину, принадлежащую текущему пользователю
        order = get_object_or_404(Products_Order, id=id_zak, user=request.user, status="cart")

        Product_OrderItem.objects.filter(order=order).delete()

        # Обновляем сумму
        order.amount = 0
        order.save()

        messages.success(request, "Корзина успешно очищена")

    except Products_Order.DoesNotExist:
        messages.error(request, "Корзина не найдена")

    return redirect('catalog:catalog_tree')

