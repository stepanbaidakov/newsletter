from django.urls import path
from .views import RecipientListView, RecipientCreateView, RecipientDeleteView, RecipientDetailView, \
    RecipientUpdateView, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    MailServiceListView, MailServiceCreateView, MailServiceDeleteView, MailServiceDetailView, MailServiceUpdateView, \
    MailSendingView, HomePageView, MailServiceDisableView, StatisticsView

app_name = "newsletter"

urlpatterns = [
    path("clients/", RecipientListView.as_view(), name="recipients_list"),
    path("clients/new/", RecipientCreateView.as_view(), name="recipient_create"),
    path("clients/<int:pk>/", RecipientDetailView.as_view(), name="recipient_detail"),
    path("clients/<int:pk>/edit/", RecipientUpdateView.as_view(), name="recipient_edit"),
    path("clients/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
    path("letters/", MessageListView.as_view(), name="messages_list"),
    path("letters/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("letters/new/", MessageCreateView.as_view(), name="message_create"),
    path("letter/<int:pk>/edit/", MessageUpdateView.as_view(), name="message_edit"),
    path("letter/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
    path("mailservices/", MailServiceListView.as_view(), name="mail_services_list"),
    path("mailservices/new/", MailServiceCreateView.as_view(), name="mail_service_create"),
    path("mailservices/<int:pk>/", MailServiceDetailView.as_view(), name="mail_service_detail"),
    path("mailservices/<int:pk>/edit/", MailServiceUpdateView.as_view(), name="mail_service_edit"),
    path("mailservices/<int:pk>/delete/", MailServiceDeleteView.as_view(), name="mail_service_delete"),
    path("mailservices/<int:pk>/send", MailSendingView.as_view(), name="mail_service_send"),
    path("home/", HomePageView.as_view(), name="home"),
    path("mailservices/<int:pk>/disable", MailServiceDisableView.as_view(), name="disable"),
    path("statistics/", StatisticsView.as_view(), name="statistics"),
]
