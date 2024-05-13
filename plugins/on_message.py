from pyrogram import filters, Client
from pyrogram.types import Message
from bot import Bot
from helper_func import extract_url,subscribed,is_question
from responses import ResponseMessage
from plugins.link_generator import moveto_cloud
from models.calling_back import hash_exists

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
async def handle_message(client: Client, message: Message):

    msg_text = message.text if not None else "_"
    msg_text = message.text.strip() if msg_text is not None else " "

    if message.media:
        msg_text = f"/upload {msg_text}"
        message.text = msg_text

    if is_question(msg_text):
        pass

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
    response_message_markup = await rspmsg.response_when_plain_text(msg_text,message.from_user.id)
    respond_text = f"<b><u>What do you want me to do with this text?</u></b>\n\n<code>{msg_text}</code>\n\n"
    await reply_text.edit_text( respond_text, reply_markup=response_message_markup )
    isSuccess, cloudLink, share_link, post_message = await moveto_cloud(client, message)
    if not isSuccess:
        sorry_text = f"Sorry, could not upload your message to cloud. 😟"
        pass
