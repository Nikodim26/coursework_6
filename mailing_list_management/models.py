from django.db import models
from django.urls import reverse


class Newsletter(models.Model):

    start_time = models.DateTimeField(verbose_name='Время запуска рассылки', blank=False, null=False)
    end_time = models.DateTimeField(verbose_name='Время остановки рассылки', blank=False, null=False)
    status = models.CharField(max_length=15, verbose_name='Тема письма')
    message = models.ForeignKey('message_management.Letter', on_delete=models.CASCADE)
    recipients = models.ManyToManyField('customer_management.Customer',
        verbose_name='Получатели',
        related_name='messages_received'
    )

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ['start_time']

    def get_absolute_url(self):
        return reverse('message_management:letter', kwargs={'pk': self.pk})