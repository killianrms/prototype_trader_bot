import os
import json
import re
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (Application,
                          CommandHandler,
                          CallbackQueryHandler,
                          ConversationHandler,
                          MessageHandler,
                          ContextTypes,
                          filters
                          )

from chain_menu import *
from wallets import *
from main_menu import *
load_dotenv()

MAX_WALLETS_FREE = 3
AWAITING_WALLET, AWAITING_NAME = range(2)

# Wallet regex patterns for different types
wallet_regex = {
    'SOL': r'[1-9A-HJ-NP-Za-km-z]{32,44}',  # Solana
    'ETH': r'^0x[a-fA-F0-9]{40}$',  # Ethereum
    'TRX': r'^T[a-zA-Z0-9]{33}$'  # TRX
}

user_data = {}

message_ids = {}
copytrade_message_id = None
copytrade_context = None
copytrade_update = None


# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in user_data:
        user_id = update.effective_user.id
        first_name = update.effective_user.first_name
        user_data[user_id] = {
            'first_name': first_name,
            'id': user_id,
            'subscribed': False,
        }
        print(user_data)
        user_data[user_id]['chain_states'] = {
            'SOL': True,
            'ETH': False,
            'TRX': False,
        }
        user_data[user_id]['wallets'] = {
            'SOL': {
                'GENERAL': {
                    'WALLETS_CT': {
                        'value': [],
                        'text': "Wallets CT",
                        'name': "Wallets d'adresse du  Copy Trade : "
                    },
                },
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

            'ETH': {
                'GENERAL': {
                    'WALLETS_CT': {
                        'value': [],
                        'text': "Wallets CT",
                        'name': "Wallets d'adresse du  Copy Trade : "
                    },
                },
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
                'GENERAL': {
                    'WALLETS_CT': {
                        'value': [],
                        'text': "Wallets CT",
                        'name': "Wallets d'adresse du  Copy Trade : "
                    },
                },
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
        message_ids[update.effective_user.id] = {
            'bot': [],
            'user': []
        }

        print(message_ids)
        user_id = update.effective_user.id
        user_data_json = json.dumps(user_data, indent=4, ensure_ascii=False)
        print(user_data_json)
        await update.message.reply_text(main_menu_message(user_id, user_data), reply_markup=main_menu_keyboard())


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
    await query.edit_message_text(text_wallet_menu(crypto, context, user_id), parse_mode="MarkdownV2",
                                  reply_markup=config_buy_wallet_keyboard(crypto, context, user_id))


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
    await query.edit_message_text(text_wallet_menu(crypto, context, user_id), parse_mode="MarkdownV2",
                                  reply_markup=config_buy_wallet_keyboard(crypto, context, user_id))


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

    if user_data[user_id]['setting_min_mc']:
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
    global copytrade_message_id
    global copytrade_context
    global copytrade_update
    query = update.callback_query
    user_id = query.from_user.id
    crypto = query.data.split('_')[-1]
    await query.answer()
    print("Showing copy trade for " + query.data.split('_')[-1] + "...")
    print(query.data)
    message = await query.edit_message_text("Copy Trade Menu",
                                            reply_markup=copytrade_crypto_keyboard(context, user_id, crypto))
    copytrade_context = context
    copytrade_update = update
    copytrade_message_id = message.message_id


async def set_copytrade_value(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    crypto = query.data.split('_')[-1]
    await query.answer()
    if crypto in user_data[user_id]['wallets']:
        user_data[user_id]['wallets'][crypto]['BUY']['bool']['COPY_TRADE']['value'] = not \
            user_data[user_id]['wallets'][crypto]['BUY']['bool']['COPY_TRADE']['value']
    print("Copy Trade for " + crypto + "...")
    print(query.data)
    await query.edit_message_text("Copy Trade Menu", reply_markup=copytrade_crypto_keyboard(context, user_id, crypto))


async def add_wallet_ct(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # User clicked a button for adding a specific wallet type
    print("add_wallet_ct")
    query = update.callback_query
    context.user_data['wallet_type'] = query.data.split('_')[-1]
    crypto = context.user_data['wallet_type']
    await query.answer()
    # Ask for wallet address in a new message
    message = await query.message.reply_text("Please provide the wallet address:")

    # Store the message ID to delete later
    user_id = update.effective_user.id
    if user_id not in message_ids:
        message_ids[user_id] = {'bot': [], 'user': []}
    message_ids[user_id]['bot'].append(message.message_id)

    return AWAITING_WALLET


async def receive_wallet_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Get the selected wallet type
    wallet_type = context.user_data.get('wallet_type')
    wallet_address = update.message.text
    user_id = update.effective_user.id

    # Validate the wallet address using the regex for the selected wallet type
    if re.match(wallet_regex[wallet_type], wallet_address):
        # Save the wallet address in the user data
        context.user_data['wallet_address'] = wallet_address
        message = await update.message.reply_text("Wallet address is valid! Please provide a name for this wallet:")

        # Store the message ID to delete later
        if user_id not in message_ids:
            message_ids[user_id] = {'bot': [], 'user': []}
        message_ids[user_id]['user'].append(update.message.message_id)
        message_ids[user_id]['bot'].append(message.message_id)

        return AWAITING_NAME
    else:
        message = await update.message.reply_text("Invalid wallet address. Please provide a correct wallet address:")

        # Store the message ID to delete later
        if user_id not in message_ids:
            message_ids[user_id] = {'bot': [], 'user': []}
        message_ids[user_id]['user'].append(update.message.message_id)
        message_ids[user_id]['bot'].append(message.message_id)

        return AWAITING_WALLET


async def receive_wallet_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Receive the wallet name
    wallet_name = update.message.text
    wallet_address = context.user_data.get('wallet_address')
    wallet_type = context.user_data.get('wallet_type')
    user_id = update.effective_user.id

    wallets_ct = user_data[user_id]['wallets'][wallet_type]['GENERAL']['WALLETS_CT']['value']

    # Check if wallet address already exists
    if wallet_address in wallets_ct:
        message = await update.message.reply_text("This wallet address already exists.")

        # Store the message ID to delete later
        if user_id not in message_ids:
            message_ids[user_id] = {'bot': [], 'user': []}
        message_ids[user_id]['user'].append(update.message.message_id)
        message_ids[user_id]['bot'].append(message.message_id)
    else:
        # Check if the user is subscribed and limit the number of wallets
        is_subscribed = user_data[user_id]['subscribed']
        if not is_subscribed and len(wallets_ct) >= MAX_WALLETS_FREE:
            message = await update.message.reply_text(
                f"You cannot add more than {MAX_WALLETS_FREE} wallets in the free version.")

            # Store the message ID to delete later
            if user_id not in message_ids:
                message_ids[user_id] = {'bot': [], 'user': []}
            message_ids[user_id]['user'].append(update.message.message_id)
            message_ids[user_id]['bot'].append(message.message_id)
        else:
            # Add wallet to the list
            # generate a i value for wallet
            i = len(user_data[user_id]['wallets'][wallet_type]['GENERAL']['WALLETS_CT']['value'])
            to_input = {
                f'{i}': {
                    'address': wallet_address,
                    'name': wallet_name
                }
            }
            wallets_ct.append(to_input)
            user_data[user_id]['wallets'][wallet_type]['GENERAL']['WALLETS_CT']['value'] = wallets_ct
            message = await update.message.reply_text(
                f"Wallet '{wallet_name}' with address '{wallet_address}' added successfully to Copy Trade!")

            # Store the message ID to delete later
            if user_id not in message_ids:
                message_ids[user_id] = {'bot': [], 'user': []}
            message_ids[user_id]['user'].append(update.message.message_id)
            message_ids[user_id]['bot'].append(message.message_id)

    if user_id in message_ids:
        for msg_id in message_ids[user_id]['bot']:
            try:
                await update.message.chat.delete_message(msg_id)
            except Exception as e:
                print(f"Failed to delete bot message {msg_id}: {e}")
        for msg_id in message_ids[user_id]['user']:
            try:
                await update.message.chat.delete_message(msg_id)
            except Exception as e:
                print(f"Failed to delete user message {msg_id}: {e}")

    user_data_json = json.dumps(user_data, indent=4, ensure_ascii=False)
    print(user_data_json)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Cancel the current conversation
    await update.message.reply_text("Operation cancelled.")

    return ConversationHandler.END


async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = update.effective_user.id
    if user_id in user_data:
        user_data[user_id]['subscribed'] = not user_data[user_id]['subscribed']

    await query.edit_message_text(main_menu_message(user_id), reply_markup=main_menu_keyboard())


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(faq_text_menu(), reply_markup=faq_keyboard())


async def show_faq_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None :
    #get the text of the button from the callback data
    query = update.callback_query
    await query.answer()
    button_name = query.data.split('_')[-1]
    print(button_name)
    #create a switch case to get the text of the button
    switcher = {
        'security': security_text_menu(),
        'setting': wallet_setting_text_menu(),
        'transactions': manual_transactions_text_menu(),
        'channels': call_channels_text_menu(),
        'warnings': auto_buy_warnings_text_menu(),
        'messages': transaction_error_messages_text_menu(),
        'monitor': trade_monitor_text_menu(),
        'wallet': multi_wallet_text_menu(),
        'presales': presales_text_menu(),
        'copytrade': copy_trade_text_menu(),
        'sniping': lp_method_sniping_text_menu(),
        'sell': smart_rug_protection_text_menu()
    }

    #get the text of the button
    text = switcher.get(button_name, "Invalid button")
    await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=faq_answer_keyboard())




# Error handling
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'Update {update} caused error {context.error}')


# Button
def button_bot_name() -> list[InlineKeyboardButton]:
    return [InlineKeyboardButton("ProtoBotTrader", callback_data="none")]


# Keyboards
def faq_answer_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='faq')]
    ]
    return InlineKeyboardMarkup(keyboard)

