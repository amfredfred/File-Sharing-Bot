from plugins.start_command import start_command
from plugins.search_command import search_command
from plugins.download_command import download_command
from plugins.statistics_command import statistics_command

# Define command names
command_names = {
    "start": "start",
    "search": "search",
    "download": "download",
    "stats": "stats",
}

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
    "statc": {
        "name": command_names["start"],
        "desc": "",
        "command": f"/{command_names['stats']}",
        "method": statistics_command,
    },
}

command_prefix_pattern = r"/\w+"