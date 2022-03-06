from django.views import generic
from product.models import Product


class FrontPageView(generic.ListView):
    queryset = Product.objects.all()[0:8]
    context_object_name = 'products'
    template_name = 'core/frontpage.html'
