from django.contrib import admin
from .models import Category, Product
# Register your models here.

admin.site.register(Category)
# admin.site.register(Product)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_featured', 'is_new')
    list_filter = ('category', 'is_featured', 'is_new')
    search_fields = ('name', 'description')
    list_per_page = 10


admin.site.register(Product, ProductAdmin)
