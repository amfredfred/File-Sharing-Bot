from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin
import os
import tempfile
from helper_func import if_only_path
from config import ALL_EXTENTIONS
import aiofiles
import aiohttp
import shutil


class DownloadManager:
    def __init__(self):
        self.should_cancel_download = False
        pass

    def _parse_link(self, link):
        parsed_url = urlparse(link)
        if parsed_url.scheme == "https" and parsed_url.netloc == "t.me":
            return {"type": "telegram", "url": link}
        elif parsed_url.path.endswith(ALL_EXTENTIONS):
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
                href = if_only_path(base_url, a_tag["href"])
                if href.endswith(ALL_EXTENTIONS):
                    downloadable_links.append(href)
        except Exception as e:
            print(f"Error while fetching links: {e}")
        return downloadable_links

    async def download_and_send_media(self, msg, url, callback, progress):
        try:
            temp_dir = tempfile.mkdtemp()
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    total_size = int(response.headers.get("content-length", 0))
                    previous_progress_percentage = 0
                    if response.status == 200:
                        file_name = os.path.join(temp_dir, os.path.basename(url))
                        async with aiofiles.open(file_name, "wb") as file:
                            downloaded_size = 0
                            async for chunk in response.content.iter_any():
                                if self.should_cancel_download:
                                    await aiofiles.os.remove(file_name)
                                    return "Download canceled."
                                await file.write(chunk)
                                downloaded_size += len(chunk)
                                current_progress_percentage = (downloaded_size / total_size) * 100
                                if current_progress_percentage - previous_progress_percentage >= 2:
                                    try:
                                        await progress(msg, total_size, downloaded_size)
                                    except Exception as e:
                                        pass
                                    finally:
                                       previous_progress_percentage = current_progress_percentage
                                       downloaded_size = 0
                        await callback(msg, url, file_name, f">>>> ✅✅✅ <<<<")
                        return True
                    elif response.status == 404:
                        return "The requested file was not found."
                    elif response.status == 403:
                        return "Access to the requested file is forbidden."
                    else:
                        return f"Error downloading media: HTTP error {response.status}"
        except Exception as e:
            print(f"Error downloading media. {e}")
            return f"Error downloading media."
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    async def cancel_download(self):
        self.should_cancel_download = True

    def download_options(self, urls):
        message = "<b>Choose a file to download:</b>\n"
        for idx, dl_link in enumerate(urls, start=1):
            file_name = urlparse(dl_link).path.split("/")[-1]
            button_text = f"{idx}. {file_name}"
            message += f"<b>{button_text}</b>\n"
        message += "\nPlease select a number to download."
        return message
