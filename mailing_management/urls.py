from django.views.decorators.cache import cache_page

from config.settings import CACHE_TIMEOUT
from mailing_management.apps import MailingManagementConfig
from mailing_management.views import NewsLettersView, NewsLetterView, NewsLetterCreateView, NewsLetterUpdateView, \
    NewsLetterDeleteView
from django.urls import path

app_name = MailingManagementConfig.name

urlpatterns = [
    path('newsletters/', cache_page(CACHE_TIMEOUT)(NewsLettersView.as_view()), name='newsletters'),
    path('newsletter/<int:pk>/',cache_page(CACHE_TIMEOUT)(NewsLetterView.as_view()), name='newsletter'),
    #
    path('newsletter/new/', NewsLetterCreateView.as_view(), name='newsletter_create'),
    path('newsletter/<int:pk>/edit/', NewsLetterUpdateView.as_view(), name='newsletter_edit'),
    path('newsletter/<int:pk>/delete/',NewsLetterDeleteView.as_view(), name='newsletter_delete'),

]

