from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'chat_id', 'telegram_username')
    search_fields = ('username', 'chat_id', 'telegram_username')
