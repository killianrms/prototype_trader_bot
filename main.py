import os
import json
import re
from idlelib.editor import keynames

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

load_dotenv()

user_data = {}


# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if  update.effective_user.id not in user_data:
        user_id = update.effective_user.id
        first_name = update.effective_user.first_name
        user_data[user_id] = {
            'first_name' : first_name,
            'id' : user_id
        }
        print(user_data)
        user_data[user_id]['chain_states'] = {
            'SOL': True,
            'ETH': False,
            'TRX': False,
        }
        user_data[user_id]['wallets'] = {
            'SOL': {
                'BUY': {
                    'bool': {
                        'COPY_TRADE': {
                            'value': False,
                            'text': "Off",
                            'name': "Copy Trade Buy : "
                        },
                        'CONFIRM_TRADE': {
                            'value': False,
                            'text': "Confirm Trade",
                            'name': "Confirm Trade Buy : "
                        },
                        'DUPE_BUY': {
                            'value': False,
                            'text': "Dupe Buy",
                            'name': "Duplicate Buy : "
                        },
                        'AUTO_BUY': {
                            'value': False,
                            'text': "Auto Buy",
                            'name': "Auto Buy : "
                        },
                    },
                    'int': {
                        'MIN_MC': {
                            'value': 0,
                            'text': "Min Mc",
                            'name': "Min MCap : "
                        },
                        'MAX_MC': {
                            'value': 0,
                            'text': "Max Mc",
                            'name': "Max MCap : "
                        },
                        'MIN_LIQ': {
                            'value': 0,
                            'text': "Min Liquidity",
                            'name': "Min Liquidity : "
                        },
                        'MAX_LIQ': {
                            'value': 0,
                            'text': "Max Liquidity",
                            'name': "Max Liquidity : "
                        },
                        'MIN_MC_LIQ': {
                            'value': 0,
                            'text': "Min Mc/Liq",
                            'name': "Min MCap/Liq : "
                        },
                        'GAS_DELTA': {
                            'value': 0,
                            'text': "Gas Delta",
                            'name': "Buy Gas Delta : "
                        },
                        'PIA': {
                            'value': 0,
                            'text': "Price Impact Alert",
                            'name': "Price impact alert : "
                        },
                        'SLIPPAGE': {
                            'value': 0,
                            'text': "Slippage",
                            'name': "Slippage : "
                        },
                    },
                },
                'SELL': {
                    'bool' : {
                        'CONFIRM_TRADE': {
                            'value': False,
                            'text': "Confirm Trade",
                            'name': "Confirm Trade Sell : "
                        },
                        'AUTO_SELL': {
                            'value': False,
                            'text': "Auto Sell",
                            'name': "Auto Sell : "
                        },
                        'TRAILING_SELL': {
                            'value': False,
                            'text': "Trailing Sell",
                            'name': "Trailing Sell : "
                        },
                        'AUTO_SELL_RETRY': {
                            'value': False,
                            'text': "Auto Sell Retry",
                            'name': "Auto Sell Retry : "
                        },
                    },
                    'int' : {
                        'SELL_HIGH': {
                            'value': 0,
                            'text': "Sell High",
                            'name': "Sell High : "
                        },
                        'SELL_LOW': {
                            'value': 0,
                            'text': "Sell Low",
                            'name': "Sell Low : "
                        },
                        'SELL_HIGH_AMOUNT': {
                            'value': 0,
                            'text': "Sell High Amount",
                            'name': "Sell High Amount : "
                        },
                        'SELL_LOW_AMOUNT': {
                            'value': 0,
                            'text': "Sell Low Amount",
                            'name': "Sell Low Amount : "
                        },
                        'GAS_DELTA': {
                            'value': 0,
                            'text': "Gas Delta",
                            'name': "Sell Gas Price : "
                        },
                        'PIA': {
                            'value': 0,
                            'text': "Price Impact Alert",
                            'name': "Price impact alert : "
                        },
                        'SLIPPAGE': {
                            'value': 0,
                            'text': "Slippage",
                            'name': "Slippage : "
                        },
                    }
                },
            },

            'ETH': {
                'BUY': {
                    'bool': {
                        'COPY_TRADE': {
                            'value': False,
                            'text': "Off",
                            'name': "Copy Trade Buy : "
                        },
                        'CONFIRM_TRADE': {
                            'value': False,
                            'text': "Confirm Trade",
                            'name': "Confirm Trade Buy : "
                        },
                        'DUPE_BUY': {
                            'value': False,
                            'text': "Dupe Buy",
                            'name': "Duplicate Buy : "
                        },
                        'AUTO_BUY': {
                            'value': False,
                            'text': "Auto Buy",
                            'name': "Auto Buy : "
                        },
                    },
                    'int': {
                        'MIN_MC': {
                            'value': 0,
                            'text': "Min Mc",
                            'name': "Min MCap : "
                        },
                        'MAX_MC': {
                            'value': 0,
                            'text': "Max Mc",
                            'name': "Max MCap : "
                        },
                        'MIN_LIQ': {
                            'value': 0,
                            'text': "Min Liquidity",
                            'name': "Min Liquidity : "
                        },
                        'MAX_LIQ': {
                            'value': 0,
                            'text': "Max Liquidity",
                            'name': "Max Liquidity : "
                        },
                        'MIN_MC_LIQ': {
                            'value': 0,
                            'text': "Min Mc/Liq",
                            'name': "Min MCap/Liq : "
                        },
                        'GAS_DELTA': {
                            'value': 0,
                            'text': "Gas Delta",
                            'name': "Buy Gas Delta : "
                        },
                        'PIA': {
                            'value': 0,
                            'text': "Price Impact Alert : ",
                            'name': "Price impact alert : "
                        },
                        'SLIPPAGE': {
                            'value': 0,
                            'text': "Slippage",
                            'name': "Slippage : "
                        },
                    },
                },
                'SELL': {
                    'bool': {
                        'CONFIRM_TRADE': {
                            'value': False,
                            'text': "Confirm Trade",
                            'name': "Confirm Trade Sell : "
                        },
                        'AUTO_SELL': {
                            'value': False,
                            'text': "Auto Sell",
                            'name': "Auto Sell : "
                        },
                        'TRAILING_SELL': {
                            'value': False,
                            'text': "Trailing Sell",
                            'name': "Trailing Sell : "
                        },
                        'AUTO_SELL_RETRY': {
                            'value': False,
                            'text': "Auto Sell Retry",
                            'name': "Auto Sell Retry : "
                        },
                    },
                    'int': {
                        'SELL_HIGH': {
                            'value': 0,
                            'text': "Sell High",
                            'name': "Sell High : "
                        },
                        'SELL_LOW': {
                            'value': 0,
                            'text': "Sell Low",
                            'name': "Sell Low : "
                        },
                        'SELL_HIGH_AMOUNT': {
                            'value': 0,
                            'text': "Sell High Amount",
                            'name': "Sell High Amount : "
                        },
                        'SELL_LOW_AMOUNT': {
                            'value': 0,
                            'text': "Sell Low Amount",
                            'name': "Sell Low Amount : "
                        },
                        'GAS_DELTA': {
                            'value': 0,
                            'text': "Gas Delta",
                            'name': "Sell Gas Price : "
                        },
                        'PIA': {
                            'value': 0,
                            'text': "Price Impact Alert",
                            'name': "Price impact alert : "
                        },
                        'SLIPPAGE': {
                            'value': 0,
                            'text': "Slippage",
                            'name': "Slippage : "
                        },
                    }
                },
            },

            'TRX': {
                'BUY': {
                    'bool': {
                        'COPY_TRADE': {
                            'value': False,
                            'text': "Off",
                            'name': "Copy Trade Buy : "
                        },
                        'CONFIRM_TRADE': {
                            'value': False,
                            'text': "Confirm Trade",
                            'name': "Confirm Trade Buy : "
                        },
                        'DUPE_BUY': {
                            'value': False,
                            'text': "Dupe Buy",
                            'name': "Duplicate Buy : "
                        },
                        'AUTO_BUY': {
                            'value': False,
                            'text': "Auto Buy",
                            'name': "Auto Buy : "
                        },
                    },
                    'int': {
                        'MIN_MC': {
                            'value': 0,
                            'text': "Min Mc",
                            'name': "Min MCap : "
                        },
                        'MAX_MC': {
                            'value': 0,
                            'text': "Max Mc",
                            'name': "Max MCap : "
                        },
                        'MIN_LIQ': {
                            'value': 0,
                            'text': "Min Liquidity",
                            'name': "Min Liquidity : "
                        },
                        'MAX_LIQ': {
                            'value': 0,
                            'text': "Max Liquidity",
                            'name': "Max Liquidity : "
                        },
                        'MIN_MC_LIQ': {
                            'value': 0,
                            'text': "Min Mc/Liq",
                            'name': "Min MCap/Liq : "
                        },
                        'GAS_DELTA': {
                            'value': 0,
                            'text': "Gas Delta",
                            'name': "Buy Gas Delta : "
                        },
                        'PIA': {
                            'value': 0,
                            'text': "Price Impact Alert : ",
                            'name': "Price impact alert : "
                        },
                        'SLIPPAGE': {
                            'value': 0,
                            'text': "Slippage",
                            'name': "Slippage : "
                        },
                    },
                },
                'SELL': {
                    'bool': {
                        'CONFIRM_TRADE': {
                            'value': False,
                            'text': "Confirm Trade",
                            'name': "Confirm Trade Sell : "
                        },
                        'AUTO_SELL': {
                            'value': False,
                            'text': "Auto Sell",
                            'name': "Auto Sell : "
                        },
                        'TRAILING_SELL': {
                            'value': False,
                            'text': "Trailing Sell",
                            'name': "Trailing Sell : "
                        },
                        'AUTO_SELL_RETRY': {
                            'value': False,
                            'text': "Auto Sell Retry",
                            'name': "Auto Sell Retry : "
                        },
                    },
                    'int': {
                        'SELL_HIGH': {
                            'value': 0,
                            'text': "Sell High",
                            'name': "Sell High : "
                        },
                        'SELL_LOW': {
                            'value': 0,
                            'text': "Sell Low",
                            'name': "Sell Low : "
                        },
                        'SELL_HIGH_AMOUNT': {
                            'value': 0,
                            'text': "Sell High Amount",
                            'name': "Sell High Amount : "
                        },
                        'SELL_LOW_AMOUNT': {
                            'value': 0,
                            'text': "Sell Low Amount",
                            'name': "Sell Low Amount : "
                        },
                        'GAS_DELTA': {
                            'value': 0,
                            'text': "Gas Delta",
                            'name': "Sell Gas Price : "
                        },
                        'PIA': {
                            'value': 0,
                            'text': "Price Impact Alert",
                            'name': "Price impact alert : "
                        },
                        'SLIPPAGE': {
                            'value': 0,
                            'text': "Slippage",
                            'name': "Slippage : "
                        },
                    }
                },
            },
        }

        user_data_json = json.dumps(user_data, indent=4, ensure_ascii=False)
        print(user_data_json)
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
                                  reply_markup=wallet_menu_keyboard(context, query.from_user.id))

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
        reply_markup=chain_menu_keyboard(context,user_id)
    )


