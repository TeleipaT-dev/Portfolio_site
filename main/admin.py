from django.contrib import admin
from .models import ContactMessage  # импорт модели


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")  # поля для списка
    list_filter = ("created_at",)
    search_fields = ("name", "email", "message")
