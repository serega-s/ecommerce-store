from django.shortcuts import render
from django.views import generic

from .cart import Cart


def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id, update_quantity=True)

    return render(request, 'cart/menu_cart.html')


class CartView(generic.TemplateView):
    template_name = 'cart/cart.html'


class CheckoutView(generic.TemplateView):
    template_name = 'cart/checkout.html'
