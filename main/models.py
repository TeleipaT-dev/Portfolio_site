from django.db import models  # импортируем базу данных
from django.db import models


class Message(models.Model):
    name = models.CharField(max_length=100)  # имя отправителя
    content = models.TextField()  # текст сообщения
    timestamp = models.DateTimeField(auto_now_add=True)  # время

    def __str__(self):
        return f"{self.name}: {self.content[:20]}"


class ContactMessage(models.Model):  # создаём таблицу
    name = models.CharField(max_length=100)  # имя пользователя
    email = models.EmailField()  # его email
    message = models.TextField()  # текст сообщения
    created_at = models.DateTimeField(auto_now_add=True)  # дата и время

    def __str__(self):
        return f"Сообщение от {self.name} ({self.email})"
