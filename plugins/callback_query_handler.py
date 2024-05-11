# (©)Codexbotz

from pyrogram import __version__
from pyrogram import filters
from bot import Bot
from config import OWNER_ID
from helper_func import decode
from models.calling_back import CallbackDataManager
from plugins.start_command import WELCOM_REPLY_MARKUP, WELCOME_TEXT
from managers.command.command_dicts import command_list, command_list_public
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)


ABOUT_TEXT = f"<b>○ Creator : <a href='tg://user?id={OWNER_ID}'>This Person</a>\n"
ABOUT_TEXT += f"○ Language : <code>Python3</code>\n"
ABOUT_TEXT += f"○ Library : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio {__version__}</a>\n"

HOW_TO_USE_TEXT = "<b>🤖 How to Use:</b>\n"
HOW_TO_USE_TEXT += "1. <b>Start:</b> Begin by starting a chat with our bot.\n"
HOW_TO_USE_TEXT += "2. <b>Enter Query:</b> Input search query or paste me a link.\n"
HOW_TO_USE_TEXT += "2. <b>Enjoy:</b> Relax as our bot fetches content for you.\n\n"
HOW_TO_USE_TEXT += "Feel free to explore! For commands, use '/start'.\n\n"

for command, details in command_list_public.items():
    HOW_TO_USE_TEXT += f"<b>{details['name']}:</b>\n"
    if details["desc"]:
        HOW_TO_USE_TEXT += f"{details['desc']}\n\n"
    else:
        HOW_TO_USE_TEXT += f"To use this command, simply type {details['command']} followed by your query.\n\n"
HOW_TO_USE_TEXT += "That's it! Now you're ready to explore few of the features i can offer. Happy browsing!"


DEFAULT_REPLY_MARKUP = [  [
    InlineKeyboardButton("🔙 Back", callback_data="start"),
    InlineKeyboardButton("🔒 Close", callback_data="close"),
]]

@Bot.on_callback_query()
async def callback_handler(client: Bot, query: CallbackQuery):
    data = query.data
    message = query.message
    try:
        cdm = CallbackDataManager()
        encoded_data = cdm.get_data_from_callback(data)
        if encoded_data:
            decoded_message = await decode(encoded_data)
            if decoded_message:
                from managers.command.methods import command_clean

                comm_clean = command_clean(encoded_data)
                if comm_clean:
                    message = query.message
                    message.text = decoded_message.replace("%20", " ")
                    from plugins.on_message import handle_message

                    # HERE======================
                    return await handle_message(client, message)
    except Exception as e:
        print(f"Exception In Callback_Handler: {e}")
        await query.message.edit_text("<b>SOMETHING UNUSUAL HAS HAPPENED</b>")

    if data == "about": 
        await query.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(DEFAULT_REPLY_MARKUP),
        )

    elif data == "start":
        return await message.edit_text(
            WELCOME_TEXT,
            reply_markup=WELCOM_REPLY_MARKUP,
            disable_web_page_preview=False,
        )

    elif data == 'how_to_use_bot':
        await query.message.edit_text(
            text=HOW_TO_USE_TEXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(DEFAULT_REPLY_MARKUP),
        )

    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

    # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # #
