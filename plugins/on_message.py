# (©)Codexbotz

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import DISABLE_CHANNEL_BUTTON
from helper_func import extract_urls, extract_url
from responses import ResponseMessage
from plugins.link_generator import moveto_cloud

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


@Bot.on_message(
    filters.private & ~filters.channel & ~filters.command(["start", "search"])
)
async def handle_message(client: Client, message: Message):

    msg_text = message.text if not None else " "
    if msg_text:
        msg_text = message.text.strip()

    try:
        from managers.command.methods import command_extract, command_call
        command_ext = command_extract(msg_text)
        if isinstance(command_ext, dict):
            await command_call(client, message, command_ext["name"])
            return
        elif command_ext == False:
            print("Invalid Command supplied")
        else:
            print(f"No Commadn Supplied, Proceed")

        reply_text = await message.reply_text("Please Wait...!", quote=True)
        hasUrl, isDownloadable  = extract_url(msg_text)
        if hasUrl:
            try:
                reply_markup = await rspmsg.response_when_has_link(hasUrl)
                print(f"response_markup: {reply_markup}")
                _text = f"<b><u>Check Out Details Below</u></b>"
                await message.delete()
                return await reply_text.edit_text(
                    _text,
                    reply_markup=reply_markup,
                    disable_web_page_preview=True,
                )
            except Exception as e:
                print(f"Exception: {e}")
        else:
            response_message_markup = await rspmsg.response_when_plain_text(msg_text)
            respond_text = f"<b><u>What do you want me to do with this text?</u></b>\n\n<code>{msg_text}</code>\n\n"
            return await reply_text.edit_text(
                respond_text, reply_markup=response_message_markup
            )

        isSuccess, cloudLink, share_link, post_message = await moveto_cloud(
            client, message
        )
        if not isSuccess:
            sorry_text = f"Sorry, could not upload your message to cloud. 😟"
            return await message.edit_text(sorry_text)

        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔁 Share URL", url=share_link)]]
        )

        await reply_text.edit(
            f"<b>Here is your link</b>\n\n{share_link}",
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
        print(f"Done {msg_text}")


handle_messages = handle_message
