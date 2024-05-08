# (©)Codexbotz

import base64, gzip, re, asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from config import (
    FORCE_SUB_CHANNEL,
    ADMINS,
    ALL_EXTENTIONS,
    DISABLE_CHANNEL_BUTTON,
    PROTECT_CONTENT,
    START_MSG,
    CUSTOM_CAPTION,
    COMMANDS_LIST,
)
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait
from urllib.parse import urlparse
from urllib.parse import urlparse, urljoin
from database.database import present_user, add_user
from pyrogram.enums import ParseMode
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
)


async def get_caption(msg):
    if bool(CUSTOM_CAPTION) & bool(msg.document):
        return CUSTOM_CAPTION.format(
            previouscaption="" if not msg.caption else msg.caption.html,
            filename=msg.document.file_name,
        )
    else:
        return "" if not msg.caption else msg.caption.html


async def send_start_message(message: Message):
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("😊 About Me", callback_data="about"),
                InlineKeyboardButton("🔒 Close", callback_data="close"),
            ]
        ]
    )
    await message.reply_text(
        text=START_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=(
                None
                if not message.from_user.username
                else "@" + message.from_user.username
            ),
            mention=message.from_user.mention,
            id=message.from_user.id,
        ),
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        quote=True,
    )


async def copy_messages(client, message: Message, messages):
    for msg in messages:
        caption = await get_caption(msg)

        if DISABLE_CHANNEL_BUTTON:
            reply_markup = msg.reply_markup
        else:
            reply_markup = None

        try:
            await msg.copy(
                chat_id=message.from_user.id,
                caption=caption,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
                protect_content=PROTECT_CONTENT,
            )
            await asyncio.sleep(0.5)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await msg.copy(
                chat_id=message.from_user.id,
                caption=caption,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
                protect_content=PROTECT_CONTENT,
            )
        except:
            pass


async def extract_ids(client, text: str):
    try:
        base64_string = text.split(" ", 1)[1]
    except:
        return []

    string = await decode(base64_string)
    argument = string.split("-")

    if len(argument) == 3:
        try:
            start = int(int(argument[1]) / abs(client.db_channel.id))
            end = int(int(argument[2]) / abs(client.db_channel.id))
        except:
            return []

        if start <= end:
            ids = range(start, end + 1)
        else:
            ids = []
            i = start
            while True:
                ids.append(i)
                i -= 1
                if i < end:
                    break
    elif len(argument) == 2:
        try:
            ids = [int(int(argument[1]) / abs(client.db_channel.id))]
        except:
            return []

    return ids


async def check_and_add_user(chat, msg_from):
    if msg_from is not None and not await present_user(telegram_id=msg_from.id):
        try:
            await add_user(
                tid=msg_from.id,
                chat_id=chat.id,
                username=msg_from.username,
                first_name=msg_from.first_name,
                last_name=msg_from.last_name,
            )
        except Exception as e:
            print(f"Exception: {e}")
            pass


async def is_subscribed(filter, client, update):
    if not FORCE_SUB_CHANNEL:
        return True
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True
    try:
        member = await client.get_chat_member(
            chat_id=FORCE_SUB_CHANNEL, user_id=user_id
        )
    except UserNotParticipant:
        return False

    if not member.status in [
        ChatMemberStatus.OWNER,
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.MEMBER,
    ]:
        return False
    else:
        return True

async def encode(string):
    # Compress the string using gzip
    compressed_bytes = gzip.compress(string.encode("utf-8"))
    # Encode the compressed bytes using base64
    base64_bytes = base64.urlsafe_b64encode(compressed_bytes)
    base64_string = (base64_bytes.decode("ascii")).strip("=")
    return base64_string


async def decode(base64_string):
    # Decode the base64 string
    base64_string = base64_string.strip("=")
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    # Decode the base64 bytes
    compressed_bytes = base64.urlsafe_b64decode(base64_bytes)
    # Decompress the compressed bytes using gzip
    decompressed_string = gzip.decompress(compressed_bytes).decode("utf-8")
    return decompressed_string