# Generate Wallet from Menu Wallet
async def menu_generate_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    cryptoChoosen = query.data.split('_')[-1]
    print("Menu generating wallet for " + cryptoChoosen + "...")
    print(query.data)
    print(context.user_data)
    message = "Generating wallet for " + cryptoChoosen + "..."
    await query.edit_message_text(message, reply_markup=generate_menu_wallet_keyboard(context, "chain", cryptoChoosen))


# Generate Wallet from Chain Menu
async def generate_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    print("Generating wallet for " + query.data.split('_')[-1] + "...")
    print(query.data)
    print(context.user_data)
    await query.edit_message_text("Generating wallet for " + query.data.split('_')[-1] + "...",
                                  reply_markup=generate_wallet_keyboard(context))


# Generate Wallet from Wallet Menu
async def generate_from_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    crypto = query.data.split('_')[-1]
    user_id = query.from_user.id
    await query.answer()
    print("Generating wallet for " + query.data.split('_')[-1] + "...")
    print(query.data)
    print(context.user_data)
    await query.edit_message_text(text_wallet_menu(crypto, context, user_id), parse_mode="MarkdownV2",
                                  reply_markup=generate_from_wallet_keyboard(context, crypto))


# Show Wallet
async def show_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    cryptoChoosen = query.data.split('_')[-1]
    print("Showing wallet for " + cryptoChoosen + "...")
    print(query.data)
    text = text_wallet_menu(cryptoChoosen, context, user_id)
    await query.edit_message_text(text, parse_mode="MarkdownV2",
                                  reply_markup=setting_wallet_keyboard(cryptoChoosen))


