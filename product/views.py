from django.views import generic

from .models import Product


class ProductView(generic.DetailView):
    queryset = Product.objects.all()
    slug_field = 'slug'
    slug_url_kwargs = 'slug'
    context_object_name = 'product'
    template_name = 'product/product.html'
