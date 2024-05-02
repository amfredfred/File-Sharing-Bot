from managers.download.manager import DownloadManager
from pyrogram.types import Message, InputMedia
from pyrogram.enums import ChatAction
from pyrogram import filters
from bot import Bot
from helper_func import extract_url, get_readable_time
from datetime import datetime
from tqdm import tqdm

dm = DownloadManager()

# Define command names
COMMAND_START = "download"
COMMAND_END = "cancel_end"


async def callback(msg: Message, media_url: str, file_name: str):
    chat_id = msg.chat.id
    media = InputMedia(file_name).media
    if media_url.endswith((".mp4", ".avi", ".mkv")):
        await msg.reply_video(media)
    elif media_url.endswith((".mp3", ".ogg")):
        await msg.reply_audio(media)
    elif media_url.endswith((".jpg", ".jpeg", ".png", ".gif")):
        await msg.reply_chat_action(action=ChatAction.UPLOAD_PHOTO)
        await msg.reply_photo(media)
    else:
        await msg.reply_chat_action(action=ChatAction.UPLOAD_DOCUMENT)
        await msg.reply_document(media)
    await msg.edit_text("<strong><u>Download completed 💪</ul></strong>")


async def progress(msg: Message, total_size, downloaded):
    current_timestamp = datetime.now().timestamp()
    readable_date = get_readable_time(current_timestamp)
    total_size_mb = total_size / (1024 * 1024)
    downloaded_mb = downloaded / (1024 * 1024)
    message = f"<b>Downloading</b>\n<b>Total Size:</b> {total_size_mb:.2f} MB\n<b>Downloaded:</b> {downloaded_mb:.2f} MB"
    await msg.edit_text(message)
 

@Bot.on_message(filters.command(COMMAND_START))
async def download_link(bot: Bot, message: Message):
    expect_link = message.text.strip()
    msg = await message.reply_text("<strong><u>Checking Link...</ul></strong>")
    expect_link = extract_url(expect_link)
    if expect_link:
        link = dm._parse_link(expect_link)
        url = link.get("url")
        link_type = link.get("type")
        if link_type is "telegram":
            print("TELEGRAAM LINK")
        elif link_type is "media":
            await msg.edit_text("<strong><u>Downloading...</ul></strong>")
            response = await dm.download_and_send_media(msg, url, callback, progress)
            if isinstance(response, str):
                return await msg.edit_text(response)
        else:
            urls = link.get("urls")
            urls_message = dm.download_options(urls)
            return await msg.edit_text(f"<b><u>Nicely Scraped</u><b>\n{urls_message}")
    await message.delete()
