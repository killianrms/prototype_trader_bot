import os
from ast import parse

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

load_dotenv()

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # a remplacer par un  appel BDD
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
                                  reply_markup=wallet_menu_keyboard(context))


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

async def menu_generate_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    cryptoChoosen = query.data.split('_')[-1]
    print("Menu generating wallet for " + cryptoChoosen + "...")
    print(query.data)
    print(context.user_data)
    message = "Generating wallet for " + cryptoChoosen + "..."
    await query.edit_message_text(message, reply_markup=generate_menu_wallet_keyboard(context, "chain", cryptoChoosen))

async def generate_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    print("Generating wallet for " + query.data.split('_')[-1] + "...")
    print(query.data)
    print(context.user_data)
    await query.edit_message_text("Generating wallet for " + query.data.split('_')[-1] + "...", reply_markup=generate_wallet_keyboard(context))

async def generate_from_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    crypto = query.data.split('_')[-1]
    await query.answer()
    print("Generating wallet for " + query.data.split('_')[-1] + "...")
    print(query.data)
    print(context.user_data)
    await query.edit_message_text(text_wallet_menu(crypto),parse_mode="MarkdownV2", reply_markup=generate_from_wallet_keyboard(context, crypto))

async def show_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    cryptoChoosen = query.data.split('_')[-1]
    print("Showing wallet for " + cryptoChoosen + "...")
    print(query.data)
    print(context.user_data)
    text = text_wallet_menu(cryptoChoosen)
    await query.edit_message_text(text,  parse_mode="MarkdownV2", reply_markup=setting_wallet_keyboard(query.data.split('_')[-1]))

async def connect_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    print("Connecting wallet for " + query.data.split('_')[-1] + "...")
    print(query.data)
    print(context.user_data)
    await query.edit_message_text("Connecting wallet for " + query.data.split('_')[-1] + "...", reply_markup=generate_connect_wallet_keyboard(context))

async def connect_from_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    crypto = query.data.split('_')[-1]
    await query.answer()
    print("Connecting wallet for " + query.data.split('_')[-1] + "...")
    print(query.data)
    print(context.user_data)
    await query.edit_message_text(text_wallet_menu(crypto),parse_mode="MarkdownV2", reply_markup=generate_connect_from_wallet_keyboard(crypto))

async  def disconnect_from_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    crypto = query.data.split('_')[-1]
    await query.answer()
    print("Disconnecting wallet for " + crypto + "...")
    print(query.data)
    print(context.user_data)
    await query.edit_message_text(text_wallet_menu(crypto),parse_mode="MarkdownV2", reply_markup=disconnect_from_wallet_keyboard(crypto))

async def config_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    crypto = query.data.split('_')[-1]
    await query.answer()
    print("Config wallet for " + crypto + "...")
    print(query.data)
    print(context.user_data)
    await query.edit_message_text(text_wallet_menu(crypto),parse_mode="MarkdownV2", reply_markup=config_wallet_keyboard(crypto))

# Error handling
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'Update {update} caused error {context.error}')


# Button
def button_bot_name() -> list[InlineKeyboardButton]:
    return [InlineKeyboardButton("ProtoBotTrader", callback_data="none")]

# Keyboards
def config_wallet_keyboard(crypto: str) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='show_wallet_'+crypto)],
        [InlineKeyboardButton("❌ Anti MEV",  callback_data='anti_mev_wallet_'+crypto), InlineKeyboardButton("❌ Degen Mode 😈", callback_data='degen_mode_wallet_'+crypto)],
        [InlineKeyboardButton("⚙ Buy",  callback_data='config_buy_wallet_'+crypto), InlineKeyboardButton("⚙ Sell", callback_data='config_sell_wallet_'+crypto)],
        [InlineKeyboardButton("✏️Slippage",  callback_data='slippage_wallet_'+crypto), InlineKeyboardButton("⌫ Slippage", callback_data='erase_wallet_'+crypto)],
    ]
    return InlineKeyboardMarkup(keyboard)

def generate_connect_wallet_keyboard(context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='toggle_chain_menu')],
    ]
    return InlineKeyboardMarkup(keyboard)

def generate_connect_from_wallet_keyboard(context: ContextTypes.DEFAULT_TYPE,crypto) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='show_wallet'+crypto)],
    ]
    return InlineKeyboardMarkup(keyboard)

def disconnect_from_wallet_keyboard(crypto) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='show_wallet_'+crypto)],
    ]
    return InlineKeyboardMarkup(keyboard)

