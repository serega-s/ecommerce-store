from django.urls import path

from . import views

urlpatterns = [
    path('product/<slug:slug>/', views.ProductView.as_view(), name='product')
]
