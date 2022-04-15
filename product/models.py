from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files import File
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


def make_thumbnail(image, size=(300, 300)):
    img = Image.open(image)
    img.convert('RGB')
    img.thumbnail(size)

    thumb_io = BytesIO()
    img.save(thumb_io, 'JPEG', quality=85)

    thumbnail = File(thumb_io, name=image.name)

    return thumbnail


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.name

    # @property
    # def get_avg_rating(self):
    #     reviews = Review.objects.filter(product=self)
    #     count = len(reviews)
    #     summary = 0
    #     try:
    #         for rvw in reviews:
    #             summary += rvw.rating
    #         return (int(summary / count))
    #     except ZeroDivisionError:
    #         return 0

    #     return Product.objects.all().select_related('category').annotate(rating=Avg('product__reviews__rate')

    @property
    def get_display_price(self):
        return self.price / 100

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg'

#
# class Review(models.Model):
#     RATE_CHOICES = [
#         (1, 'I hated it'),
#         (2, 'I didnt like it'),
#         (3, 'it was ok'),
#         (4, 'I liked it'),
#         (5, 'I loved it'),
#     ]
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     content = models.CharField(max_length=500)
#     rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)