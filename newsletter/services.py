from django.core.mail import send_mail
from django.utils import timezone

from config.settings import DEFAULT_FROM_EMAIL

from .models import MailingAttempt


class MailServiceRunner:

    @staticmethod
    def calculate_status(obj):
        now = timezone.now()

        if obj.start_time > now:
            return "Created"
        elif obj.start_time <= now <= obj.end_time:
            return "Started"
        return "Finished"

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
        MailServiceRunner.update_status(obj)
        if not obj.status == "started":
            raise ValueError("Mailing is not currently not available.")
        recipients = obj.recipients.all()

        for recipient in recipients:
            try:
                subject = obj.message.subject
                message = obj.message.body
                from_email = DEFAULT_FROM_EMAIL
                recipient_list = [recipient.email]
                result = send_mail(subject, message, from_email, recipient_list)
                if result:
                    status = "successful"
                    server_response = "250 OK: Email sent"
                else:
                    status = "failed"
                    server_response = "Email not sent"

            except Exception as e:
                status = "failed"
                server_response = f"{type.__name__}: {str(e)}"
            MailingAttempt.objects.create(
                attempt_time=now, status=status, server_response=server_response, mailing=obj
            )


class StatisticsService:
    @staticmethod
    def attempts_count(user, status):
        return MailingAttempt.objects.filter(mailing__owner=user, status=status).count()

    @staticmethod
    def all_attempts(user):
        return MailingAttempt.objects.filter(mailing__owner=user).count()
