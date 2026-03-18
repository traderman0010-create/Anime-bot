import telebot
from telebot import types
import time
from flask import Flask
from threading import Thread
import re

# --- RENDER UCHUN (BOTNI UYG'OQ SAQLASH) ---
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
    # 1-Fasl
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
    
    # 2-Fasl
    '2jahannam1': {'id': 'BAACAgIAAxkBAAIFpWml5b8ZNf0kc5u4Nje7JwEeS1etAAJlmwACJa8xST271BedaUOPOgQ', 'caption': 'Jahannam Jannati [2-Fasl 1-Qism]'},
    
    # Film
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
    
    text = "🚀 **Botdan foydalanish uchun barcha kanallarga obuna bo'ling!**\n\nPastdagi tugmalar orqali a'zo bo'lib, tasdiqlashni bosing. 👇"
    bot.send_message(user_id, text, reply_markup=markup, parse_mode="Markdown")

# --- START ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    welcome_text = "⛩️ **ANIVOX — Animelar olamiga xush kelibsiz!**\n\nBarcha animelar shu yerda: @Anivoxnews"
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_keyboard(), parse_mode="Markdown")

# --- REKLAMA VA HAMKORLIK (To'g'rilangan) ---
@bot.message_handler(func=lambda m: m.text == "💵 Reklama va Hamkorlik")
def ads_handler(message):
    reklama_matni = (
        "📢 **ANIVOX — Reklama va Hamkorlik bo'limi**\n\n"
        "Loyihangizni biz bilan birga rivojlantiring! 🚀\n\n"
        "✅ **Xizmatlarimiz:**\n"
        "• Kanallarga va botga reklama joylash\n"
        "• O'zaro hamkorlik (VP)\n"
        "• Maqsadli auditoriyaga xabar yuborish\n\n"
        "👤 **Murojaat uchun admin:** @Tobi_sensey"
    )
    bot.send_message(message.chat.id, reklama_matni, parse_mode="Markdown")

# --- RO'YXAT ---
@bot.message_handler(func=lambda m: m.text == "📜 Animelar ro'yxati")
def list_handler(message):
    text = (
        "⛩️ **Botdagi mavjud animelar:**\n\n"
        "🔥 Jahannam Jannati: 1-Fasl\n"
        "🌀 Jahannam Jannati: 2-Fasl\n"
        "🌸 Sening isming (Film)\n\n"
        "🔍 Izlash uchun **'Jahannam 1'** yoki **'2 1'** deb yozing!"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# --- QIDIRUV ---
@bot.message_handler(func=lambda m: m.text == "🔍 Anime izlash")
def search_mode(message):
    if check_sub(message.from_user.id):
        msg = bot.send_message(message.chat.id, "🔍 Anime nomini va qismini yozing:\n\n*(Masalan: 'Jahannam 1' yoki '2 1')*", reply_markup=cancel_keyboard(), parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_search)
    else:
        show_sub_menu(message.chat.id, "search")

def process_search(message):
    if message.text == "❌ Bekor qilish" or message.text == "/start":
        bot.send_message(message.chat.id, "Qidiruv to'xtatildi.", reply_markup=main_keyboard())
        return

    user_input = message.text.lower()
    num = re.findall(r'\d+', user_input)
    
    search_key = ""
    # Agar 2 ta raqam bo'lsa (masalan: "Jahannam 2 1")
    if len(num) >= 2:
        if num[0] == "2": search_key = f"2jahannam{num[1]}"
        else: search_key = f"jahannam{num[1]}"
    # Agar 1 ta raqam bo'lsa (masalan: "Jahannam 1" yoki "2 1")
    elif len(num) == 1:
        if "2" in user_input and user_input.index("2") < user_input.find(num[0]) + len(num[0]):
             # Bu qism 2-fasl ekanligini taxmin qiladi
             if user_input.strip().startswith("2"): search_key = f"2jahannam{num[0]}"
             else: search_key = f"jahannam{num[0]}"
        else:
            search_key = f"jahannam{num[0]}"
    
    found = False
    # 1. Aniq kalit bo'yicha qidirish
    if search_key in animelar:
        data = animelar[search_key]
        bot.send_video(message.chat.id, data['id'], thumb=THUMBNAIL, caption=f"🎬 {data['caption']}\n📢 @Anivoxuz", supports_streaming=True)
        found = True
    
    # 2. Agar topilmasa, captiondan qidirish
    if not found:
        for k, data in animelar.items():
            if user_input.replace(" ", "") in data['caption'].lower().replace(" ", ""):
                bot.send_video(message.chat.id, data['id'], thumb=THUMBNAIL, caption=f"🎬 {data['caption']}\n📢 @Anivoxuz", supports_streaming=True)
                found = True
                break

    if not found:
        bot.send_message(message.chat.id, "❌ Topilmadi. Masalan: 'Jahannam 1' yoki '2 1' deb yozing.")
    
    msg = bot.send_message(message.chat.id, "Yana qidiramizmi?", reply_markup=cancel_keyboard())
    bot.register_next_step_handler(msg, process_search)

@bot.callback_query_handler(func=lambda call: call.data.startswith("check_sub_"))
def callback_check(call):
    if check_sub(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Tasdiqlandi!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Xush kelibsiz!", reply_markup=main_keyboard())
    else:
        bot.answer_callback_query(call.id, "❌ Obuna bo'lmagansiz!", show_alert=True)

if __name__ == "__main__":
    bot.remove_webhook()
    keep_alive()
    bot.polling(none_stop=True)
  
