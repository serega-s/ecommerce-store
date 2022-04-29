import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View, generic

from cart.cart import Cart
from order.models import Order, OrderItem, ShippingAddress
from order.services import items_stripe_obj, create_stripe_session

User = get_user_model()


class StartOrderView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        data = json.loads(self.request.body)
        total_price = 0

        items = items_stripe_obj(request)

        session = create_stripe_session(request, items)
        payment_intent = session.payment_intent

        if request.user.is_authenticated:

            order_data = data['address']
            # order_data = request.POST.get('address')
            # order_data = request.POST.dict()
            # order_data.pop('csrfmiddlewaretoken', None)

            order = Order.objects.create(
                address_id=order_data,
                user=request.user,
                paid=True,
                paid_amount=total_price
            )
        else:
            order_data = data.dict()
            order_data.pop('csrfmiddlewaretoken', None)

            order = Order.objects.create(
                **order_data,
                paid=True,
                paid_amount=total_price
            )

        order.payment_intent = payment_intent
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


class CheckoutView(generic.TemplateView):
    template_name = 'order/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['pub_key'] = settings.STRIPE_API_KEY_PUBLISHABLE

        return context
