from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm, MessageForm, ChatForm
from .models import ContactMessage, Message

import requests
import json

# ===== Вызов OpenRouter AI =====
def query_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json",
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Ты умный помощник на сайте-портфолио программиста."},
            {"role": "user", "content": prompt},
        ],
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print("OpenRouter error:", e)
        return "⚠️ ИИ не смог ответить."


# ======= Главная чат-функция для /chat/ =======
def chat(request):
    messages = Message.objects.order_by("-timestamp")[:50]
    form = MessageForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user_msg = form.save()
        content = user_msg.content.strip()

        if content.lower().startswith("ии ответь"):
            prompt = content[len("ии ответь"):].strip()
            ai_response = query_openrouter(prompt)
            Message.objects.create(name="ИИ", content=ai_response)

        return redirect("chat")

    return render(request, "chat.html", {"form": form, "messages": messages})


# ===== Сохраняет обычное сообщение пользователя =====
@csrf_exempt
def save_user_message(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"})


# ===== Обработка запроса к ИИ (через fetch) =====
@csrf_exempt
def ask_ai(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt", "").strip()

            if prompt:
                ai_response = query_openrouter(prompt)
                Message.objects.create(name="ИИ", content=ai_response)
                return JsonResponse({"status": "ok", "reply": ai_response})

        except Exception as e:
            print("AI error:", e)

    return JsonResponse({"status": "error", "reply": "❌ Ошибка на сервере"})


# ====== Страницы сайта ======
def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")



def contacts(request):
    success = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                message=form.cleaned_data["message"],
            )
            success = True
            form = ContactForm()
    else:
        form = ContactForm()

    return render(request, "contacts.html", {"form": form, "success": success})


def unified(request):
    form = ContactForm()
    success = False

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = ContactForm()

    return render(request, "unified.html", {"form": form, "success": success})


# ===== Очистка чата =====
def clear_chat(request):
    Message.objects.all().delete()
    form = ChatForm()
    messages = Message.objects.order_by("timestamp")
    return render(request, "chat.html", {"form": form, "messages": messages})
