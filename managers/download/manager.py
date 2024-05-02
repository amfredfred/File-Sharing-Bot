from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin
import os
import tempfile
import asyncio

from config import (
    PLAYABLE_FILE_EXTENSIONS,
    ZIP_FILE_EXTENSIONS,
    NON_HARMFUL_FILE_EXTENSIONS,
)


class DownloadManager:
    def __init__(self):
        self.should_cancel_download = False
        pass

    async def download_file(self, link, chat_id):
        file_info = self._parse_link(link)
        if file_info:
            if file_info["type"] == "media":
                await self.send_video(chat_id, video=file_info["url"])
            elif file_info["type"] == "telegram":
                await self.send_document(chat_id, document=file_info["url"])
            else:
                await self.send_download_options(file_info["urls"])
        else:
            await self.app.send_message(chat_id, "Invalid l+ink.")

    def _parse_link(self, link):
        parsed_url = urlparse(link)
        if parsed_url.scheme == "https" and parsed_url.netloc == "t.me":
            return {"type": "telegram", "url": link}
        elif parsed_url.path.endswith(
            PLAYABLE_FILE_EXTENSIONS + ZIP_FILE_EXTENSIONS + NON_HARMFUL_FILE_EXTENSIONS
        ):
            return {"type": "media", "url": link}
        else:
            return {
                "type": "webpage",
                "urls": self._find_downloadable_links(link),
            }

    def _find_downloadable_links(self, link):
        downloadable_links = []
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, "html.parser")
            base_url = urlparse(link).scheme + "://" + urlparse(link).netloc
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                if href.startswith("/"):
                    href = urljoin(base_url, href)  # Prepend base URL to href
                if href.endswith(PLAYABLE_FILE_EXTENSIONS + ZIP_FILE_EXTENSIONS + NON_HARMFUL_FILE_EXTENSIONS):
                    downloadable_links.append(href)
        except Exception as e:
            print(f"Error while fetching links: {e}")
        return downloadable_links

    async def download_and_send_media(self, msg, url, callback, progress):
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                file_name = os.path.join(temp_dir, os.path.basename(url))
                response = requests.get(url, stream=True)
                total_size = int(response.headers.get('content-length', 0))
                if response.status_code == 200:
                    with open(file_name, "wb") as file:
                        downloaded_size = 0
                        chunk_size = max(total_size // 10, 1024)  # Calculate chunk size (approximately 10%)
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            if self.should_cancel_download:
                                os.remove(file_name)
                                return "Download canceled."
                            file.write(chunk)
                            try:
                                if downloaded_size >= total_size // 10:
                                    await progress(msg, total_size, downloaded_size)
                                    downloaded_size = 0
                            except Exception as e:
                                print(f"Error updating progress: {e}")
                            downloaded_size += len(chunk)
                    await callback(msg, url, file_name)
                    os.remove(file_name)
                    return True
                elif response.status_code == 404:
                    return "The requested file was not found."
                elif response.status_code == 403:
                    return "Access to the requested file is forbidden."
                else:
                    return f"Error downloading media: HTTP error {str(response.status_code)}"
        except Exception as e:
            print(f"Error downloading media. {e}")
            return f"Error downloading media."

    async def cancel_download(self):
        self.should_cancel_download = True
