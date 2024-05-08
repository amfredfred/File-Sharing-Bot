from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper_func import is_downloadable, extract_link_title, has_path, encode
from config import BOT_URL, BOT_USERNAME, TELEGRAM_SHARE_URL


class ResponseMessage:
    def __init__(self) -> None:
        pass

    def response_when_has_link(self, urls=[]):
        downloadable_links = (
            f"<b><u>Downloadable Links\n* * * *CLICK TO DOWNLOAD* * * *</u></b>\n"
        )
        keyboard_buttons = []
        reply_markup = None
        for idx, link in enumerate(urls, start=1):
            (isDownloadable), _ = is_downloadable(link)
            if isDownloadable:
                deep_link = (
                    f"tg://resolve?domain={BOT_USERNAME}&start=download%20{link}"
                )
                switch_inline_query = f"/download {link}"
                clickable_text = f"Download - {extract_link_title(link)}"
                link_tag = f"<b>{idx}</b>. <a href='{deep_link}'>{clickable_text}</a>\n"
                button = InlineKeyboardButton(
                    clickable_text, switch_inline_query_current_chat=switch_inline_query
                )
                keyboard_buttons.append([button])
                downloadable_links += link_tag
        if len(keyboard_buttons):
            reply_markup = InlineKeyboardMarkup(keyboard_buttons)
        return reply_markup if not None else None

    async def response_search_result(self, query: str, urls=[]):
        encoded_search_query = await encode(query.strip().replace(" ", "%20"))
        share_callback_data = f"{TELEGRAM_SHARE_URL}{encoded_search_query}"
        response = f"<b><u>Search Results For {query}</u></b>\n"
        response += "<b>* * * * CLICK TO BROWSE * * * *</b>"
        buttons = []
        for idx, link in enumerate(urls, start=1):
            (isDownloadable), _ = is_downloadable(link["url"])
            if link["url"]:
                print(link["url"])
                encoded_search_link = await encode(f'/download {str(link["url"]).strip().replace(" ", "%20")}')
                _url = f"{BOT_URL}?start={encoded_search_link}"
                clickable_text = f"{link['text']}"
                button = InlineKeyboardButton(clickable_text, url=_url)
                buttons.append([button])
        buttons.append([InlineKeyboardButton("📤 Share 📤", url=share_callback_data)])
        reply_markup = InlineKeyboardMarkup(buttons)
        response += "Share this search:"
        return response, reply_markup

    def response_check_links(self, links=[]):
        downloadable_links = []
        other_links = []
        for link in links:
            if is_downloadable(link) or has_path(link):
                downloadable_links.append(link)
            else:
                other_links.append(link)
        return self.response_when_has_link(downloadable_links), other_links

    async def response_when_plain_text(self, text: str):
        encoded_search_link = await encode(f'/search {text.strip().replace(" ", "%20")}')
        deep_link_search = f"{BOT_URL}?start={encoded_search_link}"
        share_link = f"{TELEGRAM_SHARE_URL}{deep_link_search}"
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔍 Search 🔎", callback_data=encoded_search_link)],
            [InlineKeyboardButton("📤 Share 📤", url=share_link)]
        ])

        return reply_markup
