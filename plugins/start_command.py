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
WELCOME_TEXT += "Whether you're in search of the latest blockbuster movie, trending music tracks, "
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


@Bot.on_message(filters.command(command) & filters.private & subscribed)
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

    if len(decoded_message) > 7 and not starts_with_bot_username(client.me.username, decoded_message):
        ids = await extract_ids(client, decoded_message)
        if not ids:
            return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()
        await copy_messages(client, message, messages)
    else:
        await send_start_message(message)


# =====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

# =====================================================================================##


@Bot.on_message(filters.command(command) & filters.private)
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

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=(
                None
                if not message.from_user.username
                else "@" + message.from_user.username
            ),
            mention=message.from_user.mention,
            id=message.from_user.id,
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True,
    )


@Bot.on_message(filters.command("users") & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")


@Bot.on_message(filters.private & filters.command("broadcast") & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply(
            "<i>Broadcasting Message.. This will Take Some Time</i>"
        )
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1

        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
