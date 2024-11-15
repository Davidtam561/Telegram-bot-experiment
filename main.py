# main.py
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from flask import Flask, request

# יצירת אפליקציית Flask
app = Flask(__name__)

# הגדרת הבוט
TOKEN = os.getenv('TELEGRAM_TOKEN')
URL = os.getenv('RENDER_EXTERNAL_URL')  # Render מספק את זה אוטומטית
bot_app = Application.builder().token(TOKEN).build()

# הפונקציה שתגיב לפקודת /start
async def start_command(update, context):
    await update.message.reply_text('שלום! אני בוט פשוט. נעים להכיר!')

# הפונקציה שתגיב לכל הודעת טקסט
async def handle_message(update, context):
    await update.message.reply_text(f'קיבלתי את ההודעה שלך: {update.message.text}')

# הגדרת הנתיב לwebhook
@app.route(f"/{TOKEN}", methods=['POST'])
async def webhook_handler():
    """Handle incoming updates from Telegram."""
    if request.method == "POST":
        await bot_app.update_queue.put(Update.de_json(
            request.get_json(force=True),
            bot_app.bot
        ))
        return "OK"

@app.route('/')
def index():
    return 'Bot is running'

def main():
    # הוספת handlers
    bot_app.add_handler(CommandHandler('start', start_command))
    bot_app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # הגדרת webhook
    bot_app.bot.set_webhook(url=f"{URL}/{TOKEN}")
    
    # הפעלת Flask
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
