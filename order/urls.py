from django.urls import path

from order import views

urlpatterns = [
    path('start_order/', views.StartOrderView.as_view(), name='start_order'),
]
