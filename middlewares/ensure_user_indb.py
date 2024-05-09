from pyrogram import Client
from pyrogram.types import Message
from helper_func import check_and_add_user

# Define your middleware function
async def ensure_user_indb(client: Client, message: Message):
    msg = message
    await check_and_add_user(msg.chat, msg.from_user)
    return True