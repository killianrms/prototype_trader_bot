import os
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram import Update

# Global variables
message_info = {}
stored_value = 0  # This is the global value that will be updated

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global stored_value
    # Send a message to the user and store the message info for later updates
    sent_message = await update.message.reply_text(f'The current value is: {stored_value}')
    message_info['chat_id'] = sent_message.chat_id
    message_info['message_id'] = sent_message.message_id

# Handle user input
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global message_info, stored_value
    user_value = int(update.message.text)  # Assume user sends a number

    # Update the global stored value
    stored_value += user_value

    # Check if the message_info has valid chat and message IDs
    if "chat_id" in message_info and "message_id" in message_info:
        # Update the message with the new stored value
        await context.bot.edit_message_text(
            chat_id=message_info['chat_id'],
            message_id=message_info['message_id'],
            text=f'The current value is: {stored_value}'
        )

def main() -> None:
    TOKEN = os.getenv('TOKEN')

    # Create the application
    application = Application.builder().token("7491040520:AAGFMSs5YUA7f1LE6wnOVPda9gX51GVX3us").build()

    # Register command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
