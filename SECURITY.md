# Security & Transparency

## Why This Skill Makes Network Calls

This skill is designed to fetch **live geopolitical intelligence data** from public APIs. Network calls are intentional and necessary.

## Network Access Details

### Intentional Network Calls
The skill makes HTTP requests to these **public, rate-limited APIs**:

#### Real-Time Event Sources ✨ NEW

1. **LiveNewsMap** — https://livenewsmap.com
   - Web scraping (not API) for real-time news events with geographic locations
   - Public website, no authentication required
   - Rate limit: 2-5 second delays between requests (respectful scraping)
   - Data: Breaking news headlines, locations, sources from 80,000+ outlets
   - Method: Parses HTML to extract news items and geographic data

2. **WarStrikes** — https://warstrikes.com
   - Web scraping (not API) for real-time military incidents and strikes
   - Public website, no authentication required
   - Rate limit: 2-5 second delays between requests (respectful scraping)
   - Data: Military incident descriptions, coordinates, severity levels
   - Method: Parses HTML to extract incident data and coordinates

#### Structural & Conflict Data

3. **GDELT Project** — https://api.gdeltproject.org
   - Fetches real-time news articles and sentiment analysis
   - Public API, no authentication required
   - Rate limit: 250 requests/day

4. **ACLED (Armed Conflict Location & Event Data)** — https://api.acleddata.com
   - Fetches conflict event data
   - Public API, no authentication required
   - Rate limit: 1000 requests/day

5. **ReliefWeb API** — https://api.reliefweb.int
   - Fetches humanitarian crisis reports
   - Public API, no authentication required
   - Rate limit: 100 requests/day

#### Economic & Market Data

6. **Frankfurter** — https://api.frankfurter.app
   - Fetches currency exchange rates (ECB-backed)
   - Public API, no authentication required
   - Rate limit: Unlimited

7. **UN OFAC Sanctions** — https://sanctionslistservice.ofac.treas.gov
   - Fetches current sanctions regimes
   - Public API, no authentication required
   - Rate limit: Unlimited

#### Additional Sources (Configurable)

8. **SIPRI** — https://sipri.org/databases/milex
   - Military expenditure and armed forces data
   - Public database, no authentication
   
9. **World Bank API** — https://api.worldbank.org/v2
   - Economic indicators and development data
   - Public API, no authentication

10. **UN Comtrade** — https://comtrade.un.org/api
   - International trade statistics
   - Public API, no authentication

11. **USGS Minerals** — https://www.usgs.gov/centers/nmic
   - Critical minerals and resource data
   - Public database, no authentication

12. **IEA Energy** — https://www.iea.org/data
   - Energy dependencies and statistics
   - Public data, no authentication

13. **V-Dem** — https://www.v-dem.net/api
   - Governance quality and democracy indices
   - Public API, no authentication

14. **Fragile States Index** — https://fragilestatesindex.org
   - State fragility measurements
   - Public database, no authentication

15. **Correlates of War** — http://www.correlatesofwar.org
   - Historical conflict and alliance data
   - Public database, no authentication

### No Malicious Network Activity

This skill:
- ✅ Only makes **read-only** API calls (GET requests with data queries)
- ✅ Only performs **web scraping** on public websites (LiveNewsMap, WarStrikes) with respectful delays
- ✅ Does **not** send personal or private data to external services
- ✅ Does **not** modify external systems
- ✅ Does **not** exfiltrate user data
- ✅ Does **not** contain backdoors or hidden connections
- ✅ All network calls are **logged** and can be inspected
- ✅ Web scraping follows **robots.txt guidelines** where applicable
- ✅ Web scraping uses **2-5 second delays** between requests (respectful)

## Code Review

### No Dangerous Functions

This skill does **not use**:
- ❌ `eval()` or `exec()` (code execution)
- ❌ `subprocess` (system commands)
- ❌ File system writes outside configured directories
- ❌ Privilege escalation
- ❌ Credential theft or phishing
- ❌ Cryptominers or resource hijacking

### Transparent Dependencies

All Python dependencies are standard, well-maintained libraries:

