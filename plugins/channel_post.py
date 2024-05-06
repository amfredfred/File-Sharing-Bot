# (©)Codexbotz

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode, extract_urls
from responses.index import ResponseMessage
from managers.command.manager import CommandManager, command_names, command_list

OFF_COMMANDS = [
    "start",
    "users",
    "broadcast",
    "batch",
    "genlink",
    "search",
    "cs",
    "download",
    "account",
]

rspmsg = ResponseMessage()


@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(OFF_COMMANDS))
async def channel_post(client: Client, message: Message):

    reply_text = await message.reply_text("Please Wait...!", quote=True)
    msg_text = message.text.strip()

    try:
        comm_man = CommandManager(client, message)
        command_ext = comm_man.command_extract(msg_text)
        if isinstance(command_ext, dict):
            await comm_man.command_call(command_ext["name"])
            await reply_text.delete()
            return
        elif command_ext == False:
            print("Invalid Command supplied")
        else:
            print(f"No Commadn Supplied, Proceed")

        urls = extract_urls(msg_text)
        if urls:
            try:
                response_text, _ = rspmsg.response_check_links(urls)
                return await reply_text.edit_text("_", reply_markup=response_text)
            except Exception as e:
                print(f"Exception: {e}")

        try:
            post_message = await message.copy(
                chat_id=client.db_channel.id, disable_notification=True
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            post_message = await message.copy(
                chat_id=client.db_channel.id, disable_notification=True
            )
        except Exception as e:
            print(e)
            await reply_text.edit_text("Something went Wrong..!")
            return
        converted_id = post_message.id * abs(client.db_channel.id)
        string = f"get-{converted_id}"
        base64_string = await encode(string)
        link = f"https://t.me/{client.username}?start={base64_string}"

        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔁 Share URL", url=f"https://telegram.me/share/url?url={link}"
                    )
                ]
            ]
        )

        await reply_text.edit(
            f"<b>Here is your link</b>\n\n{link}",
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )

        if not DISABLE_CHANNEL_BUTTON:
            try:
                await post_message.edit_reply_markup(reply_markup)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await post_message.edit_reply_markup(reply_markup)
            except Exception:
                pass
    except Exception as e:
        print(f"Happened: {e}")
    finally:
        print("Done")

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔁 Share URL", url=f"https://telegram.me/share/url?url={link}"
                )
            ]
        ]
    )
    try:
        await message.edit_reply_markup(reply_markup)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await message.edit_reply_markup(reply_markup)
    except Exception:
        pass
