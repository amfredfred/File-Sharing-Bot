from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os, tempfile, aiofiles, aiohttp, shutil
from helper_func import if_only_path
from config import ALL_EXTENTIONS, DOWNLOAD_SUCCESSFUL_TEXT
from helper_func import is_downloadable


class DownloadManager:
    def __init__(self):
        self.should_cancel_download = False
        pass

    async def _parse_link(self, link):
        parsed_url = urlparse(link)
        if parsed_url.scheme == "https" and parsed_url.netloc == "t.me":
            return {"type": "telegram", "url": link}
        elif parsed_url.path.endswith(ALL_EXTENTIONS):
            return {"type": "media", "url": link}
        else:
            return {
                "type": "webpage",
                "urls": await self._find_all_links(link),
            }

    async def _find_all_links(self, link):
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