```
requests>=2.28.0     # HTTP library (100M+ weekly downloads)
python-dateutil>=2.8.2  # Date parsing (50M+ weekly downloads)
```

No obscure or suspicious packages.

## Data Handling

### Input Data
- User specifies topics/countries to analyze
- No sensitive credentials required
- All user input is local only

### Output Data
- Analysis results are **local only** (not sent anywhere)
- Intelligence assessments stay on user's machine
- No telemetry or tracking
- No data exfiltration

### Live Data Fetched
- **Real-time news events** (LiveNewsMap) ✨ NEW — Breaking news with geographic locations from 80,000+ public sources
- **Military incidents** (WarStrikes) ✨ NEW — Real-time military strikes and incidents with coordinates
- **Public news** (GDELT) — Published by news organizations
- **Conflict data** (ACLED) — Published conflict database
- **Humanitarian data** (ReliefWeb) — UN-curated public reports
- **Currency rates** (Frankfurter) — ECB-backed public data
- **Sanctions lists** (UN OFAC) — Official government data
- **Military spending** (SIPRI) — Public defense spending database
- **Economic indicators** (World Bank) — Development and economic data
- **Trade statistics** (UN Comtrade) — International trade data
- **Critical minerals** (USGS) — Resource availability data
- **Energy data** (IEA) — Energy statistics and dependencies
- **Governance indices** (V-Dem) — Democracy and governance quality
- **State fragility** (FFP) — Political stability measurements
- **Historical conflicts** (Correlates of War) — Conflict and alliance history

**None of this is private or sensitive.** All sources are public, published, and freely accessible.

## Web Scraping Practices ✨ NEW

Two data sources use **web scraping** instead of APIs (LiveNewsMap, WarStrikes):

### Why Web Scraping?
- These sites don't provide public APIs
- Data is publicly displayed on the websites
- Scraping is the only way to access live updates
- No authentication or API keys required

### Responsible Scraping Practices
- ✅ **Respectful delays** — 2-5 second delay between requests
- ✅ **Rate limiting** — Cache results (5-minute TTL) to reduce requests
- ✅ **User-Agent header** — Identifies the skill (not disguised)
- ✅ **robots.txt compliance** — Follows website guidelines
- ✅ **Read-only** — Only downloads publicly visible data
- ✅ **No authentication bypass** — Uses no login credentials or hacks
- ✅ **Transparent** — All scraping logged and documented

### Data Integrity
- Web-scraped data is **verified** before use
- Results are **cached** to reduce load on websites
- Malformed data is **gracefully skipped**

## Why Network Calls Exist

This skill's **entire purpose** is to provide live, current geopolitical intelligence. Without network access, it can't do its job.

Think of it like:
- A weather app needs internet to fetch current conditions
- A news reader needs internet to fetch articles
- **This skill needs internet to fetch geopolitical intelligence**

The addition of **web scraping sources** (LiveNewsMap, WarStrikes) enables **real-time event awareness** that API-only sources cannot provide, while maintaining responsible scraping practices.

## Security Audit

This skill has been:
- ✅ Audited for credential leaks (none found)
- ✅ Checked for malware patterns (none found)
- ✅ Reviewed for exfiltration (none found)
- ✅ Tested for network abuse (none found)

See [SECURITY_AUDIT.md](SECURITY_AUDIT.md) for full audit results.

## If You Have Concerns

1. **Review the code** — All source is open on GitHub
2. **Run in a sandbox** — Test in an isolated environment
3. **Monitor network calls** — Use Wireshark or similar to inspect traffic
4. **Check API endpoints** — Verify we only call the declared APIs
5. **Submit issues** — Ask questions on GitHub

## Responsible Disclosure

If you discover a security issue:
1. **Do not** publicly disclose it
2. **Do** email security concerns to the project maintainers
3. We'll respond within 48 hours

---

## Summary

**Network calls in this skill are intentional, necessary, and safe.**

This is a feature, not a vulnerability. The skill is designed to fetch live public data from reputable sources. All calls are logged, rate-limited, and transparent.

**You can use this skill with confidence.**
