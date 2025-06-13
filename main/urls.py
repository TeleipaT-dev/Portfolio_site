from django.urls import path  # импортируем path для маршрутов
from . import views  # импортируем views из текущей папки
from .views import youtube_proxy
from django.shortcuts import render


urlpatterns = [
    path("", views.unified, name="home"),  # главная
    path("about/", views.about, name="about"),  # обо мне
    path("projects/", views.projects, name="projects"),  # проекты
    path("contacts/", views.contacts, name="contacts"),  # контакты
    path("skills/", views.skills, name="skills"),  # навыки
    path("chat/", views.chat, name="chat"),  # чат
    path("chat/clear/", views.clear_chat, name="clear_chat"),  # очистка чата
    path("youtube/", lambda r: render(r, "youtube_proxy.html")),
    path("proxy_youtube/", youtube_proxy),
    path("youtube/", lambda r: render(r, "youtube_auto.html")),
]
