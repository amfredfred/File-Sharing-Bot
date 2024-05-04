from scrapers.scrape_the_web import ScrapeTheWeb

def search(query):
    scraper = ScrapeTheWeb(query)
    results = scraper.search()
    return scraper.filter_links(results)


if __name__ == "__main__":
    query = input("Enter your search query: ")
    search_results,oth = search(query)
    print("Search Results:")
    print(search_results)
    # for result in search_results:
    #     print(result)
