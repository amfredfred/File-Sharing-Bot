from pyrogram import Client
from pyrogram.types import Message
from helper_func import check_and_add_user, is_subscribed


# Define your middleware function
async def ensure_user_indb(client: Client, message: Message):
    msg = message
    await check_and_add_user(msg.chat, msg.from_user) 
    return True


async def ensure_user_issubscribed_channel(client: Client, message: Message):
    isSuscribed = await is_subscribed(None, client, message) 
    if not isSuscribed and message.from_user:
        from plugins.start_command import not_joined
        await not_joined(client, message)
    return isSuscribed
