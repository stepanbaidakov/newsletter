from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from newsletter.models import MailService, Message, Recipient

from .mixins import FormControlMixin


class RecipientForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ["email", "full_name", "comment"]


class MessageForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"


class MailServiceForm(FormControlMixin, forms.ModelForm):

    start_time = forms.DateTimeField(
        input_formats=["%d.%m.%Y %H:%M"],
        widget=forms.DateTimeInput(attrs={"placeholder": "ДД.ММ.ГГГГ ЧЧ:ММ"}),
        label="Время начала",
    )
    end_time = forms.DateTimeField(
        input_formats=["%d.%m.%Y %H:%M"],
        widget=forms.DateTimeInput(attrs={"placeholder": "ДД.ММ.ГГГГ ЧЧ:ММ"}),
        label="Время окончания",
    )

    class Meta:
        fields = ["start_time", "end_time", "message", "recipients"]
        model = MailService

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_time"].widget.format = "%d.%m.%Y %H:%M"
        self.fields["end_time"].widget.format = "%d.%m.%Y %H:%M"

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        if start_time is None or end_time is None:
            return cleaned_data
        now = timezone.now().replace(second=0, microsecond=0)
        if start_time < now - timedelta(minutes=1):
            raise ValidationError("Время начала рассылки не может быть в прошлом!")
        if start_time > end_time:
            raise ValidationError("Время начало рассылки должно быть раньше окончания!")
        return cleaned_data
