from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, View

from .forms import RecipientForm, MessageForm, MailServiceForm
from .models import Recipient, Message, MailService
from django.urls import reverse_lazy
from .services import MailServiceRunner
from django.shortcuts import redirect
# Create your views here.

class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "newsletter/recipient_form.html"
    success_url = reverse_lazy("newsletter:recipients_list")


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = "newsletter/recipient_detail.html"
    context_object_name = "recipient"


class RecipientUpdateView(UpdateView):
    model = Recipient
    template_name = "newsletter/recipient_form.html"
    form_class = RecipientForm

    def get_success_url(self):
        return reverse_lazy("newsletter:recipient_detail", kwargs={"pk": self.object.pk})


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "newsletter/recipient_delete.html"
    context_object_name = "recipient"
    success_url = reverse_lazy("newsletter:recipients_list")


class RecipientListView(ListView):
    model = Recipient
    template_name = "newsletter/recipients_list.html"
    context_object_name = "recipients"


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "newsletter/message_form.html"
    success_url = reverse_lazy("newsletter:messages_list")


class MessageDetailView(DetailView):
    model = Message
    template_name = "newsletter/message_detail.html"
    context_object_name = "message"


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "newsletter/message_form.html"

    def get_success_url(self):
        return reverse_lazy("newsletter:message_detail", kwargs={"pk": self.object.pk})


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "newsletter/message_delete.html"
    context_object_name = "message"
    success_url = reverse_lazy("newsletter:messages_list")


class MessageListView(ListView):
    model = Message
    template_name = "newsletter/messages_list.html"
    context_object_name = "messages"


class MailServiceCreateView(CreateView):
    model = MailService
    form_class = MailServiceForm
    template_name = "newsletter/mail_service_form.html"
    success_url = reverse_lazy("newsletter:mail_services_list")


class MailServiceDetailView(DetailView):
    model = MailService
    template_name = "newsletter/mail_service_detail.html"
    context_object_name = "mail_service"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        MailServiceRunner.update_status(obj)
        return obj


class MailServiceUpdateView(UpdateView):
    model = MailService
    form_class = MailServiceForm
    template_name = "newsletter/mail_service_form.html"

    def get_success_url(self):
        return reverse_lazy("newsletter:mail_service_detail", kwargs={"pk": self.object.pk})


class MailServiceDeleteView(DeleteView):
    model = MailService
    template_name = "newsletter/mail_service_delete.html"
    context_object_name = "mail_service"
    success_url = reverse_lazy("newsletter:mail_services_list")


class MailServiceListView(ListView):
    model = MailService
    template_name = "newsletter/mail_services_list.html"
    context_object_name = "mail_services"

class MailSendingView(View):
    def post(self, request, pk):
        obj = MailService.objects.get(pk=pk)
        try:
            MailServiceRunner.run(obj)
            messages.success(request, "Рассылка успешно запущена")

        except Exception as e:
            messages.error(request, f"Ошибка: {e}")

        return redirect("newsletter:mail_services_list")

class HomePageView(ListView):
    template_name = "newsletter/home.html"
    model = MailService
    context_object_name = "mail_services"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_mail_services = MailService.objects.filter(status="Запущена")
        recipients = Recipient.objects.all()
        context["active_mail_services"] = active_mail_services
        context["recipients"] = recipients
        return context