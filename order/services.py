import stripe
from django.conf import settings

from cart.cart import Cart


def items_stripe_obj(request):
    cart = Cart(request)
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


def create_stripe_session(request, items):
    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url=settings.SUCCESS_URL,
        cancel_url=settings.CANCEL_URL
    )
    return session
