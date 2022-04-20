import json

import stripe as stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View, generic

from cart.cart import Cart
from order.models import Order, OrderItem, ShippingAddress

User = get_user_model()


class StartOrderView(LoginRequiredMixin, View):
    def cart(self):
        cart = Cart(self.request)
        return cart

    def request_data(self):
        data = json.loads(self.request.body)
        return data

    def items_stripe_obj(self):
        cart = self.cart()
        total_price = 0

        items = []

        for item in cart:
            product = item['product']
            total_price += product.price * int(item['quantity'])

            obj = {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name,
                    },
                    'unit_amount': product.price,
                },
                'quantity': item['quantity']
            }

            items.append(obj)
        return items

    def create_stripe_session(self, items):
        stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=items,
            mode='payment',
            success_url=settings.SUCCESS_URL,
            cancel_url=settings.CANCEL_URL
        )
        return session

    def post(self, request, *args, **kwargs):
        cart = self.cart()
        data = self.request_data()
        total_price = 0

        items = self.items_stripe_obj()

        session = self.create_stripe_session(items)
        payment_intent = session.payment_intent

        order_data = data['address']
        # order_data = request.POST.get('address')
        # order_data = request.POST.dict()
        # order_data.pop('csrfmiddlewaretoken', None)

        order = Order.objects.create(address_id=order_data, user=request.user)
        order.payment_intent = payment_intent
        order.paid_amount = total_price
        order.paid = True
        order.save()

        _order_items = []
        for item in cart:
            product = item['product']
            quantity = int(item['quantity'])
            price = product.price * quantity
            _order_items.append(OrderItem(product=product, order=order, price=price, quantity=quantity))
        order_items = OrderItem.objects.bulk_create(_order_items)

        cart.clear()

        return JsonResponse({'session': session, 'order': payment_intent})

    def get(self, request):
        return redirect('cart')


class AddAddressView(LoginRequiredMixin, generic.CreateView):
    model = ShippingAddress
    template_name = 'order/add_address.html'
    fields = '__all__'
    success_url = reverse_lazy('myaccount')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditAddressView(LoginRequiredMixin, generic.UpdateView):
    model = ShippingAddress
    template_name = 'order/edit_address.html'
    fields = ['first_name', 'last_name', 'phone', 'zipcode', 'place', 'address', 'email']
    success_url = reverse_lazy('myaccount')
    pk_url_kwarg = 'pk'
    context_object_name = 'shipping'


class CheckoutView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'order/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['pub_key'] = settings.STRIPE_API_KEY_PUBLISHABLE

        return context
