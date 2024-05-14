from bot import Bot
from pyrogram import filters, Client
from pyrogram.types import Message

from plugins.upload_command import upload_command
from injector import injector
from models.profile import Profile


@Bot.on_message(filters.forwarded)
@injector
async def handle_forwarded_message(client: Client, profile: Profile, message: Message):

    return await upload_command(client, message)
