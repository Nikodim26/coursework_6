from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from customer_management.forms import CustomerForm
from customer_management.models import Customer


class CustomersView(ListView):
    model = Customer
    template_name = 'customers.html'
    context_object_name = 'customers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = Customer.objects.all()
        return context


class CustomerView(DetailView):
    model = Customer
    template_name = 'customer.html'
    context_object_name = 'customer'
    pk_url_kwarg = 'pk'


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'create_update_customer.html'
    success_url = reverse_lazy("customer_management:customers")
    context_object_name = 'customer'


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'create_update_customer.html'
    context_object_name = 'customer'

    def get_success_url(self):
        return self.object.get_absolute_url()


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customer_delete_form.html'
    success_url = reverse_lazy("customer_management:customers")
    context_object_name = 'customer'