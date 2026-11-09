from django.db import models
from django.urls import reverse
from django.utils import timezone


class NewsLetter(models.Model):
    start_time = models.DateTimeField(verbose_name='Время запуска рассылки', blank=False, null=False)
    end_time = models.DateTimeField(verbose_name='Время остановки рассылки', blank=False, null=False)
    status = models.CharField(max_length=15, verbose_name='Статус рассылки', blank=True, null=True)
    message = models.ForeignKey(
        'message_management.Letter',
        on_delete=models.CASCADE,
        verbose_name='Тема письма',
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

    def update_status(self):
        time_now = timezone.now()

        if self.start_time is None or self.end_time is None:
            return

        if time_now < self.start_time:
            new_status = 'Создана'
        elif time_now > self.end_time:
            new_status = 'Завершена'
        else:
            new_status = 'Запущена'

        if getattr(self, 'status', None) != new_status:
            self.status = new_status
            self.save(update_fields=['status'])

    def get_absolute_url(self):
        return reverse('mailing_management:newsletter', kwargs={'pk': self.pk})
