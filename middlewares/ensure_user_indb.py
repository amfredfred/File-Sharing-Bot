from pyrogram import Client
from pyrogram.types import Message
from database.database import present_user,add_user
from models.profile import Profile
from helper_func import check_and_add_user

_profile = Profile()

# Define your middleware function
async def ensure_user_indb(client: Client, message: Message):
    msg = message
    await check_and_add_user(msg.chat, msg.from_user)
    return True
