from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper_func import (
    is_downloadable,
    extract_link_title,
    encode,
    extract_link_title,
    get_extension,
    headline_text,
)
from config import BOT_URL, TELEGRAM_SHARE_URL
from models.calling_back import CallbackDataManager


class ResponseMessage:
    def __init__(self) -> None:
        self.callback = CallbackDataManager()
        pass

    async def response_search_result(self, query: str, owner_id, urls=[]):
        encoded_query = await encode(f"/search {query}")
        deep_link_search = f"{BOT_URL}?start={self.callback.generate_callback_data(encoded_query, owner_id)}"
        deep_link_search = f"{TELEGRAM_SHARE_URL}{deep_link_search}"
        response = f"<b><u>Search Results For {query}</u></b>\n"
        buttons = []
        for idx, link in enumerate(urls, start=1):
            (isDownloadable), _ = is_downloadable(link["url"])
            if link["url"]:
                encoded_search_link = await encode(
                    f'/download {str(link["url"]).strip().replace(" ", "%20")}'
                )
                callback_data = self.callback.generate_callback_data(
                    encoded_search_link, owner_id
                )
                _url = f"{BOT_URL}?start={callback_data}"
                clickable_text = f"{link['text']}"
                button = [
                    InlineKeyboardButton(clickable_text, callback_data=callback_data)
                ]
                # visit_button = InlineKeyboardButton("🖇️📤", url=link["url"])
                # if not isDownloadable:
                #     button.append(visit_button)
                buttons.append(button)
        buttons.append([InlineKeyboardButton("📤 Share 📤", url=deep_link_search)])
        reply_markup = InlineKeyboardMarkup(buttons)
        return response, reply_markup

    async def response_when_plain_text(self, text: str, owner_id):
        search_callback_data = await encode(
            f'/search {text.strip().replace(" ", "%20")}'
        )
        search_callback_data = self.callback.generate_callback_data(
            search_callback_data, owner_id
        )

        deep_link_search = f"{BOT_URL}?start={search_callback_data}"
        share_link = f"{TELEGRAM_SHARE_URL}{deep_link_search}"

        buttons = []
        buttons.append(
            [
                InlineKeyboardButton("🔍🔎", callback_data=search_callback_data),
            ]
        )
        buttons.append([InlineKeyboardButton("📤 Share 📤", url=share_link)])

        reply_markup = InlineKeyboardMarkup(buttons)
        return reply_markup

    async def download_options(self, urls, owner_id, query: str = ""):
        cdm = CallbackDataManager()
        buttons = []
        is_seen = set()
        for idx, dl_link in enumerate(urls, start=1):
            if dl_link in is_seen:
                continue
            isDownloadable, link = is_downloadable(dl_link)
            file_name = extract_link_title(link["url"])
            button_text = f"{file_name}"
            if isDownloadable:
                callback_data = await encode(f"/download {link['url']}")
                callback_data = cdm.generate_callback_data(callback_data, owner_id)
                extension = get_extension(dl_link)
                button = [
                    InlineKeyboardButton(
                        f"⬇️ [{extension}] " + button_text, callback_data=callback_data
                    )
                ]
                buttons.append(button)
            else:
                button = [InlineKeyboardButton("🔗Visit🔗", url=dl_link)]
                buttons.append(button)
            is_seen.add(dl_link)
        buttons.append([InlineKeyboardButton("📤VISIT WEBPAGE📤", url=query)])
        reply_markup = InlineKeyboardMarkup(buttons) if buttons else None
        return bool(buttons) and bool(reply_markup), reply_markup

    async def response_when_is_question(self, text: str, owner_id):
        buttons = []
        ask_comm_cb = await encode(f"/ask_community {text.strip()}")
        ask_comm_cb = self.callback.generate_callback_data(ask_comm_cb, owner_id)
        ask_admi_cb = await encode(f"/ask_admin {text.strip()}")
        ask_admi_cb = self.callback.generate_callback_data(ask_admi_cb, owner_id)
        search_wbcb = await encode(f"/search {text.strip().replace(' ', '%20')}")
        search_wbcb = self.callback.generate_callback_data(search_wbcb, owner_id)
        do_nothincb = await encode(f"remove")
        do_nothincb = self.callback.generate_callback_data(do_nothincb, owner_id)
        deep_linkcb = await encode(f"{text.strip()}")
        deep_link_search = f"{BOT_URL}?start={self.callback.generate_callback_data(deep_linkcb, owner_id)}"
        share_link = f"{TELEGRAM_SHARE_URL}{deep_link_search}"
        buttons.append(
            [
                InlineKeyboardButton("🙋‍♂️Admin", callback_data=ask_admi_cb),
                InlineKeyboardButton("🤝Community", callback_data=ask_comm_cb),
            ]
        )
        buttons.append(
            [
                InlineKeyboardButton("🔍🔎", callback_data=search_wbcb),
                InlineKeyboardButton("❌", callback_data=do_nothincb),
                InlineKeyboardButton("📤", url=share_link),
            ]
        )
        headline = headline_text(
            "\n<code>Where to direct your questions?</code>\n"
        )
        headline += f"\n\n<b><code>{text}</code></b>\n\n- - - - -"
        reply_markup = InlineKeyboardMarkup(buttons)
        return headline, reply_markup
