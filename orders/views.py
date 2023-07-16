from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from orders.forms import OrderForm
from django.urls import reverse_lazy


# Контроллер создания заказа
class OrderCreateView(CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:success')
    title = 'Оформление заказа'

    # Берем юзера из запроса и заполняем инициатор
    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


# Контроллер страницы успешного заказа
class SuccessTemplateView(TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'
