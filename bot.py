import telebot
from telebot import types
import time
from flask import Flask
from threading import Thread

# --- RENDER UCHUN QO'SHIMCHA (TEGMANG) ---
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
TOKEN = '7747703136:AAGBBw4IewUMVF8BjnoNzkZKlGXq-sqTJzM'
KANAL_ID = '@Ani_Vox'
MAXFIY_KANAL = 'https://t.me/+oxPibE-r26c2NjM6'
INSTAGRAM = 'https://www.instagram.com/anivox.uz?igsh=MWJ3dWl1cWNxcHYzbA=='

# 🎬 ANIME RO'YXATI
THUMBNAIL = 'AgACAgIAAxkBAAICO2mG2hA7vlhpJpMaUGrDTyh0xu-PAALrC2sb1-s5SIBYET5mha17AQADAgADeAADOgQ'

animelar = {
    'jahannam1': {
        'id': 'BAACAgIAAyEFAATjsRFeAAM2aYT54IGZzyEi5CPiCvU8WNRgId0AAj6XAAKCriFIW68yMzkL46s4BA',
        'caption': 'Jahannam Jannati [1-Qism]'
    },
    'jahannam2': {
        'id': 'BAACAgIAAyEFAATjsRFeAAM5aYT8oJh3F7GrK2CyojfZ1VrnP-MAAmeTAAJsBylItxjYydrL6Qo4BA',
        'caption': 'Jahannam Jannati [2-Qism]'
    },
    'jahannam3': {
        'id': 'BAACAgIAAxkBAAIChWmHaXNeZyWoLbpaXu5rizAHeFWEAAKtkAACXgJBSPSArg0hC0iKOgQ',
        'caption': 'Jahannam Jannati [3-Qism]'
    },
    'jahannam4': {
        'id': 'BAACAgIAAxkBAAICrWmIflJBcPpMShatlvx1vKJYP6ZOAAI6kwACXgJBSPOVZ6w6WrDJOgQ',
        'caption': 'Jahannam Jannati [4-Qism]'
    },
    'sening': {
        'id': 'BAACAgIAAxkBAAIDKWmMpSKHfbAFqHZz1iubLCBQSvPqAAIpjwACrsw4SMeotftkaOVWOgQ',
        'caption': 'Sening isming [1-Film]'
    },
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

    if len(text) == 1:
        bot.send_message(user_id, f"👋 Salom! Botga xush kelibsiz.\nAsosiy kanal: {KANAL_ID}")
        return

    anime_kodi = text[1]
    
    if anime_kodi in animelar:
        if check_sub(user_id):
            video = animelar[anime_kodi]
            bot.send_video(
                user_id, 
                video['id'], 
                thumb=THUMBNAIL, 
                caption=f"🎬 {video['caption']}\n📢 Asosiy kanal: {KANAL_ID}",
                protect_content=True
            )
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton("Animelar - Uzbek Tilida", url=f"https://t.me/{KANAL_ID[1:]}")
            btn2 = types.InlineKeyboardButton("Mahfiy kanal", url=MAXFIY_KANAL)
            btn3 = types.InlineKeyboardButton("Instagram", url=INSTAGRAM)
            btn_check = types.InlineKeyboardButton("🔄 Tekshirish 🔄", callback_data=f"check_{anime_kodi}")
            markup.add(btn1, btn2, btn3, btn_check)
            
            bot.send_message(user_id, "❗ Animeni ko'rish uchun quyidagi kanallarga obuna bo'ling:", reply_markup=markup)
    else:
        bot.send_message(user_id, "😔 Anime topilmadi.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("check_"))
def callback_check(call):
    anime_kodi = call.data.replace("check_", "")
    if check_sub(call.from_user.id):
        video = animelar[anime_kodi]
        bot.answer_callback_query(call.id, "✅ Rahmat!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_video(
            call.from_user.id, 
            video['id'], 
            thumb=THUMBNAIL, 
            caption=f"🎬 {video['caption']}\n📢 Asosiy kanal: {KANAL_ID}",
            protect_content=True
        )
    else:
        bot.answer_callback_query(call.id, "❌ Obuna bo'lmagansiz!", show_alert=True)

@bot.message_handler(content_types=['video', 'photo'])
def get_id(message):
    if message.content_type == 'video':
        bot.send_message(message.chat.id, f"{message.video.file_id}", parse_mode="Markdown")
    elif message.content_type == 'photo':
        bot.send_message(message.chat.id, f"{message.photo[-1].file_id}", parse_mode="Markdown")

if __name__ == "__main__":
    keep_alive() # Render port topishi uchun
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            time.sleep(5)
          
