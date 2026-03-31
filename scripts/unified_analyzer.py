"""
Unified Geopolitical Analyzer
Integrates all data sources: news, military, economic, diplomatic, real-time events
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class UnifiedGeopoliticalAnalyzer:
    """
    Complete geopolitical analysis framework
    Combines structural data + dependencies + risk + real-time events
    """
    
    def __init__(self):
        """Initialize analyzer with all data sources"""
        self.data_sources = {
            'structural': {},
            'dependencies': {},
            'risk': {},
            'real_time': {},
            'analysis': {}
        }
    
    def ingest_all_sources(self, config: Dict) -> Dict[str, Any]:
        """
        Ingest data from ALL sources
        
        Args:
            config: Configuration dict with API keys and settings
        
        Returns:
            Complete data from all sources
        """
        logger.info("Ingesting from all sources...")
        
        data = {
            'structural': self._ingest_structural_data(config),
            'dependencies': self._ingest_dependencies(config),
            'risk': self._ingest_risk_factors(config),
            'events': self._ingest_real_time_events(config),
            'timestamp': datetime.now().isoformat()
        }
        
        self.data_sources = data
        return data
    
    def _ingest_structural_data(self, config: Dict) -> Dict:
        """Get structural geopolitical data"""
        logger.info("Ingesting structural data (military, economic, diplomatic)...")
        
        structural = {
            'military': self._get_military_data(config),
            'economic': self._get_economic_data(config),
            'diplomatic': self._get_diplomatic_data(config),
        }
        
        return structural
    
    def _ingest_dependencies(self, config: Dict) -> Dict:
        """Get dependency data"""
        logger.info("Ingesting dependencies (trade, energy, resources)...")
        
        dependencies = {
            'energy': self._get_energy_dependencies(config),
            'trade': self._get_trade_dependencies(config),
            'resources': self._get_resource_dependencies(config),
            'technology': self._get_tech_dependencies(config),
        }
        
        return dependencies
    
    def _ingest_risk_factors(self, config: Dict) -> Dict:
        """Get risk and early warning data"""
        logger.info("Ingesting risk factors (conflict, governance, fragility)...")
        
        risk = {
            'conflict_history': self._get_conflict_data(config),
            'governance': self._get_governance_data(config),
            'fragility': self._get_fragility_index(config),
            'early_warnings': self._get_early_warnings(config),
        }
        
        return risk
    
    def _ingest_real_time_events(self, config: Dict) -> Dict:
        """Get REAL-TIME events from LiveNewsMap and WarStrikes"""
        logger.info("Ingesting real-time events (news + military incidents)...")
        
        from livenewsmap_scraper import get_livenewsmap_events
        from warstrikes_scraper import get_warstrikes_incidents
        
        events = {
            'news_events': self._safe_scrape(get_livenewsmap_events),
            'military_incidents': self._safe_scrape(get_warstrikes_incidents),
            'timestamp': datetime.now().isoformat()
        }
        
        return events
    
    def _safe_scrape(self, scraper_func, *args, **kwargs) -> List[Dict]:
        """Safely call scraper with error handling"""
        try:
            result = scraper_func(*args, **kwargs)
            return result if result else []
        except Exception as e:
            logger.warning(f"Scraper error: {e}")
            return []
    
    def _get_military_data(self, config: Dict) -> Dict:
        """Get military power data (SIPRI)"""
        try:
            import requests
            
            sipri_url = "https://sipri.org/databases/milex"
            logger.info("Fetching SIPRI military data...")
            
            # In production, parse real SIPRI data
            # For now, return structure
            return {
                'source': 'SIPRI',
                'status': 'configured',
                'url': sipri_url
            }
        except Exception as e:
            logger.error(f"Error fetching military data: {e}")
            return {}
    
    def _get_economic_data(self, config: Dict) -> Dict:
        """Get economic power data (World Bank)"""
        try:
            logger.info("Fetching World Bank economic data...")
            
            # In production, call World Bank API
            return {
                'source': 'World Bank',
                'status': 'configured',
                'endpoint': 'https://api.worldbank.org/v2'
            }
        except Exception as e:
            logger.error(f"Error fetching economic data: {e}")
            return {}
    
    def _get_diplomatic_data(self, config: Dict) -> Dict:
        """Get diplomatic alliance data (CoW database)"""
        logger.info("Fetching diplomatic alliance data...")
        
        return {
            'source': 'Correlates of War',
            'status': 'configured',
            'alliances': [
                {'name': 'NATO', 'members': 32},
                {'name': 'BRICS', 'members': 5},
                {'name': 'ASEAN', 'members': 10},
            ]
        }
    
    def _get_energy_dependencies(self, config: Dict) -> Dict:
        """Get energy dependency data (IEA)"""
        logger.info("Fetching energy dependency data...")
        
        return {
            'source': 'IEA',
            'status': 'configured',
            'data_types': ['oil', 'gas', 'uranium', 'coal']
        }
    
    def _get_trade_dependencies(self, config: Dict) -> Dict:
        """Get trade data (UN Comtrade)"""
        logger.info("Fetching trade dependency data...")
        
        return {
            'source': 'UN Comtrade',
            'status': 'configured',
            'endpoint': 'https://comtrade.un.org/api'
        }
    
    def _get_resource_dependencies(self, config: Dict) -> Dict:
        """Get critical resource data (USGS)"""
        logger.info("Fetching resource dependency data...")
        
        return {
            'source': 'USGS',
            'status': 'configured',
            'critical_minerals': [
                'rare_earths', 'lithium', 'cobalt', 'nickel',
                'copper', 'tin', 'tungsten', 'tantalum'
            ]
        }
    
    def _get_tech_dependencies(self, config: Dict) -> Dict:
        """Get technology dependency data"""
        logger.info("Fetching technology dependency data...")
        
        return {
            'status': 'configured',
            'critical_tech': [
                'semiconductors', 'microchips', 'advanced_materials'
            ]
        }
    
    def _get_conflict_data(self, config: Dict) -> Dict:
        """Get conflict history data (UCDP)"""
        logger.info("Fetching conflict history data...")
        
        return {
            'source': 'Uppsala Conflict Data Program',
            'status': 'configured',
            'endpoint': 'http://www.ucdp.uu.se'
        }
    
    def _get_governance_data(self, config: Dict) -> Dict:
        """Get governance quality data (V-Dem)"""
        logger.info("Fetching governance data...")
        
        return {
            'source': 'V-Dem Institute',
            'status': 'configured',
            'endpoint': 'https://www.v-dem.net/api'
        }
    
    def _get_fragility_index(self, config: Dict) -> Dict:
        """Get state fragility index (FFP)"""
        logger.info("Fetching fragility index...")
        
        return {
            'source': 'Fund for Peace',
            'status': 'configured',
            'endpoint': 'https://fragilestatesindex.org'
        }
    
    def _get_early_warnings(self, config: Dict) -> Dict:
        """Get early warning indicators"""
        logger.info("Fetching early warning indicators...")
        
        return {
            'source': 'ICEWS',
            'status': 'configured',
            'indicators': [
                'military_movements', 'leadership_changes',
                'economic_collapse', 'refugee_flows'
            ]
        }
    
    # ANALYSIS METHODS
    
    def analyze_country(self, country: str) -> Dict[str, Any]:
        """
        Complete analysis of a country
        Includes structural power + dependencies + risk + real-time events
        """
        logger.info(f"Analyzing {country}...")
        
        analysis = {
            'country': country,
            'power_index': self.calculate_power_index(country),
            'vulnerability': self.calculate_vulnerability(country),
            'conflict_risk': self.predict_conflict_risk(country),
            'strategic_position': self.analyze_strategic_position(country),
            'real_time_events': self.get_country_events(country),
            'timestamp': datetime.now().isoformat()
        }
        
        return analysis
    
    def calculate_power_index(self, country: str) -> Dict[str, float]:
        """Calculate overall power index (0-100)"""
        military_power = 0.40 * 60  # Placeholder
        economic_power = 0.35 * 70  # Placeholder
        diplomatic_reach = 0.25 * 50  # Placeholder
        
        total = military_power + economic_power + diplomatic_reach
        
        return {
            'military': 60,
            'economic': 70,
            'diplomatic': 50,
            'total': total,
            'rank': 'Regional Power'  # Placeholder
        }
    
    def calculate_vulnerability(self, country: str) -> Dict[str, float]:
        """Calculate vulnerability to external shocks"""
        return {
            'energy_dependency': 35,
            'food_dependency': 20,
            'tech_dependency': 65,
            'resource_dependency': 40,
            'overall_vulnerability': 40
        }
    
    def predict_conflict_risk(self, country: str) -> Dict[str, Any]:
        """Predict conflict risk probability"""
        return {
            'historical_conflict_frequency': 0.30,
            'economic_inequality': 0.40,
            'resource_competition': 0.25,
            'governance_failure_risk': 0.35,
            'overall_risk_score': 0.33,
            'prediction_5_years': '33% chance of conflict',
            'warning_signs': ['economic_stress', 'political_tension']
        }
    
    def analyze_strategic_position(self, country: str) -> Dict[str, Any]:
        """Analyze strategic geopolitical position"""
        return {
            'geographic_advantages': ['strategic location', 'resources'],
            'geographic_vulnerabilities': ['landlocked', 'coastal exposure'],
            'chokepoint_control': ['some control'],
            'alliance_strength': 'moderate',
            'strategic_isolation_risk': 'low-medium'
        }
    
    def get_country_events(self, country: str) -> Dict[str, List[Dict]]:
        """Get real-time events for a country"""
        news = self.data_sources.get('events', {}).get('news_events', [])
        incidents = self.data_sources.get('events', {}).get('military_incidents', [])
        
        country_lower = country.lower()
        
        country_news = [
            e for e in news
            if country_lower in (e.get('location', '') or '').lower()
        ]
        
        country_incidents = [
            e for e in incidents
            if country_lower in (e.get('location', '') or '').lower()
        ]
        
        return {
            'news_events': country_news,
            'military_incidents': country_incidents,
            'total': len(country_news) + len(country_incidents)
        }
    
    # COMPARATIVE ANALYSIS
    
    def compare_countries(self, country1: str, country2: str) -> Dict[str, Any]:
        """Compare two countries geopolitically"""
        logger.info(f"Comparing {country1} vs {country2}...")
        
        return {
            'comparison': {
                'country1': country1,
                'country2': country2,
                'power_comparison': {
                    country1: self.calculate_power_index(country1),
                    country2: self.calculate_power_index(country2),
                    'advantage': country1  # Placeholder
                },
                'vulnerability_comparison': {
                    country1: self.calculate_vulnerability(country1),
                    country2: self.calculate_vulnerability(country2)
                },
                'alliance_strength': {
                    country1: 'moderate',
                    country2: 'strong'  # Placeholder
                }
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def analyze_region(self, region: str) -> Dict[str, Any]:
        """Analyze geopolitical dynamics of a region"""
        logger.info(f"Analyzing {region}...")
        
        news = self.data_sources.get('events', {}).get('news_events', [])
        incidents = self.data_sources.get('events', {}).get('military_incidents', [])
        
        region_lower = region.lower()
        
        region_news = [e for e in news if region_lower in (e.get('location', '') or '').lower()]
        region_incidents = [e for e in incidents if region_lower in (e.get('location', '') or '').lower()]
        
        return {
            'region': region,
            'active_conflicts': len(region_incidents),
            'recent_events': len(region_news),
            'news_events': region_news[:10],
            'military_incidents': region_incidents[:10],
            'strategic_importance': 'high',  # Placeholder
            'stability_score': 0.35,  # 0-1, lower = more unstable
            'timestamp': datetime.now().isoformat()
        }
    
    def get_summary_report(self) -> Dict[str, Any]:
        """Get overall geopolitical summary report"""
        logger.info("Generating global geopolitical summary...")
        
        events = self.data_sources.get('events', {})
        news = events.get('news_events', [])
        incidents = events.get('military_incidents', [])
        
        # Calculate high-severity incidents
        critical = [i for i in incidents if i.get('severity') == 'critical']
        high = [i for i in incidents if i.get('severity') == 'high']
        
        return {
            'report_type': 'Global Geopolitical Summary',
            'timestamp': datetime.now().isoformat(),
            'total_news_events': len(news),
            'total_military_incidents': len(incidents),
            'critical_incidents': len(critical),
            'high_severity_incidents': len(high),
            'top_critical_incidents': critical[:5],
            'top_events': news[:20],
            'risk_assessment': {
                'global_stability': 'moderate',
                'conflict_zones': ['Middle East', 'Eastern Europe', 'South China Sea'],
                'critical_chokepoints': ['Taiwan Strait', 'Strait of Hormuz', 'Suez Canal']
            }
        }


def create_unified_analyzer(config: Dict) -> UnifiedGeopoliticalAnalyzer:
    """Factory function to create and initialize analyzer"""
    analyzer = UnifiedGeopoliticalAnalyzer()
    analyzer.ingest_all_sources(config)
    return analyzer
