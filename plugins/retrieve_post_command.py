from bot import Bot
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from plugins.link_generator import get_from_cloud
from config import TELEGRAM_SHARE_URL
from injector import injector
from models.profile import Profile

command = "retrieve_post"


@Bot.on_message(filters.command(command) & filters.private)
@injector
async def retrieve_post_command(client: Client, profile: Profile, message: Message):
    retrieved_post = await get_from_cloud(client, message)
    _from = message.from_user
    _chat = message.chat
    for retrieved in retrieved_post:
        if isinstance(retrieved, Message) and _from:
            # reply_markup = {**retrieved.reply_markup}
            # reply_markup.append([InlineKeyboardButton("🔁 Share URL", url=f"{TELEGRAM_SHARE_URL}{link}")])
            # reply_markup = InlineKeyboardMarkup()
            # retrieved.reply_markup = reply_markup
            await retrieved.copy(chat_id=_chat.id)
            # return await retrieved_post.copy(_chat.id)
