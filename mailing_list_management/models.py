import datetime

from django.db import models
from django.urls import reverse
from django.utils import timezone


class NewsLetter(models.Model):
    start_time = models.DateTimeField(verbose_name='Время запуска рассылки', blank=False, null=False)
    end_time = models.DateTimeField(verbose_name='Время остановки рассылки', blank=False, null=False)
    status = models.CharField(max_length=15, verbose_name='Статус рассылки')
    message = models.ForeignKey(
        'message_management.Letter',
        on_delete=models.CASCADE,
        verbose_name='Письмо',
        related_name='newsletters'
    )
    recipients = models.ManyToManyField(
        'customer_management.Customer',
        verbose_name='Получатели',
        related_name='newsletters'
    )

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ['start_time']

    def get_absolute_url(self):
        return reverse('mailing_list_management:Newsletter', kwargs={'pk': self.pk})

    def update_status(self):

        time_now = timezone.now()

        if self.start_time > time_now:
            self.status = 'Создана'
        elif self.end_time < time_now:
            self.status = 'Завершена'
        else:
            self.status = 'Запущена'

        self.save()
