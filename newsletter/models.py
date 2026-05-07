from django.db import models
from config import settings
# Create your models here.

class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Почта")
    full_name = models.CharField(max_length=100, verbose_name="Имя Фамилия")
    comment = models.TextField(verbose_name="Комментарий")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="Recipients", verbose_name="Владелец", blank=True, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Recipient"
        verbose_name_plural = "Recipients"
        db_table = "Recipient"


class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name="Тема")
    body = models.TextField(verbose_name="Тело")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages", blank=True, null=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        db_table = "Message"

class MailService(models.Model):
    start_time = models.DateTimeField(verbose_name="Время начала")
    end_time = models.DateTimeField(verbose_name="Время конца")
    status = models.CharField(max_length=30, default="Создана", verbose_name="Статус")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение", related_name="messages")
    recipients = models.ManyToManyField(Recipient, verbose_name="Получатель")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="MailServices", verbose_name="Владелец", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.message.subject} - {self.status}"

    class Meta:
        verbose_name = "MailService"
        verbose_name_plural = "MailService"
        db_table = "MailService"
        permissions = [("can_disable_mailservice", "Can disable mailservice")]

class MailingAttempt(models.Model):
    attempt_time = models.DateTimeField()
    status = models.CharField(max_length=15)
    server_response = models.TextField()
    mailing = models.ForeignKey(MailService, on_delete=models.CASCADE, related_name="attempts")

    def __str__(self):
        return f"{self.attempt_time} - {self.status}"

    class Meta:
        verbose_name = "MailingAttempt"
        verbose_name_plural = "MailingAttempts"
        db_table = "MailingAttempt"