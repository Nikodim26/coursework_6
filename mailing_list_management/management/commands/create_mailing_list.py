from datetime import datetime

from django.core.management.base import BaseCommand
from mailing_list_management.models import NewsLetter
from message_management.models import Letter


class Command(BaseCommand):
    help = "Заполняет базу рассылками"

    def handle(self, *args, **options):
        times = {
            '2026-11-01 18:42:07': '2026-11-10 18:42:07',
            '2026-11-11 18:42:07': '2026-11-20 18:42:07',
            '2026-11-21 18:42:07': '2026-11-30 18:42:07',
        }
        for start_time, end_time in times.items():
            NewsLetter.objects.create(
                start_time=datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S'),
                end_time=datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S'),
                message=Letter.objects.latest('id')
            )
