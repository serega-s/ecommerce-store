from django.contrib import admin

from order.models import Order, ShippingAddress, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)