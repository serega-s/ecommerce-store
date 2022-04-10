from decimal import Decimal

from django.conf import settings

from product.models import Product


# class Cart(object):
#     def __init__(self, request):
#         self.session = request.session
#         cart = self.session.get(settings.CART_SESSION_ID)
#
#         if not cart:
#             cart = self.session[settings.CART_SESSION_ID] = {}
#
#         self.cart = cart
#
#     def __iter__(self):
#         for p in self.cart.keys():
#             self.cart[str(p)]['product'] = Product.objects.get(pk=p)
#
#     def __len__(self):
#         return sum(item['quantity'] for item in self.cart.values())
#
#     def save(self):
#         self.session[settings.CART_SESSION_ID] = self.cart
#         self.session.modified = True
#
#     def add(self, product_id, quantity=1, update_quantity=False):
#         product_id = str(product_id)
#
#         if product_id not in self.cart:
#             self.cart[product_id] = {'quantity': 1, 'id': product_id}
#
#         if update_quantity:
#             self.cart[product_id]['quantity'] += int(quantity)
#
#             if self.cart[product_id]['quantity'] == 0:
#                 self.remove(product_id)
#
#         self.save()
#
#     def remove(self, product_id):
#         if product_id in self.cart:
#             del self.cart[product_id]
#             self.save()

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id]['quantity'] = quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_cost(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
