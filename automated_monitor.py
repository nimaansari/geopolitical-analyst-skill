"""
Automated Geopolitical Intelligence Monitor
Continuously monitors multiple conflict zones with live data
Generates updated reports every 6 hours
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

# Load monitoring topics from config file
import json

CONFIG_FILE = "monitor_config.json"

def load_watch_list():
    """Load topics to monitor from config file"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                watch_list = {}
                for topic_config in config.get("monitor_topics", []):
                    topic = topic_config.get("topic")
                    watch_list[topic] = {
                        "keywords": topic_config.get("keywords"),
                        "depth": topic_config.get("depth", "FULL")
                    }
                logger.info(f"Loaded {len(watch_list)} topics from {CONFIG_FILE}")
                return watch_list
        except Exception as e:
            logger.warning(f"Failed to load {CONFIG_FILE}: {e}")
    
    # Fallback default
    logger.info("Using default watch list")
    return {
        "Gaza": {"keywords": ["Gaza", "Palestine", "Israel", "humanitarian crisis"], "depth": "FULL"},
        "Ukraine": {"keywords": ["Ukraine", "Russia", "Kyiv", "military", "NATO"], "depth": "FULL"},
        "Iran-Israel": {"keywords": ["Iran", "Israel", "nuclear", "Middle East", "missiles"], "depth": "FULL"},
    }

WATCH_LIST = load_watch_list()


class GeopoliticalMonitor:
    """
    Continuous monitor for multiple geopolitical situations
    """
    
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        self.reports = {}
        self.last_update = {}
    
    def analyze_all(self):
        """
        Run analysis on all watched situations
        """
        timestamp = datetime.utcnow().isoformat()
        logger.info(f"Starting monitoring cycle: {timestamp}")
        
        results = {
            "timestamp": timestamp,
            "situations": {}
        }
        
        for situation, config in WATCH_LIST.items():
            logger.info(f"Analyzing {situation}...")
            
            try:
                result = run_analysis(
                    country=situation,
                    keywords=config["keywords"],
                    depth=config["depth"]
                )
                
                results["situations"][situation] = {
                    "status": "success",
                    "analysis": result
                }
                
                self.last_update[situation] = timestamp
                logger.info(f"✓ {situation} analyzed")
                
            except Exception as e:
                logger.error(f"✗ {situation} failed: {str(e)}")
                results["situations"][situation] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return results
    
    def save_report(self, results):
        """
        Save comprehensive report
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/geopolitical_intelligence_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"Report saved: {filename}")
        return filename
    
    def generate_summary(self, results):
        """
        Generate executive summary
        """
        summary = {
            "timestamp": results["timestamp"],
            "total_situations": len(WATCH_LIST),
            "successful": sum(1 for s in results["situations"].values() if s["status"] == "success"),
            "failed": sum(1 for s in results["situations"].values() if s["status"] == "error"),
            "alerts": []
        }
        
        # Identify high-risk situations
        for situation, data in results["situations"].items():
            if data["status"] == "success":
                analysis = data.get("analysis", {}).get("analysis", {})
                risk = analysis.get("metadata", {}).get("risk_level", "UNKNOWN")
                
                if risk == "CRITICAL" or risk == "HIGH":
                    summary["alerts"].append({
                        "situation": situation,
                        "risk_level": risk,
                        "timestamp": results["timestamp"]
                    })
        
        return summary
    
    def run_continuous(self, interval_hours=6):
        """
        Run monitoring loop continuously
        """
        import time
        import schedule
        
        def job():
            logger.info("=" * 80)
            results = self.analyze_all()
            report_file = self.save_report(results)
            summary = self.generate_summary(results)
            
            logger.info(f"Summary: {summary['successful']}/{summary['total_situations']} successful")
            if summary["alerts"]:
                logger.warning(f"🚨 ALERTS: {len(summary['alerts'])} situations at HIGH/CRITICAL risk")
                for alert in summary["alerts"]:
                    logger.warning(f"   - {alert['situation']}: {alert['risk_level']}")
            
            logger.info("=" * 80)
        
        # Schedule the job
        schedule.every(interval_hours).hours.do(job)
        
        logger.info(f"Monitor started. Running analysis every {interval_hours} hours.")
        logger.info(f"Watching: {', '.join(WATCH_LIST.keys())}")
        
        # Run immediately
        job()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    def run_once(self):
        """
        Run analysis once (for testing)
        """
        logger.info("Running single monitoring cycle...")
        results = self.analyze_all()
        report_file = self.save_report(results)
        summary = self.generate_summary(results)
        
        print("\n" + "=" * 80)
        print("GEOPOLITICAL INTELLIGENCE MONITOR - SUMMARY")
        print("=" * 80)
        print(f"Timestamp: {results['timestamp']}")
        print(f"Situations analyzed: {summary['total_situations']}")
        print(f"Successful: {summary['successful']}")
        print(f"Failed: {summary['failed']}")
        
        if summary["alerts"]:
            print("\n🚨 HIGH-RISK ALERTS:")
            for alert in summary["alerts"]:
                print(f"   {alert['situation']}: {alert['risk_level']}")
        
        print(f"\nFull report: {report_file}")
        print("=" * 80 + "\n")
        
        return results


def main():
    """
    Main entry point
    """
    import sys
    
    monitor = GeopoliticalMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == "continuous":
        # Run continuously
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 6
        monitor.run_continuous(interval_hours=interval)
    else:
        # Run once
        monitor.run_once()


if __name__ == "__main__":
    main()
