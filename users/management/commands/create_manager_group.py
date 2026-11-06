from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создание группы менеджеров назначение им прав доступа."

    def handle(self, *args, **options):
        manager_group, created = Group.objects.get_or_create(name="Manager")
        view_recipient_permission = Permission.objects.get(codename="view_recipient")
        view_mail_service_permission = Permission.objects.get(codename="view_mailservice")
        view_message_permission = Permission.objects.get(codename="view_message")
        view_user_permission = Permission.objects.get(codename="view_customuser")
        can_disable_mailservice_permission = Permission.objects.get(codename="can_disable_mailservice")
        can_block_user_permission = Permission.objects.get(codename="can_block_user")
        manager_group.permissions.add(view_user_permission)
        manager_group.permissions.add(view_mail_service_permission)
        manager_group.permissions.add(view_recipient_permission)
        manager_group.permissions.add(can_disable_mailservice_permission)
        manager_group.permissions.add(can_block_user_permission)
        manager_group.permissions.add(view_message_permission)
        if created:
            self.stdout.write(self.style.SUCCESS("Группа 'Manager' успешно создана"))
        else:
            self.stdout.write(self.style.SUCCESS('Права группы "Content Manager" обновлены'))
