from django.urls import path

from . import views

urlpatterns = [
    path('', views.FrontPageView.as_view(), name="frontpage"),
]
