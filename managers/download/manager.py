from bs4 import BeautifulSoup
import random
import os, tempfile, aiofiles, aiohttp, shutil
from config import DOWNLOAD_SUCCESSFUL_TEXT
from helper_func import is_downloadable, if_only_path, link_type
from scrapers.facebook import FacebookVideoDownloader


class DownloadManager:
    def __init__(self):
        self.should_cancel_download = False
        pass

    async def check_link_type(self, link: str):
        type_of_link = link_type(link)
        if type_of_link == "facebook_watch":
            fb_downloader = FacebookVideoDownloader()
            message = fb_downloader.download(link)
            print(f"message: {message}")
            return {"type": type_of_link, "url": link}
        elif type_of_link == "telegram":
            return {"type": type_of_link, "url": link}
        elif type_of_link == "media":
            return {"type": type_of_link, "url": link}
        elif type_of_link == "webpage":
            return {"type": type_of_link, "urls": await self.find_all_links(link)}

    async def find_all_links(self, link):
        all_links = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as response:
                    response.raise_for_status()
                    html_content = await response.text()
                    soup = BeautifulSoup(html_content, "html.parser")
                    for a_tag in soup.find_all("a", href=True):
                        href = if_only_path(link, a_tag["href"])
                        isDownloadable, url = is_downloadable(href)
                        if isDownloadable:
                            all_links.append(href)
        except aiohttp.ClientError as e:
            print(f"Error while fetching links: {e}")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
        return all_links

    async def download_and_send_media(self, msg, url, on_success, on_update):
        try:
            temp_dir = tempfile.mkdtemp()
            async with aiohttp.ClientSession(headers=self._get_headers(url)) as session:
                async with session.get(url, headers=self._get_headers(url)) as response:
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
                                current_progress_percentage = (
                                    downloaded_size / total_size
                                ) * 100
                                if (
                                    current_progress_percentage
                                    - previous_progress_percentage
                                    >= 2
                                ):
                                    try:
                                        await on_update(
                                            msg, total_size, downloaded_size
                                        )
                                    except Exception as e:
                                        pass
                                    finally:
                                        previous_progress_percentage = (
                                            current_progress_percentage
                                        )
                                        downloaded_size = 0
                        await on_success(
                            msg,
                            url,
                            file_name,
                            DOWNLOAD_SUCCESSFUL_TEXT,
                        )
                        return True
                    elif response.status == 404:
                        return "The requested file was not found."
                    elif response.status == 403:
                        return "Access to the requested file is forbidden."
                    else:
                        return f"Error downloading media: HTTP error {response.status}"
        except Exception as e:
            print(f"Error downloading media. {e}")
            return f"UhUhh Something`s not right: Status CODE {response.status}"
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    async def cancel_download(self):
        self.should_cancel_download = True

    def _get_headers(self, link: str = " "):

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
        ]
        user_agent = random.choice(user_agents)

        return {
            "sec-fetch-mode": "navigate",
            "cache-control": "max-age=0",
            "authority": "(link unavailable)",
            "upgrade-insecure-requests": "1",
            "accept-language": "en-GB,en;q=0.9,tr-TR;q=0.8,tr;q=0.7,en-US;q=0.6", 
            "user-agent": user_agent,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "referer": f"wwww.facebook.com",
            "Sec-CH-UA": '"Chromium";v="93", "Google Chrome";v="93", " Not;A Brand";v="99"'
        }