def faq_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='menu')],
        # Secutiry,  Wallet Setting
        [InlineKeyboardButton("Security", callback_data='faq_security'),
         InlineKeyboardButton("Wallet Setting", callback_data='faq_wallet_setting')],
        # Manual Transactions, Call Channels
        [InlineKeyboardButton("Manual Transactions", callback_data='faq_manual_transactions'),
         InlineKeyboardButton("Call Channels", callback_data='faq_call_channels')],
        # Auto_Buy Warnings, Transaction Error Messages
        [InlineKeyboardButton("Auto_Buy Warnings", callback_data='faq_auto_buy_warnings'),
         InlineKeyboardButton("Transaction Error Messages", callback_data='faq_transaction_error_messages')],
        # Trade Monitor, Multi-Wallet
        [InlineKeyboardButton("Trade Monitor", callback_data='faq_trade_monitor'),
         InlineKeyboardButton("Multi-Wallet", callback_data='faq_multi_wallet')],
        # Presales, Copytrade
        [InlineKeyboardButton("Presales", callback_data='faq_presales'),
         InlineKeyboardButton("Copytrade", callback_data='faq_copytrade')],
        # LP/Method Sniping, Smart Rug Auto Sell
        [InlineKeyboardButton("LP/Method Sniping", callback_data='faq_lp_method_sniping'),
         InlineKeyboardButton("Smart Rug Auto Sell", callback_data='faq_smart_rug_auto_sell')],
    ]
    return InlineKeyboardMarkup(keyboard)


