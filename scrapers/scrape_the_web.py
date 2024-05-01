import requests
from bs4 import BeautifulSoup
import datetime


class ScrapeTheWeb:
    def __init__(self, search_query):
        self.search_query = search_query

    def search(self):
        search_urls = [
            f"https://netnaija.uk/?s={self.search_query}",
            f"https://9jarocks.net/?s={self.search_query}",
            f"https://netnaija.xyz/?s={self.search_query}",
            f"https://netnaijatv.com/?s={self.search_query}",
            f"https://ww16.0123movie.net/search.html?q={self.search_query}",
        ]

        all_search_results = []

        for search_url in search_urls:
            try:
                response = requests.get(search_url)
                if response.status_code == 200:
                    search_results = self.parse_search_results(response.text)
                    all_search_results.extend(search_results)
                else:
                    print(f"Failed to perform search for {search_url}")
            except Exception as e:
                print(f"Exception: {e}")

        return all_search_results

    def parse_search_results(self, html):
        soup = BeautifulSoup(html, "html.parser")
        div_elements = soup.find_all("div")
        links = []
        seen_urls = set()
        for div in div_elements:
            link_elem = div.find("a")
            if link_elem:
                href = link_elem.get("href")
                if href and ("http" in href or "https" in href):
                    if href not in seen_urls:
                        link_text = link_elem.text.strip()
                        if link_text:
                            link_data = {"text": link_text, "url": href}
                            links.append(link_data)
                        else:
                            if self.search_query.lower() in href.lower():
                                cleaned_url = (
                                    href.replace("https://", "")
                                    .replace("http://", "")
                                    .replace("www.", "")
                                )
                                parts = cleaned_url.split("/")
                                link_text = parts[-1].replace("-", " ")
                                link_data = {"text": link_text, "url": href}
                                links.append(link_data)
                        seen_urls.add(href)
        return links

    def filter_links(self, links):
        current_year = datetime.datetime.now().year
        matched_links_with_current_year = []
        matched_links_without_current_year = []
        unmatched_links = []
        search_query_words = self.search_query.lower().split()

        for link in links:
            link_text_lower = link["text"].lower()
            if any(word in link_text_lower for word in search_query_words):
                if str(current_year) in link["url"]:
                    matched_links_with_current_year.append(link)
                else:
                    matched_links_without_current_year.append(link)
            else:
                unmatched_links.append(link)

        return (
            matched_links_with_current_year,
            matched_links_without_current_year,
            unmatched_links,
        )

    def print_links(self, links):
        print("Links found in search results:")
        for link in links:
            text = link["text"].encode("utf-8").decode("utf-8")
            url = link["url"].encode("utf-8").decode("utf-8")
            print(f"Text: {text}, URL: {url}")
            if "image" in link:
                image_url = link["image"].encode("utf-8").decode("utf-8")
                print(f"Image URL: {image_url}")
