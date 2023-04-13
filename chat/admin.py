from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from chat.models import User, Chat, Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ["author", "chat", "send_time"]


admin.site.register(User, UserAdmin)
admin.site.register(Chat)
admin.site.register(Message, MessageAdmin)
