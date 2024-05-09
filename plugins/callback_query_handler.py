# (©)Codexbotz

from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from helper_func import decode
from managers.callback import CallbackDataManager
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)


@Bot.on_callback_query()
async def callback_handler(client: Bot, query: CallbackQuery):
    data = query.data
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
                    #HERE======================
                    return await handle_message(client, message)
    except Exception as e:
        print(f"Exception In Callback_Handler: {e}")
        await query.message.edit_text("<b>SOMETHING UNUSUAL HAS HAPPENED</b>")

    if data == "about":
        await query.message.edit_text(
            text=f"<b>○ Creator : <a href='tg://user?id={OWNER_ID}'>This Person</a>\n○ Language : <code>Python3</code>\n○ Library : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio {__version__}</a>\n",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔒 Close", callback_data="close")]]
            ),
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
