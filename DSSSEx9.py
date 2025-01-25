import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters

# Telegram bot API Token
TELEGRAM_BOT_TOKEN = "7228057545:AAE-tN_dAq_LkJ2NtWSHwQ1sOOBQpesAkgs"
LM_STUDIO_API_URL = "http://127.0.0.1:1234/v1/chat/completions"

#  /start order
async def start(update: Update, context):
    await update.message.reply_text("Hello! I'm your AI assistant powered by LM Studio.")

# handle text
async def chat_with_ai(update: Update, context):
    user_message = update.message.text
    await update.message.reply_text("Thinking... Please wait.")

    # send request to LM Studio API
    response = requests.post(
        LM_STUDIO_API_URL,
        json={
            "model": "llama-3.2-3b-instruct",  
            "messages": [{"role": "user", "content": user_message}],
            "max_tokens": 150
        }
    )

    if response.status_code == 200:
        result = response.json()
        ai_reply = result['choices'][0]['message']['content']
    else:
        ai_reply = "Sorry, something went wrong while processing your request."

    await update.message.reply_text(ai_reply)

#  Telegram Bot
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_ai))

print("Bot is running... Press Ctrl+C to stop.")
app.run_polling()
