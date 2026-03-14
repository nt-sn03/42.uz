from django.urls import path

from .views import HandleUpdateView, SetWebhookView, LoginView


urlpatterns = [
    path('webhook/', HandleUpdateView.as_view(), name='handle_update'),
    path('set-webhook/', SetWebhookView.as_view(), name='set_webhook'),

    path('login/', LoginView.as_view(), name='login'),
]
