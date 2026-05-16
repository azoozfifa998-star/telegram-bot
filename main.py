import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_USERNAME = "@Taqdimat1"
CHANNEL_LINK = "https://t.me/Taqdimat1"

async def check_subscription(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"خطأ: {e}")
        return False

async def send_subscribe_message(message_obj):
    keyboard = [
        [InlineKeyboardButton("اشترك في القناة", url=CHANNEL_LINK)],
        [InlineKeyboardButton("تحققت من المتابعة", callback_data="check_sub")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "لازم تتابع قناتنا أولاً عشان تستخدم البوت\n\nاضغط على الزر أدناه للمتابعة، ثم اضغط تحققت من المتابعة للمتابعة."
    await message_obj.reply_text(text, reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    is_subscribed = await check_subscription(user_id, context)
    if is_subscribed:
        await update.message.reply_text(f"أهلاً {update.effective_user.first_name}! البوت جاهز للاستخدام.")
    else:
        await send_subscribe_message(update.message)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "check_sub":
        user_id = query.from_user.id
        is_subscribed = await check_subscription(user_id, context)
        if is_subscribed:
            await query.edit_message_text(f"شكراً لاشتراكك {query.from_user.first_name}! البوت جاهز للاستخدام الآن.")
        else:
            await query.answer("لم تشترك بعد! اشترك في القناة أولاً", show_alert=True)

def main():
    app_bot = Application.builder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CallbackQueryHandler(button_handler))
    print("البوت شغال...")
    app_bot.run_polling()

if __name__ == "__main__":
    main()
