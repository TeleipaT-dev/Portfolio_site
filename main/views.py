from django.shortcuts import render  # подключаем шаблоны
from .forms import ContactForm  # импортируем форму из forms.py
from .models import ContactMessage
from .models import Message
from .forms import MessageForm
from django.shortcuts import redirect
from .models import Message

import requests


def query_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json",
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "Ты умный помощник на сайте-портфолио программиста.",
            },
            {"role": "user", "content": prompt},
        ],
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        # лог
        print("OpenRouter:", result)

        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print("Ошибка OpenRouter:", e)
        return "ИИ не смог ответить 🤖"


from django.shortcuts import render
from .models import Message
from .forms import ChatForm


def clear_chat(request):
    Message.objects.all().delete()
    form = ChatForm()
    messages = Message.objects.order_by("timestamp")
    return render(request, "chat.html", {"form": form, "messages": messages})


def chat(request):
    messages = Message.objects.order_by("-timestamp")[:50]
    form = MessageForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user_msg = form.save()

        # ответ от OpenRouter
        ai_response = query_openrouter(user_msg.content)
        Message.objects.create(name="ИИ", content=ai_response)

        return redirect("chat")

    return render(request, "chat.html", {"form": form, "messages": messages})


def home(request):  # главная
    return render(request, "home.html")


def about(request):  # страница "Обо мне"
    return render(request, "about.html")


def projects(request):  # страница "Проекты"
    return render(request, "projects.html")


def contacts(request):
    success = False

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Сохраняем сообщение в базу данных
            ContactMessage.objects.create(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                message=form.cleaned_data["message"],
            )

            success = True
            form = ContactForm()  # очищаем форму после отправки
    else:
        form = ContactForm()

    return render(request, "contacts.html", {"form": form, "success": success})


def skills(request):  # страница "Навыки"
    return render(request, "skills.html")


import requests
from django.http import HttpResponse
from urllib.parse import unquote


def youtube_proxy(request):
    url = request.GET.get("url")
    if not url:
        return HttpResponse("❌ Укажи URL через ?url=", status=400)

    try:
        response = requests.get(
            unquote(url),
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
            timeout=10,
        )

        content_type = response.headers.get("Content-Type", "text/html")
        return HttpResponse(response.content, content_type=content_type)
    except requests.exceptions.RequestException:
        return HttpResponse("⚠️ Ошибка при загрузке страницы", status=500)


def unified(request):
    from .forms import ContactForm

    form = ContactForm()
    success = False

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = ContactForm()

    return render(request, "unified.html", {"form": form, "success": success})
