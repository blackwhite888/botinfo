from dotenv import load_dotenv
import os
load_dotenv("config.env")

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from ai_engine import ask_ai
from voice_handler import recognize_speech_from_voice
import tempfile

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я автобот. Задай вопрос голосом или текстом.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    response = ask_ai(user_input)
    await update.message.reply_text(response)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = update.message.voice
    file = await voice.get_file()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_file:
        await file.download_to_drive(temp_file.name)
        temp_path = temp_file.name

    recognized_text = recognize_speech_from_voice(temp_path)
    os.remove(temp_path)

    await update.message.reply_text(f"Вы сказали: {recognized_text}")
    response = ask_ai(recognized_text)
    await update.message.reply_text(response)

app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VOICE, handle_voice))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
app.run_polling()
