import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os


class ScrapeAndDownload:
    def __init__(self, url):
        self.url = url

    def scrape_page(self):
        # Fetch the HTML content of the page
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch page: {self.url}")
            return None

    def parse_links(self, html):
        # Parse the HTML content to extract relevant links
        soup = BeautifulSoup(html, "html.parser")
        links = []
        for link in soup.find_all("a", href=True):
            href = link["href"]
            links.append(href)
        return links

    def filter_media_links(self, links):
        # Filter the links to those that point to media or file downloads
        media_files = [
            ".mp3",
            ".mpeg",
            ".mp4",
            ".avi",
            ".mkv",
            ".pdf",
        ]  # Add more extensions if needed
        filtered_links = []
        for link in links:
            url_path = urlparse(link).path
            if any(url_path.endswith(ext) for ext in media_files):
                filtered_links.append(link)
        return filtered_links

    def download_files(self, links, download_path="./downloads"):
        # Download the media or file links to the specified directory
        if not links:
            print("No media or file links found to download.")
            return
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        for link in links:
            response = requests.get(link)
            if response.status_code == 200:
                filename = os.path.join(
                    download_path, os.path.basename(urlparse(link).path)
                )
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download: {link}")


# Example usage:
url = "https://9jarocks.net/videodownload/always-on-the-move-season-1-complete-chinese-drama-id290016.html" 
downloader = ScrapeAndDownload(url)
html = downloader.scrape_page()
if html:
    links = downloader.parse_links(html)
    media_links = downloader.filter_media_links(links)
    downloader.download_files(media_links)