async def get_messages(client, message_ids):
    messages = []
    total_messages = 0
    while total_messages != len(message_ids):
        temb_ids = message_ids[total_messages : total_messages + 200]
        try:
            msgs = await client.get_messages(
                chat_id=client.db_channel.id, message_ids=temb_ids
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
            msgs = await client.get_messages(
                chat_id=client.db_channel.id, message_ids=temb_ids
            )
        except:
            pass
        total_messages += len(temb_ids)
        messages.extend(msgs)
    return messages


async def get_message_id(client, message: Message):
    if message.forward_from_chat:
        if message.forward_from_chat.id == client.db_channel.id:
            return message.forward_from_message_id
        else:
            return 0
    elif message.forward_sender_name:
        return 0
    elif message.text:
        pattern = "https://t.me/(?:c/)?(.*)/(\d+)"
        matches = re.match(pattern, message.text)
        if not matches:
            return 0
        channel_id = matches.group(1)
        msg_id = int(matches.group(2))
        if channel_id.isdigit():
            if f"-100{channel_id}" == str(client.db_channel.id):
                return msg_id
        else:
            if channel_id == client.db_channel.username:
                return msg_id
    else:
        return 0


def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time


subscribed = filters.create(is_subscribed)


def is_url(text: str):
    if not text:
        return False, []
    prefixes = ["http://", "https://", "www."]
    extensions = ALL_EXTENTIONS
    urls = []
    for prefix in prefixes:
        if text.startswith(prefix):
            urls.append(text)
    for ext in extensions:
        if text.endswith(ext):
            urls.append(text)
    try:
        result = urlparse(text)
        if all([result.scheme, result.netloc]):
            urls.append(text)
    except ValueError:
        pass
    return bool(urls), urls


def extract_urls(text: str):
    if not text:
        return []
    parts = text.split()
    urls = []
    for part in parts:
        if is_url(part)[0]:
            urls.append(part)
    return urls


def extract_url(text: str):
    if not text:
        return None, False
    parts = text.split()
    for part in parts:
        if is_url(part)[0]:
            isDownloadable, _ = is_downloadable(part)
            return clean_file_url(part), isDownloadable
    return None, False


def clean_file_url(file_url: str):
    # Use regular expressions to remove everything after the file extension
    cleaned_url = re.sub(r'(\.mp4|\.mp3|\.avi|\.mkv|\.jpg|\.jpeg|\.png|\.gif|\.ogg).*$', lambda x: x.group(1), file_url)
    return cleaned_url
    # return file_url


def is_downloadable(link: str):
    parsed_url = urlparse(link)
    if parsed_url.path.endswith(ALL_EXTENTIONS):
        return True, {"type": "media", "url": link}
    return False, {}


def extract_link_title(link: str):
    cleaned_url = clear_url(link)
    path_segments = urlparse(cleaned_url).path.split("/")
    if path_segments:
        last_segment = path_segments[-1] if path_segments[-1] else path_segments[1]
        title = last_segment.replace("-", " ")
        return title
    else:
        return None


def if_only_path(link: str, href: str) -> str:
    if link is None or href is None:
        return href
    base_url = urlparse(link).scheme + "://" + urlparse(link).netloc
    if href.startswith("/"):
        href = urljoin(base_url, href)
    return href


def clear_url(link: str):
    cleared = link.replace("https://", "").replace("http://", "").replace("www.", "")
    return cleared


def has_path(url:str):
    _link = url[:-1]  if not url.endswith("\\")  else url
    _parsed_url = urlparse(_link)
    _is_not_empty = _parsed_url.path != "\\"
    return bool(_is_not_empty)


def starts_with_bot_username(bot_username: str, message_text: str) -> bool:
    return message_text.startswith(f"@{bot_username}")


def is_second_message_command(message_text: str) -> bool:
    if message_text.startswith("/"):
        return True
    elif message_text.split()[0] in COMMANDS_LIST:
        return True
    else:
        return False


def command_clean(text: str):
    words = text.split()
    words_without_command = [
        word for word in words if not word.startswith("/") or word.startswith("@")
    ]
    result = " ".join(words_without_command)
    return result
