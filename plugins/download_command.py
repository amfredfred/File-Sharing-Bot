from managers.download.manager import DownloadManager
from pyrogram.types import Message, InputMedia
from pyrogram.enums import ChatAction
from pyrogram import filters
from bot import Bot
from helper_func import extract_url, make_share_handle, subscribed
from config import INVALID_URL_TEXT, NO_DOWNLOADABLE_RESPONSE
from responses import ResponseMessage
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

dm = DownloadManager()

# Define command names
COMMAND_START = "download"
COMMAND_END = "cancel_download"


async def on_success(msg: Message, media_url: str, file_name: str, caption=""):
    media = InputMedia(file_name).media
    _IShare, _iTGSgare = await make_share_handle(msg.command_text)
    buttons = [[InlineKeyboardButton("📤Share📤", url=_iTGSgare)]]
    reply_markup = InlineKeyboardMarkup(buttons)

    if media_url.endswith((".mp4", ".avi", ".mkv")):
        await msg.reply_chat_action(action=ChatAction.UPLOAD_VIDEO)
        await msg.reply_video(media, caption=caption, reply_markup=reply_markup)
    elif media_url.endswith((".mp3", ".ogg")):
        await msg.reply_chat_action(action=ChatAction.UPLOAD_AUDIO)
        await msg.reply_audio(media, caption=caption, reply_markup=reply_markup)
    elif media_url.endswith((".jpg", ".jpeg", ".png", ".gif")):
        await msg.reply_chat_action(action=ChatAction.UPLOAD_PHOTO)
        await msg.reply_photo(media, caption=caption, reply_markup=reply_markup)
    else:
        await msg.reply_chat_action(action=ChatAction.UPLOAD_DOCUMENT)
        await msg.reply_document(media, caption=caption, reply_markup=reply_markup)
    pass


async def on_update(msg: Message, total_size, downloaded):
    total_size_mb = total_size / (1024 * 1024)
    downloaded_mb = downloaded / (1024 * 1024)
    progress_percentage = (downloaded / total_size) * 100

    # Progress bar visualization
    completed_blocks = int(progress_percentage / 10)
    remaining_blocks = 10 - completed_blocks
    progress_bar = "🟢" * completed_blocks + "⚫" * remaining_blocks

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


@Bot.on_message(~filters.channel and filters.command(COMMAND_START) & subscribed)
async def download_command(bot: Bot, message: Message):
    msg_text = message.text.strip()
    msg = await message.reply_text("<strong><u>Checking For Options...</ul></strong>", quote=True)
    expect_link, isDownloadable = extract_url(msg_text)
    if expect_link:
        msg.command_text = msg_text
        link = await dm.check_link_type(expect_link)
        url = link.get("url")
        link_type = link.get("type")
        if link_type == "telegram":
            print("TELEGRAAM LINK")
            return await msg.edit_text(
                "<b><u>Telegram link is not supported yet</u></b>"
            )
        elif link_type == "media":
            await msg.edit_text("<strong><u>Downloading...</ul></strong>")
            response = await dm.download_and_send_media(msg, url, on_success, on_update)
            if isinstance(response, str):
                return await msg.edit_text(response)
            else:
                await msg.delete()
        elif link_type == "webpage":
            urls = link.get("urls")
            found, reply_markup = await response_msg.download_options(urls, expect_link)
            ressponse_text = "<b><u>🟢FOUND FEW STUFFS</u><b>"
            if not found:
                ressponse_text = NO_DOWNLOADABLE_RESPONSE
            # else:
            return await msg.edit_text(ressponse_text, reply_markup=reply_markup)
        elif link_type == 'facebook_watch':
            from plugins.check_link_command import check_link_command
            return await check_link_command(bot, message)
    else:
        return await msg.edit_text(INVALID_URL_TEXT.format(text=msg_text))
