from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (Application,
                          CommandHandler,
                          CallbackQueryHandler,
                          ConversationHandler,
                          MessageHandler,
                          ContextTypes,
                          filters
                          )

# Button
def button_bot_name() -> list[InlineKeyboardButton]:
    return [InlineKeyboardButton("ProtoBotTrader", callback_data="none")]

def get_button_chain_name(chain_name: str) -> str:
    return "🔗 " + chain_name