import json

from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View, generic

from .models import ReviewProductRelation, Product


# Used UpdateView because DetailView does not have a support for POST method
class ProductView(generic.UpdateView):
    queryset = Product.objects.all().select_related('category')
    slug_field = 'slug'
    slug_url_kwargs = 'slug'
    fields = []
    context_object_name = 'product'
    template_name = 'product/product.html'


class ReviewView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        review = ReviewProductRelation.objects.create(product_id=data['product_id'],
                                                      user=request.user,
                                                      content=data['content'],
                                                      rate=data['rate']
                                                      )

        return JsonResponse('Created', safe=False)

    def get(self, request):
        return redirect('product')
