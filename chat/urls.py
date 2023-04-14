from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from chat.views import MainPageView, ChatCreateView, RegistrationPageView

urlpatterns = [
    path("", MainPageView.as_view(), name="home"),
    path("<int:pk>/", MainPageView.as_view(), name="chat"),
    path("create-new-chat/", ChatCreateView.as_view(), name="chat-create"),
    path("registration/", RegistrationPageView.as_view(), name="registration")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
