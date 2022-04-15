import json

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from cart.cart import Cart
from order.models import Order, OrderItem

User = get_user_model()


class StartOrderView(LoginRequiredMixin, View):
    # model = Order
    # template_name = 'users/edit_myaccount.html'
    # fields = ['first_name', 'last_name', 'email', 'address', 'zipcode', 'place', 'phone']
    # success_url = reverse_lazy('myaccount')

    def post(self, request, *args, **kwargs):
        cart = Cart(request)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        place = request.POST.get('place')
        phone = request.POST.get('phone')

        order_data = request.POST.dict()
        order_data.pop('csrfmiddlewaretoken', None)

        order = Order.objects.create(**order_data, user=request.user)

        for item in cart:
            product = item['product']
            quantity = int(item['quantity'])
            price = product.price * quantity

            item = OrderItem.objects.create(product=product, order=order, price=price, quantity=quantity)

        return redirect('myaccount')

    def get(self, request):
        return redirect('cart')
