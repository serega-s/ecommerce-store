from django.urls import path

from . import views

urlpatterns = [
    path('product/<slug:slug>/', views.ProductView.as_view(), name='product'),
    path('product_review/', views.ReviewView.as_view(), name='review_product')
]
