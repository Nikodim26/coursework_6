from django.db import models
from django.urls import reverse


class Customer(models.Model):
    fio = models.CharField(max_length=100, verbose_name='Ф.И.О')
    email = models.EmailField(unique=True, verbose_name='Email')
    description = models.TextField(verbose_name="Описание продукта", blank=True, null=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.fio} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ['pk']

    def get_absolute_url(self):
        return reverse('customer_management:customer', kwargs={'pk': self.pk})