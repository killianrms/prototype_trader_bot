import json
from operator import concat

from telegram.ext import (Application,
                          CommandHandler,
                          CallbackQueryHandler,
                          ConversationHandler,
                          MessageHandler,
                          ContextTypes,
                          filters
                          )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from button import *
from user_data import user_data, message_ids, delete_conv, reply_message_conv

AWAITING_MIN_MC = range(1)


async def wallet_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Select target chain:",
                                  reply_markup=wallet_menu_keyboard(query.from_user.id))

# Generate Wallet from Menu Wallet
async def menu_generate_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    cryptoChoosen = query.data.split('_')[-1]
    print("Menu generating wallet for " + cryptoChoosen + "...")
    print(query.data)
    print(context.user_data)
    message = "Generating wallet for " + cryptoChoosen + "..."
    await query.edit_message_text(message, reply_markup=generate_menu_wallet_keyboard(cryptoChoosen))

# Generate Wallet from Wallet Menu
async def generate_from_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    crypto = query.data.split('_')[-1]
    user_id = query.from_user.id
    await query.answer()
    print("Generating wallet for " + query.data.split('_')[-1] + "...")
    print(query.data)
    print(context.user_data)
    await query.edit_message_text(text_wallet_menu(crypto, user_id), parse_mode="MarkdownV2",
                                  reply_markup=generate_from_wallet_keyboard(context, crypto))

# Show Wallet
async def show_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    cryptoChoosen = query.data.split('_')[-1]
    print("Showing wallet for " + cryptoChoosen + "...")
    print(query.data)
    text = text_wallet_menu(cryptoChoosen, user_id)
    await query.edit_message_text(text, parse_mode="MarkdownV2",
                                  reply_markup=setting_wallet_keyboard(cryptoChoosen))

# Connect Wallet from Wallet Menu
async def connect_from_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    crypto = query.data.split('_')[-1]
    await query.answer()
    print("Connecting wallet for " + query.data.split('_')[-1] + "...")
    print(query.data)
    print(context.user_data)
    await query.edit_message_text(text_wallet_menu(crypto, user_id), parse_mode="MarkdownV2",
                                  reply_markup=generate_connect_from_wallet_keyboard(crypto))


# Disconnect Wallet from Wallet Menu
async def disconnect_from_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    crypto = query.data.split('_')[-1]
    user_id = update.effective_user.id
    await query.answer()
    print("Disconnecting wallet for " + crypto + "...")
    print(query.data)
    await query.edit_message_text(text_wallet_menu(crypto, user_id), parse_mode="MarkdownV2",
                                  reply_markup=disconnect_from_wallet_keyboard(crypto))

# Config Wallet
async def config_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    crypto = query.data.split('_')[-1]
    user_id = query.from_user.id
    await query.answer()
    print("Config wallet for " + crypto + "...")
    print(query.data)
    print(context.user_data)
    await query.edit_message_text(text_wallet_menu(crypto, user_id), parse_mode="MarkdownV2",
                                  reply_markup=config_wallet_keyboard(crypto))

# Config Buy Wallet
async def config_buy_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    crypto = query.data.split('_')[-1]
    user_id = query.from_user.id
    await query.answer()
    print("Config buy wallet for " + crypto + "...")
    print(query.data)
    print(context.user_data)
    await query.edit_message_text(text_wallet_menu(crypto, user_id), parse_mode="MarkdownV2",
                                  reply_markup=config_buy_wallet_keyboard(crypto, user_id))

async def confirm_trade_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    crypto = query.data.split('_')[-1]
    user_id = query.from_user.id
    await query.answer()
    if crypto in user_data[user_id]['wallets']:
        user_data[user_id]['wallets'][crypto]['BUY']['bool']['CONFIRM_TRADE']['value'] = not \
            user_data[user_id]['wallets'][crypto]['BUY']['bool']['CONFIRM_TRADE']['value']
    print("Confirm Trade wallet for " + crypto + "...")
    print(query.data)
    await query.edit_message_text(text_wallet_menu(crypto, user_id), parse_mode="MarkdownV2",
                                  reply_markup=config_buy_wallet_keyboard(crypto, user_id))


