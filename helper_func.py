# (©)Codexbotz

import base64
import re
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from config import FORCE_SUB_CHANNEL, ADMINS, ALL_EXTENTIONS
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait
from urllib.parse import urlparse
from urllib.parse import urlparse, urljoin


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
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = (base64_bytes.decode("ascii")).strip("=")
    return base64_string


async def decode(base64_string):
    base64_string = base64_string.strip(
        "="
    )  # links generated before this commit will be having = sign, hence striping them to handle padding errors.
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes)
    string = string_bytes.decode("ascii")
    return string


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


async def get_message_id(client, message):
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


def extract_url(text: str):
    parts = text.split()
    for part in parts:
        if is_url(part)[0]:
            isDownloadable, _ = is_downloadable(part)
            return clean_file_url(part), isDownloadable
    return None, False


def clean_file_url(file_url: str):
    # Use regular expressions to remove everything after the file extension
    # cleaned_url = re.sub(r'(\.mp4|\.mp3|\.avi|\.mkv|\.jpg|\.jpeg|\.png|\.gif|\.ogg).*$', lambda x: x.group(1), file_url)
    # return cleaned_url
    return file_url


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
