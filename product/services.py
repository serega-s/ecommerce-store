from io import BytesIO

from PIL import Image
from django.core.files import File
from django.db.models import Avg

from product.models import ReviewProductRelation


def make_thumbnail(image, size=(300, 300)):
    img = Image.open(image)
    img.convert('RGB')
    img.thumbnail(size)

    thumb_io = BytesIO()
    img.save(thumb_io, 'JPEG', quality=85)

    thumbnail = File(thumb_io, name=image.name)

    return thumbnail


def set_rating(product):
    rating = ReviewProductRelation.objects.filter(product=product).aggregate(rating=Avg('rate')).get('rating')
    product.rating = rating
    product.save()
