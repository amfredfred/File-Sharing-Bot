from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper_func import is_downloadable, extract_link_title
from config import BOT_URL, BOT_USERNAME


class ResponseMessage:
    def __init__(self) -> None:
        pass

    def response_when_has_link(self, urls=[]):
        downloadable_links = (
            "<b><u>Downloadable Links\n* * * *CLICK TO DOWNLOAD* * * *</u></b>\n"
        )
        keyboard_buttons = []
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
        reply_markup = InlineKeyboardMarkup(keyboard_buttons)
        return downloadable_links

    def response_search_result(self, urls=[]):
        response = "<b><u>Search Results For {query}</u></b>\n"
        response += "<b>* * * * CLICK TO BROWSE * * * *</b>\n\n"
        for idx, link in enumerate(urls, start=1):
            (isDownloadable), _ = is_downloadable(link["url"])

            if link["url"]:
                deep_link = f"tg://resolve?domain={BOT_USERNAME}&start={link['url']}"
                clickable_text = f"<b> {link['text']}</b>"
                link_tag = f"<b>{idx}</b>. <a href='{deep_link}'>{clickable_text}</a>\n"
                response += link_tag

        # Add some extra spacing at the end for better visual separation
        response += "\n\n"

        return response