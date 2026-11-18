from django.views.decorators.cache import cache_page

from config.settings import CACHE_TIMEOUT
from message_management.apps import MessageManagementConfig
from django.urls import path

from message_management.views import LettersView, LetterView, LetterCreateView, LetterUpdateView, \
    LetterDeleteView

app_name = MessageManagementConfig.name

urlpatterns = [
    path('letters/', cache_page(CACHE_TIMEOUT)(LettersView.as_view()), name='letters'),
    path('letter/<int:pk>/',LetterView.as_view(), name='letter'),

    path('letter/new/', LetterCreateView.as_view(), name='letter_create'),
    path('letter/<int:pk>/edit/', LetterUpdateView.as_view(), name='letter_edit'),
    path('letter/<int:pk>/delete/',LetterDeleteView.as_view(), name='letter_delete'),

]

