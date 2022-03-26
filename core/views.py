from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from product.models import Category, Product

from .forms import SignUpForm


class FrontPageView(generic.ListView):
    queryset = Product.objects.select_related('category').all()[:8]
    context_object_name = 'products'
    template_name = 'core/frontpage.html'


class ShopView(generic.ListView):
    queryset = Product.objects.select_related('category').all()
    context_object_name = 'products'
    template_name = 'core/shop.html'

    @property
    def query(self):
        return self.request.GET.get('query', '')

    @property
    def active_category(self):
        return self.request.GET.get('category', '')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['active_category'] = self.active_category

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        if active_category := self.active_category:
            queryset = queryset.filter(category__slug=active_category)

        if query := self.query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query))

        return queryset


def register(request):
    return


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'core/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect('frontpage')


class LogInView(LoginView):
    form = AuthenticationForm
    template_name = 'core/login.html'

    def get_success_url(self):
        return reverse_lazy('frontpage')


class LogOutView(generic.RedirectView):
    url = '/login/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs)
