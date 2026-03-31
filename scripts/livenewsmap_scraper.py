"""
LiveNewsMap Scraper
Real-time news event mapping and aggregation
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from typing import List, Dict, Optional
import json
import time

logger = logging.getLogger(__name__)


class LiveNewsMapScraper:
    """Scrape real-time news events from LiveNewsMap"""
    
    def __init__(self, timeout: int = 15, delay: float = 2.0):
        """
        Initialize scraper
        
        Args:
            timeout: Request timeout in seconds
            delay: Delay between requests (be respectful)
        """
        self.base_url = "https://livenewsmap.com"
        self.timeout = timeout
        self.delay = delay
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_live_events(self, region: Optional[str] = None) -> List[Dict]:
        """
        Scrape real-time news events
        
        Args:
            region: Optional region filter (e.g., 'Middle East', 'Europe', 'Asia')
        
        Returns:
            List of event dictionaries
        """
        try:
            logger.info(f"Scraping LiveNewsMap events{f' for {region}' if region else ''}")
            
            response = requests.get(
                self.base_url,
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch LiveNewsMap: {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            events = []
            
            # Parse news items (structure may vary)
            for item in soup.find_all('div', class_=['news-item', 'event', 'item']):
                try:
                    event = self._parse_event_item(item)
                    if event:
                        events.append(event)
                except Exception as e:
                    logger.debug(f"Error parsing event item: {e}")
                    continue
            
            logger.info(f"Found {len(events)} events")
            time.sleep(self.delay)  # Be respectful
            
            return events
        
        except Exception as e:
            logger.error(f"Error scraping LiveNewsMap: {e}")
            return []
    
    def _parse_event_item(self, item) -> Optional[Dict]:
        """Parse individual event item"""
        try:
            # Extract title
            title_elem = item.find(['h2', 'h3', 'a', 'div'], class_=['title', 'headline'])
            title = title_elem.text.strip() if title_elem else None
            
            # Extract link
            link_elem = item.find('a', href=True)
            link = link_elem['href'] if link_elem else None
            
            # Extract timestamp
            time_elem = item.find(['time', 'span'], class_=['time', 'timestamp', 'published'])
            timestamp = time_elem.text.strip() if time_elem else None
            
            # Extract location (if available)
            location_elem = item.find(['span', 'div'], class_=['location', 'region', 'country'])
            location = location_elem.text.strip() if location_elem else None
            
            # Extract source
            source_elem = item.find(['span', 'a'], class_=['source', 'outlet'])
            source = source_elem.text.strip() if source_elem else 'Unknown'
            
            if not title:
                return None
            
            return {
                'title': title,
                'url': link if link and link.startswith('http') else f"{self.base_url}{link}" if link else None,
                'timestamp': timestamp,
                'location': location,
                'source': source,
                'type': 'news_event',
                'scraped_at': datetime.now().isoformat(),
                'platform': 'LiveNewsMap'
            }
        
        except Exception as e:
            logger.debug(f"Error parsing event: {e}")
            return None
    
    def get_events_by_region(self, regions: List[str]) -> Dict[str, List[Dict]]:
        """
        Get events filtered by regions
        
        Args:
            regions: List of region names
        
        Returns:
            Dictionary with region -> events mapping
        """
        all_events = self.scrape_live_events()
        
        regional_events = {region: [] for region in regions}
        
        for event in all_events:
            location = event.get('location', '').lower()
            for region in regions:
                if region.lower() in location:
                    regional_events[region].append(event)
        
        return regional_events
    
    def get_top_events(self, limit: int = 20) -> List[Dict]:
        """Get top recent events"""
        events = self.scrape_live_events()
        return events[:limit]
    
    def get_events_summary(self) -> Dict:
        """Get summary of current events"""
        events = self.scrape_live_events()
        
        # Count by region (rough categorization)
        regions = {}
        sources = {}
        
        for event in events:
            location = event.get('location', 'Unknown')
            regions[location] = regions.get(location, 0) + 1
            
            source = event.get('source', 'Unknown')
            sources[source] = sources.get(source, 0) + 1
        
        return {
            'total_events': len(events),
            'by_region': regions,
            'by_source': sources,
            'timestamp': datetime.now().isoformat(),
            'events': events
        }


class LiveNewsMapCache:
    """Cache for LiveNewsMap data to avoid excessive scraping"""
    
    def __init__(self, cache_file: str = "~/.cache/livenewsmap_cache.json", ttl_seconds: int = 300):
        """
        Initialize cache
        
        Args:
            cache_file: Path to cache file
            ttl_seconds: Time to live for cached data (5 min default)
        """
        import os
        self.cache_file = os.path.expanduser(cache_file)
        self.ttl_seconds = ttl_seconds
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self):
        """Ensure cache directory exists"""
        import os
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
    
    def get(self, key: str) -> Optional[List[Dict]]:
        """Get cached data if fresh"""
        import os
        import json
        
        if not os.path.exists(self.cache_file):
            return None
        
        try:
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
            
            if key not in cache:
                return None
            
            # Check if fresh
            cached_time = cache[key].get('timestamp')
            if cached_time:
                from datetime import datetime
                cached_dt = datetime.fromisoformat(cached_time)
                age = (datetime.now() - cached_dt).total_seconds()
                
                if age < self.ttl_seconds:
                    return cache[key].get('data')
        
        except Exception as e:
            logger.error(f"Error reading cache: {e}")
        
        return None
    
    def set(self, key: str, data: List[Dict]):
        """Cache data"""
        import os
        import json
        
        try:
            cache = {}
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
            
            cache[key] = {
                'data': data,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f, indent=2, default=str)
        
        except Exception as e:
            logger.error(f"Error writing cache: {e}")


def get_livenewsmap_events(use_cache: bool = True) -> List[Dict]:
    """Convenience function to get LiveNewsMap events"""
    scraper = LiveNewsMapScraper()
    cache = LiveNewsMapCache() if use_cache else None
    
    # Try cache first
    if cache:
        cached = cache.get('livenewsmap_events')
        if cached:
            logger.info("Using cached LiveNewsMap data")
            return cached
    
    # Scrape fresh
    events = scraper.scrape_live_events()
    
    # Cache it
    if cache and events:
        cache.set('livenewsmap_events', events)
    
    return events
