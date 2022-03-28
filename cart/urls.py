from django.urls import path

from . import views

urlpatterns = [
    path('add_to_cart/<int:product_id>/',
         views.add_to_cart, name='add_to_cart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/checkout', views.CheckoutView.as_view(), name='checkout')
]
