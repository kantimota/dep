from django.db import models
from users.models import User

# Модель категорий
class ProductCategory(models.Model):  # Создание объекта Категория с атрибутами
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    def __str__(self): # Динамическое формирование названия категории продукта
        return self.name

# Модель продукт
class Product(models.Model):  # Создание объекта Продукт с атрибутами
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/images')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    def __str__(self): # Динамическое формирование названия  продукта
        return f'Продукт: {self.name} | Категория: {self.category.name}'

# Модель корзины
class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    # Методы подчета товаров в корзине
    def sum(self):
        return self.product.price * self.quantity