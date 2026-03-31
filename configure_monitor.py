"""
Interactive Configuration Tool for Geopolitical Monitor
Allows easy setup of which topics to monitor
"""

import json
import os

CONFIG_FILE = "monitor_config.json"


def load_config():
    """Load current configuration"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    
    # Default config
    return {
        "description": "Dynamic monitoring configuration",
        "monitor_topics": [],
        "run_interval_hours": 6,
        "save_reports": True,
        "alert_on_risk_level": "HIGH"
    }


def save_config(config):
    """Save configuration to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"✓ Configuration saved to {CONFIG_FILE}")


def show_topics(config):
    """Show currently monitored topics"""
    topics = config.get("monitor_topics", [])
    
    if not topics:
        print("\n❌ No topics currently configured\n")
        return
    
    print("\n📊 Currently Monitored Topics:")
    print("=" * 80)
    
    for i, topic in enumerate(topics, 1):
        name = topic.get("topic")
        depth = topic.get("depth", "FULL")
        keywords = topic.get("keywords", [])
        print(f"\n{i}. {name}")
        print(f"   Depth: {depth}")
        print(f"   Keywords: {', '.join(keywords)}")
    
    print("\n" + "=" * 80)


def add_topic(config):
    """Add a new topic to monitor"""
    print("\n➕ Add New Topic to Monitor")
    print("=" * 80)
    
    topic = input("Topic name (e.g., 'Gaza', 'Ukraine'): ").strip()
    if not topic:
        print("❌ Topic name required")
        return
    
    # Ask for keywords
    print("\nKeywords (comma-separated):")
    print("Examples: 'Gaza, Palestine, Israel, humanitarian crisis'")
    keywords_input = input("Keywords: ").strip()
    keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
    
    if not keywords:
        keywords = [topic]  # Use topic name as fallback
    
    # Ask for depth
    print("\nAnalysis Depth:")
    print("  FLASH - Quick (90 seconds)")
    print("  BRIEF - Medium (5 minutes)")
    print("  FULL  - Comprehensive (15 minutes)")
    depth = input("Choose depth [FULL]: ").strip().upper()
    
    if depth not in ["FLASH", "BRIEF", "FULL"]:
        depth = "FULL"
    
    # Add to config
    new_topic = {
        "topic": topic,
        "keywords": keywords,
        "depth": depth
    }
    
    config["monitor_topics"].append(new_topic)
    save_config(config)
    
    print(f"\n✓ Added '{topic}' to monitoring")


def remove_topic(config):
    """Remove a topic from monitoring"""
    topics = config.get("monitor_topics", [])
    
    if not topics:
        print("❌ No topics to remove")
        return
    
    print("\n➖ Remove Topic from Monitoring")
    print("=" * 80)
    
    for i, topic in enumerate(topics, 1):
        print(f"{i}. {topic.get('topic')}")
    
    try:
        choice = int(input("\nSelect number to remove (or 0 to cancel): "))
        if 0 < choice <= len(topics):
            removed = config["monitor_topics"].pop(choice - 1)
            save_config(config)
            print(f"\n✓ Removed '{removed.get('topic')}' from monitoring")
        elif choice != 0:
            print("❌ Invalid choice")
    except ValueError:
        print("❌ Invalid input")


def set_interval(config):
    """Set monitoring interval"""
    print("\n⏱️ Set Monitoring Interval")
    print("=" * 80)
    
    current = config.get("run_interval_hours", 6)
    print(f"Current interval: {current} hours")
    
    try:
        new_interval = int(input("New interval in hours (e.g., 6): "))
        if new_interval > 0:
            config["run_interval_hours"] = new_interval
            save_config(config)
            print(f"✓ Interval set to {new_interval} hours")
        else:
            print("❌ Interval must be > 0")
    except ValueError:
        print("❌ Invalid input")


def set_alert_level(config):
    """Set risk level for alerts"""
    print("\n🚨 Set Alert Level")
    print("=" * 80)
    
    current = config.get("alert_on_risk_level", "HIGH")
    print(f"Current alert level: {current}")
    print("\nOptions: CRITICAL, HIGH, MEDIUM, LOW")
    
    new_level = input("New alert level: ").strip().upper()
    if new_level in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        config["alert_on_risk_level"] = new_level
        save_config(config)
        print(f"✓ Alert level set to {new_level}")
    else:
        print("❌ Invalid level")


def show_menu():
    """Show main menu"""
    print("\n" + "=" * 80)
    print("GEOPOLITICAL MONITOR - CONFIGURATION TOOL")
    print("=" * 80)
    print("\n1. View current topics")
    print("2. Add new topic to monitor")
    print("3. Remove topic from monitor")
    print("4. Set monitoring interval")
    print("5. Set alert level")
    print("6. Show current config (JSON)")
    print("7. Start monitoring")
    print("8. Start interactive analyzer")
    print("9. Exit")
    print()


def show_json_config(config):
    """Show full JSON configuration"""
    print("\n" + "=" * 80)
    print("CURRENT CONFIGURATION (JSON)")
    print("=" * 80)
    print(json.dumps(config, indent=2))
    print("=" * 80)


def main():
    """Main interactive configuration loop"""
    
    while True:
        config = load_config()
        show_menu()
        
        choice = input("Select option (1-9): ").strip()
        
        if choice == "1":
            show_topics(config)
        
        elif choice == "2":
            add_topic(config)
        
        elif choice == "3":
            remove_topic(config)
        
        elif choice == "4":
            set_interval(config)
        
        elif choice == "5":
            set_alert_level(config)
        
        elif choice == "6":
            show_json_config(config)
        
        elif choice == "7":
            print("\n🚀 Starting monitoring...")
            print("Run: ./monitor_setup.sh continuous 6")
            break
        
        elif choice == "8":
            print("\n🚀 Starting interactive analyzer...")
            print("Run: python3 interactive_monitor.py")
            break
        
        elif choice == "9":
            print("\nGoodbye.")
            break
        
        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main()