def setting_wallet_keyboard(crypto: str) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        #if wallet connected show disconnected wallet else  show connect wallet
        [InlineKeyboardButton("Disconnect Wallet", callback_data='disconnect_from_wallet_'+crypto), InlineKeyboardButton("🔙 Return", callback_data='wallet')],
        [InlineKeyboardButton("Generate Wallet", callback_data='generate_from_wallet_'+crypto), InlineKeyboardButton("Multi-Wallet", callback_data='menu_multi_wallet_'+crypto)],
        [InlineKeyboardButton("📤 " + crypto, callback_data='withdraw'+crypto), InlineKeyboardButton("📥 Tokens", callback_data='withdraw_token_'+crypto)],
        [InlineKeyboardButton("🔢 Buy KB",  callback_data='buy_kb_'+crypto), InlineKeyboardButton("⚙ Config", callback_data='config_wallet_'+crypto)],
    ]
    return InlineKeyboardMarkup(keyboard)

def generate_wallet_keyboard(context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='toggle_chain_menu')],
    ]
    return InlineKeyboardMarkup(keyboard)

def generate_from_wallet_keyboard(context: ContextTypes.DEFAULT_TYPE, crypto) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='show_wallet_' + crypto)],
    ]
    return InlineKeyboardMarkup(keyboard)

def generate_menu_wallet_keyboard(context: ContextTypes.DEFAULT_TYPE, call_origin, crypto) -> InlineKeyboardMarkup:
    callback_generate = 'generate_wallet_' + crypto
    connect_wallet = 'connect_wallet_' + crypto
    print(callback_generate)

    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='toggle_chain_menu')],
        [InlineKeyboardButton("🔑 Generate Wallet", callback_data=callback_generate),
         InlineKeyboardButton("🔗 Connect Wallet", callback_data=connect_wallet)]
    ]

    return InlineKeyboardMarkup(keyboard)


def get_button_text(chain_name: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    return "🟢 " + chain_name if context.user_data['chain_states'][chain_name] else "🔴 " + chain_name

def get_button_chain_name(chain_name: str) -> str:
    return "🔗 " + chain_name

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


def wallet_menu_keyboard(context) -> InlineKeyboardMarkup:
    # for chain in chains create button
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='main')],  # Return to main menu
    ]
    # verifier aussi si le wallet de la crypto a etait connecter ou generer
    for chain in context.user_data['chain_states']:
        #si la chain est a true alors on affiche le bouton
        if context.user_data['chain_states'][chain]:
            keyboard.append([InlineKeyboardButton(get_button_chain_name(chain), callback_data='show_wallet_' + chain)])
    return InlineKeyboardMarkup(keyboard)


def chain_menu_keyboard(context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='main')],  # Return to main menu
        [
            InlineKeyboardButton(get_button_text('SOL', context), callback_data='toggle_chain_SOL'),
            InlineKeyboardButton(get_button_text('ETH', context), callback_data='toggle_chain_ETH'),
            InlineKeyboardButton(get_button_text('TRX', context), callback_data='toggle_chain_TRX')
        ],
        [InlineKeyboardButton("▼ Generate or connect a wallet ▼", callback_data='none')],
        [
            InlineKeyboardButton("⚙ SOL", callback_data='menu_generate_wallet_SOL'),
            InlineKeyboardButton("⚙ ETH", callback_data='menu_generate_wallet_ETH'),
            InlineKeyboardButton("⚙ TRX", callback_data='menu_generate_wallet_TRX')
        ],
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


def text_wallet_menu(crypto) -> str:
    adresse = "Adresse : "  # + adresse de la wallet
    # mettre en majuscule et en  gras le text
    chain = "Chain : *" + crypto.upper() + "*"
    balance = "Balance : " + "* 0 " + crypto.upper() + "*"  # "*" + balance de la wallet + "*"

    general_params = "📍 General"
    buy_params = "📌 Buy"
    sell_params = "📌 Sell"
    text = f"{adresse}\n{chain}\n{balance}\n\n{general_params}\n{buy_params}\n{sell_params}"
    return text
    # Main function to set up the bot


if __name__ == '__main__':
    # Replace 'YOUR_TOKEN_HERE' with your bot's token
    TOKEN = os.getenv('TOKEN')

    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    application.add_handler(CallbackQueryHandler(generate_wallet, pattern='generate_wallet_.*'))
    application.add_handler(CallbackQueryHandler(generate_from_wallet, pattern='generate_from_wallet_*'))

    application.add_handler(CallbackQueryHandler(connect_wallet, pattern='connect_wallet_.*'))
    application.add_handler(CallbackQueryHandler(connect_from_wallet, pattern='connect_from_wallet_.*'))
    application.add_handler(CallbackQueryHandler(disconnect_from_wallet, pattern='disconnect_from_wallet_.*'))

    application.add_handler(CallbackQueryHandler(wallet_menu, pattern='wallet'))
    application.add_handler(CallbackQueryHandler(chain_menu, pattern='toggle_chain_.*'))
    application.add_handler(CallbackQueryHandler(menu_generate_wallet, pattern='menu_generate_wallet_.*'))
    application.add_handler(CallbackQueryHandler(show_wallet, pattern='show_wallet_.*'))

    application.add_handler(CallbackQueryHandler(config_wallet, pattern='config_wallet_.*'))

    application.add_error_handler(error)

    # Start polling
    application.run_polling(5)
