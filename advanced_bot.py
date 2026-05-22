# advanced_bot.py - Telegram bot for Andromeda Bingo

import os
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ========== CONFIGURATION ==========
BBOT_TOKEN = os.environ.get("BOT_TOKEN", "8423271349:AAGIeHFDKh4-phGJ_W9ao65N-YlDgZSyS10")
WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://andromeda-bingo-bot.onrender.com")
OWNER_ID = int(os.environ.get("OWNER_ID", " 840648715"))


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def call_api(endpoint, method='GET', data=None):
    try:
        url = f"{WEBAPP_URL}{endpoint}"
        if method == 'GET':
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f"API error: {e}")
        return None

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    welcome_text = f"""
🎉 *ANDROMEDA BINGO* 🎉

Hello {user.first_name}!

💰 *Game Features:*
• Play with ETB currency
• Choose 1 or 2 Cartelas per game
• Games start every 20 seconds
• Win 80% of prize pool!

👇 *Click below to start playing!* 👇
    """
    
    keyboard = [
        [InlineKeyboardButton("🎮 PLAY ANDROMEDA BINGO", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("💰 Balance", callback_data='balance'),
         InlineKeyboardButton("❓ Help", callback_data='help')]
    ]
    
    if user.id == OWNER_ID:
        keyboard.append([InlineKeyboardButton("👑 Owner Panel", callback_data='owner')])
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown', 
                                    reply_markup=InlineKeyboardMarkup(keyboard))

async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = call_api('/api/balance', method='POST', data={'user_id': user.id})
    
    if data:
        await update.message.reply_text(
            f"💰 *Your Balance*\n\n"
            f"Available: **{data.get('balance', 0):.0f} ETB**\n"
            f"Total Won: **{data.get('total_won', 0):.0f} ETB**\n"
            f"Games Won: **{data.get('games_won', 0)}**",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text("💰 Open the game to see your balance!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🎮 *HOW TO PLAY ANDROMEDA BINGO*

1️⃣ Click PLAY ANDROMEDA BINGO
2️⃣ Choose stake (10/20/50 ETB)
3️⃣ Pick 1 or 2 Cartela numbers
4️⃣ Game starts in 20 seconds
5️⃣ Numbers draw automatically
6️⃣ Click BINGO when you win!

*Commands:*
/start - Main menu
/balance - Check balance
/help - This menu

Good luck! 🍀
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def owner_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id != OWNER_ID:
        await update.message.reply_text("❌ Unauthorized")
        return
    
    data = call_api('/api/owner_balance', method='GET')
    
    if data:
        await update.message.reply_text(
            f"👑 *Owner Dashboard*\n\n"
            f"💰 Balance: **{data.get('owner_balance', 0):.2f} ETB**\n"
            f"📊 Total Commission: **{data.get('total_commission_earned', 0):.2f} ETB**\n"
            f"🎮 Games Hosted: **{data.get('total_games_hosted', 0)}**\n"
            f"📈 Rate: **{data.get('commission_rate', 20)}%**",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text("👑 Owner Panel - Bot is running!")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'balance':
        user = update.effective_user
        data = call_api('/api/balance', method='POST', data={'user_id': user.id})
        if data:
            await query.edit_message_text(
                f"💰 Balance: **{data.get('balance', 0):.0f} ETB**",
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text("💰 Open game to see balance!")
    elif query.data == 'help':
        await query.edit_message_text("Click PLAY ANDROMEDA BINGO to start!")
    elif query.data == 'owner':
        user = update.effective_user
        if user.id == OWNER_ID:
            await query.edit_message_text("👑 Owner Panel - Bot is running!\n💰 20% commission active")
        else:
            await query.edit_message_text("❌ Unauthorized")

def main():
    print("=" * 50)
    print("🎮 ANDROMEDA BINGO BOT")
    print("=" * 50)
    print(f"WebApp URL: {WEBAPP_URL}")
    print("=" * 50)
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Clear webhook
    try:
        app.bot.delete_webhook()
        print("✅ Webhook cleared")
    except Exception as e:
        print(f"Webhook clear: {e}")
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("balance", balance_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("owner", owner_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    print("✅ Bot is running! Type /start on Telegram")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()