from django.views.generic import RedirectView

from newsletter_recipient.apps import NewsletterRecipientConfig
from django.urls import path

from newsletter_recipient.views import CustomersView, CustomerView, CustomerCreateView, CustomerUpdateView, \
    CustomerDeleteView

app_name = NewsletterRecipientConfig.name

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='newsletter_recipient:customers', permanent=False), name='root'),
    path('customers/', CustomersView.as_view(), name='customers'),
    path('customer/<int:pk>/',CustomerView.as_view(), name='customer'),

    path('customer/new/', CustomerCreateView.as_view(), name='customer_create'),
    path('customer/<int:pk>/edit/', CustomerUpdateView.as_view(), name='customer_edit'),
    path('customer/<int:pk>/delete/',CustomerDeleteView.as_view(), name='customer_delete'),

]