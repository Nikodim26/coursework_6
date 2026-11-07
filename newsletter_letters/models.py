from django.db import models
from django.urls import reverse


class Letter(models.Model):
    email_subject = models.CharField(max_length=100, verbose_name='Тема письма')
    letter_body = models.TextField(verbose_name="Содержание письма", blank=True, null=True)

    def __str__(self):
        return f'{self.email_subject}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['pk']

    def get_absolute_url(self):
        return reverse('newsletter_letters:letter', kwargs={'pk': self.pk})