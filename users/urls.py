from django.urls import path

from users import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('myaccount/', views.MyAccountView.as_view(), name='myaccount'),
    path('edit-myaccount/', views.EditMyAccountView.as_view(), name='edit_myaccount')
]
