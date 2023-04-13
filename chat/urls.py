from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from chat.views import MessageCreateView, ChatCreateView

urlpatterns = [
    path("", MessageCreateView.as_view(), name="home"),
    path("<int:pk>/", MessageCreateView.as_view(), name="chat"),
    path("create-new-chat/", ChatCreateView.as_view(), name="chat-create")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
