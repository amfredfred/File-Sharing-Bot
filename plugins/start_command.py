# (©)CodeXBotz


import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from helper_func import command_clean, decode
from managers.callback import CallbackDataManager

from bot import Bot
from config import (
    ADMINS,
    FORCE_MSG,
)

from helper_func import (
    subscribed,
    get_messages,
    extract_ids,
    copy_messages,
    starts_with_bot_username,
)
from database.database import del_user, full_userbase

command = "start"

WELCOME_TEXT = "🤟💚💛💛💚🤟\n"
WELCOME_TEXT += "<b>Hi, I`m your ultimate companion</b> for exploring and downloading digital content hassle-free! "
WELCOME_TEXT += (
    "Whether you're in search of the latest blockbuster movie, trending music tracks, "
)
WELCOME_TEXT += "captivating pictures, or any downloadable files from a link, i`ve has got you covered."

#
WELCOME_TEXT += "\n\n🔑 <b>Key Features:</b>\n\n"
WELCOME_TEXT += "🎬 <b>Movie Finder:</b>\n\n"
WELCOME_TEXT += "Discover a vast collection of movies spanning various genres, from action-packed thrillers to heartwarming dramas. Simply type in the movie's title, and our bot will swiftly fetch relevant results, complete with details like synopsis, cast, and ratings. 🍿\n\n"
WELCOME_TEXT += "🎵 <b>Music Hunter:</b>\n\n"
WELCOME_TEXT += "Dive into the realm of melodies with our music search feature. Search for your favorite songs, albums, or artists, and our bot will provide you with direct download links or streaming options. 🎶\n\n"
WELCOME_TEXT += "📥 <b>Download Manager:</b>\n\n"
WELCOME_TEXT += "Need to download a file or content from a specific link? Look no further! Simply paste the link, and our bot will analyze it to extract any downloadable files, making the process effortless. 🚀"

#

WELCOM_REPLY_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🤝 About Me", callback_data="about"),
            InlineKeyboardButton("❓ Need Help", callback_data="how_to_use_bot"),
            InlineKeyboardButton("🗑️ Close", callback_data="close"),
        ]
    ]
)


async def send_start_message(message: Message):
    await message.reply_text(
        text=WELCOME_TEXT,
        reply_markup=WELCOM_REPLY_MARKUP,
        disable_web_page_preview=True,
        quote=True,
    )


@Bot.on_message(filters.command(command) & ~filters.channel & subscribed)
async def start_command(client: Client, message: Message):
    text = message.text
    comm_clean = command_clean(text)
    cdm = CallbackDataManager()
    encoded_data = cdm.get_data_from_callback(comm_clean)
    decoded_message = text
    try:
        if encoded_data:
            decoded_message = await decode(encoded_data)
            message.text = decoded_message
            if decoded_message:
                comm_clean = command_clean(decoded_message) 
                if comm_clean:
                    from plugins.on_message import handle_message
                    return await handle_message(client, message)
    except Exception as e:
        print(f"Exception In Start Command: {e}")
        return await message.reply_text(f"Something went wrong while trying to get where you wanted 😔", quote=True)

   
    return await send_start_message(message)


# =====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

# =====================================================================================##


@Bot.on_message(filters.command(command) & (filters.private or filters.group))
async def not_joined(client: Client, message: Message):
    buttons = [[InlineKeyboardButton("Join Channel", url=client.invitelink)]]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Try Again",
                    url=f"https://t.me/{client.username}?start={message.command[1]}",
                )
            ]
        )
    except IndexError:
        pass
    except Exception as e:
        pass

    # Construct the message using f-strings for formatting
    await message.reply(
        text=FORCE_MSG.format(invitelink=client.invitelink),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True,
    )

@Bot.on_message(filters.command("users") & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")
