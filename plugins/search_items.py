from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from scrapers.scrape_the_web import ScrapeTheWeb
from helper_func import subscribed
from bot import Bot
from config import SEARCH_TEXT_EMPTY
from time import sleep
from models.searchings import searching
from responses.index import ResponseMessage


def search(query):
    scraper = ScrapeTheWeb(query)
    results = scraper.search()
    print(results)
    return scraper.filter_links(results)

respond = ResponseMessage()

@Bot.on_message(filters.command("search") & filters.private & subscribed)
async def search_command(bot: Bot, message: Message):
    query = ""
    if not message.text or len(message.text.split()) < 2:
        lsg_msg = await message.reply_text(SEARCH_TEXT_EMPTY)
        sleep(0.5)
        await lsg_msg.delete()
    else:
        query = message.text.split(" ", 1)[1].strip()
    msg = await message.reply_text(f"<code>Searching for <u>{query}</u><code>", reply_to_message_id=message.id )
    try:
        matched_, others = search(query)
        if len(matched_) > 0:
            matched_ = matched_[:10] 
            matched_ = respond.response_search_result(matched_)
            matched_ = matched_.format(query=query)
            await msg.edit_text(matched_)
            _searching = searching()
            _searching.insert_searching(msg.chat.id, query)
        else:
            await msg.edit_text(f"No Result For: <u>{query}</u>")
    except Exception as e:
        await msg.edit_text("Something went wrong: ")
        print(f"Erro searching thins: {e}")
