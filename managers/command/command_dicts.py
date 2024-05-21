from plugins.start_command import start_command
from plugins.search_command import search_command
from plugins.download_command import download_command
from plugins.statistics_command import statistics_command
from plugins.check_link_command import check_link_command
from plugins.retrieve_post_command import retrieve_post_command
from plugins.upload_command import upload_command
from plugins.create_post_command import create_post_command

# Define command names
command_names = {
    "start": "start",
    "search": "search",
    "download": "download",
    "stats": "stats",
    "check_link": "check_link",
    "retrieve_post": "retrieve_post",
    "upload": "upload",
    "create_post": "create_post",
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
    "stats": {
        "name": command_names["stats"],
        "desc": "",
        "command": f"/{command_names['stats']}",
        "method": statistics_command,
    },
    "check_link": {
        "name": command_names["check_link"],
        "desc": "",
        "command": f"/{command_names['check_link']}",
        "method": check_link_command,
    },
    "retrieve_post": {
        "name": command_names["retrieve_post"],
        "desc": "",
        "command": f"/{command_names['retrieve_post']}",
        "method": retrieve_post_command,
    },
    "upload": {
        "name": command_names["upload"],
        "desc": "",
        "command": f"/{command_names['upload']}",
        "method": upload_command,
    },
    "create_post": {
        "name": command_names["create_post"],
        "desc": "",
        "command": f"/{command_names['create_post']}",
        "method": create_post_command,
    },
}

command_prefix_pattern = r"/\w+"