async def dupe_buy_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    crypto = query.data.split('_')[-1]
    user_id = query.from_user.id
    await query.answer()
    if crypto in user_data[user_id]['wallets']:
        user_data[user_id]['wallets'][crypto]['BUY']['bool']['DUPE_BUY']['value'] = not \
            user_data[user_id]['wallets'][crypto]['BUY']['bool']['DUPE_BUY']['value']
    print("Dupe Buy wallet for " + crypto + "...")
    print(query.data)
    await query.edit_message_text(text_wallet_menu(crypto, user_id), parse_mode="MarkdownV2",
                                  reply_markup=config_buy_wallet_keyboard(crypto, user_id))


async def auto_buy_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    crypto = query.data.split('_')[-1]
    user_id = query.from_user.id
    await query.answer()
    if crypto in user_data[user_id]['wallets']:
        user_data[user_id]['wallets'][crypto]['BUY']['bool']['AUTO_BUY']['value'] = not \
            user_data[user_id]['wallets'][crypto]['BUY']['bool']['AUTO_BUY']['value']
        user_data[user_id]['wallets'][crypto]['BUY']['bool']['DUPE_BUY']['value'] = user_data[user_id]['wallets'][crypto]['BUY']['bool']['AUTO_BUY']['value']
    print("Auto Buy wallet for " + crypto + "...")
    print(query.data)
    await query.edit_message_text(text_wallet_menu(crypto, user_id), parse_mode="MarkdownV2",
                                  reply_markup=config_buy_wallet_keyboard(crypto, user_id))

# Function to initiate the market cap threshold setting process
async def min_mc_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) ->  int:
    print("min_mc_wallet")
    query = update.callback_query
    chain = query.data.split('_')[-1]  # Assuming the chain is passed in callback data
    context.user_data['chain'] = chain
    await query.answer()

    # Ask for new min_mc value
    message = await query.message.reply_text(f"Please provide the new min_mc value for the {chain} chain:")

    # Store message ID to delete later
    user_id = update.effective_user.id
    if user_id not in message_ids:
        message_ids[user_id] = {'bot': [], 'user': []}
    message_ids[user_id]['bot'].append(message.message_id)

    return AWAITING_MIN_MC

async def receive_min_mc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    try:
        # Get the chain and new min_mc value from the user input
        chain = context.user_data.get('chain')
        new_min_mc = int(update.message.text)

        # Update the chain's min_mc value in user data
        user_data[user_id]['wallets'][chain]['BUY']['int']['MIN_MC']['value'] = new_min_mc
        text = f"min_mc for the {chain} chain updated to {new_min_mc}."
        await reply_message_conv(update, user_id, text)

    except ValueError:
        # Handle invalid input (non-integer value)
        message = await update.message.reply_text("Invalid value. Please provide an integer for the min_mc value.")
        message_ids[user_id]['bot'].append(message.message_id)


    # Delete conversation messages
    await delete_conv(update, user_id)

    # Print user data for verification
    user_data_json = json.dumps(user_data, indent=4, ensure_ascii=False)
    print(user_data_json)

    return ConversationHandler.END

    # Function to cancel the operation


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END


def generate_from_wallet_keyboard(context: ContextTypes.DEFAULT_TYPE, crypto) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='show_wallet_' + crypto)],
    ]
    return InlineKeyboardMarkup(keyboard)

def wallet_menu_keyboard(user_id) -> InlineKeyboardMarkup:
    # for chain in chains create button
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='main')],  # Return to main menu
    ]
    # verifier aussi si le wallet de la crypto a etait connecter ou generer
    for chain in user_data[user_id]['chain_states']:
        # si la chain est a true alors on affiche le bouton
        if user_data[user_id]['chain_states'][chain]:
            keyboard.append([InlineKeyboardButton(get_button_chain_name(chain), callback_data='show_wallet_' + chain)])
    return InlineKeyboardMarkup(keyboard)


