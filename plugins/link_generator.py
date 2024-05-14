# (©)Codexbotz

from pyrogram import Client
from pyrogram.types import Message
from helper_func import encode, get_messages
from pyrogram.errors import FloodWait
import asyncio
from models.calling_back import CallbackDataManager


async def moveto_cloud(client: Client, message: Message, owner_id):
    cdm = CallbackDataManager()

    user_from = message.from_user
    try:
        post_message = await message.copy(
            chat_id=client.db_channel.id, disable_notification=True
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        post_message = await message.copy(
            chat_id=client.db_channel.id, disable_notification=True
        )
    except Exception as e:
        print(e)
        return False, None, None, post_message

    converted_id = post_message.id * abs(client.db_channel.id)

    string = f"get-{converted_id}"
    base64_string = await encode(f"/retrieve_post {string}")
    base64_string = cdm.generate_callback_data(base64_string, owner_id)
    link = f"https://t.me/{client.username}?start={base64_string}"
    share_link = f"https://telegram.me/share/url?url={link}"
    return True, link, share_link, post_message


async def get_from_cloud(client: Client, message: Message):
    msg_id = message.text
    if msg_id:
        has_id = msg_id.split("get-")
        if has_id:
            msg_id = int(has_id[1])
    if isinstance(msg_id, int):
        converted_id = int(msg_id / abs(client.db_channel.id))
        message_byid = await get_messages(client, [converted_id])
        return message_byid
    return None
