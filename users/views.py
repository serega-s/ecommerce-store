from django.contrib.auth import login, get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from users.forms import SignUpForm

User = get_user_model()


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect('frontpage')


class LogInView(LoginView):
    form = AuthenticationForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('frontpage')


class LogOutView(generic.RedirectView):
    url = '/login/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs)


class MyAccountView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'users/myaccount.html'


class EditMyAccountView(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = 'users/edit_myaccount.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('myaccount')

    def get_object(self, queryset=None):
        return self.request.user
