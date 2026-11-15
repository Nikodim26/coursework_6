from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from customer_management.forms import CustomerForm
from customer_management.models import Customer
from users.services import access_manager


class CustomersView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customers.html'
    context_object_name = 'customers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        is_manager = user.groups.filter(name="Менеджеры").exists()
        context['customers'] = Customer.objects.all() if (user.is_superuser or is_manager) \
            else Customer.objects.filter(owner=user)
        return context

class CustomerView(DetailView):
    model = Customer
    template_name = 'customer.html'
    context_object_name = 'customer'
    pk_url_kwarg = 'pk'

    def dispatch(self, request, *args, **kwargs):
        response=access_manager(self, request, 'Не ты создавал - видеть запрещено!')
        return super().dispatch(request, *args, **kwargs) if not response else response


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'create_update_customer.html'
    success_url = reverse_lazy("customer_management:customers")
    context_object_name = 'customer'

    def form_valid(self, form):
        Customer = form.save(commit=False)
        Customer.owner = self.request.user
        Customer.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        response=access_manager(self, request, 'Ты просто менеджер - тебе Запрещено!')
        return super().dispatch(request, *args, **kwargs) if not response else response


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'create_update_customer.html'
    context_object_name = 'customer'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def dispatch(self, request, *args, **kwargs):
        response=access_manager(self, request, 'Ты просто менеджер - тебе Запрещено!')
        return super().dispatch(request, *args, **kwargs) if not response else response


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customer_delete_form.html'
    success_url = reverse_lazy("customer_management:customers")
    context_object_name = 'customer'

    def dispatch(self, request, *args, **kwargs):
        response=access_manager(self, request, 'Ты просто менеджер - тебе Запрещено!')
        return super().dispatch(request, *args, **kwargs) if not response else response