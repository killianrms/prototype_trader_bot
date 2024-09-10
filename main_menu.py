from telegram.ext import (Application,
                          CommandHandler,
                          CallbackQueryHandler,
                          ConversationHandler,
                          MessageHandler,
                          ContextTypes,
                          filters
                          )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from button import button_bot_name
from user_data import get_user_data


async def main_menu(update: Update, user_data) -> None:
    query = update.callback_query
    user_id = update.effective_user.id
    await query.answer()
    await query.edit_message_text(main_menu_message(user_id), reply_markup=main_menu_keyboard())


def main_menu_message(user_id) -> str:
    user_data = get_user_data()
    text_choose = """What would you like to do today?

Monitor
Active Trades: 0
Disabled Trades: 0

Auto Snipe
Active Auto Snipes: 0

Presale
Active Presales: 0"""
    return "Your premium statut : 🟢\n" + text_choose if user_data[user_id][
        'subscribed'] else "Your premium statut : 🔴\n" + text_choose

def main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("⚙ Chains", callback_data="toggle_chain_menu")],
        [InlineKeyboardButton("⚙ Wallets", callback_data="wallet"),
         InlineKeyboardButton("⚙ Call Channels", callback_data="cc")],
        [InlineKeyboardButton("⚙ Presales", callback_data="presales"),
         InlineKeyboardButton("⚙ Copy Trading", callback_data="ct")],
        [InlineKeyboardButton("⚙ Auto Snipe", callback_data="as"),
         InlineKeyboardButton("⚙ Signals", callback_data="signal")],
        [InlineKeyboardButton("↔️Bridge", callback_data="bridge"),
         InlineKeyboardButton("🌟Premium", callback_data="premium"),
         InlineKeyboardButton("ℹ️ FAQ", callback_data="faq")],
    ]
    return InlineKeyboardMarkup(keyboard)