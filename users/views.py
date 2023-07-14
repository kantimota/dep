from django.shortcuts import render, HttpResponseRedirect
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib import auth, messages
from django.urls import reverse
from products.models import Basket
from django.contrib.auth.decorators import login_required



# Контроллер авторизации
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:  # Если пользователь существует, тогда его авторизуем
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


# Контроллер регистрации
def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():  # Если введенные данные валидные, сохраняем объект в БД
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('users:login'))  # Редирект на главную страницу после авторизации
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)


# Контроллер профиля пользователя
@login_required  # Декоратор авторизации, запрещает вызов в неавториз зоне
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)

    # переменные для подчсета суммы и количества
    baskets = Basket.objects.filter(user=request.user)  # фильтрация товаров конкретного пользака
    total_sum = 0
    total_quantity = 0

    # Увеличиваем сумму и количество
    for basket in baskets:
        total_sum += basket.sum()  # Суммируем все добавленные объекты
        total_quantity += basket.quantity

    context = {'title': 'Книжный мир: Профиль',
               'form': form,
               'baskets': baskets,
               'total_sum': total_sum,
               'total_quantity': total_quantity,
               }
    return render(request, 'users/profile.html', context)

# Контроллер разавторизации
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
