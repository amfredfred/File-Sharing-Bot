from managers.download.manager import DownloadManager
from pyrogram.types import Message, InputMedia
from pyrogram.enums import ChatAction
from pyrogram import filters
from bot import Bot
from helper_func import extract_url
from config import INVALID_URL_TEXT
from responses import ResponseMessage
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

dm = DownloadManager()

# Define command names
COMMAND_START = "download"
COMMAND_END = "cancel_download"


async def on_success(msg: Message, media_url: str, file_name: str, caption=""):
    chat_id = msg.chat.id
    media = InputMedia(file_name).media
    if media_url.endswith((".mp4", ".avi", ".mkv")):
        await msg.reply_chat_action(action=ChatAction.UPLOAD_VIDEO)
        await msg.reply_video(media, caption=caption)
    elif media_url.endswith((".mp3", ".ogg")):
        await msg.reply_chat_action(action=ChatAction.UPLOAD_AUDIO)
        await msg.reply_audio(media, caption=caption)
    elif media_url.endswith((".jpg", ".jpeg", ".png", ".gif")):
        await msg.reply_chat_action(action=ChatAction.UPLOAD_PHOTO)
        await msg.reply_photo(media, caption=caption)
    else:
        await msg.reply_chat_action(action=ChatAction.UPLOAD_DOCUMENT)
        await msg.reply_document(media, caption=caption)
    await msg.edit_text("<b><u>Downloaded 100%</u></b>")


async def on_update(msg: Message, total_size, downloaded):
    total_size_mb = total_size / (1024 * 1024)
    downloaded_mb = downloaded / (1024 * 1024)
    progress_percentage = (downloaded / total_size) * 100

    # Progress bar visualization
    completed_blocks = int(progress_percentage / 10)
    remaining_blocks = 10 - completed_blocks
    progress_bar = "▪️" * completed_blocks + "▫️" * remaining_blocks

    # Speed calculation and formatting
    speed = downloaded / (1024)  # Speed in KB/sec
    eta_seconds = (total_size - downloaded) / speed if speed > 0 else 0
    eta_minutes = int(eta_seconds / 60)
    eta_seconds_remaining = int(eta_seconds % 60)

    # Format the message
    message = (
        f"<b>Downloading:</b> {progress_percentage:.2f}%\n"
        f"<b>Progress:</b> {progress_bar}\n"
        f"<b>Total Size:</b> {total_size_mb:.2f} MB\n"
        f"<b>Downloaded:</b> {downloaded_mb:.2f} MB\n"
        f"<b>Speed:</b> {speed:.2f} KB/sec\n"
        f"<b>ETA:</b> {eta_minutes}m, {eta_seconds_remaining}s"
    )

    # Edit the message
    return await msg.edit_text(message)


response_msg = ResponseMessage()


@Bot.on_message(filters.private and filters.command(COMMAND_START))
async def download_command(bot: Bot, message: Message):
    msg_text = message.text.strip()
    msg = await message.reply_text("<strong><u>Checking Link...</ul></strong>")
    expect_link, isDownloadable = extract_url(msg_text)
    if expect_link:
        link = await dm._parse_link(expect_link)
        url = link.get("url")
        link_type = link.get("type")
        if link_type == "telegram":
            print("TELEGRAAM LINK")
            return await msg.edit_text("<b><u>Telegram link is not supported yet</u></b>")
        elif link_type == "media":
            await msg.edit_text("<strong><u>Downloading...</ul></strong>")
            response = await dm.download_and_send_media(msg, url, on_success, on_update)
            if isinstance(response, str):
                return await msg.edit_text(response)
        else:
            urls = link.get("urls")
            found, reply_markup = await response_msg.download_options(urls)
            ressponse_text = "<b><u>➿ Found few stuffs 🍭</u><b>"
            if not found and not urls:
                ressponse_text = "<b><u>No downloadable links from your search 🙏</u><b"
                buttons = []
                buttons.append([InlineKeyboardButton("🔗 Visit Website 🔗", url=url)])
                reply_markup = InlineKeyboardMarkup(buttons)
            # else:

            return await msg.edit_text(f"{ressponse_text}", reply_markup=reply_markup)
    else:
        await message.delete()
        return await msg.edit_text(INVALID_URL_TEXT.format(text=msg_text))
