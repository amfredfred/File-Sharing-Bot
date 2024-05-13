from bot import Bot
from pyrogram.types import Message
from pyrogram import filters
from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT
from datetime import datetime
from helper_func import get_readable_time
from models.profile import ProfileManager
from models.searching import SearchingManager
from models.searching import Searching


@Bot.on_message(filters.command("stats") & filters.user(ADMINS))
async def statistics_command(bot: Bot, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)

    # Retrieve data from Profile model
    _profile = ProfileManager()
    users = _profile.get_all_users()
    get_active_users_last_24_hours = _profile.get_active_users_last_24_hours()

    # Retrieve data from Searching model
    _searchings = SearchingManager()
    queries = _searchings.get_all_searchings()
    _common = _searchings.most_common_searched_word()

    # Format statistics text
    stats_text = f"""╔═══════════════════╗
║{BOT_STATS_TEXT}
╠═══════════════════╣
║---⏳ <b>UpTime</b>: {time}
║---👥 <b>Daily Users</b>: {len(users)}
║═══════════════════
║<b>SEARCH QUERIES</b>
║═══════════════════
║---🔹 <b>Total</b>: {len(queries)}
║---🔍 <b>Popular Word</b>: {_common or 'N/A'}
╚═══════════════════╝"""

    # Reply with statistics
    msg = await message.reply_text(stats_text, quote=True)
