from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from mailing_management.models import NewsLetter


class Command(BaseCommand):
    help = 'Ручной запуск рассылки: по id или всех активных'

    def add_arguments(self, parser):
        parser.add_argument(
            'newsletter_id',
            nargs='?',
            type=int,
            default=None,
            help='ID конкретной рассылки (необязательно)',
        )

    def handle(self, *args, **options):
        newsletter_id = options['newsletter_id']

        if newsletter_id:
            newsletters = NewsLetter.objects.filter(pk=newsletter_id)
            if not newsletters.exists():
                raise CommandError(f'Рассылка с id={newsletter_id} не найдена')
        else:
            # все активные на данный момент
            now = timezone.now()
            newsletters = NewsLetter.objects.filter(
                status=NewsLetter.Status.STARTED,
                start_time__lte=now,
                end_time__gte=now,
            )

        for newsletter in newsletters:
            sent, failed = send_mailing(newsletter)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Рассылка #{newsletter.pk}: отправлено {sent}, ошибок {failed}'
                )
            )
