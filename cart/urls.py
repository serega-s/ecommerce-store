from django.urls import path

from . import views

urlpatterns = [
    # path('add_to_cart/<int:product_id>/',
    #      views.add_to_cart, name='add_to_cart'),
    path('add_to_cart/<int:product_id>/',
         views.AddToCartView.as_view(), name='add_to_cart'),
    path('update_cart/<int:product_id>/<str:action>/', views.UpdateCartView.as_view(), name='update_cart'),
    path('', views.CartView.as_view(), name='cart'),
    path('success/', views.SuccessCartView.as_view(), name='success'),
    path('hx_menu_cart/', views.hx_menu_cart, name='hx_menu_cart'),
    path('hx_cart_total/', views.hx_cart_total, name='hx_cart_total')
]
