import telebot
from telebot import types
import time
from flask import Flask
from threading import Thread

# --- RENDER UCHUN (BOTNI UYG'OQ SAQLASH) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is live!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
# -----------------------------------------

# 1. BOT SOZLAMALARI
TOKEN = '7747703136:AAFbeOSwtodo7r_TS_sefsso1_naLSm2iVg'
CHANNELS = ['@Anivoxuz', '@AniVoxnews', '-1002271291882'] 
MAXFIY_KANAL_LINK = 'https://t.me/+oxPibE-r26c2NjM6'
NEWS_KANAL_LINK = 'https://t.me/AniVoxnews'
THUMBNAIL = 'AgACAgIAAxkBAAICO2mG2hA7vlhpJpMaUGrDTyh0xu-PAALrC2sb1-s5SIBYET5mha17AQADAgADeAADOgQ'

# 🎬 ANIME RO'YXATI
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

# --- ASOSIY KLAVIATURA ---
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🔍 Anime izlash")
    btn2 = types.KeyboardButton("💵 Reklama va Hamkorlik")
    markup.add(btn1)
    markup.add(btn2)
    return markup

# 🔄 OBUNANI TEKSHIRISH FUNKSIYASI
def check_sub(user_id):
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            if status not in ['member', 'administrator', 'creator']:
                return False
        except Exception:
            continue
    return True

def show_sub_menu(user_id, param):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("Animelar || Uzbek Tilida⛩️✅", url=f"https://t.me/Anivoxuz")
    btn2 = types.InlineKeyboardButton("ANIVOX || NEWS⛩️✅", url=NEWS_KANAL_LINK)
    btn3 = types.InlineKeyboardButton("Maxfiy Kanal ✅", url=MAXFIY_KANAL_LINK)
    btn_check = types.InlineKeyboardButton("🔄 Obunani tekshirish 🔄", callback_data=f"check_{param}")
    markup.add(btn1, btn2, btn3, btn_check)
    text = "🚀 **Botdan foydalanish uchun barcha kanallarga obuna bo'ling!**"
    bot.send_message(user_id, text, reply_markup=markup, parse_mode="Markdown")

# --- START BUYRUG'I ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    text = message.text.split()
    
    # Oddiy start bosilganda
    if len(text) <= 1:
        bot.send_message(user_id, f"👋 Salom! Botga xush kelibsiz.\nBo'limni tanlang 👇", reply_markup=main_keyboard())
        return
    
    # Ssilka orqali (kod bilan) kelganda
    param = text[1]
    if check_sub(user_id):
        if param == 'all_jahannam':
            for i in range(1, 14):
                key = f'jahannam{i}'
                if key in animelar:
                    bot.send_video(user_id, animelar[key]['id'], thumb=THUMBNAIL, caption=f"🎬 {animelar[key]['caption']}\n📢 @Anivoxuz", protect_content=True, supports_streaming=True)
                    time.sleep(1.2)
        elif param in animelar:
            video = animelar[param]
            bot.send_video(user_id, video['id'], thumb=THUMBNAIL, caption=f"🎬 {video['caption']}\n📢 @Anivoxuz", protect_content=True, supports_streaming=True)
    else:
        show_sub_menu(user_id, param)

# --- KLAVIATURA TUGMALARI ISHLOVI ---

@bot.message_handler(func=lambda message: message.text == "🔍 Anime izlash")
def search_btn_click(message):
    # Avval obunani tekshiramiz
    if check_sub(message.from_user.id):
        msg = bot.send_message(message.chat.id, "🔍 Qidirayotgan anime nomini yozing (Masalan: Jahannam):")
        bot.register_next_step_handler(msg, process_search)
    else:
        show_sub_menu(message.from_user.id, "main")

def process_search(message):
    if message.text in ["🔍 Anime izlash", "💵 Reklama va Hamkorlik"]: # Agar boshqa tugmani bossa
        return 
    
    query = message.text.lower()
    found = False
    for key, data in animelar.items():
        if query in data['caption'].lower():
            bot.send_video(message.chat.id, data['id'], thumb=THUMBNAIL, caption=f"🎬 {data['caption']}\n📢 @Anivoxuz", protect_content=True, supports_streaming=True)
            found = True
            time.sleep(1)
    
    if not found:
        bot.send_message(message.chat.id, "❌ Bunday nomli anime topilmadi. Iltimos, boshqa nom yozib ko'ring.")
    
    # Qidiruvdan keyin yana menyuni qaytaramiz
    bot.send_message(message.chat.id, "Yana biror narsa qidiramizmi?", reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: message.text == "💵 Reklama va Hamkorlik")
def ads_btn_click(message):
    text = (
        "📢 **Reklama va Hamkorlik bo'limi**\n\n"
        "Barcha savollar bo'yicha adminga murojaat qiling:\n\n"
        "👤 Admin: @Tobi_sensey"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# --- CALLBACK (OBUNA TEKSHIRISH TUGMASI) ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("check_"))
def callback_check(call):
    param = call.data.replace("check_", "")
    user_id = call.from_user.id
    if check_sub(user_id):
        bot.answer_callback_query(call.id, "✅ Rahmat! Obuna tasdiqlandi.")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        if param == 'all_jahannam':
            for i in range(1, 14):
                key = f'jahannam{i}'
                if key in animelar:
                    bot.send_video(user_id, animelar[key]['id'], thumb=THUMBNAIL, caption=f"🎬 {animelar[key]['caption']}\n📢 @Anivoxuz", protect_content=True, supports_streaming=True)
                    time.sleep(1.2)
        elif param in animelar:
            video = animelar[param]
            bot.send_video(user_id, video['id'], thumb=THUMBNAIL, caption=f"🎬 {video['caption']}\n📢 @Anivoxuz", protect_content=True, supports_streaming=True)
        else:
            bot.send_message(user_id, "Endi botdan foydalanishingiz mumkin!", reply_markup=main_keyboard())
    else:
        bot.answer_callback_query(call.id, "❌ Hali hamma kanallarga obuna bo'lmagansiz!", show_alert=True)

# --- VIDEO VA RASM ID OLISH ---
@bot.message_handler(content_types=['video', 'photo'])
def get_id(message):
    if message.content_type == 'video':
        bot.send_message(message.chat.id, f"Anime ID: `{message.video.file_id}`", parse_mode="Markdown")
    elif message.content_type == 'photo':
        bot.send_message(message.chat.id, f"Thumb ID: `{message.photo[-1].file_id}`", parse_mode="Markdown")

if __name__ == "__main__":
    bot.remove_webhook()
    keep_alive()
    bot.polling(none_stop=True)
