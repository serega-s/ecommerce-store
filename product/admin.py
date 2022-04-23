from django.contrib import admin

from .models import Category, Product, ReviewProductRelation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'price', 'category', 'rating', 'created_at']
    list_filter = ['created_at']
    list_editable = ['price']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ReviewProductRelation)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'rate']
    list_filter = ['created_at']
    list_editable = ['rate']
