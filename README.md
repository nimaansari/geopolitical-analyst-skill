# 🌍 Geopolitical Analyst Intelligence Framework

> **Professional-grade geopolitical intelligence at your fingertips.** Systematize conflict analysis. Identify emerging risks. Generate probability-weighted scenarios. Know what you don't know.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/nimaansari/geopolitical-analyst-skill?style=social)](https://github.com/nimaansari/geopolitical-analyst-skill)

---

## 🎯 What It Does

Analyze **any geopolitical situation** with a proven 9-step intelligence framework. Get:

✅ **Live current data** — Real-time articles, conflict events, humanitarian reports, economic indicators  
✅ **39 analytical modules** — Game theory, escalation dynamics, historical analogs, sanctions analysis  
✅ **Multi-perspective scenarios** — Base case, upside, downside, catastrophic with probabilities  
✅ **Intelligence gap identification** — What we know. What we don't. Why it matters.  
✅ **Confidence scoring** — Explicit uncertainty tracking across all assessments  

**Use it when:**
- Analyzing geopolitical events, conflicts, or regional tensions
- Forecasting political outcomes or escalation risk
- Understanding actor incentives and strategic positioning
- Planning around emerging geopolitical crises
- Building situation assessments for decision-makers

---

## 🚀 Quick Start

### Install

```bash
# Clone the repository
git clone https://github.com/nimaansari/geopolitical-analyst-skill.git
cd geopolitical-analyst-skill

# Install dependencies
pip install -r requirements.txt

# Run it
python3 interactive_monitor.py
```

### Use It (3 Ways)

**1. Interactive Mode** — Ask about any topic:
```bash
python3 interactive_monitor.py
# 📍 Analyze: Gaza
# 📍 Analyze: Ukraine|BRIEF
# 📍 Analyze: Taiwan|FLASH
```

**2. Command Line** — Instant analysis:
```bash
python3 interactive_monitor.py "South China Sea" FULL
python3 interactive_monitor.py Ukraine BRIEF
python3 interactive_monitor.py Gaza FLASH
```

**3. Python API** — Integrate into your code:
```python
from geopolitical_analyst_agent import run_analysis

result = run_analysis(
    country="Ukraine",
    keywords=["Ukraine", "Russia", "military"],
    depth="FULL"  # FLASH (90s), BRIEF (5m), FULL (15m)
)

# Access results
print(result["live_data"])  # Current GDELT, ACLED, ReliefWeb
print(result["analysis"])   # Full 9-step analysis
print(result["scenarios"])  # 4 probability-weighted futures
```

---

## 📊 The Framework (9 Steps)

Every analysis follows this proven workflow:

| Step | What It Does | Outputs |
|------|-------------|---------|
| 1️⃣ **Data Acquisition** | Fetch GDELT, ACLED, ReliefWeb, currency data | Live articles, events, humanitarian status |
| 2️⃣ **Source Bias** | Evaluate reliability of each source | Bias matrix, confidence levels |
| 3️⃣ **Actor Mapping** | Identify players, interests, capabilities | Player profiles with incentives |
| 4️⃣ **Economic Analysis** | Trade, sanctions, currency stress | Economic pressure vectors |
| 5️⃣ **Network Mapping** | Patrons, proxies, alliances | Relationship networks |
| 6️⃣ **Historical Patterns** | Compare to archetypes | Similar conflicts + lessons |
| 7️⃣ **Info Warfare** | Analyze narratives, detect ops | Narrative divergence score |
| 8️⃣ **Red Team** | Challenge assessment | Alternative hypotheses |
| 9️⃣ **Scenarios** | Generate 4 alternative futures | Probabilistic futures |

---

## 🔧 Live Data Sources

All data is **current and verified**:

| Source | What | Freshness | Coverage |
|--------|------|-----------|----------|
| **GDELT** | News articles + sentiment | Real-time | 300M+ articles, 65 languages |
| **ACLED** | Armed conflict events | 1-3 days | 200+ countries since 1997 |
| **ReliefWeb** | Humanitarian reports | Daily | UN-curated crisis data |
| **Frankfurter** | Currency rates | Daily | 150+ currencies |
| **UN Sanctions** | Current regimes | Current | OFAC official data |

---

## 📦 What's Included

### 39 Analytical Modules

**Foundational (8):** Game theory, early warning, international law, elections, climate/resources, treaties, dead reckoning, actor behavior, diaspora networks

**Strategic Thinking (9):** Multi-perspective analysis, scenario modeling, trend detection, calibration, causal chains, elite analysis, geospatial dynamics

**Rigorous Analysis (14):** Credible commitment, alliance stability, escalation ladder, thresholds, spiral dynamics, intelligence gaps, sanctions analysis (4 modules), hybrid warfare, historical analogs

**Specialized (1):** Art of War strategic framework

### Intelligence Tools

- 🔍 **Escalation Risk Assessment** — Where on the escalation ladder?
- 🎯 **Actor Incentive Modeling** — What do they want? What can they do?
- 📈 **Scenario Simulation** — Model 6-24 month futures
- 🧠 **Red Team Analysis** — Challenge your own assumptions
- 📊 **Causal Chain Mapping** — Trace downstream effects
- 🕷️ **Network Analysis** — Identify patrons, proxies, alliances
- 💰 **Economic Pressure Mapping** — Trade, sanctions, currency effects
- 📡 **Information Operation Detection** — Find coordinated narratives
- 📚 **Historical Pattern Matching** — Learn from similar cases

---

## 💯 Validation

