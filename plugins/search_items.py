from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from scrapers.scrape_the_web import ScrapeTheWeb
from helper_func import subscribed
from bot import Bot
from config import SEARCH_TEXT_EMPTY
from time import sleep
from models.searchings import searching


def search(query):
    scraper = ScrapeTheWeb(query)
    results = scraper.search()
    return scraper.filter_links(results)

@Bot.on_message(filters.command("search") & filters.private & subscribed)
async def search_command(bot: Bot, message: Message):
    query = ''
    if not message.text or len(message.text.split()) < 2:
        lsg_msg = await message.reply_text(SEARCH_TEXT_EMPTY)
        sleep(0.5)
        await lsg_msg.delete()
    else:
        query = message.text.split(" ", 1)[1].strip()
    msg = await message.reply_text(f"<code>Searching for <u>{query}</u><code>", reply_to_message_id=message.id)
    matched_year, unmatched_year, others = search(query)
    combined_list = matched_year + unmatched_year

    if len(combined_list) > 0:
        buttons_per_row = 2
        keyboard = []
        row = []
        for result in combined_list[:10]:
            row.append(InlineKeyboardButton(result["text"], url=result["url"]))
            if len(row) == buttons_per_row:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await msg.edit_text(
            text=f"<strong>Search Results For <u>{query}</u></strong> :\n\n",
            reply_markup=reply_markup,
        )
        _searching = searching()
        _searching.insert_searching(msg.chat.id, query)
    else:
        await msg.edit_text(f"No Result For: <u>{query}</u>")
