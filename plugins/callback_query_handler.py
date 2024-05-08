# (©)Codexbotz

from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from helper_func import decode
# from plugins.on_message import handle_message
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)


@Bot.on_callback_query()
async def callback_handler(client: Bot, query: CallbackQuery):

    data = query.data
    from managers.command.methods import command_clean
    comm_clean = command_clean(data)
    if comm_clean:
        decoded_message = await decode(comm_clean)
        if decoded_message:
            message = query.message
            message.text = decoded_message.replace("%20", ' ')
            await query.message.reply_to_message.delete()
            from plugins.on_message import handle_message
            return await handle_message(client, message)

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

    elif True:
        command_ext = "command_extract(data)"
        # print(f"callback data {data} command_ext: {command_ext}, ")
        # if isinstance(command_ext, dict):
        #     await handle_message(client, query.message)
