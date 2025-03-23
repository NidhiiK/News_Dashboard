import os
import json
from newsapi import NewsApiClient

# Replace with your actual NewsAPI key
NEWS_API_KEY = "dc8887d4c0634f6ebe411f4f55c927cb"
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def fetch_news(domains, scope="all"):
    """Fetch news articles for given domains and scope (national/international)."""
    if not domains:  # Handle empty domains list
        query = "general"  # Default query if no domains selected
    else:
        query = " OR ".join(domains)  # e.g., "sports OR technology"
    
    if scope == "national":
        query += " US"  # Append "US" for national scope
    elif scope == "international":
        query += " -US"  # Exclude "US" for international scope
    
    try:
        articles = newsapi.get_everything(q=query, language="en")
        # Save to file
        os.makedirs("data", exist_ok=True)
        with open("data/articles.json", "w") as f:
            json.dump(articles["articles"], f)
        return articles["articles"]
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

if __name__ == "__main__":
    # Test fetch
    articles = fetch_news(["sports", "technology"], "national")
    print(f"Fetched {len(articles)} articles")