def copytrade_crypto_keyboard(context: ContextTypes.DEFAULT_TYPE, user_id, crypto) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton(get_button_text_ct(crypto, user_id), callback_data='set_copy_trade_' + crypto),
         InlineKeyboardButton("🔙 Return", callback_data='ct')],
        [InlineKeyboardButton("Add Wallet or Contract", callback_data='add_ct_wallet_' + crypto)],
    ]

    if user_data[user_id]['wallets'][crypto]['GENERAL']['WALLETS_CT']['value']:
        for i in user_data[user_id]['wallets'][crypto]['GENERAL']['WALLETS_CT']['value']:
            for wallet in i:
                print(i)
                print(wallet)
                keyboard.append(
                    [InlineKeyboardButton(i[wallet]['name'], callback_data='param_ct_wallet_' + crypto + '_' + wallet),
                     InlineKeyboardButton("Rename", callback_data='rename_ct_wallet_' + crypto + '_' + wallet),
                     InlineKeyboardButton("❌", callback_data='remove_ct_wallet_' + crypto + '_' + wallet)])
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


def get_button_text_ct(chain_name: str, user_id) -> str:
    if chain_name in user_data[user_id]['wallets']:
        return "🟢 ON" if user_data[user_id]['wallets'][chain_name]['BUY']['bool']['COPY_TRADE']['value'] else "🔴 OFF"


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


def copytrade_menu_keyboard(context: ContextTypes.DEFAULT_TYPE, user_id) -> InlineKeyboardMarkup:
    keyboard = [
        button_bot_name(),
        [InlineKeyboardButton("🔙 Return", callback_data='main')],  # Return to main menu
    ]
    for chain in user_data[user_id]['chain_states']:
        print(chain)
        if user_data[user_id]['chain_states'][chain]:
            keyboard.append(
                [InlineKeyboardButton(get_button_chain_name(chain), callback_data='show_copytrade_' + chain)])
    return InlineKeyboardMarkup(keyboard)


