from plugins.start_command import start_command
from plugins.search_command import search_command
from plugins.download_command import download_command

from bot import Bot
from pyrogram.types import Message
from pyrogram import Client
import re

# Define command names
command_names = {"start": "start", "search": "search", "download": "download"}

# Define command list with command details
command_list = {
    "start": {
        "name": command_names["start"],
        "desc": "",
        "command": f"/{command_names['start']}",
        "method": start_command,
    },
    "search": {
        "name": command_names["search"],
        "desc": "",
        "command": f"/{command_names['search']}",
        "method": search_command,
    },
    "download": {
        "name": command_names["download"],
        "desc": "",
        "command": f"/{command_names['download']}",
        "method": download_command,
    },
    # Add more commands here
}

command_prefix_pattern = r"/\w+"

# Class to manage commands
class CommandManager:
    def __init__(self, bot: Client, message: Message):
        self.bot = bot
        self.message = message

    async def command_call(self, command_name: str):
        bot = self.bot
        message =  self.message
        message.text = self.command_clean(self.message.text.strip())
        comm = command_list.get(command_name, None)
        if comm:
            await comm["method"](bot, message)

    def command_names(self):
        return command_names.values()

    def command_extract(self, input_string: str):
        command_matches = re.findall(command_prefix_pattern, input_string)
        if command_matches:
            comm_dict = command_list.get(str(command_matches[0]).replace("/", ''))
            if comm_dict:
                return comm_dict
            else:
                return False
        return None
    
    def command_clean(self, text:str):
        words = text.split()
        words_without_command = [word for word in words if not word.startswith("/")]
        result = " ".join(words_without_command)
        return result
