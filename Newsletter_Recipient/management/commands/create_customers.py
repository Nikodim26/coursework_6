from django.core.management.base import BaseCommand

from Newsletter_Recipient.models import Customer


class Command(BaseCommand):
    help = "Заполняет базу клиентами"

    def handle(self, *args, **options):
        names = {
            'Юрий Владимирович Никулин':'Balbes@mail.ru',
            'Георгий Михайлович Вицин':'Trus@yandex.ru',
            'Евгений Александрович Моргунов':'Byvaliy@gmail.com',
            }
        for fio,email in names.items():
            Customer.objects.create(
                fio=fio,
                email=email,
                description='Тестовый клиент'
            )

