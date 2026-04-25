from django.contrib import admin
from newsletter.models import MailService


# Register your models here.
@admin.register(MailService)
class MailServiceAdmin(admin.ModelAdmin):
    list_display = ("status", "start_time", "end_time")
    list_filter = ("status",)