from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, View
from .forms import RecipientForm, MessageForm, MailServiceForm
from .models import Recipient, Message, MailService, MailingAttempt
from django.urls import reverse_lazy
from .services import MailServiceRunner, StatisticsService
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.

class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "newsletter/recipient_form.html"
    success_url = reverse_lazy("newsletter:recipients_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Recipient
    template_name = "newsletter/recipient_detail.html"
    context_object_name = "recipient"

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        is_owner = user == product.owner
        is_manager = user.has_perm("newsletter.view_recipient")
        return is_owner or is_manager


class RecipientUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Recipient
    template_name = "newsletter/recipient_form.html"
    form_class = RecipientForm

    def get_success_url(self):
        return reverse_lazy("newsletter:recipient_detail", kwargs={"pk": self.object.pk})

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner


class RecipientDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Recipient
    template_name = "newsletter/recipient_delete.html"
    context_object_name = "recipient"
    success_url = reverse_lazy("newsletter:recipients_list")

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "newsletter/recipients_list.html"
    context_object_name = "recipients"

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("newsletter.view_recipient"):
            return Recipient.objects.all()
        else:
            return Recipient.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "newsletter/message_form.html"
    success_url = reverse_lazy("newsletter:messages_list")


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "newsletter/message_detail.html"
    context_object_name = "message"


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "newsletter/message_form.html"

    def get_success_url(self):
        return reverse_lazy("newsletter:message_detail", kwargs={"pk": self.object.pk})


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "newsletter/message_delete.html"
    context_object_name = "message"
    success_url = reverse_lazy("newsletter:messages_list")


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "newsletter/messages_list.html"
    context_object_name = "letters"


class MailServiceCreateView(LoginRequiredMixin, CreateView):
    model = MailService
    form_class = MailServiceForm
    template_name = "newsletter/mail_service_form.html"
    success_url = reverse_lazy("newsletter:mail_services_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailServiceDetailView(LoginRequiredMixin,UserPassesTestMixin, DetailView):
    model = MailService
    template_name = "newsletter/mail_service_detail.html"
    context_object_name = "mail_service"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        MailServiceRunner.update_status(obj)
        return obj

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        is_owner = user == product.owner
        is_manager = user.has_perm("newsletter.view_mailservice")
        return is_owner or is_manager


class MailServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MailService
    form_class = MailServiceForm
    template_name = "newsletter/mail_service_form.html"

    def get_success_url(self):
        return reverse_lazy("newsletter:mail_service_detail", kwargs={"pk": self.object.pk})

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner


class MailServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = MailService
    template_name = "newsletter/mail_service_delete.html"
    context_object_name = "mail_service"
    success_url = reverse_lazy("newsletter:mail_services_list")

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner


class MailServiceListView(LoginRequiredMixin, ListView):
    model = MailService
    template_name = "newsletter/mail_services_list.html"
    context_object_name = "mail_services"

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("newsletter.view_mailservice"):
            return MailService.objects.filter(is_active=True)
        else:
            return MailService.objects.filter(owner=user, is_active=True)


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


class MailServiceDisableView(View):
    def post(self, request, pk):
        mail_service = MailService.objects.get(pk=pk)
        if not request.user.has_perm("newsletter.can_disable_mailservice"):
            return HttpResponseForbidden("У Вас нет прав на отключения сервиса")
        mail_service.is_active = False
        mail_service.save()
        return redirect("newsletter:mail_services_list")


class StatisticsView(ListView):
    template_name = "newsletter/statistics.html"
    model = MailingAttempt
    context_object_name = "mailing_attempts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["successful_attempts"] = StatisticsService.attempts_count(user, "Успешно")
        context["failed_attempts"] = StatisticsService.attempts_count(user, "Не успешно")
        return context
