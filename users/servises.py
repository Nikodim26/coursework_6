# mailings/services.py
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone


def send_mailing(newsletter: NewsLetter) -> tuple[int, int]:
    """Отправляет рассылку всем клиентам. Возвращает (успешно, с ошибкой)."""
    sent, failed = 0, 0

    for client in newsletter.clients.all():
        try:
            send_mail(
                subject=newsletter.message.subject,
                message=newsletter.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email],
                fail_silently=False,
            )
            sent += 1
            Log.objects.create(  # адаптируйте под свои поля
                newsletter=newsletter,
                client=client,
                status='успешно',
                server_response='200 OK',
                sent_at=timezone.now(),
            )
        except Exception as e:
            failed += 1
            Log.objects.create(
                newsletter=newsletter,
                client=client,
                status='ошибка',
                server_response=str(e),
                sent_at=timezone.now(),
            )

    return sent, failed
