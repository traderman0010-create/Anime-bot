import telebot
from telebot import types
import time
from flask import Flask
from threading import Thread
import re

# --- RENDER UCHUN ---
app = Flask('')
@app.route('/')
def home(): return "Bot is live!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- BOT SOZLAMALARI ---
TOKEN = '7747703136:AAFbeOSwtodo7r_TS_sefsso1_naLSm2iVg'
CHANNELS = ['@Anivoxuz', '@AniVoxnews', '-1002271291882'] 
MAXFIY_KANAL_LINK = 'https://t.me/+oxPibE-r26c2NjM6'
NEWS_KANAL_LINK = 'https://t.me/AniVoxnews'
THUMBNAIL = 'AgACAgIAAxkBAAICO2mG2hA7vlhpJpMaUGrDTyh0xu-PAALrC2sb1-s5SIBYET5mha17AQADAgADeAADOgQ'

# 🎬 ANIME BAZASI
animelar = {
    'jahannam1': {'id': 'BAACAgIAAyEFAATjsRFeAAM2aYT54IGZzyEi5CPiCvU8WNRgId0AAj6XAAKCriFIW68yMzkL46s4BA', 'caption': 'Jahannam Jannati [1-Fasl 1-Qism]'},
    'jahannam2': {'id': 'BAACAgIAAyEFAATjsRFeAAM5aYT8oJh3F7GrK2CyojfZ1VrnP-MAAmeTAAJsBylItxjYydrL6Qo4BA', 'caption': 'Jahannam Jannati [1-Fasl 2-Qism]'},
    'jahannam3': {'id': 'BAACAgIAAxkBAAIChWmHaXNeZyWoLbpaXu5rizAHeFWEAAKtkAACXgJBSPSArg0hC0iKOgQ', 'caption': 'Jahannam Jannati [1-Fasl 3-Qism]'},
    'jahannam4': {'id': 'BAACAgIAAxkBAAICrWmIflJBcPpMShatlvx1vKJYP6ZOAAI6kwACXgJBSPOVZ6w6WrDJOgQ', 'caption': 'Jahannam Jannati [1-Fasl 4-Qism]'},
    'jahannam5': {'id': 'BAACAgIAAxkBAAIDu2mPOKoZjIEPyY2qcuG3ono9blQ9AALqjwACrxBxSCyQp5QIZf4IOgQ', 'caption': 'Jahannam Jannati [1-Fasl 5-Qism]'},
    'jahannam6': {'id': 'BAACAgIAAxkBAAIEOWmQmmPA7CtOxdxEiEn-sxmK_885AALxmgACGPqISCytSobWdKdkOgQ', 'caption': 'Jahannam Jannati [1-Fasl 6-Qism]'},
    'jahannam7': {'id': 'BAACAgIAAxkBAAIEQGmRfQzCDi6cfpAhZk8DzAMsaQ_TAALBmwACGPqISKL90UBkoZgcOgQ', 'caption': 'Jahannam Jannati [1-Fasl 7-Qism]'},
    'jahannam8': {'id': 'BAACAgIAAxkBAAIEiWmXZqizE31X4LuZJgHSZ4vlFPc5AALznAACGPqQSERBy1a5fEXMOgQ', 'caption': 'Jahannam Jannati [1-Fasl 8-Qism]'},
    'jahannam9': {'id': 'BAACAgIAAxkBAAIEi2mXZrgS-or2yKYvHf1bLXr4KL-oAAIjowACnoO5SPXg2oO0hM0SOgQ', 'caption': 'Jahannam Jannati [1-Fasl 9-Qism]'},
    'jahannam10': {'id': 'BAACAgIAAxkBAAIE7Wme9PoWv3ER8mPDCz-rfW7vrB7XAAKehwACnoPBSPRnda5ftNvxOgQ', 'caption': 'Jahannam Jannati [1-Fasl 10-Qism]'},
    'jahannam11': {'id': 'BAACAgIAAxkBAAIE8Wmfnrb-v3_O_-uXFn9rx_7_HPMAA2OfAALWvwABSYngseA8X7e7OgQ', 'caption': 'Jahannam Jannati [1-Fasl 11-Qism]'},
    'jahannam12': {'id': 'BAACAgIAAxkBAAIE9WmgEwxJ75Dx3EXAuBtU-2kbsanxAAJDjQACBt8BSbCIbCw1Cyh_OgQ', 'caption': 'Jahannam Jannati [1-Fasl 12-Qism]'},
    'jahannam13': {'id': 'BAACAgIAAxkBAAIE92mgHSslGuS-xyTvvN-m7lOMXu1zAAIOjgACBt8BScGlXDDsjwdoOgQ', 'caption': 'Jahannam Jannati [1-Fasl 13-Qism Final]'},
    '2jahannam1': {'id': 'BAACAgIAAxkBAAIFpWml5b8ZNf0kc5u4Nje7JwEeS1etAAJlmwACJa8xST271BedaUOPOgQ', 'caption': 'Jahannam Jannati [2-Fasl 1-Qism]'},
    'sening': {'id': 'BAACAgIAAxkBAAIEPWmRfKeh-gtFnCxMI9jaOZ2_0T3RAAIpjwACrsw4SMeotftkaOVWOgQ', 'caption': 'Sening isming [Film]'}
}

