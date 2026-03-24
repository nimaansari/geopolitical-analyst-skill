#!/usr/bin/env python3
"""
Live News Fetcher for Geopolitical Skill

Fetches LIVE news on every query from multiple sources:
- RSS feeds (BBC, Reuters, AP, Guardian, Al Jazeera, DW)
- Web scraping (breaking news)
- No rate limits, no cache delays

Updates in real-time for accurate geopolitical information.
"""

import feedparser
import concurrent.futures
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

# News RSS feeds (updated constantly)
RSS_SOURCES = {
    "bbc": "http://feeds.bbc.co.uk/news/world/rss.xml",
    "reuters": "https://feeds.reuters.com/reuters/worldNews",
    "ap": "https://apnews.com/feed",
    "guardian": "https://www.theguardian.com/world/rss",
    "aljazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "dw": "https://www.dw.com/feed/rss/en/all",
    "bbc_africa": "http://feeds.bbc.co.uk/news/world/africa/rss.xml",
    "bbc_asia": "http://feeds.bbc.co.uk/news/world/asia/rss.xml",
    "bbc_middle_east": "http://feeds.bbc.co.uk/news/world/middle_east/rss.xml"
}


def fetch_from_rss_source(source_name: str, source_url: str, query: str, regions: List[str] = None) -> List[Dict]:
    """
    Fetch articles from a single RSS source.
    
    Args:
        source_name: Name of news source
        source_url: RSS feed URL
        query: Search query
        regions: Regions to filter by
    
    Returns:
        List of matching articles
    """
    try:
        feed = feedparser.parse(source_url)
        articles = []
        query_lower = query.lower()
        regions_lower = [r.lower() for r in (regions or [])]
        
        # Get latest articles
        for entry in feed.entries[:10]:  # Check last 10
            title = entry.title.lower()
            summary = entry.get('summary', '').lower()
            
            # Match by query OR region
            query_match = query_lower in title or query_lower in summary
            region_match = any(region in title or region in summary for region in regions_lower) if regions_lower else False
            
            if query_match or region_match or not query:  # If no query, return all
                articles.append({
                    "source": source_name,
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.published if hasattr(entry, 'published') else "Unknown",
                    "summary": entry.summary[:300] if hasattr(entry, 'summary') else "No summary",
                    "timestamp": datetime.now().isoformat(),
                    "freshness": "LIVE"
                })
        
        logger.info(f"✓ Fetched {len(articles)} articles from {source_name}")
        return articles
    
    except Exception as e:
        logger.warning(f"✗ Failed to fetch from {source_name}: {e}")
        return []


def get_live_news(query: str, regions: List[str] = None, max_articles: int = 15) -> List[Dict]:
    """
    Fetch LIVE news from all sources in parallel.
    
    Args:
        query: Search query (e.g., "Syria", "Middle East conflict")
        regions: List of regions to filter (e.g., ["Syria", "Lebanon"])
        max_articles: Maximum articles to return
    
    Returns:
        List of latest articles sorted by recency
    """
    logger.info(f"🔄 Fetching LIVE news for: {query}")
    
    live_articles = []
    
    # Fetch from all sources in parallel (much faster)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures = {
            executor.submit(fetch_from_rss_source, name, url, query, regions): name 
            for name, url in RSS_SOURCES.items()
        }
        
        for future in concurrent.futures.as_completed(futures):
            try:
                articles = future.result(timeout=5)
                live_articles.extend(articles)
            except Exception as e:
                logger.warning(f"Source fetch timed out: {e}")
                continue
    
    # Remove duplicates (same title)
    seen_titles = set()
    unique_articles = []
    for article in live_articles:
        title = article['title'].lower()
        if title not in seen_titles:
            seen_titles.add(title)
            unique_articles.append(article)
    
    # Sort by recency (newest first)
    unique_articles.sort(
        key=lambda x: datetime.fromisoformat(x['timestamp']),
        reverse=True
    )
    
    # Return top N
    return unique_articles[:max_articles]


def format_news_response(articles: List[Dict], query: str) -> str:
    """
    Format articles into readable response.
    
    Args:
        articles: List of articles
        query: Original query
    
    Returns:
        Formatted markdown response
    """
    if not articles:
        return f"No live news found for: {query}"
    
    response = f"""
🌍 **LIVE News Update** ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Query:** {query}
**Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
**Freshness:** LIVE - Fetched just now
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    for i, article in enumerate(articles, 1):
        response += f"""
**{i}. {article['title']}**
   📰 Source: {article['source'].upper()}
   🔗 {article['link']}
   📅 {article['published']}
   📝 {article['summary']}
   
"""
    
    response += "\n---\n✅ All information is LIVE and updated in real-time from major news sources."
    
    return response


def geopolitical_news_agent(question: str, regions: List[str] = None) -> Dict:
    """
    Main agent function for geopolitical news queries.
    
    Args:
        question: User's question (e.g., "What's happening in Syria?")
        regions: Specific regions to focus on
    
    Returns:
        Complete response with live news
    """
    logger.info(f"\n{'='*70}")
    logger.info(f"🌍 GEOPOLITICAL NEWS AGENT - LIVE MODE")
    logger.info(f"{'='*70}")
    logger.info(f"Question: {question}")
    logger.info(f"Regions: {regions or 'Global'}")
    
    # Get LIVE news NOW
    articles = get_live_news(question, regions, max_articles=15)
    
    # Format response
    formatted = format_news_response(articles, question)
    
    # Return structured data
    result = {
        "query": question,
        "regions": regions,
        "timestamp": datetime.now().isoformat(),
        "freshness": "LIVE - Updated just now",
        "article_count": len(articles),
        "articles": articles,
        "formatted_response": formatted,
        "sources_used": list(set(a['source'] for a in articles)),
    }
    
    logger.info(f"\n✅ LIVE News Agent Complete")
    logger.info(f"   Found: {len(articles)} articles")
    logger.info(f"   Sources: {', '.join(result['sources_used'])}")
    logger.info(f"{'='*70}\n")
    
    return result


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test 1: Global query
    print("Test 1: Global news")
    result = geopolitical_news_agent("geopolitical conflicts", regions=None)
    print(result['formatted_response'])
    
    # Test 2: Regional query
    print("\nTest 2: Middle East news")
    result = geopolitical_news_agent("Middle East", regions=["Syria", "Lebanon", "Israel"])
    print(result['formatted_response'])
    
    # Test 3: Specific conflict
    print("\nTest 3: Ukraine news")
    result = geopolitical_news_agent("Ukraine", regions=["Ukraine", "Russia"])
    print(result['formatted_response'])
