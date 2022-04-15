from django.contrib.auth import get_user_model
from django.db import models

from product.models import Product

User = get_user_model()


# class ShippingAddress(models.Model):
#     user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, blank=True, null=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(max_length=150)
#     address = models.CharField(max_length=150)
#     zipcode = models.CharField(max_length=150)
#     place = models.CharField(max_length=150)
#     phone = models.CharField(max_length=50)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     paid = models.BooleanField(default=False)

class Order(models.Model):
    ORDERED = 'ordered'
    SHIPPED = 'shipped'

    STATUS_CHOICES = [
        (ORDERED, 'Ordered'),
        (SHIPPED, 'Shipped')
    ]

    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    address = models.CharField(max_length=150)
    zipcode = models.CharField(max_length=150)
    place = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    paid_amount = models.IntegerField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
