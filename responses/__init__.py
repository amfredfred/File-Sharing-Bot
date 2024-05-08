from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper_func import (
    is_downloadable,
    extract_link_title,
    has_path,
    encode,
    extract_link_title,
)
from config import BOT_URL, BOT_USERNAME, TELEGRAM_SHARE_URL
from urllib.parse import urlparse
from managers.callback import CallbackDataManager


class ResponseMessage:
    def __init__(self) -> None:
        self.callback = CallbackDataManager()
        pass

    async def response_when_has_link(self, url: str):
        callback_data = await encode(f"/download {url}")
        callback_data = self.callback.generate_callback_data(callback_data)
        deep_link_search = f"{BOT_URL}?start={callback_data}"
        share_link = f"{TELEGRAM_SHARE_URL}{deep_link_search}"

        isDownloadable, link_data = is_downloadable(url)
        btn_text = "🔍 Explore 🔎"
        if isDownloadable:
            btn_text = f"⬇️ Download ⬇️"

        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(f"{btn_text}", callback_data=callback_data)],
                [InlineKeyboardButton("📤 Share 📤", url=share_link)],
            ]
        )
        return reply_markup

    async def response_search_result(self, query: str, urls=[]):
        encoded_query = await encode(f"/search {query}")
        deep_link_search = f"{BOT_URL}?start={self.callback.generate_callback_data(encoded_query)}"
        deep_link_search = f"{TELEGRAM_SHARE_URL}{deep_link_search}"
        print(f"deep_link_search: {deep_link_search}")
        response = f"<b><u>Search Results For {query}</u></b>\n"
        buttons = []
        for idx, link in enumerate(urls, start=1):
            (isDownloadable), _ = is_downloadable(link["url"])
            if link["url"]:
                encoded_search_link = await encode(
                    f'/download {str(link["url"]).strip().replace(" ", "%20")}'
                )
                callback_data = self.callback.generate_callback_data(
                    encoded_search_link
                )
                _url = f"{BOT_URL}?start={callback_data}"
                clickable_text = f"{link['text']}"
                button = [InlineKeyboardButton( clickable_text, callback_data=callback_data)]
                visit_button = InlineKeyboardButton("🖇️📤", url=link["url"])
                if not isDownloadable:
                    button.append(visit_button)
                buttons.append(button)
        buttons.append([InlineKeyboardButton("📤 Share 📤", url=deep_link_search)])
        reply_markup = InlineKeyboardMarkup(buttons)
        return response, reply_markup

    async def response_when_plain_text(self, text: str):
        callback_data = await encode(f'/search {text.strip().replace(" ", "%20")}')
        callback_data = self.callback.generate_callback_data(callback_data)
        deep_link_search = f"{BOT_URL}?start={callback_data}"
        share_link = f"{TELEGRAM_SHARE_URL}{deep_link_search}"
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🔍 Search 🔎", callback_data=callback_data)],
                [InlineKeyboardButton("📤 Share 📤", url=share_link)],
            ]
        )
        return reply_markup

    async def download_options(self, urls):
        cdm = CallbackDataManager()
        buttons = []
        reply_markup = None
        for idx, dl_link in enumerate(urls, start=1):
            isDownloadable, link = is_downloadable(dl_link)
            file_name = extract_link_title(link["url"])
            button_text = f"{idx}. {file_name}"
            if isDownloadable:
                button_text = "Download " + button_text
                callback_data = await encode(f"/download {link['url']}")
                callback_data = cdm.generate_callback_data(callback_data)
                button = InlineKeyboardButton(button_text, callback_data=callback_data)
            else:
                button_text = "Go to " + button_text
                button = InlineKeyboardButton(button_text, url=dl_link)
            buttons.append([button])
        if buttons:
            reply_markup = InlineKeyboardMarkup(buttons)

        return len(buttons) > 0, reply_markup
