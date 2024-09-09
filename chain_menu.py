from telegram.ext import (Application,
                          CommandHandler,
                          CallbackQueryHandler,
                          ConversationHandler,
                          MessageHandler,
                          ContextTypes,
                          filters
                          )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from main import button_bot_name, get_user_data

# Chains Menu
async def chain_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    user_data = get_user_data()
    print(query.data)

    # Toggle the specific button's state
    button_name = query.data.split('_')[-1]  # Extract the chain name from the callback data (e.g., 'SOL')
    if button_name != 'menu':
        user_data[user_id]['chain_states'][button_name] = not user_data[user_id]['chain_states'][button_name]

    # Update the chain menu message with the user-specific states
    await query.edit_message_text(
        """🟢 Enable or 🔴 Disable chains based on your preference.

The ⚙️ Setup section can be used to connect or generate a wallet for each chain with a missing wallet.""",
        reply_markup=chain_menu_keyboard(context, user_id)
    )

def chain_menu_keyboard(context: ContextTypes.DEFAULT_TYPE, user_id) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='main')],  # Return to main menu
        [
            InlineKeyboardButton(get_button_text('SOL', context, user_id), callback_data='toggle_chain_SOL'),
            InlineKeyboardButton(get_button_text('ETH', context, user_id), callback_data='toggle_chain_ETH'),
            InlineKeyboardButton(get_button_text('TRX', context, user_id), callback_data='toggle_chain_TRX')
        ],
        [InlineKeyboardButton("▼ Generate or connect a wallet ▼", callback_data='none')],
        [
            InlineKeyboardButton("⚙ SOL", callback_data='menu_generate_wallet_SOL'),
            InlineKeyboardButton("⚙ ETH", callback_data='menu_generate_wallet_ETH'),
            InlineKeyboardButton("⚙ TRX", callback_data='menu_generate_wallet_TRX')
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_button_text(chain_name: str, user_data, user_id) -> str:
    print(chain_name)
    print(user_id)
    print(user_data[user_id]['chain_states'])
    if chain_name in user_data[user_id]['chain_states']:
        print(user_data[user_id]['chain_states'][chain_name])
        return "🟢 " + chain_name if user_data[user_id]['chain_states'][chain_name] else "🔴 " + chain_name

