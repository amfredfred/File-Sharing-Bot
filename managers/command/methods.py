from managers.command.command_dicts import (
    command_list,
    command_names as comm_names,
    command_prefix_pattern,
)
from pyrogram.types import Message
from pyrogram import Client
import re


async def command_call(bot: Client, message: Message, command_name: str):
    message.text = command_clean(message.text)
    comm = command_list.get(command_name, None)
    if comm:
        await comm["method"](bot, message)


def command_clean(text: str):
    words = text.split()
    words_without_command = [word for word in words if not word.startswith("/")]
    result = " ".join(words_without_command)
    return result


def command_extract(input_string: str):
    if not input_string:
        return None
    command_matches = re.findall(command_prefix_pattern, input_string)
    if command_matches:
        comm_dict = command_list.get(str(command_matches[0]).replace("/", ""))
        if comm_dict:
            return comm_dict
        else:
            return False
    return None


def command_names():
    return comm_names.values()
