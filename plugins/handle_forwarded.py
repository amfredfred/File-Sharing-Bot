from bot import Bot
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from plugins.link_generator import moveto_cloud
from config import TELEGRAM_SHARE_URL


@Bot.on_message(filters.forwarded)
async def handle_forwarded_message(client: Client, message: Message):

    reply_text = await message.reply_text("Please wait...")
    isSuccess, link, share_link, post_message = await moveto_cloud(client, message)
    if isSuccess:
        buttons = []
        buttons.append([InlineKeyboardButton("🔁 Share URL", url=f"{TELEGRAM_SHARE_URL}{link}")])
        reply_markup = InlineKeyboardMarkup(buttons)

        await reply_text.edit(
            text=f"<b>Your Post Is Uploaded: </b>\n\n{link}",
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )
