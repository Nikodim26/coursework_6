from django.views.generic import RedirectView

from mailing_list_management.views import NewsLettersView, NewsLetterView
from message_management.apps import MessageManagementConfig
from django.urls import path

from message_management.views import LettersView, LetterView, LetterCreateView, LetterUpdateView, \
    LetterDeleteView

app_name = MessageManagementConfig.name

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='mailing_list_management:newsletters', permanent=False), name='root'),
    path('newsletters/', NewsLettersView.as_view(), name='newsletters'),
    path('newsletter/<int:pk>/',NewsLetterView.as_view(), name='newsletter'),
    #
    # path('letter/new/', LetterCreateView.as_view(), name='letter_create'),
    # path('letter/<int:pk>/edit/', LetterUpdateView.as_view(), name='letter_edit'),
    # path('letter/<int:pk>/delete/',LetterDeleteView.as_view(), name='letter_delete'),

]

