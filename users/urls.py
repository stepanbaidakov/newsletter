from django.contrib.auth.views import LogoutView, PasswordResetDoneView
from .views import RegisterView, UserUpdateView, UserLoginView, ActivateView, CustomPasswordResetView, \
    ActivationSentView, CustomPasswordResetConfirmView, UserListView, UserDetailView, BlockUserView
from django.urls import path

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page='newsletter:home'), name="logout"),
    path("profiles/<int:pk>/edit/", UserUpdateView.as_view(), name="profile_edit"),
    path("profiles/<int:pk>", UserDetailView.as_view(), name="profile"),
    path("profiles/", UserListView.as_view(), name="users"),
    path("profile/<int:pk>/block", BlockUserView.as_view(), name="block"),
    path("activate/<uidb64>/<token>/", ActivateView.as_view(), name="activate"),
    path("password/reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("password/reset/done/", PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("register/activation_sent/", ActivationSentView.as_view(), name="activation_sent"),
]
