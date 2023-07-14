from django.contrib import admin

# Регистрация созданных моделей чтобы они появились в админке
from products.models import ProductCategory, Product
admin.site.register(Product)
admin.site.register(ProductCategory)