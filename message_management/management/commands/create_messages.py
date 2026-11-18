from django.core.management.base import BaseCommand

from message_management.models import Letter


class Command(BaseCommand):
    help = "Заполняет базу сообщениями"

    def handle(self, *args, **options):
        email_subjects = {
            'Привет':'Привет, балбес!',
            'Напоминание':'Ты трус!',
            'Малява':'Ты в авторитете',
            }
        for email_subject,letter_body in email_subjects.items():
            Letter.objects.create(
                email_subject=email_subject,
                letter_body = letter_body
            )

