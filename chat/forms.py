from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import SelectMultiple, EmailField

from chat.models import Chat, User


class SearchFieldForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search"})
    )


class SendMessageForm(forms.Form):
    message = forms.CharField(
        max_length=255,
        required=True,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Message", "name": "message", "class": "new-message-input"})
    )

    def clean_message(self):
        message = self.cleaned_data["message"]
        if message == "":
            raise ValidationError("Field is empty")

        return message


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['title', 'users']

    title = forms.CharField(
        max_length=255,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Title",
            "name": "title",
            "class": "chat-title-input"
        })
    )

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        label="",
        widget=SelectMultiple(attrs={'class': 'hide-select-box'})
    )


class UserCreationForm(UserCreationForm):
    email = EmailField(label=("Email address"), required=True)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
        model = User

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
