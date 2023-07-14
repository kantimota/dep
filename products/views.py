from django.shortcuts import render, HttpResponseRedirect
from products.models import ProductCategory, Product, Basket
from users.models import User
from django.contrib.auth.decorators import login_required


# Функция отображения страницы главной страницы

def index(request):
    context = {'title': 'Книжный магазин', }
    return render(request, template_name='products/index.html', context=context)


# Контроллер отображения страницы с продуктами

def products(request):
    context = {
        'title': 'Каталог книг',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'products/products.html', context=context)


# Контроллер добавления товаров в корзину
@login_required  # Декоратор авторизации, запрещает вызов в неавториз зоне
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    # Если товара нет в корзине, передаем товар и +1
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)

    else:  # Если товар уже добавлен, увеличиваем количество +1
        basket = baskets.first()
        basket.quantity = basket.quantity + 1
        basket.save()
    # Возвращаем на ту же страницу где находится пользак
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# Контроллер удаления товаров
@login_required  # Декоратор авторизации, запрещает вызов в неавториз зоне
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    # Возвращаем на ту же страницу
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
