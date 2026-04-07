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
TOKEN = '7747703136:AAFbeOSwtodo7r_TS_sefsso1_naLSm2iVg' # Tokeningizni xavfsiz saqlang!
bot = telebot.TeleBot(TOKEN)

# Kanallar ro'yxati (ID yoki username)
# Zayafka kanalingiz ID-sini kiritishingiz kerak (masalan: -100...)
CHANNELS = ['@anivoxuz', '@AniVoxnews', '-1002271291882'] 

# Linklar
MAIN_CHANNEL = 'https://t.me/anivoxuz'
NEWS_CHANNEL = 'https://t.me/AniVoxnews'
ZAYAFKA_CHANNEL = 'https://t.me/+_D6al-MME8RmZmFi'

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
        except:
            return False # Bot admin bo'lmasa yoki xato bo'lsa False
    return True

def show_sub_menu(user_id, param="search"):
    markup = types.InlineKeyboardMarkup(row_width=1)
    # Sen so'ragan uzun va chiroyli tugmalar
    btn1 = types.InlineKeyboardButton("Anivox     ||   Animelar ⛩️✅", url=MAIN_CHANNEL)
    btn2 = types.InlineKeyboardButton("Anivox    ||  AnimeNews ❗✅", url=NEWS_CHANNEL)
    btn3 = types.InlineKeyboardButton("Anivox    ||  zayafka♻️⛩️", url=ZAYAFKA_CHANNEL)
    btn_check = types.InlineKeyboardButton("🔄 OBUNANI TASDIQLASH 🔄", callback_data=f"check_sub_{param}")
    markup.add(btn1, btn2, btn3, btn_check)
    
    text = "🚀 **Botdan foydalanish uchun barcha kanallarga obuna bo'ling!**\n\nObuna bo'lgach, 'Obunani tasdiqlash' tugmasini bosing."
    bot.send_message(user_id, text, reply_markup=markup, parse_mode="Markdown")

# --- START (LINK VA ODDIY KIRISH) ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    text = message.text.split()
    
    # Kanaldan link (parametr) bilan kelsa
    if len(text) > 1:
        param = text[1]
        if check_sub(user_id):
            if param in animelar:
                data = animelar[param]
                bot.send_video(user_id, data['id'], thumb=THUMBNAIL, caption=f"🎬 {data['caption']}\n📢 @Anivoxuz", supports_streaming=True)
            else:
                bot.send_message(user_id, "❌ Bunday anime topilmadi.")
        else:
            show_sub_menu(user_id, param)
        return

    # Oddiy kirish
    bot.send_message(user_id, "⛩️ **ANIVOX — Animelar olamiga xush kelibsiz!**", reply_markup=main_keyboard(), parse_mode="Markdown")

# --- RO'YXAT (OBUNASIZ ISHLAYDI) ---
@bot.message_handler(func=lambda m: "ro'yxati" in m.text)
def list_handler(message):
    list_text = (
        "⛩️ **Mavjud animelar ro'yxati:**\n\n"
        "🔥 **Jahannam Jannati:**\n"
        "• 1-Fasl (1-13 qismlar)\n"
        "• 2-Fasl (1-4 qismlar)\n\n"
        "🌸 **To'liq metrajli:**\n"
        "• Sening isming (Film)\n"
    )
    bot.send_message(message.chat.id, list_text, parse_mode="Markdown")

# --- QIDIRUV (OBUNA TALAB QILADI) ---
@bot.message_handler(func=lambda m: "izlash" in m.text)
def search_mode(message):
    user_id = message.from_user.id
    if check_sub(user_id):
        msg = bot.send_message(message.chat.id, "🔍 Anime nomini yozing:", reply_markup=cancel_keyboard())
        bot.register_next_step_handler(msg, process_search)
    else:
        show_sub_menu(user_id, "search")

def process_search(message):
    if message.text == "❌ Bekor qilish" or message.text == "/start":
        bot.send_message(message.chat.id, "Qidiruv to'xtatildi.", reply_markup=main_keyboard())
        return

    user_input = message.text.lower()
    num = re.findall(r'\d+', user_input)
    
    search_key = ""
    if len(num) >= 2:
        if num[0] == "2": search_key = f"2jahannam{num[1]}"
        else: search_key = f"jahannam{num[1]}"
    elif len(num) == 1:
        if "2" in user_input and user_input.index("2") < 3: search_key = f"2jahannam{num[0]}"
        else: search_key = f"jahannam{num[0]}"
    
    if search_key in animelar:
        data = animelar[search_key]
        bot.send_video(message.chat.id, data['id'], thumb=THUMBNAIL, caption=f"🎬 {data['caption']}\n📢 @Anivoxuz", supports_streaming=True)
    else:
        bot.send_message(message.chat.id, "❌ Topilmadi.")
    
    msg = bot.send_message(message.chat.id, "Yana qidiramizmi?", reply_markup=cancel_keyboard())
    bot.register_next_step_handler(msg, process_search)

# --- CALLBACK (OBUNANI TEKSHIRISH TUGMASI) ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("check_sub_"))
def callback_check(call):
    param = call.data.replace("check_sub_", "")
    user_id = call.from_user.id
    
    if check_sub(user_id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        if param in animelar:
            # Agar foydalanuvchi linkdan kelib keyin obuna bo'lgan bo'lsa, videoni yuboramiz
            data = animelar[param]
            bot.send_video(user_id, data['id'], thumb=THUMBNAIL, caption=f"🎬 {data['caption']}\n📢 @Anivoxuz", supports_streaming=True)
        else:
            bot.send_message(user_id, "✅ Tasdiqlandi! Endi botdan foydalanishingiz mumkin.", reply_markup=main_keyboard())
    else:
        bot.answer_callback_query(call.id, "❌ Hali barcha kanallarga obuna bo'lmagansiz!", show_alert=True)

# --- REKLAMA (OBUNASIZ ISHLAYDI) ---
@bot.message_handler(func=lambda m: "Reklama" in m.text or "Hamkorlik" in m.text)
def ads_handler(message):
    bot.send_message(message.chat.id, "📢 Murojaat uchun bosh admin: @Tobi_sensey⛩️✅")

# --- ISHGA TUSHIRISH ---
if __name__ == "__main__":
    bot.remove_webhook()
    keep_alive() # Render uchun
    bot.polling(none_stop=True)
  
