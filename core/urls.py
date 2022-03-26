from django.urls import path

from . import views

urlpatterns = [
    path('', views.FrontPageView.as_view(), name="frontpage"),
    path('shop/', views.ShopView.as_view(), name="shop"),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout')
]
