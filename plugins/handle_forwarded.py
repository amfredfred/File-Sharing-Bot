from bot import Bot
from pyrogram import filters, Client
from pyrogram.types import Message

from plugins.upload_command import upload_command


@Bot.on_message(filters.forwarded)
async def handle_forwarded_message(client: Client, message: Message):

    return await upload_command(client, message)
