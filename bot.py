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
    'jahannam1': {'id': 'BAACAgIAAyEFAATjsRFeAAM2aYT54IGZzyEi5CPiCvU8WNRgId0AAj6XAAKCriFIW68yMzkL46s4BA', 'caption': 'Jahannam Jannati [1-Qism]'},
    'jahannam2': {'id': 'BAACAgIAAyEFAATjsRFeAAM5aYT8oJh3F7GrK2CyojfZ1VrnP-MAAmeTAAJsBylItxjYydrL6Qo4BA', 'caption': 'Jahannam Jannati [2-Qism]'},
    'jahannam3': {'id': 'BAACAgIAAxkBAAIChWmHaXNeZyWoLbpaXu5rizAHeFWEAAKtkAACXgJBSPSArg0hC0iKOgQ', 'caption': 'Jahannam Jannati [3-Qism]'},
    'jahannam4': {'id': 'BAACAgIAAxkBAAICrWmIflJBcPpMShatlvx1vKJYP6ZOAAI6kwACXgJBSPOVZ6w6WrDJOgQ', 'caption': 'Jahannam Jannati [4-Qism]'},
    'jahannam5': {'id': 'BAACAgIAAxkBAAIDu2mPOKoZjIEPyY2qcuG3ono9blQ9AALqjwACrxBxSCyQp5QIZf4IOgQ', 'caption': 'Jahannam Jannati [5-Qism]'},
    'jahannam6': {'id': 'BAACAgIAAxkBAAIEOWmQmmPA7CtOxdxEiEn-sxmK_885AALxmgACGPqISCytSobWdKdkOgQ', 'caption': 'Jahannam Jannati [6-Qism]'},
    'jahannam7': {'id': 'BAACAgIAAxkBAAIEQGmRfQzCDi6cfpAhZk8DzAMsaQ_TAALBmwACGPqISKL90UBkoZgcOgQ', 'caption': 'Jahannam Jannati [7-Qism]'},
    'jahannam8': {'id': 'BAACAgIAAxkBAAIEiWmXZqizE31X4LuZJgHSZ4vlFPc5AALznAACGPqQSERBy1a5fEXMOgQ', 'caption': 'Jahannam Jannati [8-Qism]'},
    'jahannam9': {'id': 'BAACAgIAAxkBAAIEi2mXZrgS-or2yKYvHf1bLXr4KL-oAAIjowACnoO5SPXg2oO0hM0SOgQ', 'caption': 'Jahannam Jannati [9-Qism]'},
    'jahannam10': {'id': 'BAACAgIAAxkBAAIE7Wme9PoWv3ER8mPDCz-rfW7vrB7XAAKehwACnoPBSPRnda5ftNvxOgQ', 'caption': 'Jahannam Jannati [10-Qism]'},
    'jahannam11': {'id': 'BAACAgIAAxkBAAIE8Wmfnrb-v3_O_-uXFn9rx_7_HPMAA2OfAALWvwABSYngseA8X7e7OgQ', 'caption': 'Jahannam Jannati [11-Qism]'},
    'jahannam12': {'id': 'BAACAgIAAxkBAAIE9WmgEwxJ75Dx3EXAuBtU-2kbsanxAAJDjQACBt8BSbCIbCw1Cyh_OgQ', 'caption': 'Jahannam Jannati [12-Qism]'},
    'jahannam13': {'id': 'BAACAgIAAxkBAAIE92mgHSslGuS-xyTvvN-m7lOMXu1zAAIOjgACBt8BScGlXDDsjwdoOgQ', 'caption': 'Jahannam Jannati [13-Qism - 1-Fasl Finali]'},
    '2jahannam1': {'id': 'BAACAgIAAxkBAAIFpWml5b8ZNf0kc5u4Nje7JwEeS1etAAJlmwACJa8xST271BedaUOPOgQ', 'caption': 'Jahannam Jannati [2-Fasl 1-Qism]'},
    'sening': {'id': 'BAACAgIAAxkBAAIEPWmRfKeh-gtFnCxMI9jaOZ2_0T3RAAIpjwACrsw4SMeotftkaOVWOgQ', 'caption': 'Sening isming [1-Film]'}
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

