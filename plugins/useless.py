from bot import Bot
from pyrogram.types import Message
from pyrogram import filters
from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT
from datetime import datetime
from helper_func import get_readable_time
from models.profile import profile
from models.searchings import searching


@Bot.on_message(filters.command("stats") & filters.user(ADMINS))
async def stats(bot: Bot, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    users = profile().get_all_users()
    queries = searching().get_all_seachings()
    stats_text = "".join(
        [
            f"<u>{BOT_STATS_TEXT}</u>",
            f"<strong>UpTime</strong> - {time}\n",
            f"<strong>Daily users</strong> - {len(users)}\n\n",
            f"<strong><u>SEARCH QUERIES</u></strong>\n",
            f"<strong>Total</strong> - {len(queries)}\n",
            # f"<strong>Today</strong> - {len(queries)}\n",
            # f"<strong>Yesterday</strong> - {len(queries)}\n",
        ]
    )
    msg = await message.reply(stats_text, reply_to_message_id=message.id)

@Bot.on_message(filters.private & filters.incoming)
async def useless(_, message: Message):
    if USER_REPLY_TEXT:
        await message.reply(USER_REPLY_TEXT)