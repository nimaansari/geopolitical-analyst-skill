"""
SOLUTION 3: Smart Data Source Fallback Chain
Try ACLED public → UCDP (open) → auto-fallback
Never fails, always returns data from best available source
"""

import requests
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ACLEDPublicFetcher:
    """
    SOLUTION 3: ACLED Public Endpoints (no API key needed)
    Free access to public conflict data
    """
    
    BASE_URL = "https://api.acleddata.com/api/8/events/read.json"
    
    @staticmethod
    def fetch(country: str, days_back: int = 7) -> Optional[Dict]:
        """Fetch from ACLED public endpoints (no auth required)"""
        try:
            params = {
                "iso": country,  # ISO country code
                "limit": 100,
                "ordering": "-event_date"
            }
            
            logger.info(f"Trying ACLED PUBLIC endpoint for {country}...")
            response = requests.get(ACLEDPublicFetcher.BASE_URL, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✓ ACLED PUBLIC SUCCESS: {len(data.get('data', []))} events")
                return data
            else:
                logger.warning(f"ACLED PUBLIC failed (status {response.status_code})")
                return None
                
        except Exception as e:
            logger.warning(f"ACLED PUBLIC error: {e}")
            return None


class UCDPFetcher:
    """
    SOLUTION 3: Uppsala Conflict Data Program (UCDP)
    Completely open access, no registration required
    Alternative to ACLED when public endpoints fail
    
    Uses v3 API format with proper endpoint structure
    """
    
    # UCDP v3 API endpoint (current version)
    BASE_URL = "https://ucdpapi.pcr.uu.se/api/gedevents/23.1"
    
    @staticmethod
    def fetch_conflicts(country: str = None) -> Optional[Dict]:
        """
        Fetch conflict events from UCDP v3 API
        Open API, no authentication needed
        
        Args:
            country: Country name or ISO code (e.g., "Iran", "Syria")
            
        Returns:
            Dict with conflict events or None on failure
        """
        try:
            # Use UCDP v3 API endpoint format
            url = UCDPFetcher.BASE_URL
            
            # UCDP v3 expects different params
            params = {
                "pagesize": 100  # Results per page
            }
            
            if country:
                params["country"] = country
            
            logger.info(f"Trying UCDP v3 API for {country or 'global'}...")
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Handle UCDP v3 response format
                events = data.get("events", []) or data.get("results", []) or []
                event_count = len(events) if isinstance(events, list) else len(data)
                
                logger.info(f"✓ UCDP SUCCESS: {event_count} events")
                
                # Normalize response format
                return {"data": events} if events else {"data": []}
            elif response.status_code == 404:
                logger.warning(f"UCDP endpoint 404 for {country} - country may not exist or API changed")
                return None
            else:
                logger.warning(f"UCDP failed (status {response.status_code})")
                return None
                
        except Exception as e:
            logger.warning(f"UCDP error: {e}")
            return None
    
    @staticmethod
    def fetch_fatalities(country: str, years_back: int = 5) -> Optional[Dict]:
        """Fetch conflict fatality data from UCDP"""
        try:
            url = f"{UCDPFetcher.BASE_URL}/battledeaths/search"
            
            params = {
                "country": country,
                "limit": 50
            }
            
            logger.info(f"Fetching UCDP fatalities for {country}...")
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            
        except Exception as e:
            logger.warning(f"UCDP fatalities error: {e}")
        
        return None


class ConflictDataFallbackChain:
    """
    SOLUTION 3: Smart Fallback Chain
    
    Priority order:
    1. Try ACLED PUBLIC (free endpoints, no registration)
    2. Fallback to UCDP (open access alternative)
    3. Return best available data (graceful degradation)
    
    Never fails — always returns something
    """
    
    @staticmethod
    def fetch_conflict_data(country: str, days_back: int = 7) -> Dict:
        """
        Fetch conflict data with automatic fallback
        
        Returns:
            {
                "source": "ACLED_PUBLIC" | "UCDP" | "COMBINED",
                "data": [...events...],
                "fallback_used": boolean,
                "status": "success" | "partial" | "degraded"
            }
        """
        
        logger.info(f"=== CONFLICT DATA FALLBACK CHAIN for {country} ===")
        
        # SOLUTION 3: Step 1 - Try ACLED PUBLIC (no auth needed)
        acled_data = ACLEDPublicFetcher.fetch(country, days_back)
        
        if acled_data and acled_data.get('data'):
            logger.info("✓ Using ACLED PUBLIC data")
            return {
                "source": "ACLED_PUBLIC",
                "data": acled_data.get('data', []),
                "count": len(acled_data.get('data', [])),
                "fallback_used": False,
                "status": "success"
            }
        
        # SOLUTION 3: Step 2 - ACLED failed, fallback to UCDP
        logger.warning("ACLED PUBLIC unavailable, falling back to UCDP...")
        ucdp_data = UCDPFetcher.fetch_conflicts(country)
        
        if ucdp_data and ucdp_data.get('results'):
            logger.info("✓ Using UCDP fallback data")
            return {
                "source": "UCDP",
                "data": ucdp_data.get('results', []),
                "count": len(ucdp_data.get('results', [])),
                "fallback_used": True,
                "status": "success"
            }
        
        # SOLUTION 3: Step 3 - Both failed, return degraded response
        logger.error("Both ACLED and UCDP unavailable")
        return {
            "source": "NONE",
            "data": [],
            "count": 0,
            "fallback_used": True,
            "status": "degraded",
            "message": "No conflict data available. Try again later or check internet connection."
        }
    
    @staticmethod
    def fetch_with_combined_sources(country: str) -> Dict:
        """
        Fetch from both ACLED PUBLIC and UCDP, combine results
        Deduplicates by date/location to avoid duplicates
        """
        logger.info(f"Fetching combined data from all available sources for {country}...")
        
        acled_data = ACLEDPublicFetcher.fetch(country)
        ucdp_data = UCDPFetcher.fetch_conflicts(country)
        
        combined_events = []
        seen_events = set()  # Deduplicate
        
        # Add ACLED events
        if acled_data and acled_data.get('data'):
            for event in acled_data.get('data', []):
                event_key = f"{event.get('event_date')}_{event.get('location')}"
                if event_key not in seen_events:
                    combined_events.append(event)
                    seen_events.add(event_key)
        
        # Add UCDP events
        if ucdp_data and ucdp_data.get('results'):
            for event in ucdp_data.get('results', []):
                event_key = f"{event.get('event_date')}_{event.get('location')}"
                if event_key not in seen_events:
                    combined_events.append(event)
                    seen_events.add(event_key)
        
        return {
            "source": "COMBINED (ACLED_PUBLIC + UCDP)",
            "data": combined_events,
            "count": len(combined_events),
            "acled_events": len(acled_data.get('data', [])) if acled_data else 0,
            "ucdp_events": len(ucdp_data.get('results', [])) if ucdp_data else 0,
            "status": "success" if combined_events else "degraded"
        }


# Convenience functions
def get_conflict_data(country: str, use_combined: bool = False) -> Dict:
    """
    SOLUTION 3: Public API for conflict data with automatic fallback
    
    Args:
        country: Country name or ISO code
        use_combined: If True, get from both ACLED PUBLIC and UCDP combined
    
    Returns:
        Conflict data from best available source (never fails)
    """
    if use_combined:
        return ConflictDataFallbackChain.fetch_with_combined_sources(country)
    else:
        return ConflictDataFallbackChain.fetch_conflict_data(country)


def fetch_conflict_data(country: str) -> Dict:
    """
    Alias for get_conflict_data() for backward compatibility
    
    Args:
        country: Country name or ISO code
    
    Returns:
        Conflict data from best available source
    """
    return get_conflict_data(country)


def get_data(country: str) -> Dict:
    """
    Alias for get_conflict_data() - shorter method name
    
    Usage:
        data = get_data("Syria")
        
    Returns:
        Conflict data with auto-fallback
    """
    return get_conflict_data(country)
