from django.db.models import Q
from django.views import generic
from product.models import Category, Product


class FrontPageView(generic.ListView):
    queryset = Product.objects.all()[0:8]
    context_object_name = 'products'
    template_name = 'core/frontpage.html'


class ShopView(generic.ListView):
    queryset = Product.objects.all()
    context_object_name = 'products'
    template_name = 'core/shop.html'

    @property
    def active_category(self):
        return self.request.GET.get('category', '')

    @property
    def query(self):
        return self.request.GET.get('query', '')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['active_category'] = self.active_category

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        active_category = self.active_category
        query = self.query

        if active_category:
            queryset = queryset.filter(category__slug=active_category)

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query))

        return queryset