def generate_menu_wallet_keyboard(crypto) -> InlineKeyboardMarkup:
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

def text_wallet_menu(crypto, user_id) -> str:
    adresse = "Adresse : "  # + adresse de la wallet
    # mettre en majuscule et en  gras le text
    chain = "Chain : *" + crypto.upper() + "*"
    balance = "Balance : " + "* 0 " + crypto.upper() + "*"  # "*" + balance de la wallet + "*"

    general_params = "📍 General"
    buy_params = "📌 Buy"
    for param in user_data[user_id]['wallets'][crypto]['BUY']['bool']:
        buy_params += "\n" + get_button_menu_param_name(param, crypto, 'bool', user_id, 'BUY')
    buy_params += "\n"
    for param in user_data[user_id]['wallets'][crypto]['BUY']['int']:
        buy_params += "\n" + get_button_menu_param_name(param, crypto, 'int', user_id,'BUY')
    sell_params = "📌 Sell"

    for param in user_data[user_id]['wallets'][crypto]['SELL']['bool']:
        sell_params += "\n" + get_button_menu_param_name(param, crypto, 'bool', user_id,'SELL')
    sell_params += "\n"
    for param in user_data[user_id]['wallets'][crypto]['SELL']['int']:
        sell_params += "\n" + get_button_menu_param_name(param, crypto, 'int', user_id, 'SELL')

    text = f"{adresse}\n{chain}\n{balance}\n\n{general_params}\n\n{buy_params}\n\n{sell_params}"
    return text

def get_button_menu_param_name(param_name: str, crypto, type: str, user_id, BorS) -> str:
    if type == 'bool':
        print(user_data[user_id]['wallets'][crypto][BorS]['bool'][param_name]['name'])
        return user_data[user_id]['wallets'][crypto][BorS]['bool'][param_name]['name'] + "✅ " if \
            user_data[user_id]['wallets'][crypto][BorS]['bool'][param_name]['value'] else \
            user_data[user_id]['wallets'][crypto][BorS]['bool'][param_name]['name'] + "❌ "
    elif type == 'int':
        value = str(user_data[user_id]['wallets'][crypto][BorS]['int'][param_name]['value'])
        name = user_data[user_id]['wallets'][crypto][BorS]['int'][param_name]['name']
        return name + value


def setting_wallet_keyboard(crypto: str) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("Disconnect Wallet", callback_data='disconnect_from_wallet_' + crypto),
         InlineKeyboardButton("🔙 Return", callback_data='wallet')],
        [InlineKeyboardButton("Generate Wallet", callback_data='generate_from_wallet_' + crypto),
         InlineKeyboardButton("Multi-Wallet", callback_data='menu_multi_wallet_' + crypto)],
        [InlineKeyboardButton("📤 " + crypto, callback_data='withdraw' + crypto),
         InlineKeyboardButton("📥 Tokens", callback_data='withdraw_token_' + crypto)],
        [InlineKeyboardButton("🔢 Buy KB", callback_data='buy_kb_' + crypto),
         InlineKeyboardButton("⚙ Config", callback_data='config_wallet_' + crypto)],
    ]
    return InlineKeyboardMarkup(keyboard)

def generate_connect_from_wallet_keyboard(crypto) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='show_wallet' + crypto)],
    ]
    return InlineKeyboardMarkup(keyboard)

def disconnect_from_wallet_keyboard(crypto) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='show_wallet_' + crypto)],
    ]
    return InlineKeyboardMarkup(keyboard)

