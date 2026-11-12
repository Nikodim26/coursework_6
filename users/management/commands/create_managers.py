from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Создаёт группу менеджеров и назначает права"

    def handle(self, *args, **options):
        group, _ = Group.objects.get_or_create(name="Менеджеры")

        codenames = ["view_newsletter", "view_letter", "view_customer","view_user"]

        permissions = Permission.objects.filter(codename__in=codenames)

        if permissions.count() != len(codenames):
            found = set(permissions.values_list("codename", flat=True))
            missing = set(codenames) - found
            raise CommandError(
                f"Не найдены права: {', '.join(missing)}. "
                "Сначала выполните миграции."
            )

        group.permissions.add(*permissions)
        self.stdout.write(
            self.style.SUCCESS("Группа «Менеджеры» создана, права назначены")
        )
