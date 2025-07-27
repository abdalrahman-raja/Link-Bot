import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# ضع التوكن الجديد هنا
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 مرحباً! أرسل لي الرابط بهذا الشكل:\n\nالرابط | الوصف | رابط الصورة")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        msg = update.message.text
        parts = msg.split('|')
        if len(parts) != 3:
            await update.message.reply_text("❌ تأكد من إرسال الرسالة بهذا الشكل:\nالرابط | الوصف | رابط الصورة")
            return

        long_url = parts[0].strip()
        description = parts[1].strip()
        image_url = parts[2].strip()

        # تقصير الرابط عبر TinyURL API
        response = requests.get(f"https://tinyurl.com/api-create.php?url={long_url}")
        short_url = response.text

        caption = f"🔗 [اضغط هنا لزيارة الرابط المختصر]({short_url})\n\n📄 {description}"

        await update.message.reply_photo(photo=image_url, caption=caption, parse_mode="Markdown")

    except Exception as e:
        print(e)
        await update.message.reply_text("⚠️ حدث خطأ أثناء المعالجة. تأكد من صحة البيانات.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
