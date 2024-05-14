from pyrogram import filters, client
from helper_func import link_type, extract_url, encode
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from scrapers.facebook import FacebookVideoDownloader
from models.calling_back import CallbackDataManager
import json
from bot import Bot
from injector import injector
from models.profile import Profile
from config import FACEBOOK_DISCALIMER


@Bot.on_message(filters.command("check_link") & ~filters.channel)
@injector
async def check_link_command(bot: client, profile: Profile, message: Message):
    callable_m = CallbackDataManager()
    msg_text = message.text if not None else " "
    if msg_text:
        msg_text = message.text.strip()
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    hasUrl, isDownloadable = extract_url(msg_text)
    type_link = link_type(hasUrl)

    # Construct message based on link type
    if type_link == "facebook_watch":
        msg = "This is a Facebook Watch link."
        facebook = FacebookVideoDownloader()
        result = json.loads(await facebook.download(hasUrl))
        if result["success"]:
            title = result["title"]
            links = result["links"]
            msg = FACEBOOK_DISCALIMER + f"\n\nTitle: {title}\n\nDownload Options:"
            buttons = []
            for key, value in links.items():
                # callable_mdata = await encode(f"/download {value}")
                # callable_mdata = callable_m.generate_callback_data(callable_mdata)
                buttons.append([InlineKeyboardButton(text=key, url=value)])
            keyboard = InlineKeyboardMarkup(buttons)
            return await reply_text.edit_text(msg, reply_markup=keyboard)
    elif type_link == "telegram":
        return await reply_text.edit_text("Sorry, telegram links are not supported yet")
    elif type_link == "media":
        from plugins.download_command import download_command

        return await download_command(bot, message)
    elif type_link == "webpage":
        from plugins.download_command import download_command

        return await download_command(bot, message)
    else:
        return await reply_text.edit("Hey, sorry i could not process your link")
