import telebot
from flask import Flask, request
from notion_client import Client
import requests
import json
import os

# =======================
# 🔐 تنظیمات (توکن‌های شما)
# =======================
BOT_TOKEN = "8414750573:AAFN9-Yd49cNZzFnw562zlv4whAjwVCE1C4"
NOTION_TOKEN = "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"
GEMINI_API_KEY = "AIzaSyAmADW8ZRLcVLx994xTasGD9IWUdhca978"
DATABASE_ID = "2fe97660f72880259d8bd6ece3fa1b57"
CHANNEL_ID = -1003872981712

# آدرس هوشمند برای رندر (خودش پیدا می‌کند)
WEBHOOK_URL = os.environ.get('RENDER_EXTERNAL_URL')
if not WEBHOOK_URL:
    WEBHOOK_URL = "https://sadid-bot.onrender.com" # آدرس پیش‌فرض

# لیست مجاز
ALLOWED_USERS = [5129819517] 

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
notion = Client(auth=NOTION_TOKEN)
app = Flask(__name__)

# =======================
# 🎹 منو
# =======================
def main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("📝 ارسال گزارش")
    btn2 = telebot.types.KeyboardButton("📅 وظایف هفته")
    btn3 = telebot.types.KeyboardButton("🤖 مشاوره هوشمند")
    btn4 = telebot.types.KeyboardButton("📂 وضعیت بایگانی")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

# =======================
# 🧠 هوش مصنوعی (Gemini)
# =======================
def ask_gemini(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": f"تو مشاور سدید هستی. پاسخ کوتاه و مدیریتی بده. سوال: {text}"}]}]}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=20)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        return "⚠️ سیستم جمنای در دسترس نیست."
    except:
        return "❌ خطای شبکه."

# =======================
# 🎮 دستورات
# =======================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.id not in ALLOWED_USERS: 
        bot.reply_to(message, "⛔ شما مجاز به استفاده از سیستم سدید نیستید.")
        return
    bot.reply_to(message, "🫡 سیستم مدیریت سدید (نسخه ابری) متصل شد.", reply_markup=main_menu())

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    if message.from_user.id not in ALLOWED_USERS: return
    txt = message.text if message.text else ""

    if txt == "📝 ارسال گزارش":
        bot.reply_to(message, "گزارش خود را بنویسید...", reply_markup=main_menu())
    
    elif txt == "🤖 مشاوره هوشمند":
        bot.reply_to(message, "سوال خود را با علامت ! بپرسید. مثال: !نکات جلسه فردا", reply_markup=main_menu())

    elif txt.startswith("!"):
        bot.send_chat_action(message.chat.id, 'typing')
        ans = ask_gemini(txt[1:])
        bot.reply_to(message, f"🤖 **پاسخ:**\n{ans}", reply_markup=main_menu())
    
    else:
        bot.reply_to(message, f"✅ پیام دریافت شد: {txt}", reply_markup=main_menu())

# =======================
# 🌐 سرور (Flask)
# =======================
@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.stream.read().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + "/" + BOT_TOKEN)
    return "✅ ربات سدید روی رندر فعال شد.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
