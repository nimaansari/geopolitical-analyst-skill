"""
Interactive Geopolitical Intelligence Monitor
Analyzes whatever topics the user/AI asks about
Flexible, request-driven analysis with live data
"""

import json
import os
from datetime import datetime
from geopolitical_analyst_agent import run_analysis
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class InteractiveAnalyzer:
    """
    Request-driven analyzer
    Analyzes whatever topic/region is requested
    No hardcoded watch list — flexible by design
    """
    
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        self.analysis_history = []
    
    def analyze_topic(self, topic, keywords=None, depth="FULL"):
        """
        Analyze any geopolitical topic requested
        
        Args:
            topic: Region/situation name ("Gaza", "Ukraine", "Iran-Israel", etc.)
            keywords: Search keywords (auto-generated if not provided)
            depth: "FLASH" (quick), "BRIEF" (medium), "FULL" (comprehensive)
        
        Returns:
            Analysis result with live data
        """
        
        logger.info(f"Analyzing: {topic} (depth: {depth})")
        
        # Auto-generate keywords if not provided
        if not keywords:
            keywords = self._generate_keywords(topic)
            logger.info(f"Auto-generated keywords: {keywords}")
        
        try:
            result = run_analysis(
                country=topic,
                keywords=keywords,
                depth=depth
            )
            
            logger.info(f"✓ Analysis complete for {topic}")
            
            # Store in history
            self.analysis_history.append({
                "topic": topic,
                "timestamp": datetime.utcnow().isoformat(),
                "depth": depth,
                "keywords": keywords
            })
            
            return result
            
        except Exception as e:
            logger.error(f"✗ Failed to analyze {topic}: {str(e)}")
            return {"error": str(e), "topic": topic}
    
    def analyze_multiple(self, topics_config):
        """
        Analyze multiple topics in one batch
        
        Args:
            topics_config: List of dicts with topic, keywords, depth
            Example:
            [
                {"topic": "Gaza", "keywords": ["Gaza", "Palestine", "Israel"], "depth": "FULL"},
                {"topic": "Ukraine", "keywords": ["Ukraine", "Russia", "military"], "depth": "BRIEF"}
            ]
        """
        
        timestamp = datetime.utcnow().isoformat()
        results = {
            "timestamp": timestamp,
            "analyses": {}
        }
        
        logger.info(f"Starting batch analysis: {len(topics_config)} topics")
        
        for config in topics_config:
            topic = config.get("topic")
            keywords = config.get("keywords")
            depth = config.get("depth", "FULL")
            
            logger.info(f"Analyzing {topic}...")
            
            result = self.analyze_topic(topic, keywords, depth)
            results["analyses"][topic] = result
        
        return results
    
    def _generate_keywords(self, topic):
        """
        Auto-generate search keywords from topic name
        """
        
        keyword_map = {
            # Exact matches
            "Gaza": ["Gaza", "Palestine", "Israel", "humanitarian crisis"],
            "Palestine": ["Palestine", "Gaza", "West Bank", "Israel"],
            "Israel": ["Israel", "Gaza", "Palestine", "military"],
            "Ukraine": ["Ukraine", "Russia", "Kyiv", "military", "NATO"],
            "Russia": ["Russia", "military", "sanctions", "conflict"],
            "Iran": ["Iran", "nuclear", "IAEA", "enrichment", "sanctions"],
            "Iran-Israel": ["Iran", "Israel", "nuclear", "Middle East", "missiles"],
            "Israel-Iran": ["Israel", "Iran", "nuclear", "Middle East", "missiles"],
            "China": ["China", "military", "regional", "strategic", "tensions"],
            "Taiwan": ["Taiwan", "China", "strait", "military", "USA", "independence"],
            "Syria": ["Syria", "Assad", "Russia", "Turkey", "civil war", "refugees"],
            "Yemen": ["Yemen", "Houthis", "Saudi", "humanitarian", "conflict", "blockade"],
            "Myanmar": ["Myanmar", "military", "junta", "ethnic", "conflict", "Rohingya"],
            "Sudan": ["Sudan", "RSF", "SAF", "humanitarian", "war", "refugees"],
            "Somalia": ["Somalia", "Al-Shabaab", "military", "conflict", "humanitarian"],
            "DRC": ["DRC", "Congo", "M23", "conflict", "humanitarian", "military"],
            "Nagorno-Karabakh": ["Azerbaijan", "Armenia", "Nagorno-Karabakh", "conflict"],
            "Kashmir": ["Kashmir", "India", "Pakistan", "military", "border", "tensions"],
            "South China Sea": ["South China Sea", "China", "Philippines", "Vietnam", "maritime"],
            "Venezuela": ["Venezuela", "Maduro", "humanitarian", "sanctions", "refugees"],
            "Mexico": ["Mexico", "drug cartels", "violence", "military", "humanitarian"],
            "Colombia": ["Colombia", "ELN", "FARC", "drug trafficking", "conflict"],
        }
        
        # Try exact match first
        if topic in keyword_map:
            return keyword_map[topic]
        
        # Try case-insensitive match
        for key, value in keyword_map.items():
            if key.lower() == topic.lower():
                return value
        
        # Fallback: use topic itself as keywords
        return [topic, "conflict", "military", "humanitarian", "crisis"]
    
    def save_results(self, results):
        """
        Save analysis results to JSON file
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/analysis_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"Results saved: {filename}")
        return filename
    
    def interactive_mode(self):
        """
        Interactive command-line mode
        Ask user what to analyze
        """
        print("\n" + "=" * 80)
        print("GEOPOLITICAL INTELLIGENCE ANALYZER - INTERACTIVE MODE")
        print("=" * 80)
        print("\nWhat geopolitical situation do you want to analyze?")
        print("(Type 'help' for examples, 'batch' for multiple, 'quit' to exit)\n")
        
        while True:
            try:
                user_input = input("📍 Analyze: ").strip()
                
                if user_input.lower() == "quit":
                    print("Goodbye.")
                    break
                
                if user_input.lower() == "help":
                    print("\nExamples:")
                    print("  Gaza")
                    print("  Ukraine")
                    print("  Iran-Israel")
                    print("  Taiwan")
                    print("  Syria")
                    print("  Yemen")
                    print("\nYou can also ask:")
                    print("  'Gaza|BRIEF'  (topic|depth)")
                    print("  'Taiwan|FLASH'")
                    continue
                
                if user_input.lower() == "batch":
                    self._batch_mode()
                    continue
                
                # Parse input (format: "topic|depth" or just "topic")
                parts = user_input.split("|")
                topic = parts[0].strip()
                depth = parts[1].strip().upper() if len(parts) > 1 else "FULL"
                
                if depth not in ["FLASH", "BRIEF", "FULL"]:
                    print(f"Invalid depth '{depth}'. Use FLASH, BRIEF, or FULL.")
                    continue
                
                print(f"\n🔍 Analyzing {topic} ({depth})...\n")
                
                result = self.analyze_topic(topic, depth=depth)
                
                # Save results
                self.save_results({"topic": topic, "depth": depth, "analysis": result})
                
                # Show summary
                if "error" not in result:
                    print(f"✓ Analysis complete")
                    if "analysis" in result:
                        analysis = result["analysis"]
                        print(f"   Risk Level: {analysis.get('metadata', {}).get('risk_level', 'Unknown')}")
                        if "step_9_scenarios" in analysis:
                            scenarios = analysis["step_9_scenarios"]
                            print(f"   Scenarios: {len(scenarios)} generated")
                else:
                    print(f"✗ Error: {result['error']}")
                
                print()
                
            except KeyboardInterrupt:
                print("\n\nGoodbye.")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def _batch_mode(self):
        """
        Batch analysis mode
        Analyze multiple topics
        """
        print("\nBATCH MODE: Analyze multiple situations")
        print("(Enter topics separated by commas, or 'cancel' to go back)\n")
        
        user_input = input("Topics (comma-separated): ").strip()
        
        if user_input.lower() == "cancel":
            return
        
        topics = [t.strip() for t in user_input.split(",")]
        
        print(f"\nAnalyzing {len(topics)} topics...")
        
        config = [{"topic": t} for t in topics]
        results = self.analyze_multiple(config)
        
        # Save
        self.save_results(results)
        
        print(f"✓ Batch analysis complete. {len(results['analyses'])} topics analyzed.\n")


def main():
    """
    Main entry point
    """
    import sys
    
    analyzer = InteractiveAnalyzer()
    
    # Command-line arguments
    if len(sys.argv) > 1:
        topic = sys.argv[1]
        keywords = sys.argv[2:] if len(sys.argv) > 2 else None
        depth = "FULL"
        
        # Check if last arg is depth level
        if keywords and keywords[-1].upper() in ["FLASH", "BRIEF", "FULL"]:
            depth = keywords.pop().upper()
        
        print(f"Analyzing {topic}...")
        result = analyzer.analyze_topic(topic, keywords, depth)
        analyzer.save_results({"topic": topic, "analysis": result})
        
        print("\n" + "=" * 80)
        print(f"Analysis of {topic} complete")
        print("=" * 80)
        
    else:
        # Interactive mode if no args
        analyzer.interactive_mode()


if __name__ == "__main__":
    main()