# Connect Wallet from Chain Menu
async def connect_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    print("Connecting wallet for " + query.data.split('_')[-1] + "...")
    print(query.data)
    await query.edit_message_text("Connecting wallet for " + query.data.split('_')[-1] + "...",
                                  reply_markup=generate_connect_wallet_keyboard(context))


# Connect Wallet from Wallet Menu
async def connect_from_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    crypto = query.data.split('_')[-1]
    await query.answer()
    print("Connecting wallet for " + query.data.split('_')[-1] + "...")
    print(query.data)
    print(context.user_data)
    await query.edit_message_text(text_wallet_menu(crypto, context, user_id), parse_mode="MarkdownV2",
                                  reply_markup=generate_connect_from_wallet_keyboard(crypto))


# Disconnect Wallet from Wallet Menu
async def disconnect_from_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    crypto = query.data.split('_')[-1]
    await query.answer()
    print("Disconnecting wallet for " + crypto + "...")
    print(query.data)
    await query.edit_message_text(text_wallet_menu(crypto, context), parse_mode="MarkdownV2",
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
    await query.edit_message_text(text_wallet_menu(crypto, context, user_id), parse_mode="MarkdownV2",
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
    await query.edit_message_text(text_wallet_menu(crypto, context,user_id), parse_mode="MarkdownV2",
                                  reply_markup=config_buy_wallet_keyboard(crypto, context, user_id))


async def confirm_trade_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    crypto = query.data.split('_')[-1]
    user_id = query.from_user.id
    await query.answer()
    if crypto in user_data[user_id]['wallets']:
       user_data[user_id]['wallets'][crypto]['BUY']['bool']['CONFIRM_TRADE']['value'] = not user_data[user_id]['wallets'][crypto]['BUY']['bool']['CONFIRM_TRADE']['value']
    print("Confirm Trade wallet for " + crypto + "...")
    print(query.data)
    await query.edit_message_text(text_wallet_menu(crypto, context,user_id), parse_mode="MarkdownV2",
                                  reply_markup=config_buy_wallet_keyboard(crypto, context, user_id))


async def dupe_buy_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    crypto = query.data.split('_')[-1]
    user_id  = query.from_user.id
    await query.answer()
    if crypto in user_data[user_id]['wallets']:
        user_data[user_id]['wallets'][crypto]['BUY']['bool']['DUPE_BUY']['value'] = not user_data[user_id]['wallets'][crypto]['BUY']['bool']['DUPE_BUY']['value']
    print("Dupe Buy wallet for " + crypto + "...")
    print(query.data)
    await query.edit_message_text(text_wallet_menu(crypto, context, user_id), parse_mode="MarkdownV2",
                                  reply_markup=config_buy_wallet_keyboard(crypto, context, user_id))


async def auto_buy_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    crypto = query.data.split('_')[-1]
    user_id = query.from_user.id
    await query.answer()
    if crypto in user_data[user_id]['wallets']:
        user_data[user_id]['wallets'][crypto]['BUY']['bool']['AUTO_BUY']['value'] = not \
            user_data[user_id]['wallets'][crypto]['BUY']['bool']['AUTO_BUY']['value']
    print("Auto Buy wallet for " + crypto + "...")
    print(query.data)
    await query.edit_message_text(text_wallet_menu(crypto, context, user_id), parse_mode="MarkdownV2",
                                  reply_markup=config_buy_wallet_keyboard(crypto, context, user_id))


# Function to initiate the market cap threshold setting process
async def min_mc_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send a message prompting the user to reply with their desired minimum market cap
    crypto = update.callback_query.data.split('_')[-1]
    user_id = update.callback_query.from_user.id
    prompt_message = await update.message.reply_text(
        "Reply to this message with your desired minimum market cap threshold in USD. Minimum is $1! ⚠️"
    )

    # Store the prompt message ID to track replies and to delete it later
    user_data[user_id]['prompt_message_id'] = prompt_message.message_id
    user_data[user_id]['setting_min_mc'] = True
    user_data[user_id]['crypto_choosen'] = crypto

    # Function to handle the user's reply and update the min_mc value


async def set_market_cap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    if user_data[user_id]['setting_min_mc'] :
        user_reply = update.message.text
        crypto = user_data[user_id]['crypto_choosen']
        # Validate the user's input
        try:
            min_market_cap = int(user_reply)
            if min_market_cap < 1:
                await update.message.reply_text("The minimum market cap must be at least $1. Please try again.")
                return
        except ValueError:
            await update.message.reply_text("Invalid input. Please enter a valid number.")
            return

        # Update the user's minimum market cap in the user_data dictionary
        user_data[user_id]['wallets'][crypto]['BUY']['int']['MIN_MC']['value'] = min_market_cap

        # Delete the prompt message
        prompt_message_id = user_data[user_id]['prompt_message_id']
        if prompt_message_id:
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=prompt_message_id)

        # Confirm the update to the user
        await update.message.reply_text(f"Your minimum market cap has been set to ${min_market_cap}.")

        # Clear the state
        user_data[user_id]['setting_min_mc'] = False
        user_data[user_id]['crypto'] = None


async def ct(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    print("Open copy trade menu for " + query.data.split('_')[-1] + "...")
    print(query.data)
    await query.edit_message_text("Copy Trade Menu", reply_markup=copytrade_menu_keyboard(context, user_id))

async def show_copytrade(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    crypto = query.data.split('_')[-1]
    await query.answer()
    print("Showing copy trade for " + query.data.split('_')[-1] + "...")
    print(query.data)
    await query.edit_message_text("Copy Trade Menu", reply_markup=copytrade_crypto_keyboard(context, user_id, crypto))

async def set_copytrade_value(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    crypto = query.data.split('_')[-1]
    await query.answer()
    if crypto in user_data[user_id]['wallets']:
        user_data[user_id]['wallets'][crypto]['BUY']['bool']['COPY_TRADE']['value'] = not user_data[user_id]['wallets'][crypto]['BUY']['bool']['COPY_TRADE']['value']
    print("Copy Trade for " + crypto + "...")
    print(query.data)
    await query.edit_message_text("Copy Trade Menu", reply_markup=copytrade_crypto_keyboard(context, user_id, crypto))

# Error handling
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'Update {update} caused error {context.error}')


# Button
def button_bot_name() -> list[InlineKeyboardButton]:
    return [InlineKeyboardButton("ProtoBotTrader", callback_data="none")]


# Keyboards

def copytrade_crypto_keyboard(context: ContextTypes.DEFAULT_TYPE, user_id, crypto) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='ct')],
        [InlineKeyboardButton(get_button_text_ct(crypto,user_id), callback_data='set_copy_trade_' + crypto)],
        [InlineKeyboardButton("Add Wallet or Contract", callback_data='add_wallet_' + crypto)],
    ]
    return InlineKeyboardMarkup(keyboard)

def config_buy_wallet_keyboard(crypto: str, context: ContextTypes.DEFAULT_TYPE, user_id) -> InlineKeyboardMarkup:
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
        [InlineKeyboardButton(get_button_buy_config_name("MIN_LIQ",crypto, user_id),
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


def change_value_bool(context: ContextTypes.DEFAULT_TYPE, crypto: str, param_name: str) -> None:
    if param_name in context.user_data['wallets'][crypto]['BUY']['bool']:
        context.user_data['wallets'][crypto]['BUY']['bool'][param_name] = not \
            context.user_data['wallets'][crypto]['bool'][
                param_name]


def change_value_int(context: ContextTypes.DEFAULT_TYPE, crypto: str, param_name: str, value: int) -> None:
    if param_name in context.user_data['wallets'][crypto]['BUY']['int']:
        context.user_data['wallets'][crypto]['BUY']['int'][param_name] = value


def generate_connect_wallet_keyboard(context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='toggle_chain_menu')],
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


def get_button_text(chain_name: str, context: ContextTypes.DEFAULT_TYPE, user_id) -> str:
    print(chain_name)
    print(user_id)
    print(user_data[user_id]['chain_states'])
    if chain_name in user_data[user_id]['chain_states']:
        print(user_data[user_id]['chain_states'][chain_name])
        return "🟢 " + chain_name if user_data[user_id]['chain_states'][chain_name] else "🔴 " + chain_name

def get_button_text_ct(chain_name: str, user_id) -> str:
    if chain_name in user_data[user_id]['wallets']:
        return "🟢 ON"  if user_data[user_id]['wallets'][chain_name]['BUY']['bool']['COPY_TRADE']['value'] else "🔴 OFF"


def get_button_buy_config_name(param_name: str, crypto, user_id) -> str:
    if param_name in user_data[user_id]['wallets'][crypto]['BUY']['bool']:
        text_to_show = user_data[user_id]['wallets'][crypto]['BUY']['bool'][param_name]['text']
        return "✅ " + text_to_show if user_data[user_id]['wallets'][crypto]['BUY']['bool'][param_name][
            'value'] else "❌ " + text_to_show
    elif param_name in user_data[user_id]['wallets'][crypto]['BUY']['int']:
        text_to_show = user_data[user_id]['wallets'][crypto]['BUY']['int'][param_name]['text']
        return "✏️ " + text_to_show


def get_button_menu_param_name(param_name: str, crypto, type: str, user_id) -> str:
    if type == 'bool':
        print(user_data[user_id]['wallets'][crypto]['BUY']['bool'][param_name]['name'])
        return user_data[user_id]['wallets'][crypto]['BUY']['bool'][param_name]['name'] + "✅ " if \
            user_data[user_id]['wallets'][crypto]['BUY']['bool'][param_name]['value'] else \
            user_data[user_id]['wallets'][crypto]['BUY']['bool'][param_name]['name'] + "❌ "
    elif type == 'int':
        return user_data[user_id]['wallets'][crypto]['BUY']['int'][param_name]['name'] + str(
            user_data[user_id]['wallets'][crypto]['BUY']['int'][param_name]['value'])


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


def wallet_menu_keyboard(context, user_id) -> InlineKeyboardMarkup:
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

def  copytrade_menu_keyboard(context: ContextTypes.DEFAULT_TYPE,user_id) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='main')],  # Return to main menu
    ]
    for chain in user_data[user_id]['chain_states']:
        if user_data[user_id]['chain_states'][chain]:
            keyboard.append([InlineKeyboardButton(get_button_chain_name(chain), callback_data='show_copytrade_' + chain)])
    return InlineKeyboardMarkup(keyboard)


