from django import forms  # импортируем модуль forms
from .models import Message
from django import forms


class ChatForm(forms.Form):
    name = forms.CharField(label="Ваше имя", max_length=100)
    content = forms.CharField(
        label="Сообщение", widget=forms.Textarea(attrs={"rows": 3})
    )


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["name", "content"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ваше имя"}
            ),
            "content": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Сообщение", "rows": 3}
            ),
        }


class ContactForm(forms.Form):  # создаём форму
    name = forms.CharField(max_length=100, label="Имя")  # поле "Имя"
    email = forms.EmailField(label="Email")  # поле "Email"
    message = forms.CharField(  # поле "Сообщение"
        label="Сообщение", widget=forms.Textarea  # делаем его большим текстовым
    )
