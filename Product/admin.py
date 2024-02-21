from django.contrib import admin
from .models import Product, ProductImage, Promotions, Category


admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Category)
