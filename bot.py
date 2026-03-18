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
    # 1-Fasl
    'jahannam1': {'id': 'BAACAgIAAyEFAATjsRFeAAM2aYT54IGZzyEi5CPiCvU8WNRgId0AAj6XAAKCriFIW68yMzkL46s4BA', 'caption': 'Jahannam Jannati [1-Fasl 1-Qism]'},
    'jahannam2': {'id': 'BAACAgIAAyEFAATjsRFeAAM5aYT8oJh3F7GrK2CyojfZ1VrnP-MAAmeTAAJsBylItxjYydrL6Qo4BA', 'caption': 'Jahannam Jannati [1-Fasl 2-Qism]'},
    'jahannam3': {'id': 'BAACAgIAAxkBAAIChWmHaXNeZyWoLbpaXu5rizAHeFWEAAKtkAACXgJBSPSArg0hC0iKOgQ', 'caption': 'Jahannam Jannati [1-Fasl 3-Qism]'},
    'jahannam4': {'id': 'BAACAgIAAxkBAAICrWmIflJBcPpMShatlvx1vKJYP6ZOAAI6kwACXgJBSPOVZ6w6WrDJOgQ', 'caption': 'Jahannam Jannati [1-Fasl 4-Qism]'},
    'jahannam5': {'id': 'BAACAgIAAxkBAAIDu2mPOKoZjIEPyY2qcuG3ono9blQ9AALqjwACrxBxSCyQp5QIZf4IOgQ', 'caption': 'Jahannam Jannati [1-Fasl 5-Qism]'},
    'jahannam13': {'id': 'BAACAgIAAxkBAAIE92mgHSslGuS-xyTvvN-m7lOMXu1zAAIOjgACBt8BScGlXDDsjwdoOgQ', 'caption': 'Jahannam Jannati [1-Fasl 13-Qism Final]'},
    
    # 2-Fasl (Qidiruvda oson bo'lishi uchun '2jahannam' deb nomlangan)
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
    
    text = "🚀 **Botdan foydalanish uchun barcha kanallarga obuna bo'ling!**\n\nPastdagi tugmalar orqali a'zo bo'lib, tasdiqlashni bosing. 👇"
    bot.send_message(user_id, text, reply_markup=markup, parse_mode="Markdown")

# --- START ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    welcome_text = "⛩️ **ANIVOX — Animelar olamiga xush kelibsiz!**\n\nBarcha animelar shu yerda: @Anivoxnews"
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_keyboard(), parse_mode="Markdown")

# --- HAMKORLIK TUGMASI (MATN SHU YERDA) ---
@bot.message_handler(func=lambda m: m.text == "💵 Reklama va Hamkorlik")
def ads_handler(message):
    reklama_matni = (
        "📢 **ANIVOX — Reklama va Hamkorlik bo'limi**\n\n"
        "Loyihangizni biz bilan birga rivojlantiring! 🚀\n\n"
        "✅ **Xizmatlarimiz:**\n"
        "• Kanallarga va botga reklama joylash\n"
        "• O'zaro hamkorlik (VP)\n"
        "• Maqsadli auditoriyaga xabar yuborish\n\n"
        "💳 **To'lovlar:** Click, Payme, Uzum orqali.\n\n"
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
        "🔍 Izlash uchun **'Jahannam 1'** yoki **'2-fasl 1'** deb yozing!"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# --- QIDIRUV REJIMI ---
@bot.message_handler(func=lambda m: m.text == "🔍 Anime izlash")
def search_mode(message):
    if check_sub(message.from_user.id):
        msg = bot.send_message(message.chat.id, "🔍 Anime nomini va qismini yozing:\n\n*(Masalan: 'Jahannam 1' yoki '2-fasl 1')*", reply_markup=cancel_keyboard(), parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_search)
    else:
        show_sub_menu(message.chat.id, "search")

# --- AQLLI QIDIRUV (2-FASL UCHUN HAM) ---
def process_search(message):
    if message.text == "❌ Bekor qilish" or message.text == "/start":
        bot.send_message(message.chat.id, "Qidiruv to'xtatildi.", reply_markup=main_keyboard())
        return

    user_input = message.text.lower()
    
    # 2-faslni qidirishni osonlashtirish (foydalanuvchi '2-fasl 1' deb yozsa, uni '2jahannam1'ga o'tkazamiz)
    if "2" in user_input and ("fasl" in user_input or "jahannam" in user_input or "qism" in user_input):
        num = re.findall(r'\d+', user_input)
        # Agar foydalanuvchi "2-fasl 1" deb yozsa, num=['2', '1'] bo'ladi. Bizga ikkinchi raqam kerak.
        if len(num) >= 2:
            search_key = f"2jahannam{num[1]}"
        else:
            search_key = f"2jahannam{num[0]}" if num else ""
    else:
        # Oddiy 1-fasl uchun
        num = re.findall(r'\d+', user_input)
        search_key = f"jahannam{num[0]}" if num else user_input.replace(" ", "")

    found = False
    for k, data in animelar.items():
        if k == search_key:
            bot.send_video(message.chat.id, data['id'], thumb=THUMBNAIL, caption=f"🎬 {data['caption']}\n📢 @Anivoxuz", supports_streaming=True)
            found = True
            break
        
    if not found:
        # Agar aniq kalit bilan topilmasa, captiondan qidirib ko'radi
        for k, data in animelar.items():
            if user_input.replace(" ", "") in data['caption'].lower().replace(" ", ""):
                bot.send_video(message.chat.id, data['id'], thumb=THUMBNAIL, caption=f"🎬 {data['caption']}\n📢 @Anivoxuz", supports_streaming=True)
                found = True
                break

    if not found:
        bot.send_message(message.chat.id, "❌ Anime topilmadi. To'g'ri yozganingizga ishonch hosil qiling.\nMasalan: 'Jahannam 1' yoki '2-fasl 1'")
    
    msg = bot.send_message(message.chat.id, "Yana qidiramizmi? (Chiqish uchun 'Bekor qilish'ni bosing)", reply_markup=cancel_keyboard())
    bot.register_next_step_handler(msg, process_search)

@bot.callback_query_handler(func=lambda call: call.data.startswith("check_sub_"))
def callback_check(call):
    if check_sub(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Tasdiqlandi!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Xush kelibsiz! Anime izlashni boshlashingiz mumkin.", reply_markup=main_keyboard())
    else:
        bot.answer_callback_query(call.id, "❌ Hali hamma kanallarga obuna bo'lmagansiz!", show_alert=True)

if __name__ == "__main__":
    bot.remove_webhook()
    keep_alive()
    bot.polling(none_stop=True)
  
