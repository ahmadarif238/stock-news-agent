import feedparser
from typing import List, Dict

# Standard finance RSS feeds
RSS_FEEDS = [
    "https://finance.yahoo.com/news/rssindex",
    "http://feeds.marketwatch.com/marketwatch/topstories/",
    "https://www.investing.com/rss/news.rss"
]

def fetch_news_from_rss(tickers: List[str]) -> List[Dict]:
    """
    Fetches news from RSS feeds and filters by tickers.
    """
    found_news = []
    seen_links = set() # Per-fetch dedup

    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.get("title", "")
                summary = entry.get("summary", entry.get("description", "No summary available."))
                link = entry.get("link", "#")

                # Extract image/thumbnail
                image_url = None
                if "media_thumbnail" in entry and entry.media_thumbnail:
                    image_url = entry.media_thumbnail[0]["url"]
                elif "media_content" in entry and entry.media_content:
                    image_url = entry.media_content[0]["url"]
                elif "links" in entry:
                    for l in entry.links:
                        if l.get("rel") == "enclosure" and "image" in l.get("type", ""):
                            image_url = l.get("href")
                            break

                # Basic dedup
                if link in seen_links:
                    continue
                seen_links.add(link)

                # Check if any ticker is in the text
                # Normalize text for better matching
                text_to_check = (title + " " + summary).upper()
                
                for ticker in tickers:
                    # Simple matching: ticker + space or space + ticker or specific symbols
                    # This can be improved with regex
                    if ticker.upper() in text_to_check:
                         found_news.append({
                            "ticker": ticker.upper(),
                            "title": title,
                            "summary": summary,
                            "link": link,
                            "image_url": image_url
                        })
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
            
    return found_news
