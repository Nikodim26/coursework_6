from django.views.generic import RedirectView

from newsletter_recipient.apps import NewsletterRecipientConfig
from django.urls import path

from newsletter_recipient.views import CustomersView, CustomerView

app_name = NewsletterRecipientConfig.name

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='newsletter_recipient:customers', permanent=False), name='root'),
    path('customers/', CustomersView.as_view(), name='customers'),
    path('customer/<int:pk>/',CustomerView.as_view(), name='customer'),

    # path('customer/new/', ProductCreateView.as_view(), name='customer_create'),
    # path('customer/<int:pk>/edit/', ProductUpdateView.as_view(), name='customer_edit'),
    # path('customer/<int:pk>/delete/', ProductDeleteView.as_view(), name='customer_delete'),

]