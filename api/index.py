import os
import asyncio
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- CONFIGURATION ---
# Use an environment variable for security!
BOT_TOKEN = os.getenv("BOT_TOKEN")

COURSES = [
    {"name": "Digital Pedagogy", "url": "https://app.mindsmith.ai/learn/cmvz626c7000008l00xqa8ydb"},
    {"name": "Different Teaching-Learning Methods for Early Grade Numeracy", "url": "https://app.mindsmith.ai/learn/cmwp4qd3n006402mkxxefsy9p"},
    {"name": "Different Ways of Using Flash Cards for Early Grade Numeracy", "url": "https://app.mindsmith.ai/learn/cmwp77a15000008l9fsf5as3x"},
]

app = FastAPI()

# Initialize the Telegram Application
# Note: We initialize it globally so it's reused across requests
ptb_app = ApplicationBuilder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for course in COURSES:
        keyboard.append([InlineKeyboardButton(text=f"{course['name']}", web_app=WebAppInfo(url=course['url']))])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Welcome! Select a course to begin:", reply_markup=reply_markup)

# Register handlers
ptb_app.add_handler(CommandHandler("start", start))

@app.post("/api/index.py")
@app.post("/api/webhook")
@app.post("/")
async def webhook_handler(request: Request):
    """Handles incoming updates from Telegram"""
    data = await request.json()
    update = Update.de_json(data, ptb_app.bot)

    async with ptb_app:
        await ptb_app.process_update(update)

    return {"status": "ok"}

@app.get("/api/index.py")
@app.get("/api/webhook")
@app.get("/")
def index():
    return {"message": "Mindsmith Bot is running!", "token_present": BOT_TOKEN is not None}
