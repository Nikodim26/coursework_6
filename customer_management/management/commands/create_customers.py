from django.core.management.base import BaseCommand

from customer_management.models import Customer


class Command(BaseCommand):
    help = "Заполняет базу клиентами"

    def handle(self, *args, **options):
        names = {
            'Никулин Юрий Владимирович':'Balbes@mail.ru',
            'Вицин Георгий Михайлович':'Trus@yandex.ru',
            'Моргунов Евгений Александрович':'Byvaliy@gmail.com',
            }
        for fio,email in names.items():
            Customer.objects.create(
                fio=fio,
                email=email,
                description='Тестовый клиент'
            )

