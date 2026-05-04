from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.core.checks import messages
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib import messages
from users.forms import CustomUserCreationForm, CustomUserChangeForm, CustomLoginForm, CustomPasswordResetForm, \
    CustomPasswordResetConfirmForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.views.generic.edit import UpdateView
from django.core.mail import send_mail
from config.settings import DEFAULT_FROM_EMAIL
from .models import CustomUser

# Create your views here.

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:activation_sent")

    def form_valid(self, form):
        form.instance.is_active = False
        response = super().form_valid(form)
        user = self.object

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        domain = get_current_site(self.request).domain
        link = f"http://{domain}/activate/{uid}/{token}/"
        send_mail(
            "Подтверждение регистрации",
            f"Перейдите по ссылке для подтверждения регистрации: {link}",
            DEFAULT_FROM_EMAIL,
            [user.email],
        )
        return response


class UserUpdateView(UpdateView):
    form_class = CustomUserChangeForm
    template_name = "users/profile_form.html"
    model = CustomUser
    def get_success_url(self):
        return reverse_lazy("users:profile_detail", kwargs={"pk": self.object.pk})


class UserLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "users/login.html"


class UserListView(LoginRequiredMixin,UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = "users/users_list.html"
    context_object_name = "users"

    def test_func(self):
        user = self.request.user
        is_manager = user.has_perm("users.view_users")
        return is_manager

    def get_queryset(self):
        return CustomUser.objects.filter(is_active=True)


class UserDetailView(UserPassesTestMixin, DetailView):
    model = CustomUser
    template_name = "users/profile_detail.html"
    context_object_name = "user"

    def test_func(self):
        user = self.request.user
        obj = self.get_object()
        is_manager = user.has_perm("users.view_users")
        return is_manager or obj == user

class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            User = get_user_model()
            uid = int(urlsafe_base64_decode(uidb64).decode())
            user = User.objects.get(pk=uid)
        except Exception:
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Активация уккаунта прошла успешно")
            return redirect("users:login")
        return render(request, "users/activation_invalid.html")


class CustomPasswordResetView(PasswordResetView):
    template_name = "users/password_reset_form.html"
    success_url = reverse_lazy("users:password_reset_done")
    form_class = CustomPasswordResetForm
    email_template_name = "users/password_reset_email.html"


class ActivationSentView(View):
    template_name = "users/activation_sent.html"

    def get(self, request):
        return render(request, "users/activation_sent.html")


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm_form.html"
    success_url = reverse_lazy("users:login")
    form_class = CustomPasswordResetConfirmForm

    def form_valid(self, form):
        messages.success(self.request, "Пароль успешно изменен. Вы можете войти в аккаунт.")
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request, "Не удалось изменить пароль.")
        return super().form_invalid(form)

class BlockUserView(View):
    def post(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        if not request.user.has_perm("users.can_block_user"):
            return HttpResponseForbidden("У Вас нет прав на блокировку пользователя")
        user.is_active = False
        user.save()
        return redirect("users:users_list")
