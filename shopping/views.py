from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.urls import reverse


SHIPPING_TYPES = {
    "standard": 10,
    "premium": 15,
}


def products_view(request):
    products = Product.get_latest_products()
    if request.method == "POST":
        product_type = request.POST.get("product_type")
        start_rows = int(request.POST.get("start_row"))
        if not product_type == "":
            products = Product.get_latest_products(product_type, start_rows, start_rows+20)
        else:
            products = Product.get_latest_products(start_rows, start_rows+20)
        return redirect()
    return render(request, "index.html", {"products": products})


def one_product_view(request, product_id=None):
    if not product_id:
        products = Product.get_latest_products()
        return render(request, "index.html", {"products": products})
    product = get_object_or_404(Product, id=product_id)
    if request.method == "GET":
        return render(request, "product.html", {"product": product})
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponse(405)
        user = UserApp.objects.get(original_user=request.user)
        user.shopping_cart.add(product)
        user.save()
        return HttpResponse(200)


@login_required
def show_cart(request):
    user = UserApp.objects.get(original_user=request.user)
    final_price = 0.00
    for product in user.shopping_cart.all():
        final_price += product.price
    if request.method == "GET":
        # Show cart
        return render(request, "cart.html", {"cart": user.shopping_cart.all(),
            "cart_price": final_price,})
    elif request.method == "DELETE":
        # Delete item from cart
        product_id = request.DELETE.get("delete_product_id")
        product_obj = get_object_or_404(Product, id=product_id)
        final_price -= product_obj.price
        if product_id == "":
            user.shopping_cart.clear()
        else:
            user.shopping_cart.remove(id=int(product_id))
        user.save()
        return HttpResponse(201)
    elif request.method == "POST":
        # Order confirmation
        return redirect(reverse('order_confirmation'))


@login_required
def order_confirmation(request, shipping_type="standard"):
    user = UserApp.objects.get(original_user=request.user)
    final_price = 0.00
    for product in user.shopping_cart.all():
        final_price += product.price
    cart_price = final_price
    final_price = final_price + (final_price * TAX_RATES[user.province.upper()])
    tax = final_price
    if request.method == "GET":
        # See the confirmation
        return render(request, "order_confirmation.html", {
            "cart": user.shopping_cart.all(),
            "cart_price": cart_price,
            "tax": tax,
            "final_price_before_shipping": final_price
        })
    elif request.method == "POST":
        # Go to payment page
        description = request.POST.get("description")
        delivery_address = request.POST.get("address")
        final_price = final_price + SHIPPING_TYPES[shipping_type]
        user_id = user.id
        order = Order()
        order.ordered_by_user = user
        order.products = user.shopping_cart.all()
        order.shipping_type = shipping_type
        order.final_price = final_price
        order.address = delivery_address
        order.description = description
        order.save()
        # TODO: Go to payment page
    elif request.method == "PUT":
        # Payment done
        pass
