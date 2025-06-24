import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your bot token from BotFather
BOT_TOKEN = "8133489563:AAEMzvmyECqqMhdtqoKhQILY5dzLsvGQulA"

# Your Vercel hosted URL
WEBAPP_URL = "https://your-vercel-url.vercel.app"

async def mines_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /mines command"""
    
    # Create inline keyboard with Web App button
    keyboard = [
        [InlineKeyboardButton(
            "🎯 Open Mines Calculator", 
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send message with the Web App button
    await update.message.reply_text(
        "🎮 **Mines Multiplier Calculator**\n\n"
        "Calculate your potential winnings for Mines game!\n"
        "• Supports Stake and Jacks casinos\n"
        "• Enter mines count (1-24)\n"
        "• Enter tiles clicked (1-24)\n"
        "• Enter your bet amount\n\n"
        "Click the button below to open the calculator:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command"""
    await update.message.reply_text(
        "🎮 Welcome to Mines Calculator Bot!\n\n"
        "Use /mines to open the calculator in any group or private chat.\n\n"
        "This bot helps you calculate multipliers and potential winnings for the Mines game."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command"""
    await update.message.reply_text(
        "🎮 **Mines Calculator Bot Help**\n\n"
        "**Commands:**\n"
        "/mines - Open the Mines multiplier calculator\n"
        "/start - Welcome message\n"
        "/help - Show this help message\n\n"
        "**How to use:**\n"
        "1. Type /mines in any group or private chat\n"
        "2. Click the 'Open Mines Calculator' button\n"
        "3. Select your casino (Stake or Jacks)\n"
        "4. Enter number of mines (1-24)\n"
        "5. Enter tiles clicked (1-24)\n"
        "6. Enter your bet amount\n"
        "7. Click Calculate to see your multiplier and potential winnings!",
        parse_mode='Markdown'
    )

def main() -> None:
    """Start the bot"""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("mines", mines_command))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
