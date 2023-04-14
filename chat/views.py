from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import redirect
from django.views.generic import TemplateView

from chat.forms import SearchFieldForm, SendMessageForm, ChatForm, UserCreationForm
from chat.models import User, Message, Chat


class MainPageView(TemplateView, LoginRequiredMixin):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        username = self.request.user.username
        title = self.request.GET.get("title")
        context = super(MainPageView, self).get_context_data(**kwargs)
        context["chats"] = Chat.objects.filter(users=User.objects.get(username=username))
        if title:
            context["chats"] = context["chats"].filter(title__icontains=title)
        context["search_form"] = SearchFieldForm
        context["send_message_form"] = SendMessageForm
        if self.kwargs.get("pk"):
            if Chat.objects.get(id=self.kwargs["pk"]) in context["chats"]:
                context["chat"] = Chat.objects.get(pk=self.kwargs["pk"])
                context["messages"] = Message.objects.filter(chat=context["chat"]).order_by("send_time")
        return context


class ChatCreateView(generic.CreateView, LoginRequiredMixin):
    model = Chat
    form_class = ChatForm
    template_name = "create_chat.html"

    def post(self, request, *args, **kwargs):
        super(ChatCreateView, self).post(request)
        users = self.object.users
        title = self.object.title
        id = self.object.id
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "all_users",  # group name
            {
                "type": "chat.create",
                "title": title,
                "users": list(users.values_list('id', flat=True)),
                "id": id,
            },
        )

        return redirect("chat", pk=id)

    def get_success_url(self):
        return reverse("chat", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super(ChatCreateView, self).get_context_data(**kwargs)
        context["users"] = User.objects.all()
        context["search_form"] = SearchFieldForm

        return context


class RegistrationPageView(generic.CreateView):
    template_name = "registration/registration.html"
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
