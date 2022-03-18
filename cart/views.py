from django.shortcuts import render
from django.views import View, generic

from .cart import Cart


class AddToCartView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        cart.add(product_id)

        context = {
            'cart': cart
        }

        return render(request, 'cart/menu_cart.html', context)
