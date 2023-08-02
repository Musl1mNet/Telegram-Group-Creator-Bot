from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from telegrambot.models import User as TgUser


async def start(update:Update, context:ContextTypes.DEFAULT_TYPE):
    
    pass

handlers = [
    CommandHandler("start", start),
]