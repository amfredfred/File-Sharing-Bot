from bot import Bot
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from plugins.link_generator import moveto_cloud
from config import TELEGRAM_SHARE_URL
from injector import injector
from models.profile import Profile


@Bot.on_message(filters.forwarded)
@injector
async def upload_command(client: Client, profile: Profile, message: Message):

    try:
        isSuccess, link, share_link, post_message = await moveto_cloud(
            client, message, profile.id
        )
        if isSuccess:
            reply_text = await message.reply_text("Please wait...", quote=True)
            buttons = []
            buttons.append(
                [
                    InlineKeyboardButton(
                        "🔁 Share URL", url=f"{TELEGRAM_SHARE_URL}{link}"
                    )
                ]
            )
            reply_markup = InlineKeyboardMarkup(buttons)

            UPLOADED_TEXT = "<b>✨✨Uploaded✨✨</b>\n\n"
            UPLOADED_TEXT += f"<code>{link}</code>"
            await reply_text.edit_text(
                text=UPLOADED_TEXT,
                reply_markup=reply_markup,
                disable_web_page_preview=True,
            )
    except Exception as e:
        await message.delete()
        pass