def faq_text_menu() -> str:
    return "ℹ️ FAQ \n\n*Is the bot free?*\n\nThe bot is free to access, but not free to use\. Buying through the Maestro Sniper Bot \(manually or automatically\) will be charged a 1% tax on every buy and sell\. The bot will NOT take the 1% directly from each transaction\. It simply accumulates how much you owe us, and once that amount reaches 0\.01 BNB or ETH, the bot extracts them to: \(the addresse of the bot transaction fees wallet\)\.\n\nThe sniper will deal with this silently \(no messages, streamlined\), but we're tracking all transactions in the backend\. In the future, you'll be able to export all of the transactions you've done through the sniper\. If you want to double check, you can always visit your block explorer \(e\.g\. bscscan\) to find all transactions\."


def security_text_menu() -> str:
    return "ℹ️ FAQ\n\n*Section 1 \- Security*\n\n*1\. Do I need to connect my wallet to the bot?*\nNo\. You can generate burner wallets directly in the bot\.\n\n*2\. What security measures has the team taken?*\nAll private keys are AES encrypted, and our servers' security is airtight\.\n\n*3\. Are there any security concerns?*\nThe only security concerns revolve around your actions\. Make sure your Telegram is secure by enabling two\-factor authentication\. If you generate a wallet through the bot, do NOT share the private key with anyone else, and make sure you store it in a secure location\.\n\n*4\. I see 0\.01 BNB/ETH transfers that I haven't authorized\.*\nIf the transfers were to \(wallet eth crypto du bot\), then those are the 1% bot usage fees being extracted\. This is explained in the first part of the FAQ, as well as the manual\."

def wallet_setting_text_menu() -> str:
    return "ℹ️ FAQ\n\n*Section 2 \- Wallet Settings*\n\n*1\. Gas Price*\nThis determines your transaction priority on the blockchain\. On BSC, 5\-7 gwei is good for normal transactions, 8\-12 is decent for casual sniping, but it can go way WAY higher for hyped launches and presales\. On ETH, remove any custom gas price and set gas delta to 3 gwei or above\.\n\n*2\. Gas delta*\nThis is meant for ETH users\. It determines the maximum priority gwei you're willing to spend in a Type\-2 transaction\. A minimum of 3 is recommended, but you can go much higher depending on your needs and preferences\. Your base gwei will automatically adjust to the current average at the time, so you don't have to worry about that\.\n\n*3\. Gas Limits*\nThis is the maximum amount of gas units you're willing to consume for the transaction\. Since the bot can optimally determine this value, you don't need to bother with it, unless you want to block contracts that require a lot of gas\.\n\n*4\. Smart Slippage*\nThis overrides your slippage and automatically adjusts it based on the token's taxes and your price impact\. It is very convenient for quick swaps and casual call channel sniping, as it can protect you from frontrunning bots\. However, it is not suitable for highly volatile situations like stealth launches and LP/method snipes through Auto Snipe\. For those cases, please disable Smart Slippage and specify a suitable slippage tolerance\.\n\n*5\. Do I need to adjust all the settings?*\nNo\. You can leave them on default/disabled\. However, tailoring the bot using these settings makes for a more focused and profitable experience\."

#TODO: place \ in front of  ()-. characters
def manual_transactions_text_menu() -> str:
    return "ℹ️ FAQ\n\n*Section 3 - Manual Transactions*\n\n*1\. How can I buy a token manually?*\nYou paste the token\'s contract address into the bot, then use the buy menu to pick a suitable amount\.\n\n*2\. How can I sell a token manually?*\nYou paste the token\'s contract address into the bot, then use the Buy ↔️ Sell button to open the sell menu, or use the Track button\.\n\n*3\. Can I automate buying pasted contracts?*\nYes\. You can configure the \'Me\' channel in the /start \-> Call Channels menu for that\.\n\n*4\. If I bought a token inside the bot, can I sell it outside?*\nYes\.\n\n*5\. If I bought a token outside the bot, can I sell it inside?*\nYes\. Paste the token\'s contract address into the bot then use the Buy ↔️ Sell or Track buttons\.\n\n*6\. What gas settings do manual buys/sells use?*\nManual buys/sells use your wallet\'s gas settings\.\n\n*7\. How can I make my buys/sells go faster?*\nYour gas price determines your transaction\'s priority on the blockchain\. If you want more speed, please increase your gas price \(or gas delta if you\'re on ETH\)\.\n\n*8\. What if I try to buy an amount bigger than max buy?*\nThe bot automatically adjusts your buy amount to match the max buy of the contract\. The only case where we don\'t do that is 0\-block\-delay LP/method sniping through Auto Snipe\.\n\n*9. Can I buy a specific amount of tokens?*\nYes\. Paste the token\'s contract address then use the Buy X Tokens button\."