bot = telebot.TeleBot(TOKEN)

# --- KLAVIATURALAR ---
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("🔍 Anime izlash"), types.KeyboardButton("📜 Animelar ro'yxati"))
    markup.row(types.KeyboardButton("💵 Reklama va Hamkorlik"))
    return markup

def cancel_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❌ Bekor qilish"))
    return markup

# --- OBUNA TEKSHIRISH ---
def check_sub(user_id):
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            if status not in ['member', 'administrator', 'creator']: return False
        except: continue
    return True

def show_sub_menu(user_id, action_type="search"):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("⛩️ Animelar || Uzbek Tilida ✅", url="https://t.me/Anivoxuz")
    btn2 = types.InlineKeyboardButton("⛩️ ANIVOX || NEWS Kanali ✅", url=NEWS_KANAL_LINK)
    btn3 = types.InlineKeyboardButton("⛩️ Maxfiy Kanalimizga A'zo Bo'lish ✅", url=MAXFIY_KANAL_LINK)
    btn_check = types.InlineKeyboardButton("🔄 OBUNANI TASDIQLASH 🔄", callback_data=f"check_sub_{action_type}")
    markup.add(btn1, btn2, btn3, btn_check)
    
    text = "🚀 **Botdan foydalanish uchun barcha kanallarga obuna bo'ling!**"
    bot.send_message(user_id, text, reply_markup=markup, parse_mode="Markdown")

# --- START (Havolani tekshiradigan qismi to'g'rilandi) ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    text = message.text.split()
    
    # Havola orqali kelgan bo'lsa (masalan: /start jahannam1)
    if len(text) > 1:
        param = text[1]
        if check_sub(user_id):
            if param in animelar:
                data = animelar[param]
                bot.send_video(user_id, data['id'], thumb=THUMBNAIL, caption=f"🎬 {data['caption']}\n📢 @Anivoxuz", protect_content=True, supports_streaming=True)
            else:
                bot.send_message(user_id, "❌ Bunday anime topilmadi.")
        else:
            show_sub_menu(user_id, param)
        return # Havola bo'lsa, pastdagi kutib olish xabari chiqmaydi

    # Oddiy /start bosilganda
    welcome_text = "⛩️ **ANIVOX — Animelar olamiga xush kelibsiz!**\n\nBarcha animelar shu yerda: @Anivoxnews"
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_keyboard(), parse_mode="Markdown")

# --- QOLGAN BO'LIMLAR ---
@bot.message_handler(func=lambda m: "Reklama" in m.text or "Hamkorlik" in m.text)
def ads_handler(message):
    bot.send_message(message.chat.id, "📢 **Murojaat uchun admin:** @Tobi_sensey", parse_mode="Markdown")

@bot.message_handler(func=lambda m: "ro'yxati" in m.text)
def list_handler(message):
    bot.send_message(message.chat.id, "⛩️ **Ro'yxat:**\n🔥 Jahannam Jannati (1-2)\n🌸 Sening isming", parse_mode="Markdown")

@bot.message_handler(func=lambda m: "izlash" in m.text)
def search_mode(message):
    msg = bot.send_message(message.chat.id, "🔍 Anime nomini yozing:", reply_markup=cancel_keyboard())
    bot.register_next_step_handler(msg, process_search)

def process_search(message):
    if message.text == "❌ Bekor qilish":
        bot.send_message(message.chat.id, "Bekor qilindi.", reply_markup=main_keyboard())
        return
    # Qidiruv logikasi shu yerda davom etadi...

@bot.callback_query_handler(func=lambda call: call.data.startswith("check_sub_"))
def callback_check(call):
    param = call.data.replace("check_sub_", "")
    if check_sub(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        if param in animelar:
            data = animelar[param]
            bot.send_video(call.message.chat.id, data['id'], caption=f"🎬 {data['caption']}", supports_streaming=True)
        else:
            bot.send_message(call.message.chat.id, "Tasdiqlandi! Endi izlashingiz mumkin.", reply_markup=main_keyboard())
    else:
        bot.answer_callback_query(call.id, "❌ Hali obuna bo'lmagansiz!", show_alert=True)

if __name__ == "__main__":
    bot.remove_webhook()
    keep_alive()
    bot.polling(none_stop=True)
  
