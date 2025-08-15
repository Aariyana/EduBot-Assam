
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import pymongo

# MongoDB Connection
client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
db = client.education_bot
# app = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()  # এই লাইন কমেণ্ট কৰক
app = Application.builder().token("7233321528:AAGpnOqQd-9vjfR1UXnkUyTLViL1KoAAT4I").build()   # প্ৰত্যক্ষভাৱে দিয়ক
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Welcome! Use /qa [topic] for questions")

async def handle_qa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    topic = " ".join(context.args)
    
    # Premium check
    user = db.users.find_one({"user_id": user_id})
    if user and user.get("premium", False):
        await update.message.reply_document(f"https://drive.google.com/{topic}.pdf")
    else:
        await update.message.reply_text(f"❌ Watch 40s ads to download: https://your-site.com/ads?pdf={topic}")

# Referral System
async def handle_referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    referrer_id = context.args[0]
    db.users.update_one(
        {"user_id": update.message.from_user.id},
        {"$set": {"premium": True, "premium_expiry": datetime.now() + timedelta(days=1)}}
    )
    await update.message.reply_text("🎉 You got 1-day premium access!")

if __name__ == "__main__":
    app = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("qa", handle_qa))
    app.add_handler(CommandHandler("referral", handle_referral))
    app.run_polling()
