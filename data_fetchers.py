"""
Live Data Fetchers for Geopolitical Analysis
Fetches real-time data from public APIs for conflict analysis
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# SOLUTION 1: EXPONENTIAL BACKOFF FOR RATE LIMITING (429 ERRORS)
# ============================================================================

class RateLimitCache:
    """Local cache for API results (1-4 hour TTL)"""
    def __init__(self):
        self.cache = {}
        self.ttl_seconds = 3600  # 1 hour default
    
    def _cache_key(self, url: str, params: dict) -> str:
        """Generate cache key from URL + params"""
        key_str = f"{url}_{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, url: str, params: dict) -> Optional[Dict]:
        """Get cached result if not expired"""
        key = self._cache_key(url, params)
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl_seconds:
                logger.info(f"Cache HIT for {url[:50]}...")
                return data
            else:
                logger.info(f"Cache EXPIRED for {url[:50]}...")
                del self.cache[key]
        return None
    
    def set(self, url: str, params: dict, data: Dict):
        """Cache result with timestamp (skip empty/failed responses)"""
        # Don't cache empty or failed responses
        if not data or not data.get("data") and not data.get("articles") and not data.get("events"):
            logger.info(f"Skipped caching empty/failed response for {url[:50]}...")
            return
        
        key = self._cache_key(url, params)
        self.cache[key] = (data, time.time())
        logger.info(f"Cached result for {url[:50]}...")
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()


# Global cache instance
_api_cache = RateLimitCache()


def _fetch_with_exponential_backoff(url: str, params: dict = None, max_retries: int = 4, timeout: int = 30) -> Optional[Dict]:
    """
    Fetch URL with exponential backoff on rate limit (429) or timeout errors
    
    Backoff strategy:
    - 2 seconds on first retry
    - 5 seconds on second retry
    - 10 seconds on third retry
    - 30 seconds on fourth retry
    
    Caching: Results cached for 1 hour to reduce repeated requests
    """
    # SOLUTION 1: Check cache first
    cached = _api_cache.get(url, params)
    if cached:
        return cached
    
    backoff_times = [2, 5, 10, 30]  # Exponential backoff: 2s → 5s → 10s → 30s
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            
            # Handle rate limiting (429)
            if response.status_code == 429:
                if attempt < max_retries - 1:
                    wait_time = backoff_times[attempt]
                    logger.warning(f"Rate limited (429) on {url[:50]}... (attempt {attempt+1}/{max_retries}), waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(f"Rate limited after {max_retries} retries. API is heavily congested.")
                    return None
            
            response.raise_for_status()
            data = response.json()
            
            # SOLUTION 1: Cache successful result
            _api_cache.set(url, params, data)
            return data
            
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                wait_time = backoff_times[attempt]
                logger.warning(f"Timeout on {url[:50]}... (attempt {attempt+1}/{max_retries}), waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"Failed to fetch {url} after {max_retries} attempts (timeout)")
                return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    return None


# Backward compatibility
_fetch_with_retry = _fetch_with_exponential_backoff


class GDELTFetcher:
    """Fetch articles, tone, themes from GDELT"""
    
    BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
    
    @staticmethod
    def fetch(keyword: str, days_back: int = 7, max_records: int = 250) -> Dict:
        """
        Fetch GDELT articles on a keyword with retry logic
        
        Args:
            keyword: Topic to search (e.g., "Ukraine conflict")
            days_back: How many days of history
            max_records: Maximum articles to return
            
        Returns:
            Dict with articles, tone analysis, key themes
        """
        try:
            params = {
                "query": keyword,
                "mode": "artlist",
                "maxrecords": max_records,
                "format": "json",
                "sort": "date",
                "timespan": f"{days_back}d"
            }
            
            data = _fetch_with_retry(GDELTFetcher.BASE_URL, params=params, max_retries=3, timeout=30)
            
            if not data:
                return {"source": "GDELT", "error": "Failed to fetch after retries", "articles": []}
            
            articles = data.get("articles", [])
            
            return {
                "source": "GDELT",
                "keyword": keyword,
                "articles_found": len(articles),
                "articles": articles[:max_records],
                "timestamp": datetime.utcnow().isoformat(),
                "tone_analysis": GDELTFetcher._analyze_tone(articles)
            }
            
        except Exception as e:
            logger.error(f"GDELT fetch error: {e}")
            return {"source": "GDELT", "error": str(e), "articles": []}
    
    @staticmethod
    def _analyze_tone(articles: List[Dict]) -> Dict:
        """Analyze tone across articles"""
        if not articles:
            return {"average_tone": 0, "positive": 0, "negative": 0, "neutral": 0}
        
        tones = [float(a.get("tone", 0)) for a in articles if a.get("tone")]
        avg_tone = sum(tones) / len(tones) if tones else 0
        
        return {
            "average_tone": round(avg_tone, 2),
            "positive": len([t for t in tones if t > 2]),
            "negative": len([t for t in tones if t < -2]),
            "neutral": len([t for t in tones if -2 <= t <= 2])
        }


class ACLEDFetcher:
    """Fetch armed conflict events from ACLED"""
    
    BASE_URL = "https://api.acleddata.com/api/events/read"
    
    @staticmethod
    def fetch(country: str, days_back: int = 7, limit: int = 1000) -> Dict:
        """
        Fetch ACLED events for a country
        
        Args:
            country: Country code or name (e.g., "Ukraine", "Gaza")
            days_back: Days of history
            limit: Max events
            
        Returns:
            Dict with events, event types, casualties
        """
        try:
            date_from = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")
            
            params = {
                "country": country,
                "limit": limit,
                "date_filter": date_from
            }
            
            data = _fetch_with_retry(ACLEDFetcher.BASE_URL, params=params, max_retries=3, timeout=30)
            if not data:
                return {"source": "ACLED", "error": "Failed to fetch after retries", "events": []}
            events = data.get("data", [])
            response.raise_for_status()
            
            data = response.json()
            events = data.get("data", [])
            
            return {
                "source": "ACLED",
                "country": country,
                "events_found": len(events),
                "events": events,
                "timestamp": datetime.utcnow().isoformat(),
                "event_summary": ACLEDFetcher._summarize_events(events)
            }
            
        except Exception as e:
            logger.error(f"ACLED fetch error: {e}")
            return {"source": "ACLED", "error": str(e), "events": []}
    
    @staticmethod
    def _summarize_events(events: List[Dict]) -> Dict:
        """Summarize events by type"""
        if not events:
            return {"total": 0, "by_type": {}, "total_deaths": 0}
        
        event_types = {}
        total_deaths = 0
        
        for event in events:
            event_type = event.get("event_type", "Unknown")
            event_types[event_type] = event_types.get(event_type, 0) + 1
            total_deaths += event.get("fatalities", 0)
        
        return {
            "total": len(events),
            "by_type": event_types,
            "total_deaths": total_deaths,
            "events_per_day": round(len(events) / 7, 1) if events else 0
        }


class ReliefWebFetcher:
    """Fetch humanitarian data from ReliefWeb"""
    
    BASE_URL = "https://api.reliefweb.int/v2/reports"
    
    @staticmethod
    def fetch(country: str, days_back: int = 7, limit: int = 100) -> Dict:
        """
        Fetch ReliefWeb humanitarian reports
        
        Args:
            country: Country name
            days_back: Days of history
            limit: Max reports
            
        Returns:
            Dict with humanitarian reports, affected populations
        """
        try:
            date_from = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")
            
            # Build filter query
            filters = f'filter[operators][0][name]=country&filter[operators][0][value][name]={country}&filter[operators][1][name]=date&filter[operators][1][value]=>{date_from}'
            
            params = {
                "appname": "geopolitical-analyst",
                "limit": limit,
                "sort": ["date:desc"]
            }
            
            response = requests.get(ReliefWebFetcher.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            reports = data.get("data", [])
            
            return {
                "source": "ReliefWeb",
                "country": country,
                "reports_found": len(reports),
                "reports": reports,
                "timestamp": datetime.utcnow().isoformat(),
                "humanitarian_summary": ReliefWebFetcher._summarize_reports(reports)
            }
            
        except Exception as e:
            logger.error(f"ReliefWeb fetch error: {e}")
            return {"source": "ReliefWeb", "error": str(e), "reports": []}
    
    @staticmethod
    def _summarize_reports(reports: List[Dict]) -> Dict:
        """Summarize humanitarian situation"""
        if not reports:
            return {"total_reports": 0, "priority": "Unknown"}
        
        return {
            "total_reports": len(reports),
            "latest": reports[0].get("date", "") if reports else None,
            "report_types": list(set([r.get("type", "Unknown") for r in reports]))
        }


class EconomicDataFetcher:
    """Fetch economic data from IMF, World Bank, Frankfurter"""
    
    @staticmethod
    def fetch_currency(country_code: str = "USD") -> Dict:
        """
        Fetch currency exchange rates via Frankfurter API
        
        Args:
            country_code: Currency code (e.g., "RUB", "CNY", "EUR")
            
        Returns:
            Dict with exchange rates vs major currencies
        """
        try:
            url = f"https://api.frankfurter.app/latest?from={country_code}"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "source": "Frankfurter",
                "currency": country_code,
                "timestamp": datetime.utcnow().isoformat(),
                "rates": data.get("rates", {}),
                "base": data.get("base", "")
            }
            
        except Exception as e:
            logger.error(f"Frankfurter fetch error: {e}")
            return {"source": "Frankfurter", "error": str(e), "rates": {}}
    
    @staticmethod
    def fetch_sanctions(target: str = None) -> Dict:
        """
        Fetch active UN sanctions (static list + update path)
        
        Returns:
            Dict with active sanctions regimes
        """
        # Note: This is a static reference; for live updates, would need to monitor UN site
        sanctions_data = {
            "source": "UN Security Council",
            "timestamp": datetime.utcnow().isoformat(),
            "note": "Static reference; check un.org/securitycouncil/sanctions for live updates",
            "major_regimes": {
                "North Korea": {"since": "2006", "type": "comprehensive"},
                "Iran": {"since": "2006", "type": "targeted"},
                "Russia": {"since": "2014", "type": "targeted"},
                "Venezuela": {"since": "2017", "type": "targeted"},
                "Syria": {"since": "2011", "type": "targeted"}
            }
        }
        return sanctions_data


class NewsSourcesTrending:
    """Track trending topics across major outlets"""
    
    @staticmethod
    def fetch_trends(keywords: List[str]) -> Dict:
        """
        Use GDELT to identify trending topics
        
        Args:
            keywords: List of keywords to track
            
        Returns:
            Dict with trend data across outlets
        """
        trends = {}
        
        for keyword in keywords:
            result = GDELTFetcher.fetch(keyword, days_back=7, max_records=100)
            trends[keyword] = {
                "articles": result.get("articles_found", 0),
                "tone": result.get("tone_analysis", {})
            }
        
        return {
            "source": "Multi-outlet trend analysis",
            "timestamp": datetime.utcnow().isoformat(),
            "trends": trends
        }


def fetch_all_data(conflict_country: str, keywords: List[str]) -> Dict:
    """
    Fetch all live data for a conflict situation
    
    Args:
        conflict_country: Country name
        keywords: Key search terms
        
    Returns:
        Comprehensive Dict with all data sources
    """
    logger.info(f"Fetching live data for {conflict_country}...")
    
    all_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "country": conflict_country,
        "gdelt": GDELTFetcher.fetch(f"{conflict_country} conflict", days_back=7),
        "acled": ACLEDFetcher.fetch(conflict_country, days_back=7),
        "reliefweb": ReliefWebFetcher.fetch(conflict_country, days_back=7),
        "currency": EconomicDataFetcher.fetch_currency(),
        "sanctions": EconomicDataFetcher.fetch_sanctions(),
        "trends": NewsSourcesTrending.fetch_trends(keywords)
    }
    
    return all_data


if __name__ == "__main__":
    # Example usage
    print("Fetching live data for Gaza conflict...")
    data = fetch_all_data(
        "Gaza",
        ["Gaza", "Palestine", "Israel", "humanitarian crisis"]
    )
    print(json.dumps(data, indent=2, default=str))
