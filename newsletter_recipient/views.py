from django.views.generic import ListView, DetailView

from newsletter_recipient.models import Customer


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