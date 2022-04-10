from django.shortcuts import render, get_object_or_404
from django.views import generic

from product.models import Product
from .cart import Cart


def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product, update_quantity=True)

    return render(request, 'cart/menu_cart.html')


class CartView(generic.TemplateView):
    template_name = 'cart/cart.html'


class CheckoutView(generic.TemplateView):
    template_name = 'cart/checkout.html'
