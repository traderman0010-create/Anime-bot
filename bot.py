import telebot
from telebot import types
import time
from flask import Flask
from threading import Thread
import re

# --- RENDER UCHUN (24/7 ISHLASHI UCHUN) ---
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
bot = telebot.TeleBot(TOKEN)

# FAQAT 2 TA ASOSIY KANAL (Bot admin bo'lishi shart!)
CHANNELS = ['@anivoxuz', '@AniVoxnews'] 

# Linklar
MAIN_CHANNEL = 'https://t.me/anivoxuz'
NEWS_CHANNEL = 'https://t.me/AniVoxnews'

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
    '2jahannam2': {'id': 'BAACAgIAAxkBAAIF9WmruB75Pb4BdSHl8jvjwhGcnNQXAALPjwACBClhSaedW75iKE0tOgQ', 'caption': 'Jahannam Jannati [2-Fasl 2-Qism]'},
    '2jahannam3': {'id': 'BAACAgIAAxkBAAIF9WmruB75Pb4BdSHl8jvjwhGcnNQXAALPjwACBClhSaedW75iKE0tOgQ', 'caption': 'Jahannam Jannati [2-Fasl 3-Qism]'},
    '2jahannam4': {'id': 'BAACAgIAAxkBAAIF_mmuHcoi9DGLB36gpFueo4xMYhDCAAIwlQACx35xSYZSb6aLlf-nOgQ', 'caption': 'Jahannam Jannati [2-Fasl 4-Qism]'},
    'sening': {'id': 'BAACAgIAAxkBAAIEPWmRfKeh-gtFnCxMI9jaOZ2_0T3RAAIpjwACrsw4SMeotftkaOVWOgQ', 'caption': 'Sening isming [Film]'}
}

# --- OBUNA TEKSHIRISH ---
def check_sub(user_id):
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            if status not in ['member', 'administrator', 'creator']:
                return False
        except Exception as e:
            print(f"Xato: {channel} da bot admin emas!")
            return False
    return True

# --- INLINE KNOPKALAR (UZUN VARIANT) ---
def show_sub_menu(user_id, param="search"):
    markup = types.InlineKeyboardMarkup()
    
    # Tugmalarni cho'zish uchun probellar bilan to'ldirildi
    btn1 = types.InlineKeyboardButton("Anivox                ||                Animelar ⛩️✅", url=MAIN_CHANNEL)
    btn2 = types.InlineKeyboardButton("Anivox                ||                AnimeNews ❗✅", url=NEWS_CHANNEL)
    btn_check = types.InlineKeyboardButton("🔄  OBUNANI TASDIQLASH  🔄", callback_data=f"check_sub_{param}")
    
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn_check)
    
    text = "🚀 **Botdan foydalanish uchun kanallarga obuna bo'ling!**\n\nObuna bo'lgach, pastdagi tasdiqlash tugmasini bosing."
    bot.send_message(user_id, text, reply_markup=markup, parse_mode="Markdown")

# --- START ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    text = message.text.split()
    
    if len(text) > 1:
        param = text[1]
        if check_sub(user_id):
            if param in animelar:
                bot.send_video(user_id, animelar[param]['id'], caption=f"🎬 {animelar[param]['caption']}\n📢 @Anivoxuz")
            return
        else:
            show_sub_menu(user_id, param)
            return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("🔍 Anime izlash"), types.KeyboardButton("📜 Animelar ro'yxati"))
    markup.row(types.KeyboardButton("💵 Reklama va Hamkorlik"))
    bot.send_message(user_id, "⛩️ **ANIVOX — Animelar olamiga xush kelibsiz!**", reply_markup=markup, parse_mode="Markdown")

# --- IZLASH ---
@bot.message_handler(func=lambda m: "izlash" in m.text)
def search_mode(message):
    if check_sub(message.from_user.id):
        msg = bot.send_message(message.chat.id, "🔍 Anime nomini yozing:", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("❌ Bekor qilish"))
        bot.register_next_step_handler(msg, process_search)
    else:
        show_sub_menu(message.from_user.id, "search")

def process_search(message):
    if message.text == "❌ Bekor qilish":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(types.KeyboardButton("🔍 Anime izlash"), types.KeyboardButton("📜 Animelar ro'yxati"))
        markup.row(types.KeyboardButton("💵 Reklama va Hamkorlik"))
        bot.send_message(message.chat.id, "Bekor qilindi.", reply_markup=markup)
        return
    
    user_input = message.text.lower()
    found = False
    for key, data in animelar.items():
        if user_input in data['caption'].lower():
            bot.send_video(message.chat.id, data['id'], caption=f"🎬 {data['caption']}\n📢 @Anivoxuz")
            found = True
            break
    if not found:
        bot.send_message(message.chat.id, "❌ Topilmadi.")

# --- CALLBACK ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("check_sub_"))
def callback_check(call):
    param = call.data.replace("check_sub_", "")
    if check_sub(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        if param in animelar:
            bot.send_video(call.from_user.id, animelar[param]['id'], caption=f"🎬 {animelar[param]['caption']}")
        else:
            bot.send_message(call.from_user.id, "✅ Obuna tasdiqlandi! Endi botdan foydalana olasiz.")
    else:
        bot.answer_callback_query(call.id, "❌ Hali hamma kanallarga obuna bo'lmagansiz!", show_alert=True)

# --- RO'YXAT VA REKLAMA ---
@bot.message_handler(func=lambda m: "ro'yxati" in m.text)
def list_handler(message):
    bot.send_message(message.chat.id, "📜 Animelar ro'yxati yaqin kunlarda yangilanadi.")

@bot.message_handler(func=lambda m: "Reklama" in m.text)
def ads_handler(message):
    bot.send_message(message.chat.id, "📢 Reklama uchun: @Tobi_sensey")

if __name__ == "__main__":
    bot.remove_webhook()
    keep_alive()
    bot.polling(none_stop=True)
  
