from .models import MailingAttempt
from django.utils import timezone
from config.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail


class MailServiceRunner:

    @staticmethod
    def calculate_status(obj):
        now = timezone.now()

        if obj.start_time > now:
            return "Создана"
        elif obj.start_time <= now <= obj.end_time:
            return "Запущена"
        return "Завершена"

    @staticmethod
    def update_status(obj):
        new_status = MailServiceRunner.calculate_status(obj)

        if obj.status != new_status:
            obj.status = new_status
            obj.save(update_fields=["status"])
        return obj

    @staticmethod
    def run(obj):
        now = timezone.now()
        if not obj.start_time < now < obj.end_time:
            raise ValueError("В текущее время рассылка не доступна")
        recipients = obj.recipients.all()

        for recipient in recipients:
            try:
                subject = obj.message.subject
                message = obj.message.body
                from_email = DEFAULT_FROM_EMAIL
                recipient_list = [recipient.email]
                result = send_mail(subject, message, from_email, recipient_list)
                if result:
                    status = "Успешно"
                    server_response = "250 OK: Message accepted"
                else:
                    status = "Не успешно"
                    server_response = "Email not sent"

            except Exception as e:
                status = "Не успешно"
                server_response = f"{type.__name__}: {str(e)}"
            MailingAttempt.objects.create(attempt_time=now, status=status, server_response=server_response, mailing=obj)
