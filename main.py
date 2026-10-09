import os
import telebot
import google.generativeai as genai
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# جلب المفاتيح بأمان من متغيرات البيئة
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
أنت البوت الرسمي الذكي لمنصة ومجتمع "حاشد نت" (HashedNetBot).
مهامك هي:
1. الإجابة على استفسارات الأعضاء بأسلوب راقٍ ومحترم يعبر عن الأصالة والتراث والشهامة اليمنية.
2. توجيه وإرشاد من يريد الانضمام للتسجيل عبر المنصة أو متابعة القنوات الرسمية.
3. الرد بوضوح واختصار دون إطالة غير ضرورية.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def get_main_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    
    btn_website = InlineKeyboardButton("🌐 منصة حاشد نت", url="https://emolina-ecf12e.netlify.app")
    btn_telegram = InlineKeyboardButton("📢 القناة الرسمية", url="https://t.me/HashedNet")
    btn_whatsapp = InlineKeyboardButton("💬 مجتمع الواتساب", url="https://whatsapp.com")
    btn_help = InlineKeyboardButton("❓ كيف أنضم؟", callback_data="how_to_join")
    
    markup.add(btn_website, btn_telegram, btn_whatsapp, btn_help)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f"أهلاً وسهلاً بك يا **{message.from_user.first_name}** في بوت **منصة حاشد نت** الذكي! 🌿\n\n"
        "أنا هنا لمساعدتك والإجابة على استفساراتك حول المنصة، التراث، وتسهيل انضمامك لمجتمعنا عبر كافة المنصات.\n\n"
        "اختر من الأزرار أدناه أو اكتب سؤالك مباشرة:"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

@bot.message_handler(commands=['join', 'register'])
def join_command(message):
    join_text = (
        "✨ **خطوات الانضمام إلى شبكة ومنصة حاشد نت:**\n\n"
        "1️⃣ **التسجيل في المنصة:** اضغط على رابط المنصة أدناه وسجل دخولك برقم الهاتف أو حساب Google.\n"
        "2️⃣ **متابعة القناة:** اشترك في القناة ليصلك كل جديد ومهم.\n"
        "3️⃣ **مجموعة النقاش:** انضم إلى المجموعة للتعليق والمشاركة مع بقية الأعضاء.\n"
        "4️⃣ **مجتمع الواتساب:** انضم لمجموعتنا على الواتساب لمتابعة الأخبار العاجلة."
    )
    bot.reply_to(message, join_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        welcome_msg = (
            f"مرحباً بك يا **{new_member.first_name}** في مجتمع **حاشد نت**! 🇾🇪\n"
            "أنورت المجموعة بوجودك. يسعدنا انضمامك وتسجيلك في المنصة الرسمية عبر الزر أدناه."
        )
        bot.send_message(message.chat.id, welcome_msg, parse_mode="Markdown", reply_markup=get_main_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "how_to_join":
        info_text = (
            "📌 **للتسجيل الفوري:**\n"
            "افتح رابط المنصة الرسمي [من هنا](https://emolina-ecf12e.netlify.app)، "
            "ثم أدخل رقم هاتفك وكلمة المرور لتفعيل حسابك خلال ثوانٍ."
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, info_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_ai_chat(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "أهلاً بك! يمكنك استخدام الأزرار أدناه للوصول السريع إلى روابط منصة حاشد نت.", reply_markup=get_main_keyboard())

print("HashedNetBot is running...")
bot.infinity_polling()