# --- HANDLERLAR ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.send_message(message.chat.id, "👋 Xush kelibsiz! Bo'limni tanlang:", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text == "📜 Animelar ro'yxati")
def list_handler(message):
    text = "⛩️ **Botdagi mavjud animelar:**\n\n"
    seen_titles = set()
    for key, data in animelar.items():
        # Takrorlanmas nomlarni chiqarish (masalan, Jahannam Jannati bitta qator bo'lib chiqishi uchun)
        title = data['caption'].split('[')[0].strip()
        if title not in seen_titles:
            text += f"🔹 {title}\n"
            seen_titles.add(title)
    text += "\n🔍 Qidirish uchun **Anime izlash** tugmasidan foydalaning!"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "💵 Reklama va Hamkorlik")
def ads_handler(message):
    bot.send_message(message.chat.id, "📢 **Reklama va Hamkorlik**\n\n👤 Admin: @Tobi_sensey", parse_mode="Markdown")

# --- QIDIRUV ---
@bot.message_handler(func=lambda m: m.text == "🔍 Anime izlash")
def search_mode(message):
    if check_sub(message.from_user.id):
        msg = bot.send_message(message.chat.id, "🔍 Anime nomini va qismini yozing (Masalan: Jahannam 1):", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(msg, process_search)
    else:
        # Obuna bo'lmagan bo'lsa... (oldingi show_sub_menu mantiqi shu yerga keladi)
        bot.send_message(message.chat.id, "Obuna bo'lmagansiz!")

def process_search(message):
    if message.text == "❌ Bekor qilish" or message.text == "/start":
        bot.send_message(message.chat.id, "Qidiruv to'xtatildi.", reply_markup=main_keyboard())
        return

    # Qidiruvni aniqroq qilish uchun raqamni alohida ajratamiz
    user_input = message.text.lower()
    # Raqamlarni ajratib olish (masalan: "Jahannam 1" -> ["1"])
    numbers_in_input = re.findall(r'\d+', user_input)
    
    found = False
    for k, data in animelar.items():
        caption_lower = data['caption'].lower()
        key_lower = k.lower()
        
        # 1. Agar foydalanuvchi raqam yozgan bo'lsa (Masalan: 1)
        if numbers_in_input:
            search_num = numbers_in_input[0]
            # Lug'atdagi kalit so'z (jahannam1) aynan shu raqam bilan tugashini tekshiramiz
            # Bu jahannam11, jahannam12 larni chiqarib tashlaydi
            if user_input.replace(search_num, "").strip() in caption_lower or user_input.replace(search_num, "").strip() in key_lower:
                if key_lower.endswith(search_num) and not key_lower.endswith(f"1{search_num}") and not key_lower.endswith(f"2{search_num}"):
                    # Yoki oddiyroq: key jahannam1 bo'lsa va user 1 yozsa:
                    if re.search(r'\b' + search_num + r'\b', caption_lower) or key_lower == user_input.replace(" ", ""):
                        bot.send_video(message.chat.id, data['id'], thumb=THUMBNAIL, caption=f"🎬 {data['caption']}\n📢 @Anivoxuz")
                        found = True
                        break # Faqat bitta aniq natija

        # 2. Agar raqam yozmagan bo'lsa, shunchaki nomini qidiradi
        elif user_input in caption_lower:
            bot.send_video(message.chat.id, data['id'], thumb=THUMBNAIL, caption=f"🎬 {data['caption']}\n📢 @Anivoxuz")
            found = True
            time.sleep(0.5)

    if not found:
        bot.send_message(message.chat.id, "❌ Aniq natija topilmadi. Masalan: 'Jahannam 1' deb yozib ko'ring.")
    
    msg = bot.send_message(message.chat.id, "Yana qidiramizmi? (Chiqish uchun 'Bekor qilish'ni bosing)", reply_markup=cancel_keyboard())
    bot.register_next_step_handler(msg, process_search)

if __name__ == "__main__":
    bot.remove_webhook()
    keep_alive()
    bot.polling(none_stop=True)
      
