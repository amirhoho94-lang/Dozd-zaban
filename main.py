from telegram import Update, ForceReply
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import json
import random
from words import words

BOT_TOKEN = "8648043092:AAEfd3oypEtSlf4ezuTyESF8YeWctqSO91s"

# بارگذاری یا ایجاد فایل کاربران
try:
    with open("users.json", "r") as f:
        users = json.load(f)
except:
    users = {}

# دستور شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in users:
        users[user_id] = {"dozd": 0}
    await update.message.reply_text(
        f"سلام {update.effective_user.first_name}! آماده‌ای لغت یاد بگیری؟\nبرای گرفتن سوال /quiz بزن"
    )

# دستور گرفتن سوال
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    question = random.choice(words)
    context.user_data["current"] = question
    await update.message.reply_text(f"معنی این کلمه چیه؟\n{question['word']}", reply_markup=ForceReply(selective=True))

# پاسخ کاربر
async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if "current" not in context.user_data:
        await update.message.reply_text("ابتدا /quiz بزن تا سوال دریافت کنی.")
        return
    correct = context.user_data["current"]["meaning"].lower()
    user_answer = update.message.text.lower()
    if user_id not in users:
        users[user_id] = {"dozd": 0}

    if user_answer == correct:
        users[user_id]["dozd"] += 10
        await update.message.reply_text(f"آفرین! 10 dozd بهت اضافه شد.\nمجموع: {users[user_id]['dozd']}")
    else:
        users[user_id]["dozd"] -= 1
        await update.message.reply_text(f"اشتباه! 1 dozd کم شد.\nجواب درست: {correct}\nمجموع: {users[user_id]['dozd']}")

    # ذخیره کاربران
    with open("users.json", "w") as f:
        json.dump(users, f)

# اجرای ربات
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("quiz", quiz))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))

app.run_polling()