def call_channels_text_menu() -> str:
    return "ℹ️ FAQ\n\n*Section 4 \- Call Channels*\n\n*1\. My bot detects the call but doesn\'t auto buy\.*\nPlease consult the Auto Buy Warnings section\.\n\n*2\. My bot auto buys but Auto Sell is always turned off\.*\nYou need to enable Auto\-Sell in both your wallet settings and the call channel settings\. This enables Auto\-Sell by default\.\n\n*3\. My bot isn\'t detecting a channel\'s calls\.*\nThis can happen for one of three reasons:\n  a\. You didn\'t enable \'Track\' for the call channel\. Even if you enable Auto Buy for the channel, you still need to enable \'Track\'\.\n  b\. The channel\'s call had no contract address in it\. If the call has any form of contract \(be it raw, manipulated, or through a chart link\), the bot will detect it\. If the channel call only has a description of the token and/or its Telegram group, you will NOT be notified\.\n  c\. The channel edited the contract address into the post more than 30 seconds after the initial post\. We don\'t report the contract in this case to protect you from late buys\.\n\n*4\. Will the bot buy the same token multiple times?*\nThe bot will never report the same token twice from a single channel\. This protects you from update posts\. However, the bot can buy the same token multiple times if multiple channels that you\'re following call the token\.\n\n*5\. How can I find call channels easily in the bot?*\nUse the \'Search\' button\. The button will prompt you for the channel\'s link or ID\.\n\n*6\. How can we add call channels?*\nChannel additions are now limited to top tier channels only\. To track groups/channels not currently in the bot, you can use the Maestro Telegram Scraper\.\n\n*7\. Can we add private channels and groups?*\nYou can follow whatever groups and channels you want using Maestro Telegram Scraper\.\n\n*8\. How many channels can I follow?*\nAs many as you wish\.\n\n*9\. Can I receive notifications without auto buying?*\nYes\. Simply track the channel without enabling Auto Buy\."

def auto_buy_warnings_text_menu() -> str:
    return "ℹ️ FAQ\n\n*Section 5 \- Auto\-Buy Warnings*\n\n*1\. Wallet auto buy is disabled*\nAuto\-Buy is disabled in your wallet configuration, which is accessible through /start ➡️ Wallets ➡️ BSC/ETH ➡️ Config\. If you want any call channel auto\-buys to activate, this needs to be enabled \(this has no effect on Auto Snipes\).\n\n*2\. Channel auto buy is disabled*\nAuto\-Buy is disabled in your call channel settings \(or \'Me\' channel settings in case of pasted contracts\), which is accessible through /start ➡️ Call Channels ➡️ BSC/ETH then clicking on the relevant channel\. If you want any call channel auto\-buys to activate, this needs to be enabled \(this has no effect on Auto Snipes\)\.\n\n*3\. Buy/Sell tax could not be estimated*\nThis normally happens for tokens that don\'t have trade enabled yet, or have no liquidity\. It will obviously prevent auto\-buys from going through\.\n\n*4\. Blacklist risk! Buying now could get you BLed*\nThis happens when the bot detects that your buy will get you blacklisted on the contract\. It will block the auto\-buy in these cases\.\n\n*5\. Token detected as honeypot!*\nThis happens when the bot detects that the token is a honeypot, which means that the token is unsellable\. It will block the auto\-buy in these cases\."

