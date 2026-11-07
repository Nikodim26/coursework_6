from django.core.management.base import BaseCommand

from newsletter_letters.models import Message


class Command(BaseCommand):
    help = "Заполняет базу сообщениями"

    def handle(self, *args, **options):
        email_subjects = {
            'Привет':'Привет, балбес!',
            'Напоминание':'Ты трус!',
            'Малява':'Ты в авторитете',
            }
        for email_subject,Letter_body in email_subjects.items():
            Message.objects.create(
                email_subject=email_subject,
                Letter_body = Letter_body
            )

