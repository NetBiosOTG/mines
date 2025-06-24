import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram.error import BadRequest
from urllib.parse import urlparse

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your bot token from BotFather (use environment variable for security)
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL')

def validate_url(url):
    """Validate if URL is properly formatted"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and result.scheme in ['http', 'https']
    except:
        return False

# Validate environment variables
if not BOT_TOKEN:
    logger.error("BOT_TOKEN environment variable is not set!")
    exit(1)

if not WEBAPP_URL:
    logger.error("WEBAPP_URL environment variable is not set!")
    exit(1)

if not validate_url(WEBAPP_URL):
    logger.error(f"WEBAPP_URL is not a valid URL: {WEBAPP_URL}")
    exit(1)

# Ensure HTTPS for production
if not WEBAPP_URL.startswith('https://'):
    logger.warning(f"WebApp URL should use HTTPS for production: {WEBAPP_URL}")

logger.info(f"Bot starting with WebApp URL: {WEBAPP_URL}")

async def mines_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /mines command"""
    try:
        # First try with a simple fallback approach
        keyboard = [
            [InlineKeyboardButton(
                "🎯 Open Mines Calculator", 
                url=WEBAPP_URL  # Using url instead of web_app as fallback
            )],
            [InlineKeyboardButton(
                "📱 Open as Web App", 
                web_app=WebAppInfo(url=WEBAPP_URL)
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send message with the buttons
        await update.message.reply_text(
            "🎮 *Mines Multiplier Calculator*\n\n"
            "Calculate your potential winnings for Mines game!\n"
            "• Supports Stake and Jacks casinos\n"
            "• Enter mines count (1-24)\n"
            "• Enter tiles clicked (1-24)\n"
            "• Enter your bet amount\n\n"
            "Choose how to open the calculator:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        logger.info(f"Mines command executed for user {update.effective_user.id}")
        
    except BadRequest as e:
        logger.error(f"BadRequest error in mines_command: {e}")
        # Fallback to simple URL button if WebApp fails
        try:
            keyboard = [
                [InlineKeyboardButton(
                    "🎯 Open Mines Calculator", 
                    url=WEBAPP_URL
                )]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "🎮 *Mines Multiplier Calculator*\n\n"
                "Calculate your potential winnings for Mines game!\n"
                "Click the button below to open the calculator:",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        except Exception as fallback_error:
            logger.error(f"Fallback also failed: {fallback_error}")
            await update.message.reply_text(
                f"🎮 *Mines Multiplier Calculator*\n\n"
                f"Open the calculator at: {WEBAPP_URL}",
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Unexpected error in mines_command: {e}")
        await update.message.reply_text(
            "An unexpected error occurred. Please try again later."
        )

async def mines_simple_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /mines_simple command with just URL button"""
    try:
        keyboard = [
            [InlineKeyboardButton(
                "🎯 Open Mines Calculator", 
                url=WEBAPP_URL
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🎮 *Mines Multiplier Calculator*\n\n"
            "Calculate your potential winnings for Mines game!\n"
            "Click the button below to open the calculator:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        logger.info(f"Mines simple command executed for user {update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Error in mines_simple_command: {e}")
        await update.message.reply_text(
            f"🎮 *Mines Multiplier Calculator*\n\n"
            f"Open the calculator at: {WEBAPP_URL}",
            parse_mode='Markdown'
        )

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command"""
    await update.message.reply_text(
        "🎮 Welcome to Mines Calculator Bot!\n\n"
        "Use /mines to open the calculator in any group or private chat.\n"
        "Use /mines_simple for a simple URL button version.\n\n"
        "This bot helps you calculate multipliers and potential winnings for the Mines game."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command"""
    await update.message.reply_text(
        "🎮 **Mines Calculator Bot Help**\n\n"
        "**Commands:**\n"
        "/mines - Open the Mines multiplier calculator (with WebApp)\n"
        "/mines_simple - Open with simple URL button\n"
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

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    logger.error(f"Exception while handling an update: {context.error}")
    
    # Only send error message if we have an update with a message
    if isinstance(update, Update) and update.message:
        try:
            await update.message.reply_text(
                "Sorry, an error occurred while processing your request. Please try again later."
            )
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")

def main() -> None:
    """Start the bot"""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("mines", mines_command))
    application.add_handler(CommandHandler("mines_simple", mines_simple_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add error handler
    application.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
