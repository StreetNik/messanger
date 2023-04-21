from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from messanger import settings


class User(AbstractUser):
    class Meta:
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Chat(models.Model):
    title = models.TextField(max_length=30)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="chats")
    last_modified = models.DateTimeField(auto_now=True)

    def get_last_message(self):
        return Message.objects.filter(chat_id=self.id).first()

    class Meta:
        ordering = ["-last_modified"]

    def __str__(self):
        return f"id = {self.id}; title = {self.title}"


class Message(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    send_time = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-send_time"]

    def __str__(self):
        return f"{self.author} {self.chat} {self.send_time}"


@receiver(post_save, sender=Message)
def update_chat_last_modified(sender, instance, **kwargs):
    instance.chat.last_modified = instance.send_time
    instance.chat.save()
