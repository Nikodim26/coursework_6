from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from customer_management.forms import CustomerForm
from customer_management.models import Customer
from users.services import ProtectedView


class CustomersView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customers.html'
    context_object_name = 'customers'

    def get_queryset(self):
        user = self.request.user
        is_manager = user.groups.filter(name="Менеджеры").exists()
        if user.is_superuser or is_manager:
            return Customer.objects.all()
        return Customer.objects.filter(owner=user)


class CustomerView(ProtectedView, DetailView):
    model = Customer
    template_name = 'customer.html'
    context_object_name = 'customer'
    pk_url_kwarg = 'pk'
    access_message = 'Не ты создавал — видеть запрещено!'


class CustomerCreateView(ProtectedView, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'create_update_customer.html'
    success_url = reverse_lazy("customer_management:customers")
    context_object_name = 'customer'
    access_message = 'Ты просто менеджер — тебе запрещено!'

    def form_valid(self, form):
        customer = form.save(commit=False)
        customer.owner = self.request.user
        customer.save()
        return super().form_valid(form)


class CustomerUpdateView(ProtectedView, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'create_update_customer.html'
    context_object_name = 'customer'
    access_message = 'Ты просто менеджер — тебе запрещено!'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.clear()
        return response


class CustomerDeleteView(ProtectedView, DeleteView):
    model = Customer
    template_name = 'customer_delete_form.html'
    success_url = reverse_lazy("customer_management:customers")
    context_object_name = 'customer'
    access_message = 'Ты просто менеджер — тебе запрещено!'
