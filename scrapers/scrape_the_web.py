from bs4 import BeautifulSoup
import datetime, aiohttp, asyncio
from helper_func import if_only_path, extract_link_title, has_path


class ScrapeTheWeb:
    def __init__(self, search_query):
        self.search_query = str(search_query)

    def get_query_urls(self):
        search_query = self.search_query.replace(" ", "%20")
        query_urls = [
            f"https://archive.org/search?query={search_query}",
            f"https://9jarocks.net/?s={search_query}",
            f"https://parrotvibes.com/?s={search_query}",
        ]
        return query_urls

    async def search(self):
        query_urls = self.get_query_urls()
        all_search_results = []
        async def fetch_search_results(session, url):
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        search_results = await response.text()
                        all_search_results.extend(self.parse_search_results(search_results, url) )
                    else:
                        print(f"Failed to perform search for {url}")
            except aiohttp.ClientError as e:
                print(f"Error while fetching search results: {e}")
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_search_results(session, url) for url in query_urls]
            await asyncio.gather(*tasks)
        return all_search_results

    def parse_search_results(self, html, search_url: str):
        soup = BeautifulSoup(html, "html.parser")
        div_elements = soup.find_all("div")
        links = []
        seen_urls = set()
        for div in div_elements:
            link_elem = div.find("a")
            if link_elem:
                href = link_elem.get("href")
                href = if_only_path(search_url, href)
                if href and href != search_url:
                    if href not in seen_urls:
                        link_text = link_elem.text.strip()
                        link_data = None
                        if link_text:
                            link_data = {"text": link_text, "url": href}
                        else:
                            title = link_elem.get("title")
                            if title:
                                link_data = {"text": title, "url": href}
                            else:
                                title = extract_link_title(href)
                                link_data = {"text": title, "url": href}
                        if link_data:
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
            if any(word in link_text_lower for word in search_query_words) and has_path(
                link["url"]
            ):
                if str(current_year) in link["url"]:
                    matched_links_with_current_year.append(link)
                else:
                    matched_links_without_current_year.append(link)
            else:
                unmatched_links.append(link)

        comb = matched_links_with_current_year + matched_links_without_current_year
        return (comb, unmatched_links)
