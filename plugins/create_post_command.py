from injector import injector
from bot import Bot
from pyrogram.types import Message
from pyrogram import filters, Client
from models import Profile

COMMAND = "create_post"
DESCRIPTION = ""

@Bot.on_message(filters.command(COMMAND))
@injector
async def create_post_command(client: Client, profile: Profile, message: Message):
    print(" Creat Post", profile)