def chain_menu_keyboard(context: ContextTypes.DEFAULT_TYPE, user_id) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='main')],  # Return to main menu
        [
            InlineKeyboardButton(get_button_text('SOL', context,user_id), callback_data='toggle_chain_SOL'),
            InlineKeyboardButton(get_button_text('ETH', context,user_id), callback_data='toggle_chain_ETH'),
            InlineKeyboardButton(get_button_text('TRX', context,user_id), callback_data='toggle_chain_TRX')
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


def text_wallet_menu(crypto, context,user_id) -> str:
    adresse = "Adresse : "  # + adresse de la wallet
    # mettre en majuscule et en  gras le text
    chain = "Chain : *" + crypto.upper() + "*"
    balance = "Balance : " + "* 0 " + crypto.upper() + "*"  # "*" + balance de la wallet + "*"

    general_params = "📍 General"
    buy_params = "📌 Buy"
    for param in user_data[user_id]['wallets'][crypto]['BUY']['bool']:
        buy_params += "\n" + get_button_menu_param_name(param, crypto, 'bool', user_id)
    buy_params += "\n"
    for param in user_data[user_id]['wallets'][crypto]['BUY']['int']:
        buy_params += "\n" + get_button_menu_param_name(param, crypto, 'int', user_id)
    sell_params = "📌 Sell"
    text = f"{adresse}\n{chain}\n{balance}\n\n{general_params}\n\n{buy_params}\n\n{sell_params}"
    return text
    # Main function to set up the bot


def extract_user_data(update: Update) -> dict:
    user = update.message.from_user
    return {
        'id': user.id,
        'first_name': user.first_name,
    }

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

    # Config Buy  Handler
    application.add_handler(CallbackQueryHandler(config_buy_wallet, pattern='config_buy_wallet_.*'))

    application.add_handler(CallbackQueryHandler(confirm_trade_wallet, pattern='confirm_trade_wallet_.*'))
    application.add_handler(CallbackQueryHandler(dupe_buy_wallet, pattern='dupe_buy_wallet_.*'))
    application.add_handler(CallbackQueryHandler(auto_buy_wallet, pattern='auto_buy_wallet_.*'))

    application.add_handler(CallbackQueryHandler(min_mc_wallet, pattern='min_mc_wallet_.*'))
    application.add_handler(MessageHandler(filters.REPLY & filters.TEXT, set_market_cap))
    #
    # application.add_handler(CallbackQueryHandler(min_mc_wallet, pattern='min_mc_wallet_.*'))
    # application.add_handler(CallbackQueryHandler(erase_min_mc_wallet, pattern='erase_min_mc_wallet_.*'))
    #
    # application.add_handler(CallbackQueryHandler(max_mc_wallet, pattern='max_mc_wallet_.*'))
    # application.add_handler(CallbackQueryHandler(erase_max_mc_wallet, pattern='erase_max_mc_wallet_.*'))
    #
    # application.add_handler(CallbackQueryHandler(min_liq_wallet, pattern='min_liq_wallet_.*'))
    # application.add_handler(CallbackQueryHandler(erase_min_liq_wallet, pattern='erase_min_liq_wallet_.*'))
    #
    # application.add_handler(CallbackQueryHandler(max_liq_wallet, pattern='max_liq_wallet_.*'))
    # application.add_handler(CallbackQueryHandler(erase_max_liq_wallet, pattern='erase_max_liq_wallet_.*'))
    #
    # application.add_handler(CallbackQueryHandler(min_mc_liq_wallet, pattern='min_mc_liq_wallet_.*'))
    # application.add_handler(CallbackQueryHandler(erase_min_mc_liq_wallet, pattern='erase_min_mc_liq_wallet_.*'))
    #
    # application.add_handler(CallbackQueryHandler(gas_delta_wallet, pattern='gas_delta_wallet_.*'))
    # application.add_handler(CallbackQueryHandler(erase_gd_wallet, pattern='erase_gd_wallet_.*'))
    #
    # application.add_handler(CallbackQueryHandler(pia_wallet, pattern='pia_wallet_.*'))
    # application.add_handler(CallbackQueryHandler(erase_pia_wallet, pattern='erase_pia_wallet_.*'))
    #
    # application.add_handler(CallbackQueryHandler(slippage_wallet, pattern='slippage_wallet_.*'))
    # application.add_handler(CallbackQueryHandler(erase_slippage_wallet, pattern='erase_slippage_wallet_.*'))

    application.add_handler(CallbackQueryHandler(ct, pattern='ct'))
    application.add_handler(CallbackQueryHandler(show_copytrade, pattern='show_copytrade_.*'))
    application.add_handler(CallbackQueryHandler(set_copytrade_value, pattern='set_copy_trade_.*'))

    # Error handler
    application.add_error_handler(error)

    # Start polling
    application.run_polling(5)
