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
from user_data import user_data


# Chains Menu
async def chain_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    print(query.data)
    print(user_data)

    # Toggle the specific button's state
    button_name = query.data.split('_')[-1]  # Extract the chain name from the callback data (e.g., 'SOL')
    if button_name != 'menu':
        user_data[user_id]['chain_states'][button_name] = not user_data[user_id]['chain_states'][button_name]

    # Update the chain menu message with the user-specific states
    await query.edit_message_text(
        """🟢 Enable or 🔴 Disable chains based on your preference.

The ⚙️ Setup section can be used to connect or generate a wallet for each chain with a missing wallet.""",
        reply_markup=chain_menu_keyboard(user_id)
    )

def generate_wallet_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='toggle_chain_menu')],
    ]
    return InlineKeyboardMarkup(keyboard)

def chain_menu_keyboard(user_id) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='main')],  # Return to main menu
        [
            InlineKeyboardButton(get_button_text('SOL', user_id), callback_data='toggle_chain_SOL'),
            InlineKeyboardButton(get_button_text('ETH', user_id), callback_data='toggle_chain_ETH'),
            InlineKeyboardButton(get_button_text('TRX', user_id), callback_data='toggle_chain_TRX')
        ],
        [InlineKeyboardButton("▼ Generate or connect a wallet ▼", callback_data='none')],
        [
            InlineKeyboardButton("⚙ SOL", callback_data='menu_generate_wallet_SOL'),
            InlineKeyboardButton("⚙ ETH", callback_data='menu_generate_wallet_ETH'),
            InlineKeyboardButton("⚙ TRX", callback_data='menu_generate_wallet_TRX')
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_button_text(chain_name: str, user_id) -> str:
    print(chain_name)
    print(user_id)
    print(user_data[user_id]['chain_states'])
    if chain_name in user_data[user_id]['chain_states']:
        print(user_data[user_id]['chain_states'][chain_name])
        return "🟢 " + chain_name if user_data[user_id]['chain_states'][chain_name] else "🔴 " + chain_name

# Connect Wallet from Chain Menu
async def connect_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    print("Connecting wallet for " + query.data.split('_')[-1] + "...")
    print(query.data)
    await query.edit_message_text("Connecting wallet for " + query.data.split('_')[-1] + "...",
                                  reply_markup=generate_connect_wallet_keyboard(context))

def generate_connect_wallet_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='toggle_chain_menu')],
    ]
    return InlineKeyboardMarkup(keyboard)

def generate_wallet_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='toggle_chain_menu')],
    ]
    return InlineKeyboardMarkup(keyboard)

# Generate Wallet from Chain Menu
async def generate_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    print("Generating wallet for " + query.data.split('_')[-1] + "...")
    print(query.data)
    print(context.user_data)
    await query.edit_message_text("Generating wallet for " + query.data.split('_')[-1] + "...",
                                  reply_markup=generate_wallet_keyboard())
