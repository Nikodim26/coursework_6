from django.views.generic import RedirectView

from mailing_management.apps import MailingManagementConfig
from mailing_management.views import NewsLettersView, NewsLetterView, NewsLetterCreateView, NewsLetterUpdateView, \
    NewsLetterDeleteView
from django.urls import path

app_name = MailingManagementConfig.name

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='mailing_management:newsletters', permanent=False), name='root'),
    path('newsletters/', NewsLettersView.as_view(), name='newsletters'),
    path('newsletter/<int:pk>/',NewsLetterView.as_view(), name='newsletter'),
    #
    path('newsletter/new/', NewsLetterCreateView.as_view(), name='newsletter_create'),
    path('newsletter/<int:pk>/edit/', NewsLetterUpdateView.as_view(), name='newsletter_edit'),
    path('newsletter/<int:pk>/delete/',NewsLetterDeleteView.as_view(), name='newsletter_delete'),

]

