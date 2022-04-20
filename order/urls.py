from django.urls import path

from order import views

urlpatterns = [
    path('start_order/', views.StartOrderView.as_view(), name='start_order'),
    path('add_address/', views.AddAddressView.as_view(), name='add_address'),
    path('edit_address/<int:pk>/', views.EditAddressView.as_view(), name='edit_address'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]
