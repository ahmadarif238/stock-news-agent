import feedparser

def fetch_news_from_rss(tickers, rss_urls):
    found_news = []
    for url in rss_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.get("title", "")
            summary = entry.get("summary", entry.get("description", "No summary available."))

            for ticker in tickers:
                if ticker in title or ticker in summary:
                    found_news.append({
                        "ticker": ticker,
                        "title": title,
                        "summary": summary,
                        "link": entry.get("link", "#")
                    })
    return found_news
