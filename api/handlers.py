from random import randint

from django.core.cache import cache
from telegram import Update
from telegram.ext import CallbackContext

from .models import User


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    first_name = update.effective_chat.first_name
    last_name = update.effective_chat.last_name

    existing_user = User.objects.filter(username=user_id).first()
    if existing_user:
        welcome_message = f"Welcome back, {first_name}!"
        context.bot.send_message(chat_id=chat_id, text=welcome_message)
        return
    # Save user info to the database
    user = User.objects.create(
        username=user_id,
        chat_id=chat_id,
        first_name=first_name,
        last_name=last_name
    )
    welcome_message = f"Hello, {first_name}! You have been registered successfully."

    context.bot.send_message(chat_id=chat_id, text=welcome_message)


def login(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    first_name = update.effective_chat.first_name

    existing_user = User.objects.filter(username=user_id).first()
    if not existing_user:
        welcome_message = f"Hello, {first_name}! You are not registered yet. Please use /start to register."
        context.bot.send_message(chat_id=chat_id, text=welcome_message)
        return
    
    existing_opt = cache.get(f"otp_{user_id}")
    if existing_opt:
        welcome_message = f"Your OTP is still valid: {existing_opt}"
        context.bot.send_message(chat_id=chat_id, text=welcome_message)
        return
    
    opt = randint(100000, 999999)

    cache.set(f"otp_{user_id}", opt, timeout=60)  # OTP valid for 1 minutes

    update.message.reply_text(f"Your OTP is: {opt}")