def transaction_error_messages_text_menu() -> str:
    return "ℹ️ FAQ\n\n*Section 6 \- Transaction Error Messages*\n\n*1\. Insufficient Output Amount*\nYour slippage tolerance is too low for this transaction\. Either increase your slippage tolerance in the wallet settings or increase your gas price/delta to gain more priority on the blockchain\.\n\n*2\. Excessive/Insufficient Input Amount*\nThis happens when the bot attempts to buy an exact number of number of tokens, but the token's volatility turns out to be too extreme, even with your slippage taken into consideration\. For example, assume that you want to buy exactly 1 token, and the current price for that 1 token is 1 BNB\. With 100% slippage, the bot will allow you to pay up to 2 BNB to get that token\. If the token's volatility is too extreme that even 2 BNB isn't enough to purchase 1 token, the transaction will fail\. For sells, it can happen when the bot is trying to sell 0 tokens\.\n\n*3\. Insufficient funds for gas x price + value*\nYour wallet doesn't have enough funds to cover the transaction value and its gas fees\. If you're using Ape Max, disable it and try again\. If not, double check your gas settings and compare the potential gas fees to your wallet's BNB/ETH balance\.\n\n*4\. Transfer Failed*\nThis error can happen for a multitude of reasons\. We mention a few here:\n  a\. Trade hasn't been enabled yet\.\n  b\. The transaction would've caused your wallet to exceed the contract's max wallet\.\n  c\. There's a maximum allowed gas price on the contract\.\n  d\. There's a transaction cooldown on the contract\.\n  e\. For sells, the maximum allowed sell might be smaller than your attempted transaction\.\n  f\. You got blacklisted, or the token became a honeypot\.\n\n*5\. Underpriced Transaction*\nThis error happens when you attempt a transaction while another transaction from the same wallet is already pending\. The bot supports only one transaction per wallet at any given time\."

def trade_monitor_text_menu() -> str:
    return "ℹ️ FAQ\n\n*Section 7 \- Trade Monitor*\n\n*1\. What's the difference between active and disabled trades?*\nActive trades benefit form access to live profit/loss tracking, Auto Sell functionality, and Smart Rug Auto Sell support\. However, disabled trades do not receive such benefits\.\n\n*2\. Why was my trade disabled?*\nTrades can become disabled for 2 reasons:\n  a\. You sold your entire balance of the token you were tracking\.\n  b\. 36 hours passed since you bought the token\. The timer next to each token indicates how much of the 36 hours is left\. You can refresh this duration back to 36 hours using the Refresh button\. The button can also re-activate disabled trades\.\n\n*3\. If I disable/delete a trade, will the bot sell?*\nNo\. Disabling or deleting a trade will not sell your holdings\.\n\n*4\. What does the Reset button do?*\nThe Reset button restarts tracking for the token, but uses your current token's BNB/ETH worth as the new initial\.\n\n*5\. I can't find my trade monitor\.*\nTry the following steps:\n  1\. Use /monitor\n  2\. If /monitor doesn't give you a trade monitor, you can paste the token's contract address into the bot, then press the Track button\. This will start a new monitor for that token\. However, your initial will be your token's current BNB/ETH worth\. If you want to restore the actual initial you bought in the bot, please navigate to the '✅ Buy transaction succeeded' message, and press the Track button under it\.\n\n*6\. Can I create a monitor for a token I bought outside the bot?*\nYes\. Paste the token's contract address and press the Track button\.\n\n*7\. How can I activate a disabled trade?*\nUse the Refresh button\.\n\n*8\. How many trades can the monitor hold?*\nYou are currently limited to 5 trades \(active and disabled\)\. To clear space for new trades, make sure to delete disabled trades using the Delete button\. The bot will also automatically replace disabled trades if you attempt to start another trade monitor while you're already at 5 trades\.\n\n*9\. I made two buys of the same token\. Can I combine them?*\nYou can combine multiple buys of the same token on the trade monitor ONLY IF the buys came from the same wallet\. For example, if you bought a token twice from the same wallet and are currently looking at two separate trade monitor panels for the same token, press Delete to remove one of the trades, then scroll over to the other trade and press Reset\. This will change the initial of that trade to match your current total worth of the token\.\n\n*10\. My monitor always starts with Auto Sell turned off\.*\nYou need to enable Auto Sell in both your wallet settings and the call channel settings \('Me' channel for pasted contracts\)\. This enables Auto Sell on the trade monitor by default\."

