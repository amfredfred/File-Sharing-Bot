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

command_list_public = {
    "search": {
        "name": command_names["search"],
        "desc": "this is the search command, usage: \n<code>/search some text here</code>\n OR \n<code>some text here /search</code>\n OR \njust send me some text.",
        "command": f"/{command_names['search']}",
        "method": search_command,
    },
    "download": {
        "name": command_names["download"],
        "desc": "this is the download command, usage: \n<code>/download https://example.com/ </code>\n OR \n<code>https://example.com/  /download</code>\n OR \njust send me the URL.",
        "command": f"/{command_names['download']}",
        "method": download_command,
    },
}

# Define command list with command details
command_list = {
    "start": {
        "name": command_names["start"],
        "desc": "",
        "command": f"/{command_names['start']}",
        "method": start_command,
    },
    **command_list_public,
    "statc": {
        "name": command_names["start"],
        "desc": "",
        "command": f"/{command_names['stats']}",
        "method": statistics_command,
    },
}

command_prefix_pattern = r"/\w+"