**Tested against real intelligence scenarios:**

✅ Iran-Middle East conflict analysis (March 2026)  
✅ All 9-step workflow verified correct  
✅ Multi-perspective analysis working  
✅ Scenario modeling realistic  
✅ Intelligence gaps properly identified  
✅ Confidence scoring appropriate  

See [VERIFICATION.md](VERIFICATION.md) for details.

---

## 🔒 Security & Privacy

- ✅ **No API keys stored** — Uses only public endpoints
- ✅ **No credentials hardcoded** — Completely open
- ✅ **Fully audited** — Security audit passed
- ✅ **Open source** — MIT license, review the code
- ✅ **Graceful error handling** — No silent failures

Full security audit in [SECURITY_AUDIT.md](SECURITY_AUDIT.md)

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| **README.md** | This file |
| **SKILL.md** | Technical specification + workflow details |
| **QUICK_REFERENCE.md** | Cheat sheet for fast lookup |
| **SKILL_USAGE.md** | How to integrate with AI agents |
| **LIVE_DATA_USAGE.md** | API reference + data sources |
| **FIXES.md** | Error handling + fallback mechanisms |
| **SECURITY_AUDIT.md** | Complete security verification |
| **CONTRIBUTING.md** | How to contribute improvements |

---

## ⚡ Performance

```
Installation:      < 1 minute
First Analysis:    90s - 15m depending on depth
Data Freshness:    Real-time articles, daily events
Concurrent Users:  Unlimited (API rate limiting handled)
Disk Space:        154 KB (compressed), 357 KB (uncompressed)
Memory Usage:       ~50-100 MB during analysis
```

**Depth Levels:**
- 🏃 **FLASH** (90 seconds) — Current overview
- 🚶 **BRIEF** (5 minutes) — Decision support
- 🧠 **FULL** (15 minutes) — Comprehensive analysis

---

## 🎓 Real-World Examples

### Example 1: Crisis Assessment
```
Analyze Gaza situation with FULL depth
→ Get live conflict data (ACLED)
→ Analyze media narrative (GDELT tone)
→ Map key actors and incentives
→ Generate 4 scenarios with probabilities
→ Identify critical unknowns
```

### Example 2: Escalation Risk Monitoring
```
Monitor Ukraine escalation ladder
→ Track recent military events
→ Assess economic pressure (sanctions)
→ Identify historical parallels
→ Red team your own assessment
→ Get 6-month probabilistic scenarios
```

### Example 3: Strategic Planning
```
Understand Taiwan risks
→ Map regional actor networks
→ Analyze economic dependencies
→ Game theory incentive analysis
→ Generate alternative futures
→ Identify decision points
```

---

## 🛠️ Configuration

Edit `monitor_config.json` to customize monitoring:

```json
{
  "monitor_topics": [
    {"topic": "Gaza", "keywords": ["Gaza", "Palestine"], "depth": "FULL"},
    {"topic": "Ukraine", "keywords": ["Ukraine", "Russia"], "depth": "BRIEF"}
  ],
  "run_interval_hours": 6,
  "alert_on_risk_level": "HIGH"
}
```

Or use interactive setup:
```bash
python3 configure_monitor.py
```

---

## 🔄 Deployment Options

### Local Development
```bash
python3 interactive_monitor.py
```

### Background Monitoring (Every 6 Hours)
```bash
./monitor_setup.sh continuous 6
```

### Cron Job (Production)
```bash
./monitor_setup.sh install-cron 6
```

### Python Integration
```python
from geopolitical_analyst_agent import run_analysis
result = run_analysis("Gaza", depth="FULL")
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- How to report bugs
- How to suggest features
- Code style guidelines
- Pull request process
- Development setup

**Areas we need help with:**

- Additional analytical modules
- New data source integrations
- REST API wrapper
- Web dashboard
- Docker support
- Documentation improvements

---

## 📄 License

MIT License — See [LICENSE](LICENSE)

**Created by:** Nima Ansari

---

## 🔗 Links

- **GitHub:** https://github.com/nimaansari/geopolitical-analyst-skill
- **Documentation:** [SKILL.md](SKILL.md) | [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **Issues:** [GitHub Issues](https://github.com/nimaansari/geopolitical-analyst-skill/issues)
- **Discussions:** [GitHub Discussions](https://github.com/nimaansari/geopolitical-analyst-skill/discussions)

---

## ⭐ Support

If you find this useful:

- **Star** ⭐ on GitHub
- **Share** with analysts and researchers
- **Contribute** improvements via PRs
- **Report** bugs and suggestions

---

## 🎯 Use Cases

**Intelligence Analysts** — Systematic conflict analysis  
**Journalists** — Geopolitical context for stories  
**Researchers** — Academic conflict studies  
**Policy Teams** — Risk assessment and forecasting  
**AI Agents** — Autonomous situation analysis  
**Decision-Makers** — Quick geopolitical briefings  

---

## 💡 Why This Matters

Geopolitical analysis is often done **intuitively**. This framework makes it:

✅ **Systematic** — 9-step workflow, not guesswork  
✅ **Transparent** — Every assumption is documented  
✅ **Rigorous** — 39 analytical models applied  
✅ **Honest** — Intelligence gaps explicitly identified  
✅ **Probabilistic** — Scenarios with confidence levels  
✅ **Current** — Live data feeds, not old reports  

---

**Ready to understand geopolitical situations with rigor?**

```bash
git clone https://github.com/nimaansari/geopolitical-analyst-skill.git
python3 interactive_monitor.py
```

Start analyzing. 🚀
