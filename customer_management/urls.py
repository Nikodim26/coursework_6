from django.views.generic import RedirectView

from customer_management.apps import CustomerManagementConfig
from django.urls import path

from customer_management.views import CustomersView, CustomerView, CustomerCreateView, CustomerUpdateView, \
    CustomerDeleteView

app_name = CustomerManagementConfig.name

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='customer_management:customers', permanent=False), name='root'),
    path('customers/', CustomersView.as_view(), name='customers'),
    path('customer/<int:pk>/',CustomerView.as_view(), name='customer'),

    path('customer/new/', CustomerCreateView.as_view(), name='customer_create'),
    path('customer/<int:pk>/edit/', CustomerUpdateView.as_view(), name='customer_edit'),
    path('customer/<int:pk>/delete/',CustomerDeleteView.as_view(), name='customer_delete'),

]