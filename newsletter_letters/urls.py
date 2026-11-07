from django.views.generic import RedirectView

from newsletter_letters.apps import NewsletterLettersConfig
from django.urls import path

from newsletter_letters.views import LettersView, LetterView, LetterCreateView, LetterUpdateView, \
    LetterDeleteView

app_name = NewsletterLettersConfig.name

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='newsletter_letters:letters', permanent=False), name='root'),
    path('letters/', LettersView.as_view(), name='letters'),
    path('letter/<int:pk>/',LetterView.as_view(), name='letter'),

    path('letter/new/', LetterCreateView.as_view(), name='letter_create'),
    path('letter/<int:pk>/edit/', LetterUpdateView.as_view(), name='letter_edit'),
    path('letter/<int:pk>/delete/',LetterDeleteView.as_view(), name='letter_delete'),

]

