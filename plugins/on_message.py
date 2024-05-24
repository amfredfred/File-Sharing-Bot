from pyrogram import filters, Client
from pyrogram.types import Message
from bot import Bot
from helper_func import extract_url, subscribed, is_question
from responses import ResponseMessage
from plugins.link_generator import moveto_cloud
from models.calling_back import hash_exists
from injector import injector
from models.profile import Profile

from conversations.profile_update_conversations import UpdateAccountConversation

OFF_COMMANDS = [
    "start",
    "users",
    "broadcast",
    "batch",
    "genlink",
    "search",
    "cs",
    "download",
    "account",
]

rspmsg = ResponseMessage()


@Bot.on_message((~filters.channel & ~filters.command(OFF_COMMANDS) & subscribed))
@injector
async def handle_message(client: Client, profile: Profile, message: Message):

    msg_text = message.text if not None else "_"
    msg_text = message.text.strip() if msg_text is not None else " "

    conversate = UpdateAccountConversation(profile, message)
    return await conversate.start()

    if message.media:
        msg_text = f"/upload {msg_text}"
        message.text = msg_text

    if is_question(msg_text) and not message.outgoing:
        headline, reply_markup = await rspmsg.response_when_is_question(
            msg_text, profile.id
        )
        return await message.reply_text(headline, reply_markup=reply_markup, quote=True)

    from managers.command.methods import command_extract, command_call

    command_ext = command_extract(msg_text)
    if isinstance(command_ext, dict):
        return await command_call(client, message, command_ext["name"])
    elif command_ext == False:
        pass
    else:
        pass

    if extract_url(msg_text)[0]:
        from plugins.check_link_command import check_link_command

        return await check_link_command(client, message)

    if hash_exists(msg_text):
        from plugins.start_command import start_command

        message.text = msg_text
        return await start_command(client, message)

    reply_text = await message.reply_text("Please wait...", quote=True)
    response_message_markup = await rspmsg.response_when_plain_text(
        msg_text, profile.id
    )
    respond_text = f"<b><u>WHAT TO DO? 🤔</u></b>\n\n<code>{msg_text}</code>\n"
    respond_text += f"\n @{profile.username if not None else profile.first_name}"
    await reply_text.edit_text(respond_text, reply_markup=response_message_markup)
    isSuccess, cloudLink, share_link, post_message = await moveto_cloud(
        client, message, profile.id
    )
    if not isSuccess:
        sorry_text = f"Sorry, could not upload your message to cloud. 😟"
        pass
