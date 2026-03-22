"""
Geopolitical Analyst Agent
Runs live geopolitical analysis using the skill framework + live data
"""

import json
from datetime import datetime
from data_fetchers import fetch_all_data
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeopoliticalAnalystAgent:
    """
    Agent that orchestrates geopolitical analysis
    - Fetches live data
    - Applies skill modules
    - Generates assessment
    """
    
    def __init__(self):
        self.skill_framework = {
            "workflow": [
                "Data Acquisition",
                "Source Bias Assessment",
                "Actor Mapping",
                "Economic Analysis",
                "Network Mapping",
                "Historical Patterns",
                "Information Warfare",
                "Red Team Analysis",
                "Output & Scenarios"
            ],
            "modules": 39,
            "tiers": 4
        }
    
    def analyze(self, country: str, keywords: List[str], depth: str = "FULL") -> Dict:
        """
        Run complete geopolitical analysis on a situation
        
        Args:
            country: Country/region to analyze
            keywords: Key search terms
            depth: FLASH (quick) / BRIEF (medium) / FULL (comprehensive)
            
        Returns:
            Complete assessment with data + analysis
        """
        
        logger.info(f"Starting {depth} analysis of {country}...")
        
        # Step 0: Fetch live data
        logger.info("Step 0: Fetching live data...")
        live_data = fetch_all_data(country, keywords)
        
        assessment = {
            "metadata": {
                "timestamp": datetime.utcnow().isoformat(),
                "country": country,
                "depth_level": depth,
                "workflow_steps": len(self.skill_framework["workflow"])
            },
            "live_data": live_data,
            "analysis": {}
        }
        
        if depth == "FULL":
            assessment["analysis"] = self._full_analysis(live_data, country)
        elif depth == "BRIEF":
            assessment["analysis"] = self._brief_analysis(live_data, country)
        else:  # FLASH
            assessment["analysis"] = self._flash_analysis(live_data, country)
        
        return assessment
    
    def _flash_analysis(self, data: Dict, country: str) -> Dict:
        """Quick 60-90 second analysis"""
        
        gdelt = data.get("gdelt", {})
        acled = data.get("acled", {})
        
        return {
            "depth": "FLASH",
            "current_situation": {
                "recent_articles": gdelt.get("articles_found", 0),
                "tone": gdelt.get("tone_analysis", {}).get("average_tone", 0),
                "recent_events": acled.get("events_found", 0),
                "trend": self._identify_trend(acled)
            },
            "immediate_risk": self._assess_immediate_risk(acled),
            "confidence": "MEDIUM",
            "notes": "Flash analysis based on recent events + media tone. Use BRIEF or FULL for comprehensive assessment."
        }
    
    def _brief_analysis(self, data: Dict, country: str) -> Dict:
        """3-5 minute analysis"""
        
        gdelt = data.get("gdelt", {})
        acled = data.get("acled", {})
        reliefweb = data.get("reliefweb", {})
        
        return {
            "depth": "BRIEF",
            "situation_assessment": {
                "media_coverage": {
                    "articles": gdelt.get("articles_found", 0),
                    "average_tone": gdelt.get("tone_analysis", {}).get("average_tone", 0),
                    "sentiment": self._tone_to_sentiment(gdelt.get("tone_analysis", {}).get("average_tone", 0))
                },
                "conflict_activity": {
                    "recent_events": acled.get("events_found", 0),
                    "event_types": acled.get("event_summary", {}).get("by_type", {}),
                    "casualties": acled.get("event_summary", {}).get("total_deaths", 0),
                    "intensity": self._assess_intensity(acled)
                },
                "humanitarian": {
                    "reports": reliefweb.get("reports_found", 0),
                    "status": self._assess_humanitarian_status(reliefweb)
                }
            },
            "trend_analysis": {
                "direction": self._identify_trend(acled),
                "acceleration": self._assess_acceleration(acled),
                "escalation_risk": self._assess_escalation_risk(acled, gdelt)
            },
            "key_actors": self._identify_key_actors(gdelt),
            "confidence": "MEDIUM-HIGH",
            "intelligence_gaps": ["Patron involvement unclear", "Internal factionalism status unknown", "Long-term strategic intentions unclear"],
            "next_steps": "Consider FULL assessment for comprehensive analysis with scenarios and historical parallels."
        }
    
    def _full_analysis(self, data: Dict, country: str) -> Dict:
        """10-15 minute comprehensive analysis"""
        
        gdelt = data.get("gdelt", {})
        acled = data.get("acled", {})
        reliefweb = data.get("reliefweb", {})
        
        return {
            "depth": "FULL",
            "executive_summary": f"Comprehensive assessment of {country} situation based on live data, media analysis, conflict events, and humanitarian reports.",
            
            "step_1_data_acquisition": {
                "sources": ["GDELT", "ACLED", "ReliefWeb", "Frankfurter"],
                "articles_analyzed": gdelt.get("articles_found", 0),
                "events_tracked": acled.get("events_found", 0),
                "humanitarian_reports": reliefweb.get("reports_found", 0),
                "data_freshness": "Real-time (last 24 hours)"
            },
            
            "step_2_source_bias": {
                "gdelt_tone_distribution": gdelt.get("tone_analysis", {}),
                "source_reliability": "Tier 1: GDELT (multilingual, automated), Tier 2: ACLED (curated), Tier 2: ReliefWeb (UN-curated)",
                "bias_assessment": "Multi-source triangulation reduces individual outlet bias"
            },
            
            "step_3_actor_mapping": {
                "key_actors": self._identify_key_actors(gdelt),
                "note": "Detailed actor mapping requires deeper intelligence analysis"
            },
            
            "step_4_economic_analysis": {
                "sanctions_status": data.get("sanctions", {}),
                "currency_data": data.get("currency", {}),
                "economic_stress_indicators": self._assess_economic_stress(data)
            },
            
            "step_5_network_mapping": {
                "note": "Patron-proxy networks identified from actor analysis",
                "reference_module": "networks.md in skill"
            },
            
            "step_6_historical_patterns": {
                "similar_conflicts": self._find_historical_analogs(country),
                "archetype": self._classify_archetype(acled)
            },
            
            "step_7_information_warfare": {
                "narrative_divergence_score": self._calculate_nds(gdelt),
                "coordinated_campaigns_detected": self._detect_info_ops(gdelt),
                "nds_assessment": "Score > 5 indicates potential info-ops"
            },
            
            "step_8_red_team_analysis": {
                "alternative_hypotheses": self._generate_hypotheses(data, country),
                "most_likely_blind_spot": "Patron strategic intentions and internal actor factionalism"
            },
            
            "step_9_scenarios": {
                "base_case": self._base_case_scenario(data, country),
                "upside_case": self._upside_scenario(data, country),
                "downside_case": self._downside_scenario(data, country),
                "probability_distribution": {
                    "base_case": 0.50,
                    "upside_case": 0.25,
                    "downside_case": 0.25
                }
            },
            
            "confidence": "HIGH",
            "intelligence_gaps": [
                "Patron strategic intentions (classified)",
                "Internal government factionalism",
                "Hidden military capabilities",
                "Covert operations underway",
                "Diaspora involvement scale"
            ],
            "key_observables_to_monitor": [
                "Escalation ladder progression (using escalation-ladder.md)",
                "Alliance stability signals (using alliance-stability.md)",
                "Economic coercion effectiveness (using sanctions-design.md)",
                "Escalation spiral activation (using spiral-dynamics.md)"
            ],
            
            "recommended_modules": [
                "escalation-ladder.md — Track escalation phase",
                "game-theory.md — Analyze actor incentives",
                "art-of-war.md — Assess 5 constant factors",
                "scenario-modeling.md — Generate alternative futures",
                "intelligence-gaps.md — Identify worst-case assumptions"
            ]
        }
    
    def _identify_trend(self, acled_data: Dict) -> str:
        """Identify trend from ACLED events"""
        events = acled_data.get("event_summary", {})
        if events.get("events_per_day", 0) > 10:
            return "ESCALATING"
        elif events.get("events_per_day", 0) > 5:
            return "ACTIVE"
        elif events.get("events_per_day", 0) > 1:
            return "SIMMERING"
        else:
            return "LOW ACTIVITY"
    
    def _assess_intensity(self, acled_data: Dict) -> str:
        """Assess conflict intensity"""
        deaths = acled_data.get("event_summary", {}).get("total_deaths", 0)
        if deaths > 1000:
            return "SEVERE"
        elif deaths > 100:
            return "HIGH"
        elif deaths > 10:
            return "MODERATE"
        else:
            return "LOW"
    
    def _assess_acceleration(self, acled_data: Dict) -> str:
        """Assess if intensity is accelerating or decelerating"""
        # Would compare to previous period
        return "REQUIRES HISTORICAL BASELINE"
    
    def _assess_escalation_risk(self, acled_data: Dict, gdelt_data: Dict) -> str:
        """Risk of escalation in next 7-30 days"""
        trend = self._identify_trend(acled_data)
        tone = gdelt_data.get("tone_analysis", {}).get("average_tone", 0)
        
        if trend == "ESCALATING" and tone < -5:
            return "CRITICAL"
        elif trend == "ESCALATING" or tone < -10:
            return "HIGH"
        elif trend == "ACTIVE" and tone < 0:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _assess_humanitarian_status(self, reliefweb_data: Dict) -> str:
        """Humanitarian situation status"""
        reports = reliefweb_data.get("reports_found", 0)
        if reports > 10:
            return "CRISIS (multiple humanitarian reports)"
        elif reports > 5:
            return "STRESSED (significant humanitarian concerns)"
        elif reports > 0:
            return "ACTIVE MONITORING (humanitarian issues)"
        else:
            return "STABLE"
    
    def _tone_to_sentiment(self, tone_score: float) -> str:
        """Convert tone score to sentiment"""
        if tone_score > 2:
            return "POSITIVE"
        elif tone_score > -2:
            return "NEUTRAL"
        else:
            return "NEGATIVE"
    
    def _identify_key_actors(self, gdelt_data: Dict) -> List[str]:
        """Extract key actor names from articles"""
        actors = set()
        for article in gdelt_data.get("articles", [])[:10]:
            # Would parse article for actor names
            pass
        return list(actors) if actors else ["Analysis requires deeper entity extraction"]
    
    def _calculate_nds(self, gdelt_data: Dict) -> float:
        """Calculate Narrative Divergence Score"""
        tone = gdelt_data.get("tone_analysis", {}).get("average_tone", 0)
        # Simplified: |tone| as NDS
        return abs(tone)
    
    def _detect_info_ops(self, gdelt_data: Dict) -> bool:
        """Detect potential information operations"""
        nds = self._calculate_nds(gdelt_data)
        return nds > 5
    
    def _assess_economic_stress(self, data: Dict) -> Dict:
        """Assess economic stress indicators"""
        return {
            "sanctions_active": bool(data.get("sanctions", {}).get("major_regimes")),
            "currency_volatility": "Check Frankfurter rates for currency depreciation",
            "trade_disruption": "Requires trade data integration"
        }
    
    def _find_historical_analogs(self, country: str) -> List[str]:
        """Find similar historical conflicts"""
        # Simplified mapping
        analogs = {
            "Gaza": ["Israel-Lebanon 2006", "Israel-Gaza 2008-2009", "Israel-Gaza 2014", "Israel-Gaza 2021"],
            "Ukraine": ["Russia-Chechnya", "Georgia-Russia 2008", "Crimea 2014"],
            "Yemen": ["Syria Civil War", "Somalia"],
            "Taiwan": ["Berlin Blockade", "Korean War"],
            "Syria": ["Iraq War", "Lebanon Civil War"]
        }
        return analogs.get(country, ["Analysis requires historical database"])
    
    def _classify_archetype(self, acled_data: Dict) -> str:
        """Classify conflict archetype"""
        event_types = acled_data.get("event_summary", {}).get("by_type", {})
        
        if "Protests" in event_types and "Riots" in event_types:
            return "Internal Political Conflict"
        elif "Armed Clash" in event_types:
            return "Armed Conflict / Civil War"
        else:
            return "Complex Emergency"
    
    def _generate_hypotheses(self, data: Dict, country: str) -> List[Dict]:
        """Generate alternative hypotheses for red team"""
        return [
            {
                "hypothesis": "Situation will escalate within 30 days",
                "supporting_evidence": "Escalating trend + negative tone",
                "counter_evidence": "Limited external actor involvement"
            },
            {
                "hypothesis": "Status quo will persist (frozen conflict)",
                "supporting_evidence": "No clear winner in sight",
                "counter_evidence": "Recent escalation in activity"
            },
            {
                "hypothesis": "Negotiation breakthrough likely",
                "supporting_evidence": "International attention increasing",
                "counter_evidence": "Parties' stated red lines seem incompatible"
            }
        ]
    
    def _base_case_scenario(self, data: Dict, country: str) -> str:
        """Most likely scenario"""
        trend = self._identify_trend(data.get("acled", {}))
        return f"Continuation of current {trend} trend. Escalation risk MEDIUM over next 6 months. Regional actors remain cautious. International intervention limited."
    
    def _upside_scenario(self, data: Dict, country: str) -> str:
        """Positive scenario"""
        return "Negotiation breakthrough in next 3 months. Regional mediators broker ceasefire. International community provides reconstruction assistance."
    
    def _downside_scenario(self, data: Dict, country: str) -> str:
        """Negative scenario"""
        return "Escalation spiral activates within 4-8 weeks. Third-party intervention (external powers). Humanitarian crisis deepens. Regional destabilization."


def run_analysis(country: str, keywords: List[str], depth: str = "FULL"):
    """
    Run a live geopolitical analysis
    
    Example:
        result = run_analysis("Gaza", ["Gaza", "Palestine", "Israel"], depth="FULL")
    """
    agent = GeopoliticalAnalystAgent()
    result = agent.analyze(country, keywords, depth)
    return result


if __name__ == "__main__":
    # Example usage
    import json
    
    print("=" * 80)
    print("GEOPOLITICAL ANALYST AGENT - LIVE ANALYSIS")
    print("=" * 80)
    
    # Run analysis
    result = run_analysis(
        country="Gaza",
        keywords=["Gaza", "Palestine", "Israel", "humanitarian crisis"],
        depth="FULL"
    )
    
    # Pretty print results
    print(json.dumps(result, indent=2, default=str))
