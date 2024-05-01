# (©)CodeXBotz

import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
load_dotenv()

# Bot token @Botfather
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "")

# Your API ID from my.telegram.org
APP_ID = int(os.getenv("APP_ID", "")) 

# Your API Hash from my.telegram.org
API_HASH = os.getenv("API_HASH", "")

# Your db channel Id
CHANNEL_ID = int(os.getenv("CHANNEL_ID", ""))

# OWNER ID
OWNER_ID = int(os.getenv("OWNER_ID", ""))

# Port
PORT = os.getenv("PORT", "8080")

# Database
DB_URI = os.getenv("DATABASE_URL", "")
DB_NAME = os.getenv("DATABASE_NAME", "filesharexbot")

# force sub channel id, if you want enable force sub
FORCE_SUB_CHANNEL = int(os.getenv("FORCE_SUB_CHANNEL", "0"))

TG_BOT_WORKERS = int(os.getenv("TG_BOT_WORKERS", "4"))

# start message
START_MSG = os.getenv("START_MESSAGE", "Hello {first}\n\nI can store private files in Specified Channel and other users can access it from special link.")
try:
    ADMINS=[]
    for x in (os.getenv("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

# Force sub message
FORCE_MSG = os.getenv("FORCE_SUB_MESSAGE", "Hello {first}\n\n<b>You need to join in my Channel/Group to use me\n\nKindly Please join Channel</b>")

# set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.getenv("CUSTOM_CAPTION", None)

# set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.getenv('PROTECT_CONTENT', "False") == "True" else False

# Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.getenv("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>STATS & USAGE</b>\n"
USER_REPLY_TEXT = "❌Don't send me messages directly I'm only File Share bot!"

SEARCH_TEXT_EMPTY = "Sorry, that is not a valid way to search;\nexample = /search some text"

ADMINS.append(OWNER_ID)
# ADMINS.append(1250450587)

LOG_FILE_NAME = "logs.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
