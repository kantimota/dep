from django.contrib import admin
from users.models import User

# Регистрация модели пользователя
admin.site.register(User)
