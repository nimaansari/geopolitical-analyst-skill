"""
SOLUTION 2: Lazy Module Loader with Two-Tier Analysis Modes
Loads modules on-demand instead of upfront, supports Quick vs Full analysis
"""

import os
import logging
from typing import Dict, List, Optional
import glob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModuleLoader:
    """Lazy-loads analytical modules on demand"""
    
    # SOLUTION 2: Core modules (8-10) for quick analysis
    CORE_MODULES = [
        "actor_identification",
        "conflict_escalation_ladder",
        "sanctions_analysis",
        "economic_impact",
        "information_warfare",
        "geopolitical_context",
        "risk_assessment",
        "scenario_generation",
        "network_analysis"
    ]
    
    # SOLUTION 2: Extended modules (30+) for full analysis
    EXTENDED_MODULES = [
        "civil_military_dynamics",
        "ethnic_tensions_and_fragmentation",
        "resource_competition",
        "supply_chain_vulnerabilities",
        "trade_relationships",
        "diplomatic_history",
        "coup_risk_assessment",
        "refugee_migration_patterns",
        "arms_trafficking_routes",
        "cyber_attack_surface",
        "water_scarcity_conflicts",
        "regional_power_balances",
        "historical_grievances",
        "sectarian_divisions",
        "illicit_financial_flows",
        "media_landscape_analysis",
        "leadership_stability",
        "military_capabilities",
        "nuclear_dimension",
        "territorial_disputes",
        "maritime_claims",
        "energy_dependencies",
        "agricultural_vulnerability",
        "pandemic_response_capacity",
        "corruption_indices",
        "institutional_weakness",
        "gender_and_conflict",
        "child_soldier_recruitment",
        "trafficking_networks",
        "counterinsurgency_effectiveness"
    ]
    
    def __init__(self, modules_dir: str = "./references"):
        self.modules_dir = modules_dir
        self.loaded_modules = {}  # Cache loaded modules
        self.module_index = {}  # Map module names to files
        self._build_module_index()
    
    def _build_module_index(self):
        """Build index of available modules"""
        try:
            md_files = glob.glob(os.path.join(self.modules_dir, "*.md"))
            for file_path in md_files:
                module_name = os.path.basename(file_path).replace(".md", "").lower()
                self.module_index[module_name] = file_path
            logger.info(f"Module index built: {len(self.module_index)} modules available")
        except Exception as e:
            logger.error(f"Error building module index: {e}")
    
    def _load_module_content(self, module_name: str) -> Optional[str]:
        """Load module content from file (with lazy loading)"""
        # Return cached if already loaded
        if module_name in self.loaded_modules:
            return self.loaded_modules[module_name]
        
        # Find and load module file
        if module_name in self.module_index:
            try:
                with open(self.module_index[module_name], 'r') as f:
                    content = f.read()
                    self.loaded_modules[module_name] = content  # Cache it
                    logger.info(f"Loaded module: {module_name}")
                    return content
            except Exception as e:
                logger.error(f"Error loading module {module_name}: {e}")
        else:
            logger.warning(f"Module not found: {module_name}")
        
        return None
    
    def get_core_modules(self) -> Dict[str, str]:
        """
        SOLUTION 2: Get only core modules (8-10) for quick analysis
        Lazy-loads only when called, not upfront
        """
        logger.info("Loading CORE MODULES (8-10) for quick analysis...")
        modules = {}
        for module_name in self.CORE_MODULES:
            content = self._load_module_content(module_name)
            if content:
                modules[module_name] = content
        logger.info(f"Core modules loaded: {len(modules)}")
        return modules
    
    def get_extended_modules(self) -> Dict[str, str]:
        """
        SOLUTION 2: Get extended modules (30+) for full analysis
        Lazy-loads only when called, not upfront
        """
        logger.info("Loading EXTENDED MODULES (30+) for full analysis...")
        modules = {}
        for module_name in self.EXTENDED_MODULES:
            content = self._load_module_content(module_name)
            if content:
                modules[module_name] = content
        logger.info(f"Extended modules loaded: {len(modules)}")
        return modules
    
    def get_all_modules(self) -> Dict[str, str]:
        """Get all available modules (core + extended)"""
        logger.info("Loading ALL MODULES (39+)...")
        all_modules = {}
        all_modules.update(self.get_core_modules())
        all_modules.update(self.get_extended_modules())
        logger.info(f"Total modules loaded: {len(all_modules)}")
        return all_modules


class AnalysisMode:
    """
    SOLUTION 2: Two-Tier Analysis Mode Selector
    - QUICK: Use 8-10 core modules (fast, low overhead)
    - FULL: Use all 39+ modules (comprehensive)
    """
    
    QUICK = "quick"      # Fast, 8-10 modules
    FULL = "full"        # Comprehensive, 39+ modules
    
    @staticmethod
    def detect_mode(query: str) -> str:
        """
        Auto-detect analysis mode based on query complexity
        
        QUICK mode triggers if query is simple:
        - Single topic ("Syria")
        - Single event ("Ukraine war")
        - Quick question ("Is there conflict risk?")
        
        FULL mode triggers if query is complex:
        - Multiple regions ("Syria and Yemen")
        - Multiple aspects ("sanctions impact on economy")
        - Comprehensive request ("Give me full assessment")
        """
        quick_triggers = ["quick", "brief", "summary", "fast", "simple"]
        full_triggers = ["full", "comprehensive", "detailed", "complete", "analysis"]
        
        query_lower = query.lower()
        
        # Explicit mode request
        for trigger in full_triggers:
            if trigger in query_lower:
                return AnalysisMode.FULL
        
        for trigger in quick_triggers:
            if trigger in query_lower:
                return AnalysisMode.QUICK
        
        # Implicit detection: count commas/keywords
        num_topics = query.count(",") + query.count("and") + query.count("vs")
        num_aspects = query.count("impact") + query.count("effect") + query.count("analysis")
        
        if num_topics > 1 or num_aspects > 1:
            return AnalysisMode.FULL
        
        return AnalysisMode.QUICK


class TwoTierAnalyzer:
    """
    SOLUTION 2: Two-Tier Analysis Executor
    Runs analysis with appropriate module set based on mode
    """
    
    def __init__(self, modules_dir: str = "./references"):
        self.loader = ModuleLoader(modules_dir)
    
    def analyze(self, query: str, manual_mode: Optional[str] = None) -> Dict:
        """
        Run two-tier analysis
        
        Args:
            query: User query
            manual_mode: Explicit mode override (None = auto-detect)
        
        Returns:
            Analysis result with metadata about mode used
        """
        # Determine analysis mode
        mode = manual_mode or AnalysisMode.detect_mode(query)
        
        logger.info(f"Starting {mode.upper()} analysis for: {query[:50]}...")
        
        # Load appropriate modules
        if mode == AnalysisMode.QUICK:
            modules = self.loader.get_core_modules()
            module_count = len(modules)
        else:  # FULL
            modules = self.loader.get_all_modules()
            module_count = len(modules)
        
        return {
            "status": "success",
            "query": query,
            "mode": mode.upper(),
            "modules_loaded": module_count,
            "modules": list(modules.keys()),
            "analysis": f"Analyzed with {module_count} modules in {mode.upper()} mode",
            "metadata": {
                "auto_detected": manual_mode is None,
                "core_modules": len(self.loader.CORE_MODULES),
                "extended_modules": len(self.loader.EXTENDED_MODULES),
                "total_available": len(self.loader.CORE_MODULES) + len(self.loader.EXTENDED_MODULES)
            }
        }