def multi_wallet_text_menu() -> str:
    return "ℹ️ FAQ\n\n*Section 8 \- Multi-wallet*\n\n*1\. How many wallets can I use?*\nYou can connect/generate 5 wallets in total \(1 main wallet + 4 additional wallets\)\.\n\n*2\. Can I buy with multiple wallets at the same time?*\nYes\. You need to enable Multi in the wallet settings \(in the Multi-Wallet menu\) and in the settings of the channel you wish to snipe \('Me' channel for pasted contracts\)\. Multi-wallet buys will not activate unless Multi is enabled in BOTH locations\.\n\n*3\. I enabled Multi but can't see a multi-buy button\.*\nThere is no multi-buy button\. If you want to multi-buy a pasted contract for example, enable Multi in the wallet settings and 'Me' channel settings\. Pasted contracts will now display ℹ️ Multi-wallet enabled, which means that any buy initiated from the main wallet will initiate a multi-wallet buy\.\n\n*4\. Does multi-wallet work for LP/method snipes?*\nYes, as long as Multi is enabled in the wallet settings \(no channel requirements\)\.\n\n*5\. Can I sell all wallets at the same time?*\nThere's no 'sell all' button in the bot yet\. Each wallet you bought with will get its own panel on the trade monitor\. You can setup Auto Sell beforehand to ensure that all wallets sell at the same time\.\n\n*6\. Gas and slippage settings for multi-wallets*\nYour multi-wallets will follow the settings of your main wallet\. This is done to ensure uniformity between all your wallets\."

def presales_text_menu() -> str:
    return  "ℹ️ FAQ\n\n*Section 9 \- Presales*\n\n*1\. What kind of presales do you support?*\nWe currently support Pinksale presales with BNB contributions only\. We will be expanding to other launchpads later on\.\n\n*2\. What is a presale address?*\nThe presale address is NOT the webpage link of the presale\. Go to the Pinksale presale page and find where it says 'Presale Address'\. It looks like a wallet address\.\n\n*3\. Which wallet will buy the presale?*\nYou can select the wallet you wish to contribute with directly in the Presale menu. Click on 💳 Main to cycle through the wallets.\n\n*4. Can the bot handle whitelists?*\nAs long as the wallet you choose to snipe with is whitelisted on the presale, you'll be able to buy.\n\n*5. Does the bot claim tokens for me?*\nNot at the moment. You have to claim the tokens manually, so make sure you have access to the wallet outside the bot.\n\n*6. What gas settings does presale sniping use?*\nYou can setup your presale gas price directly in the Presale menu. This will not affect your wallet gas price.\n\n*7. I always get beat by other buyers.*\nYour gas price determines your priority on the blockchain. It's common to see 100+ gwei on presales, so tailor your gas price to match how hyped the presale is going to be.\n\n*8. Does multi-wallet work with presales?*\nNot at the moment. Only your chosen wallet will attempt to buy the presale."

def copy_trade_text_menu() -> str:
    return "ℹ️ FAQ\n\n*Section 10 - Copytrade*\n\n*1. How does copytrade work?*\nAt the moment, copytrade enables you to auto buy/sell a token whenever the wallet you're tracking buys/sells it.\n\n*2. How many wallets can we track?*\nYou can track up to 2 wallets at the moment.\n\n*3. How does Auto Buy work in copytrade?*\nIf you want the bot to auto buy immediately when the tracked wallet performs a buy transaction, you NEED to choose an auto buy amount. The bot will use this amount as the maximum allowed auto buy. For example, if you set Auto Buy to 0.5 BNB and the tracked wallet buys 0.1 BNB, then the bot will also buy 0.1 BNB, matching the tracked wallet. However, if the tracked wallet buys any amount LARGER than 0.5 BNB, the bot will still only buy 0.5 BNB. This is done to shield you from the fluctuations in transaction values coming from tracked wallets, especially if you're tracking 'whale' wallets that are prone to large buys that most people can't afford.\n\n*4. How does Copy Sell work in copytrade?*\nThe bot will notify you whenever the tracked wallet sells tokens. It will then check whether you own the token or not. If you do own the token AND Copy Sell is enabled in the copytrade settings, the bot will attempt to copy the sell. If the tracked wallet sells a certain percentage (50% for example) of their token holdings, then the bot will sell the same percentage from your wallet (50% as well).\n\n*5. Can we frontrun the tracked wallet?*\nYes. More details on frontrunning can be found in the manual.\n\n*6. Does copytrade work with multi-wallets?*\nYes. Make sure that Multi is enabled in both the wallet settings and copytrade wallet settings.\n\n*7. Can I simply get notified without committing to an Auto Buy?*\nYes. Add the tracked wallet, turn on Copytrade, and make sure Auto Buy is disabled in the copytrade wallet settings."

