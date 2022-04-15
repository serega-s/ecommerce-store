from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import generic, View

from product.models import Product
from .cart import Cart


def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product, update_quantity=True)

    return render(request, 'cart/menu_cart.html')


class AddToCartView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product, update_quantity=True)

        return render(request, 'cart/menu_cart.html')


class CartView(generic.TemplateView):
    template_name = 'cart/cart.html'


def hx_menu_cart(request):
    return render(request, 'cart/menu_cart.html')


def hx_cart_total(request):
    return render(request, 'cart/partials/cart_total.html')


class UpdateCartView(View):
    def get(self, request, product_id, action):
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)

        if action == 'increment':
            cart.add(product, 1, True)
        else:
            cart.add(product, -1, True)

        quantity = cart.get_item(product_id)['quantity']

        item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'image': product.image,
                'get_thumbnail': product.get_thumbnail(),
                'price': product.price
            },
            'total_price': (quantity * product.price) / 100,
            'quantity': quantity
        }

        response = render(request, 'cart/partials/cart_item.html', {'item': item})
        response['HX-Trigger'] = 'update-menu-cart'
        return response


class CheckoutView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'cart/checkout.html'
