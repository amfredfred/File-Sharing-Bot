from pyrogram import filters
from pyrogram.types import Message
from scrapers.scrape_the_web import ScrapeTheWeb
from helper_func import subscribed, command_clean
from bot import Bot
from config import SEARCH_TEXT_EMPTY, LOOKING_UP_TEXT
from models.searchings import Searching
from responses import ResponseMessage


async def search(query):
    scraper = ScrapeTheWeb(query)
    results = await scraper.search()
    return scraper.filter_links(results)


respond = ResponseMessage()

@Bot.on_message(filters.command("search") & ~filters.channel & subscribed)
async def search_command(bot: Bot, message: Message):
    message.text = command_clean(message.text)
    query = message.text
    if not query:
        return await message.reply_text(SEARCH_TEXT_EMPTY, quote=True)
    msg = await message.reply_text(
        LOOKING_UP_TEXT.format(query=query), reply_to_message_id=message.id, quote=True
    )
    try:
        matched_, others = await search(query)
        if len(matched_) > 0:
            matched_ = matched_[:10]
            response_text, reply_markup = await respond.response_search_result(
                query, matched_
            )
            await msg.edit_text(response_text, reply_markup=reply_markup)
            _searching = Searching()
            _searching.insert_searching(msg.chat.id, query)
        else:
            await msg.edit_text(f"No Result For: <u>{query}</u>")
    except Exception as e:
        await msg.edit_text("Something went wrong: ")
        print(f"Erro searching thins: {e}")
