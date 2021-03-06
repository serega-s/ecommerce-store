from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    slug = models.SlugField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    @property
    def get_display_price(self):
        return self.price / 100

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                from product.services import make_thumbnail
                self.thumbnail = make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg'


#
class ReviewProductRelation(models.Model):
    RATE_CHOICES = [
        (1, 'I hated it'),
        (2, 'I didnt like it'),
        (3, 'it was ok'),
        (4, 'I liked it'),
        (5, 'I loved it'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=500)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.content}, {self.rate}'

    def save(self, *args, **kwargs):
        from product.services import set_rating

        creating = not self.pk

        old_rating = self.rate
        super().save(*args, **kwargs)
        new_rating = self.rate

        if old_rating != new_rating or creating:
            set_rating(self.product)