def lp_method_sniping_text_menu() -> str:
    return  "ℹ️ FAQ\n\n*Section 11 - LP/Method Sniping*\n\n*1. Can the bot snipe liquidity and launch methods?*\nYes. LP/method sniping is accessible through Auto Snipe. Paste a token's contract, then press Auto Snipe to get started.\n\n*2. When do I use liquidity sniping?*\nSniping liquidity is an advanced technique that allows you to buy as soon as liquidity is added, provided that trading has NO OTHER RESTRICTIONS. In other words, the only restriction to trading is the fact that liquidity is not yet present.\n\n*3. When do I use method sniping?*\nMethod sniping, unlike liquidity sniping, allows you to buy as soon as the targeted launch method is activated by the contract owner. Method sniping should be used in situations where trade is restricted from within the contract, and those restrictions can only be lifted when the owner activates a method like 'enableTrading' for example.\n\n*4. Why do we need block delays?*\nYou should utilize block delays to avoid deadblocks. A deadblock is a block that would get your transaction rejected or your wallet blacklisted on the contract. Contract owners place a small number of deadblocks after launch to deter and catch snipers. You can counter this by setting a block delay to avoid the deadblocks. To find the ideal block delay, make sure you go through the contract you're attempting to snipe.\n\n*5. Can the bot adjust for max buy on Auto Snipe?*\nYes. The only case where we can't auto-adjust for you is 0 block delay sniping, so make sure you choose a suitable amount of BNB/ETH in those scenarios.\n\n*6. Risks of 0 block delay sniping*\nZero block delay sniping means that the bot will attempt to buy as soon as the transaction that adds liquidity or activates the targeted method (depending on your choice) is initiated. In this case, the bot will adjust your gas price in an attempt to avoid frontrunning these transactions. However, these launch transactions normally use the minimum required gas price to be mined, so we can only match their gas price. With matched gas prices, there's a small chance that your snipe will fail, as the buy transaction could go through before the liquidity addition or method. Even if there are no deadblocks, the safest liquidity/method sniping involves setting the block delay to 1. This ensures that the bot will buy on the next block, removing the possibility of accidentally frontrunning the liquidity addition or method activation transactions.\n\n*7. What gas settings does Auto Snipe use?*\nFor 0 block delay sniping, the bot automatically matches the gas price of the transaction you're targeting. For anything other than 0 block delay sniping, Auto Snipe uses your wallet's gas settings.\n\n*8. Can you use multi-wallet with Auto Snipe?*\nYes, as long as Multi is enabled in the wallet settings (no channel requirements)."

def smart_rug_protection_text_menu() -> str:
    return "ℹ️ FAQ\n\n*Section 12 - Smart Rug Auto Sell*\n\n*1. How does this work?*\nWhen the bot detects any 'rug' transaction that can mess with your ability to sell successfully, the bot will attempt to frontrun that transaction.\n\n*2. Does it only work for liquidity pulls?*\nNo. Smart Rug Auto Sell covers blacklisting, trade disabling, tax changes, max transaction changes, and many other types of rugs. We call it Smart for a reason.\n\n*3. Will I be facing high gas fees for frontrunning?*\nThat depends on the gas settings used by the rug transaction. The bot will automatically re-configure its gas settings based on those used by the rug transaction. This is done to maximize the chances of frontrunning. If the rug is using a very high gas price, then frontrunning it requires paying higher gas fees. If the rug is using normal gas prices, then frontrunning it is cheap.\n\n*4. I keep getting the 'insufficient funds' error.*\nThen your wallet doesn't have enough to fund the frontrun, or the rug transaction was using a prohibitively high gas price.\n\n*5. Why does the frontrun fail here and there?*\nThere's a myriad of variables at play when frontruns of this nature are attempted. Frontrunning rug transactions is extremely consistent on ETH, where block times are sufficiently long. However, it's less consistent on BSC, since the chain's block times are quite short and give us very little leeway. Frontrunning rugs will save you in most situations, but it's never guaranteed, so don't over-rely on it.\n\n*6. Is this active for all tokens in my wallet?*\nNo. Smart Rug Auto Sell can only activate for tokens being tracked by an ACTIVE trade monitor in the bot."



def text_wallet_menu(crypto, context, user_id) -> str:
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

def get_user_data():
    return user_data


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

    application.add_handler(CallbackQueryHandler(premium, pattern='premium'))

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
    application.add_handler(CallbackQueryHandler(show_faq_text, pattern='faq_.*'))
    application.add_handler(CallbackQueryHandler(faq, pattern='faq'))


    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_wallet_ct, pattern='add_ct_wallet_.*')],
        states={
            AWAITING_WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_wallet_address)],
            AWAITING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_wallet_name)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    # Error handler
    application.add_error_handler(error)

    # Start polling
    application.run_polling(5)
