import telebot
from telebot import types

# توکن اختصاصی شما که در فایل قرار گرفت
TOKEN = '8414750573:AAFN9-Yd49cNZzFnw562zlv4whAjwVCE1C4'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('📋 لیست وظایف')
    item2 = types.KeyboardButton('➕ افزودن وظیفه')
    item3 = types.KeyboardButton('❓ سوالات شرعی')
    markup.add(item1, item2, item3)
    
    welcome_text = (
        "سلام علیکم و رحمة الله.\n"
        "به ربات مدیریت پروژه «سدید» خوش آمدید.\n\n"
        "این ربات جهت سهولت در امور جاری و پاسخگویی به سوالات شرعی (مطابق با فتاوای حضرت آیت‌الله فیاض علیه السلام) طراحی شده است."
    )
    bot.reply_to(message, welcome_text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '❓ سوالات شرعی')
def sharia_info(message):
    bot.send_message(message.chat.id, "لطفاً سوال خود را بنویسید تا جهت کسب تکلیف به دفتر معظّم‌له ارجاع شود.")

bot.infinity_polling()

