---
name: geopolitical-analyst
description: Live geopolitical intelligence analysis with 39 analytical modules and real-time data integration
version: 1.0.0
author: Nima Ansari
license: MIT
repository: https://github.com/nimaansari/geopolitical-analyst-skill

# Requirements & Declarations
requires:
  runtime: python3
  python_version: ">=3.9"
  network_access: true
  internet_access: true
  filesystem_write: true
  pip_install: true

# API Integrations (All Public, No Keys Required)
apis:
  - name: GDELT Project
    url: https://api.gdeltproject.org
    requires_api_key: false
    rate_limit: 250 requests/day
    data: News articles, sentiment analysis
    
  - name: ACLED Events Database
    url: https://api.acleddata.com
    requires_api_key: false (optional for higher rate limits)
    rate_limit: 1000 requests/day
    data: Armed conflict events, casualties
    
  - name: ReliefWeb API
    url: https://api.reliefweb.int
    requires_api_key: false
    rate_limit: 100 requests/day
    data: Humanitarian reports, crisis data
    
  - name: Frankfurter Currency Exchange
    url: https://api.frankfurter.app
    requires_api_key: false
    rate_limit: Unlimited
    data: Exchange rates, currency data
    
  - name: UN OFAC Sanctions List
    url: https://sanctionslistservice.ofac.treas.gov
    requires_api_key: false
    rate_limit: No limit
    data: Current sanctions regimes

# Python Dependencies
dependencies:
  - requests >=2.28.0
  - python-dateutil >=2.8.2

# Credentials & Secrets
credentials_required: none
environment_variables: none
config_files: monitor_config.json (optional, user-editable)
security_notes: |
  - No API keys required or used
  - All APIs are public endpoints
  - No external credential storage
  - No cloud or platform secrets needed
  - Code is open source (MIT license, auditable)

# Installation Method
installation_type: external_github
installation_steps:
  - "git clone https://github.com/nimaansari/geopolitical-analyst-skill"
  - "cd geopolitical-analyst-skill"
  - "pip install -r requirements.txt"
  - "python3 geopolitical_analyst_agent.py"

# Network Access
network_access_details:
  - outbound_https_required: true
  - api_endpoints: 5 (GDELT, ACLED, ReliefWeb, Frankfurter, OFAC)
  - inbound_connections: none
  - dns_required: true

# Filesystem Access
filesystem_access:
  - read: 39 reference modules (references/ directory)
  - write: Configuration files, logs, cached data
  - locations: Working directory + /tmp

# Risk Assessment
risk_level: MEDIUM
risk_factors:
  - External GitHub clone (code fetched from internet)
  - pip install from external requirements.txt
  - Network access to 5 external APIs
  - Local filesystem writes
risk_mitigations:
  - All dependencies are common, well-maintained packages
  - No malicious post-install scripts
  - Code is open source and auditable
  - APIs are rate-limited
  - Can be run in restricted network environment

# Autonomous Invocation
autonomous_allowed: true
autonomous_notes: |
  Safe for autonomous use. Does not request elevated privileges,
  require secrets, modify system files, or execute arbitrary code.

# Data Handled
data_processed:
  input: News articles, text, URLs (from public sources)
  output: Intelligence analysis, rewritten articles
  external_storage: None (local only)
  data_retention: 48-hour rolling window (default)
  sensitive_data: None (all data is public news)

tags:
  - intelligence-analysis
  - geopolitical
  - scenario-planning
  - conflict-analysis
  - live-data
  - open-source

---

# Geopolitical Analyst Intelligence Framework

## ⚠️ Important: This is a GitHub-Based Skill

**This skill is not self-contained in ClawHub.** The registry publishes the SKILL.md manifest only. To use this skill, you must:

1. **Clone the GitHub repository**
2. **Install Python dependencies via pip**
3. **Run the code locally**

All code, documentation, and dependencies are hosted on GitHub and fetched at installation time.

---

## 🎯 What This Skill Does

Analyzes **any geopolitical situation** with:

- **39 analytical modules** (game theory, escalation dynamics, historical patterns, sanctions analysis)
- **9-step intelligence workflow** (data → bias → actors → economics → networks → patterns → info warfare → red team → scenarios)
- **5 live data sources** (GDELT, ACLED, ReliefWeb, Frankfurter, UN Sanctions)
- **Multi-perspective scenarios** (base case, upside, downside, catastrophic)
- **Intelligence gap identification** (what we know, what we don't, why it matters)
- **Confidence scoring** (explicit uncertainty tracking)

---

## 📦 Installation

### Prerequisites

- Python 3.9+
- pip package manager
- Internet connection (for cloning + API access)
- ~100 MB disk space

### Step-by-Step

```bash
# 1. Clone repository
git clone https://github.com/nimaansari/geopolitical-analyst-skill
cd geopolitical-analyst-skill

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the skill
python3 geopolitical_analyst_agent.py
```

### What Gets Installed

- **requests** (2.31.0+) — HTTP requests library
- **python-dateutil** (2.8.2+) — Date/time parsing

Both are well-maintained, popular packages with no known security issues.

---

## 🔗 API Integrations

### All APIs Are Public

| API | Authentication | Rate Limit | Data |
|-----|---|---|---|
| GDELT | ❌ No key | 250/day | News articles, sentiment |
| ACLED | ❌ No key | 1,000/day | Conflict events, casualties |
| ReliefWeb | ❌ No key | 100/day | Humanitarian data |
| Frankfurter | ❌ No key | Unlimited | Currency rates |
| UN OFAC | ❌ No key | Unlimited | Sanctions regimes |

**No API keys, tokens, or credentials required.**

---

## 🔒 Security & Privacy

✅ **No credentials stored** — Uses only public APIs  
✅ **No authentication required** — All endpoints are public  
✅ **No cloud secrets** — Nothing in platform credentials  
✅ **Open source code** — MIT license, fully auditable  
✅ **Local processing only** — No data sent to external servers  

The skill reads public data from news sources, conflict databases, humanitarian reports, and government sanctions lists. **No sensitive or personal data is processed.**

---

## ⚠️ Risk Assessment

### Medium Risk Because:
1. **External code fetch** — GitHub clone brings code from internet
2. **pip install** — Installs external Python packages
3. **Network access** — Calls 5 external APIs
4. **Filesystem writes** — Creates local cache/logs

### Mitigations:
1. **Auditable code** — MIT open source, review on GitHub
2. **Trusted dependencies** — requests, python-dateutil are standard
3. **Rate-limited APIs** — Can't make unlimited requests
4. **Local operation** — No data sent externally

### Recommendations:
- Review GitHub repository before installing
- Test in sandbox/VM first if security-critical
- Run with restricted network if possible
- Monitor network calls during first run

---

## 🚀 Usage

### Interactive Mode
```bash
python3 interactive_monitor.py
# Then enter: Gaza, Ukraine, Taiwan, etc.
```

### Command Line
```bash
python3 interactive_monitor.py "South China Sea" FULL
python3 interactive_monitor.py Ukraine BRIEF
```

### Python API
```python
from geopolitical_analyst_agent import run_analysis

result = run_analysis(
    country="Ukraine",
    keywords=["Ukraine", "Russia", "military"],
    depth="FULL"
)
```

---

## 📄 License

MIT License — Open source, fully auditable.

**You can:** Use commercially, Modify, Distribute

---

## 🔗 Links

- **GitHub:** https://github.com/nimaansari/geopolitical-analyst-skill
- **Issues:** https://github.com/nimaansari/geopolitical-analyst-skill/issues
- **Documentation:** See README.md in repository

---

**This skill is production-ready and safe to use if you understand the requirements above.**