def config_wallet_keyboard(crypto: str) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='show_wallet_' + crypto)],
        [InlineKeyboardButton("❌ Anti MEV", callback_data='anti_mev_wallet_' + crypto),
         InlineKeyboardButton("❌ Degen Mode 😈", callback_data='degen_mode_wallet_' + crypto)],
        [InlineKeyboardButton("⚙ Buy", callback_data='config_buy_wallet_' + crypto),
         InlineKeyboardButton("⚙ Sell", callback_data='config_sell_wallet_' + crypto)],
    ]
    return InlineKeyboardMarkup(keyboard)

def config_buy_wallet_keyboard(crypto: str, user_id) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='config_wallet_' + crypto)],
        [InlineKeyboardButton(get_button_buy_config_name("CONFIRM_TRADE", crypto, user_id),
                              callback_data='confirm_trade_wallet_' + crypto)],
        [InlineKeyboardButton(get_button_buy_config_name("DUPE_BUY", crypto, user_id),
                              callback_data='dupe_buy_wallet_' + crypto),
         InlineKeyboardButton(get_button_buy_config_name("AUTO_BUY", crypto, user_id),
                              callback_data='auto_buy_wallet_' + crypto)],
        [InlineKeyboardButton(get_button_buy_config_name("MIN_MC", crypto, user_id),
                              callback_data='min_mc_wallet_' + crypto),
         InlineKeyboardButton("⌫ Min MC", callback_data='erase_min_mc_wallet_' + crypto)],
        [InlineKeyboardButton(get_button_buy_config_name("MAX_MC", crypto, user_id),
                              callback_data='max_mc_wallet_' + crypto),
         InlineKeyboardButton("⌫ Max MC", callback_data='erase_max_mc_wallet_' + crypto)],
        [InlineKeyboardButton(get_button_buy_config_name("MIN_LIQ", crypto, user_id),
                              callback_data='min_liq_wallet_' + crypto),
         InlineKeyboardButton("⌫ Min Liq", callback_data='erase_min_liq_wallet_' + crypto)],
        [InlineKeyboardButton(get_button_buy_config_name("MAX_LIQ", crypto, user_id),
                              callback_data='max_liq_wallet_' + crypto),
         InlineKeyboardButton("⌫ Max Liq", callback_data='erase_max_liq_wallet_' + crypto)],
        [InlineKeyboardButton(get_button_buy_config_name("MIN_MC_LIQ", crypto, user_id),
                              callback_data='min_mc_liq_wallet_' + crypto),
         InlineKeyboardButton("⌫ Min MC/Liq", callback_data='erase_min_mc_liq_wallet_' + crypto)],
        [InlineKeyboardButton(get_button_buy_config_name("GAS_DELTA", crypto, user_id),
                              callback_data='gas_delta_wallet_' + crypto),
         InlineKeyboardButton("⌫ Gas Delta", callback_data='erase_gd_wallet_' + crypto)],
        [InlineKeyboardButton(get_button_buy_config_name("PIA", crypto, user_id), callback_data='pia_wallet_' + crypto),
         InlineKeyboardButton("⌫ PIA", callback_data='erase_pia_wallet_' + crypto)],
        [InlineKeyboardButton(get_button_buy_config_name("SLIPPAGE", crypto, user_id),
                              callback_data='slippage_wallet_' + crypto),
         InlineKeyboardButton("⌫ Slippage", callback_data='erase_slippage_wallet_' + crypto)],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_button_buy_config_name(param_name: str, crypto, user_id) -> str:
    if param_name in user_data[user_id]['wallets'][crypto]['BUY']['bool']:
        text_to_show = user_data[user_id]['wallets'][crypto]['BUY']['bool'][param_name]['text']
        return "✅ " + text_to_show if user_data[user_id]['wallets'][crypto]['BUY']['bool'][param_name][
            'value'] else "❌ " + text_to_show
    elif param_name in user_data[user_id]['wallets'][crypto]['BUY']['int']:
        text_to_show = user_data[user_id]['wallets'][crypto]['BUY']['int'][param_name]['text']
        return "✏️ " + text_to_show