user_data = {}
message_ids = {}


def get_user_data():
    return user_data

async def reply_message_conv(update, user_id, text):
    message = await update.message.reply_text(text)
    # Store the message ID to delete later
    if user_id not in message_ids:
        message_ids[user_id] = {'bot': [], 'user': []}
    message_ids[user_id]['user'].append(update.message.message_id)
    message_ids[user_id]['bot'].append(message.message_id)

async def delete_conv(update, user_id):
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