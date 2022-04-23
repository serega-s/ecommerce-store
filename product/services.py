from django.db.models import Avg

from product.models import ReviewProductRelation


def set_rating(product):
    rating = ReviewProductRelation.objects.filter(product=product).aggregate(rating=Avg('rate')).get('rating')
    product.rating = rating
    product.save()
