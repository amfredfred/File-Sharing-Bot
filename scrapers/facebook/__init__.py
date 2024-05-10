import aiohttp
import asyncio
import json
import re


class FacebookVideoDownloader:
    def __init__(self):
        self.msg = {}

    async def download(self, url):
        try:
            if not url:
                raise Exception("Please provide the URL")

            headers = {
                "sec-fetch-user": "?1",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-site": "none",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "cache-control": "max-age=0",
                "authority": "www.facebook.com",
                "upgrade-insecure-requests": "1",
                "accept-language": "en-GB,en;q=0.9,tr-TR;q=0.8,tr;q=0.7,en-US;q=0.6",
                "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            }

            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as response:
                    response_text = await response.text()

                    self.msg["success"] = True

                    self.msg["id"] = self.generateId(url)
                    self.msg["title"] = self.getTitle(response_text)

                    sdLink = self.getSDLink(response_text)
                    if sdLink:
                        self.msg["links"] = {"Download Low Quality": sdLink + "&dl=1"}

                    hdLink = self.getHDLink(response_text)
                    if hdLink:
                        self.msg["links"]["Download High Quality"] = hdLink + "&dl=1"

        except Exception as e:
            self.msg["success"] = False
            self.msg["message"] = str(e)

        return json.dumps(self.msg)

    def generateId(self, url):
        id = ""
        if str(url).isdigit():
            id = url
        elif re.search(r"(\d+)/?$", url):
            id = re.search(r"(\d+)/?$", url).group(1)
        return id

    def cleanStr(self, str):
        return json.loads('{"text": "%s"}' % str)["text"]

    def getSDLink(self, curl_content):
        regexRateLimit = r'browser_native_sd_url":"([^"]+)"'
        match = re.search(regexRateLimit, curl_content)
        if match:
            return self.cleanStr(match.group(1))
        else:
            return False

    def getHDLink(self, curl_content):
        regexRateLimit = r'browser_native_hd_url":"([^"]+)"'
        match = re.search(regexRateLimit, curl_content)
        if match:
            return self.cleanStr(match.group(1))
        else:
            return False

    def getTitle(self, curl_content):
        title = None
        match = re.search(r"<title>(.*?)<\/title>", curl_content)
        if match:
            title = match.group(1)
        elif re.search(r'title id="pageTitle">(.+?)<\/title>', curl_content):
            title = re.search(
                r'title id="pageTitle">(.+?)<\/title>', curl_content
            ).group(1)
        return self.cleanStr(title)

    def getDescription(self, curl_content):
        match = re.search(r'span class="hasCaption">(.+?)<\/span>', curl_content)
        if match:
            return self.cleanStr(match.group(1))
        return False
