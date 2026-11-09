from django.views.generic import RedirectView

from message_management.apps import MessageManagementConfig
from django.urls import path

from message_management.views import LettersView, LetterView, LetterCreateView, LetterUpdateView, \
    LetterDeleteView, HomeView

app_name = MessageManagementConfig.name

urlpatterns = [
    # path('', RedirectView.as_view(pattern_name='message_management:letters', permanent=False), name='root'),
    path('letters/', LettersView.as_view(), name='letters'),
    path('letter/<int:pk>/',LetterView.as_view(), name='letter'),

    path('letter/new/', LetterCreateView.as_view(), name='letter_create'),
    path('letter/<int:pk>/edit/', LetterUpdateView.as_view(), name='letter_edit'),
    path('letter/<int:pk>/delete/',LetterDeleteView.as_view(), name='letter_delete'),
    path('home/',HomeView.as_view(), name='home'),

]

