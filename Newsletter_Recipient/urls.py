from django.views.generic import RedirectView

from Newsletter_Recipient.apps import NewsletterRecipientConfig
from django.urls import path

from Newsletter_Recipient.views import CustomersView

app_name = NewsletterRecipientConfig.name

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='Newsletter_Recipient:customers', permanent=False), name='root'),
    path('customers/', CustomersView.as_view(), name='customers'),
    # path('customer/<int:pk>/',СustomerDetailView.as_view(), name='customer'),
    #
    # path('customer/new/', ProductCreateView.as_view(), name='customer_create'),
    # path('customer/<int:pk>/edit/', ProductUpdateView.as_view(), name='customer_edit'),
    # path('customer/<int:pk>/delete/', ProductDeleteView.as_view(), name='customer_delete'),

]