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
    t.start()
# -----------------------------------------

# 1. BOT SOZLAMALARI
TOKEN = '7747703136:AAFbeOSwtodo7r_TS_sefsso1_naLSm2iVg'
KANAL_ID = '@Ani_Vox'
MAXFIY_KANAL = 'https://t.me/+oxPibE-r26c2NjM6'
INSTAGRAM = 'https://www.instagram.com/anivox.uz?igsh=MWJ3dWl1cWNxcHYzbA=='
THUMBNAIL = 'AgACAgIAAxkBAAICO2mG2hA7vlhpJpMaUGrDTyh0xu-PAALrC2sb1-s5SIBYET5mha17AQADAgADeAADOgQ'

# 🎬 ANIME RO'YXATI (1-13 QISMLAR)
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
    'sening': {'id': 'BAACAgIAAxkBAAIEPWmRfKeh-gtFnCxMI9jaOZ2_0T3RAAIpjwACrsw4SMeotftkaOVWOgQ', 'caption': 'Sening isming [1-Film]'}
}

bot = telebot.TeleBot(TOKEN)

def check_sub(user_id):
    try:
        status = bot.get_chat_member(KANAL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    text = message.text.split()

    if len(text) <= 1:
        bot.send_message(user_id, f"👋 Salom! Botga xush kelibsiz.\nBarcha animelar shu yerda👉: {KANAL_ID}")
        return

    param = text[1]

    # --- BARCHA QISMLARNI TASHLAIDIGAN QISM ---
    if param == 'all_jahannam':
        if check_sub(user_id):
            bot.send_message(user_id, "🎬 Jahannam Jannati: 1-Fasl (Barcha qismlar) yuborilmoqda...")
            for i in range(1, 14):
                key = f'jahannam{i}'
                if key in animelar:
                    bot.send_video(
                        user_id, 
                        animelar[key]['id'], 
                        thumb=THUMBNAIL, 
                        caption=f"🎬 {animelar[key]['caption']}\n📢 @Ani_Vox",
                        protect_content=True
                    )
                    time.sleep(1) # Telegram bloklamasligi uchun
        else:
            show_sub_menu(user_id, param)
        return

    # --- BITTA QISM UCHUN ---
    if param in animelar:
        if check_sub(user_id):
            video = animelar[param]
            bot.send_video(user_id, video['id'], thumb=THUMBNAIL, caption=f"🎬 {video['caption']}\n📢 @Ani_Vox", protect_content=True)
        else:
            show_sub_menu(user_id, param)
    else:
        bot.send_message(user_id, "😔 Anime topilmadi.")

def show_sub_menu(user_id, param):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("Animelar - Uzbek Tilida✅", url=f"https://t.me/{KANAL_ID[1:]}")
    btn2 = types.InlineKeyboardButton("Mahfiy kanal✅", url=MAXFIY_KANAL)
    btn3 = types.InlineKeyboardButton("Instagram✅", url=INSTAGRAM)
    btn_check = types.InlineKeyboardButton("🔄 Tekshirish 🔄", callback_data=f"check_{param}")
    markup.add(btn1, btn2, btn3, btn_check)
    bot.send_message(user_id, "❗ Ko'rish uchun quyidagi kanallarga obuna bo'ling:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("check_"))
def callback_check(call):
    param = call.data.replace("check_", "")
    user_id = call.from_user.id
    
    if check_sub(user_id):
        bot.answer_callback_query(call.id, "✅ Rahmat!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        
        # Obunadan keyin nima tashlab berishni aniqlash
        if param == 'all_jahannam':
            # Start funksiyasini qayta chaqirish yoki shunchaki yuborish
            message = call.message
            message.text = f"/start all_jahannam"
            start(message)
        elif param in animelar:
            video = animelar[param]
            bot.send_video(user_id, video['id'], thumb=THUMBNAIL, caption=f"🎬 {video['caption']}\n📢 @Ani_Vox", protect_content=True)
    else:
        bot.answer_callback_query(call.id, "❌ Obuna bo'lmagansiz!", show_alert=True)

# ... (get_id funksiyasi va main qismi o'zgarishsiz qoladi)
