from django.urls import path

from . import views

urlpatterns = [
    path('', views.FrontPageView.as_view(), name="frontpage"),
    path('shop/', views.ShopView.as_view(), name="shop")
]
