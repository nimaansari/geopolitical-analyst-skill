"""
WarStrikes Scraper
Real-time military strike and conflict incident tracking
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from typing import List, Dict, Optional, Tuple
import json
import time
import re

logger = logging.getLogger(__name__)


class WarStrikesScraper:
    """Scrape real-time military strikes and incidents from WarStrikes"""
    
    def __init__(self, timeout: int = 15, delay: float = 2.0):
        """
        Initialize scraper
        
        Args:
            timeout: Request timeout in seconds
            delay: Delay between requests (be respectful)
        """
        self.base_url = "https://warstrikes.com"
        self.timeout = timeout
        self.delay = delay
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_incidents(self) -> List[Dict]:
        """
        Scrape real-time military incidents and strikes
        
        Returns:
            List of incident dictionaries
        """
        try:
            logger.info("Scraping WarStrikes incidents")
            
            response = requests.get(
                self.base_url,
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch WarStrikes: {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            incidents = []
            
            # Parse incident items
            for item in soup.find_all(['div', 'li', 'article'], class_=['incident', 'strike', 'event', 'item']):
                try:
                    incident = self._parse_incident_item(item)
                    if incident:
                        incidents.append(incident)
                except Exception as e:
                    logger.debug(f"Error parsing incident: {e}")
                    continue
            
            logger.info(f"Found {len(incidents)} incidents")
            time.sleep(self.delay)  # Be respectful
            
            return incidents
        
        except Exception as e:
            logger.error(f"Error scraping WarStrikes: {e}")
            return []
    
    def _parse_incident_item(self, item) -> Optional[Dict]:
        """Parse individual incident item"""
        try:
            # Extract description/title
            title_elem = item.find(['h2', 'h3', 'span', 'div'], class_=['title', 'description', 'incident-title'])
            title = title_elem.text.strip() if title_elem else None
            
            # Extract timestamp
            time_elem = item.find(['time', 'span'], class_=['time', 'timestamp', 'date'])
            timestamp = time_elem.text.strip() if time_elem else None
            
            # Extract location (coordinates or text)
            location_elem = item.find(['span', 'div'], class_=['location', 'coord', 'coordinates'])
            location = location_elem.text.strip() if location_elem else None
            
            # Try to extract coordinates
            coordinates = self._extract_coordinates(location) if location else None
            
            # Extract incident type
            type_elem = item.find(['span', 'div'], class_=['type', 'incident-type', 'category'])
            incident_type = type_elem.text.strip() if type_elem else 'Unknown'
            
            # Extract details
            details_elem = item.find(['p', 'div'], class_=['details', 'description', 'notes'])
            details = details_elem.text.strip() if details_elem else None
            
            if not title and not details:
                return None
            
            return {
                'title': title or details[:100],
                'description': details,
                'timestamp': timestamp,
                'location': location,
                'coordinates': coordinates,
                'incident_type': incident_type,
                'type': 'military_incident',
                'scraped_at': datetime.now().isoformat(),
                'platform': 'WarStrikes',
                'severity': self._assess_severity(incident_type, details)
            }
        
        except Exception as e:
            logger.debug(f"Error parsing incident: {e}")
            return None
    
    def _extract_coordinates(self, location_str: str) -> Optional[Tuple[float, float]]:
        """Extract latitude, longitude from location string"""
        try:
            # Try to match pattern like "34.5°N, 39.2°E" or "34.5, 39.2"
            pattern = r'(-?\d+\.?\d*)[°,\s]+(-?\d+\.?\d*)'
            matches = re.findall(pattern, location_str)
            
            if matches:
                lat, lon = float(matches[0][0]), float(matches[0][1])
                return (lat, lon)
        
        except Exception as e:
            logger.debug(f"Error extracting coordinates: {e}")
        
        return None
    
    def _assess_severity(self, incident_type: str, details: Optional[str]) -> str:
        """Assess incident severity (low/medium/high/critical)"""
        incident_type_lower = incident_type.lower()
        details_lower = (details or "").lower()
        
        # Critical indicators
        critical_keywords = ['nuclear', 'chemical', 'biological', 'wmd', 'mass casualty']
        if any(kw in incident_type_lower or kw in details_lower for kw in critical_keywords):
            return 'critical'
        
        # High severity indicators
        high_keywords = ['major offensive', 'capital city', 'airbase', 'government', 'infrastructure']
        if any(kw in incident_type_lower or kw in details_lower for kw in high_keywords):
            return 'high'
        
        # Medium severity indicators
        medium_keywords = ['strike', 'attack', 'bombing', 'missile', 'drone']
        if any(kw in incident_type_lower or kw in details_lower for kw in medium_keywords):
            return 'medium'
        
        return 'low'
    
    def get_incidents_by_type(self) -> Dict[str, List[Dict]]:
        """Get incidents grouped by type"""
        incidents = self.scrape_incidents()
        
        by_type = {}
        for incident in incidents:
            itype = incident.get('incident_type', 'Unknown')
            if itype not in by_type:
                by_type[itype] = []
            by_type[itype].append(incident)
        
        return by_type
    
    def get_incidents_by_severity(self) -> Dict[str, List[Dict]]:
        """Get incidents grouped by severity"""
        incidents = self.scrape_incidents()
        
        by_severity = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }
        
        for incident in incidents:
            severity = incident.get('severity', 'low')
            by_severity[severity].append(incident)
        
        return by_severity
    
    def get_incidents_by_location(self, region: str) -> List[Dict]:
        """Get incidents in specific region"""
        incidents = self.scrape_incidents()
        
        region_lower = region.lower()
        return [
            i for i in incidents
            if region_lower in (i.get('location', '') or '').lower()
        ]
    
    def get_recent_incidents(self, hours: int = 24) -> List[Dict]:
        """Get incidents from last N hours"""
        incidents = self.scrape_incidents()
        
        from datetime import datetime, timedelta
        cutoff = datetime.now() - timedelta(hours=hours)
        
        recent = []
        for incident in incidents:
            try:
                ts = incident.get('timestamp')
                if ts:
                    # Try to parse timestamp
                    incident_dt = datetime.fromisoformat(ts)
                    if incident_dt > cutoff:
                        recent.append(incident)
            except:
                # If parsing fails, include it (assume recent)
                recent.append(incident)
        
        return recent
    
    def get_incidents_summary(self) -> Dict:
        """Get summary of current incidents"""
        incidents = self.scrape_incidents()
        by_type = self.get_incidents_by_type()
        by_severity = self.get_incidents_by_severity()
        
        return {
            'total_incidents': len(incidents),
            'by_type': {k: len(v) for k, v in by_type.items()},
            'by_severity': {k: len(v) for k, v in by_severity.items()},
            'critical_incidents': by_severity['critical'],
            'high_severity_incidents': by_severity['high'],
            'timestamp': datetime.now().isoformat(),
            'incidents': incidents
        }


class WarStrikesCache:
    """Cache for WarStrikes data to avoid excessive scraping"""
    
    def __init__(self, cache_file: str = "~/.cache/warstrikes_cache.json", ttl_seconds: int = 300):
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


def get_warstrikes_incidents(use_cache: bool = True) -> List[Dict]:
    """Convenience function to get WarStrikes incidents"""
    scraper = WarStrikesScraper()
    cache = WarStrikesCache() if use_cache else None
    
    # Try cache first
    if cache:
        cached = cache.get('warstrikes_incidents')
        if cached:
            logger.info("Using cached WarStrikes data")
            return cached
    
    # Scrape fresh
    incidents = scraper.scrape_incidents()
    
    # Cache it
    if cache and incidents:
        cache.set('warstrikes_incidents', incidents)
    
    return incidents
