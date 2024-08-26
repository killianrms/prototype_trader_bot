import os
from email.policy import default
from typing import List

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

load_dotenv()

# Initialize the button states
button_chain_states = {
    'SOL': True,
    'ETH': False,
    'TRX': False
}


# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Initialize the user-specific chain button states if not already set
    if 'chain_states' not in context.user_data:
        context.user_data['chain_states'] = {
            'SOL': True,
            'ETH': False,
            'TRX': False,
        }
    await update.message.reply_text(main_menu_message(), reply_markup=main_menu_keyboard())


# Main Menu
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(main_menu_message(), reply_markup=main_menu_keyboard())



# Wallets Menu
async def wallet_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Select target chain:",
                                  reply_markup=wallet_menu_keyboard())


# Chains Menu
async def chain_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    print(query.data)
    print(context.user_data)

    # Toggle the specific button's state
    button_name = query.data.split('_')[-1]  # Extract the chain name from the callback data (e.g., 'SOL')
    if button_name != 'menu':
        context.user_data['chain_states'][button_name] = not context.user_data['chain_states'][button_name]

    # Update the chain menu message with the user-specific states
    await query.edit_message_text(
        """🟢 Enable or 🔴 Disable chains based on your preference.

The ⚙️ Setup section can be used to connect or generate a wallet for each chain with a missing wallet.""",
        reply_markup=chain_menu_keyboard(context)
    )


def get_button_text(chain_name: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    return "🟢 " + chain_name if context.user_data['chain_states'][chain_name] else "🔴 " + chain_name



# First Menu
async def first_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(first_menu_message(),
                                  reply_markup=first_menu_keyboard())


# Second Menu
async def second_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(second_menu_message(),
                                  reply_markup=second_menu_keyboard())


# Handlers for submenus (you can expand these as needed)
async def first_submenu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("You selected Submenu 1-1. Here are your options:",
                                  reply_markup=return_to_first_keyboard())


async def second_submenu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("You selected Submenu 2-1. Here are your options:",
                                  reply_markup=return_to_second_keyboard())


# Error handling
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'Update {update} caused error {context.error}')


# Button
def button_bot_name() -> list[InlineKeyboardButton]:
    return [InlineKeyboardButton("ProtoBotTrader", callback_data="none")]


# Keyboards
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


def wallet_menu_keyboard() -> InlineKeyboardMarkup:
    # for chain in chains create button
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='main')],  # Return to main menu
        [InlineKeyboardButton("SOL", callback_data='sol')],
    ]
    return InlineKeyboardMarkup(keyboard)


def chain_menu_keyboard(context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [
            InlineKeyboardButton(get_button_text('SOL', context), callback_data='toggle_chain_SOL'),
            InlineKeyboardButton(get_button_text('ETH', context), callback_data='toggle_chain_ETH'),
            InlineKeyboardButton(get_button_text('TRX', context), callback_data='toggle_chain_TRX')
        ],
        [InlineKeyboardButton("🔙 Return", callback_data='main')]  # Return to main menu
    ]
    return InlineKeyboardMarkup(keyboard)



def first_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton('Submenu 1-1', callback_data='m1_1')],
        [InlineKeyboardButton('Submenu 1-2', callback_data='m1_2')],
        [InlineKeyboardButton('Main menu', callback_data='main')]
    ]
    return InlineKeyboardMarkup(keyboard)


def second_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
        [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')],
        [InlineKeyboardButton('Main menu', callback_data='main')]
    ]
    return InlineKeyboardMarkup(keyboard)


def return_to_first_keyboard() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton('🔙 Return to First Menu', callback_data='m1')]]
    return InlineKeyboardMarkup(keyboard)


def return_to_second_keyboard() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton('🔙 Return to Second Menu', callback_data='m2')]]
    return InlineKeyboardMarkup(keyboard)

    # Messages


def main_menu_message() -> str:
    return 'Choose the option in the main menu:'


def first_menu_message() -> str:
    return 'Choose the submenu in the first menu:'


def second_menu_message() -> str:
    return 'Choose the submenu in the second menu:'

    # Main function to set up the bot


if __name__ == '__main__':
    # Replace 'YOUR_TOKEN_HERE' with your bot's token
    TOKEN = os.getenv('TOKEN')

    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    application.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
    application.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
    application.add_handler(CallbackQueryHandler(first_submenu, pattern='m1_1'))
    application.add_handler(CallbackQueryHandler(second_submenu, pattern='m2_1'))
    application.add_handler(CallbackQueryHandler(second_submenu, pattern='m2_2'))
    application.add_handler(CallbackQueryHandler(second_submenu, pattern='m1_2'))

    application.add_handler(CallbackQueryHandler(wallet_menu, pattern='wallet'))
    application.add_handler(CallbackQueryHandler(chain_menu, pattern='toggle_chain_.*'))

    application.add_error_handler(error)

    # Start polling
    application.run_polling(5)
