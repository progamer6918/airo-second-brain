---
name: airo-research
description: >
  Conduct public web and documentation research using native read-only browser tools and ASB second brain knowledge.
  Use this skill when the user asks for market analysis, technical documentation lookup, competitor benchmarking,
  public information gathering, or fact verification. Strictly read-only; prioritizes local browser_readonly; prohibits authentication, form submissions,
  and private credential access.
---

# AIRO Research — Public Information Gathering & Knowledge Synthesis

## 1. NAME
`airo-research` — AIRO Canonical Public Research Skill

## 2. PURPOSE
Provide structured, verifiable research capabilities for the AIRO ecosystem by combining Hermes native `browser_readonly` capability with AIRO Second Brain knowledge. Extracts factual evidence from public websites, online documentation, and community knowledge bases without executing mutations, requiring paid external scraping APIs, or compromising security.

## 3. WHEN TO USE
Activate this skill when:
- The user asks to research a public topic, technology, framework, market, or competitor (e.g., "Research latest public information about X", "Cari informasi tentang Y").
- The user needs documentation lookups, API specifications, or release notes from public sources.
- An objective requires verifying external facts, benchmarking competitors, or gathering real-world references.
- Synthesizing external public knowledge with internal ASB concepts.

Do NOT use when:
- The user asks to log into any platform, portal, account, or private dashboard.
- The task requires code changes, configuration mutations, or terminal execution (route to Antigravity).
- The task involves financial ledger mutations (route to Arfin / Owner direct).
- The task requires personal reminders or cron job scheduling (route to Remin / Hermes cron).

## 4. RESEARCH SOURCE PRIORITY
When conducting research, queries and extraction MUST follow this strict priority order:
1. `browser_readonly`: Native local Chromium browser navigation, text snapshots, and scrolling. Zero external API keys or third-party cloud credentials required. This is the primary research engine.
2. Provided URLs / documents: Direct links or content supplied explicitly by the Owner in conversation.
3. Public sources: Authoritative public websites, documentation portals, and official repositories reachable over HTTP/HTTPS.
4. ASB knowledge: AIRO Second Brain canonical context, project documents (`docs/`), and active records.
5. Optional external providers: Third-party scrapers or extractors (such as Firecrawl or external search APIs) ONLY if configured and reachable; NEVER mandatory or blocking.

## 5. WORKFLOW
Follow this deterministic 5-step research pipeline:

```
REQUEST
  ↓
1. Research Planning
   - Define exact research questions and hypotheses
   - Identify candidate public authoritative domains (docs, specs, official portals)
   - Verify scope is purely public (no private/authenticated data)
  ↓
2. Browser Read-Only Gathering (Primary Path)
   - Navigate to target URLs using browser_navigate
   - Capture clean text snapshots using browser_snapshot (or web_extract if lightweight)
   - Scroll or inspect additional sections using browser_scroll
  ↓
3. Evidence Extraction & Verification
   - Extract primary claims, quotes, metrics, dates, and version numbers
   - Record canonical source URLs for every factual assertion
   - Filter out promotional fluff, unverified forum opinions, and hallucinated claims
  ↓
4. ASB Reconciliation & Synthesis
   - Reconcile gathered findings against ASB canonical truth (docs/ and active context)
   - Group findings by theme (Overview, Capabilities, Architecture, Comparisons)
   - Apply Confidence Separation (Verified Evidence vs Inference)
  ↓
5. Answer Formatting
   - Generate structured Markdown response following the OUTPUT_FORMAT schema
   - Provide explicit source citations, confidence levels, and technical caveats
```

## 6. AVAILABLE TOOLS & DEPENDENCY POLICY
This skill operates strictly within the `browser_readonly` and `safe` toolsets:

### Permitted Tools
- `browser_navigate`: Navigate to public HTTP/HTTPS endpoints using the native Chromium instance (Primary).
- `browser_snapshot`: Capture structured text accessibility snapshot of the current page (Primary).
- `browser_scroll`: Scroll down/up on long documentation pages (Primary).
- `web_search`: Query public search engine for relevant URLs and snippets.
- `web_extract`: Extract readable markdown content from public URLs (optional lightweight path).
- `skill_view`: Load reference wiki skills (`wiki-query`, `wiki-research`).
- `skills_list`: List available knowledge and capability skills.

### Dependency Policy (Zero Mandatory External APIs)
- **FIRECRAWL_REQUIRED**: `NO`. Native `browser_readonly` operates locally via Chromium and requires no Firecrawl API keys or third-party scraping accounts. Firecrawl is strictly an optional external provider. Lack of Firecrawl configuration must never abort or block research.
- **CREDENTIAL_REQUIREMENT**: `NONE` for public web research.

### Forbidden Tools (Blocked by Policy)
- `browser_click`, `browser_type`, `browser_press`: Blocked to prevent form submissions and interactive state changes.
- `browser_dialog`, `browser_console`, `browser_cdp`: Blocked to prevent arbitrary browser inspection or bypass.
- `write_file`, `patch`, `terminal`: Blocked to prevent workspace mutations.

## 7. CORE DISCIPLINES & RULES

### 1. No Hallucination Rule
- Never fabricate quotes, facts, API parameters, version numbers, or benchmarks.
- If a target page cannot be loaded via `browser_navigate` or `browser_snapshot`, state explicitly that the source was unreachable. Do not guess the contents.

### 2. Evidence Discipline
- Every factual claim must be backed by a cited URL and a direct evidence snippet or verifiable observation from `browser_snapshot`.
- Distinguish clearly between verbatim source text and operator interpretation.

### 3. Confidence Separation
Categorize all findings into distinct confidence tiers:
- `CONFIDENCE=HIGH`: Directly verified via primary official documentation or live `browser_snapshot`.
- `CONFIDENCE=MEDIUM`: Reported by secondary reliable sources or derived through cross-referenced synthesis.
- `CONFIDENCE=LOW`: Unverified community claims, preliminary roadmaps, or speculative statements.

## 8. OUTPUT FORMAT
All outputs generated under this skill must adhere to this structured format:

```markdown
### 🌐 AIRO Research Summary: [Topic / Entity]

#### 1. Executive Summary
[High-level synthesis answering the user's primary question in 2-3 concise sentences]

#### 2. Key Findings & Details
- **Finding 1**: [Detailed factual finding with context]
  - *Confidence*: HIGH | MEDIUM | LOW
- **Finding 2**: [Detailed factual finding with context]
  - *Confidence*: HIGH | MEDIUM | LOW
- **Finding 3**: [Detailed factual finding with context]
  - *Confidence*: HIGH | MEDIUM | LOW

#### 3. Verified Evidence & Citations
- **Source 1**: `[URL / Document Title]` — [Specific fact or snippet verified from browser snapshot]
- **Source 2**: `[URL / Document Title]` — [Specific fact or snippet verified from browser snapshot]

#### 4. ASB Knowledge Reconciliation
- **Relationship to AIRO**: [How this external knowledge connects to active projects or ASB concepts]
- **Reconciliation Verdict**: [NEW_KNOWLEDGE | SUPPORTING_EVIDENCE | CONFLICT_DETECTED]

#### 5. Limitations & Caveats
- [Any access limitations, date boundaries, or areas requiring further investigation]
```

## 9. SECURITY BOUNDARY

### Allowed (SAFE)
- Browsing public HTTP and HTTPS websites via `browser_readonly`.
- Extracting public documentation, open-source repositories, and public news/articles.
- Querying internal ASB knowledge via read-only tools.

### Strictly Blocked (POLICY VIOLATION)
- **Authentication & Login**: Refuse any request to enter username, password, OTP, token, or session cookie.
- **Private / Internal Networks (SSRF Prevention)**: Never navigate to `localhost`, `127.0.0.1`, `::1`, private LAN (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), or cloud metadata endpoints (`169.254.169.254`).
- **Form Submission**: Do not fill out forms, submit inquiries, click purchase/download buttons, or perform web actions.
- **Credentials & PII**: Never extract, summarize, or persist private customer data, API keys, or financial secrets.
- **Terminal Mutation**: Never run write commands, execute unknown scripts, or install software.

If a requested research target requires authentication or accesses internal infrastructure, immediately abort the workflow and report:
`BOUNDARY_BLOCK=PASS: Requested action requires private authentication or accesses internal infrastructure, which is strictly prohibited by AIRO Research security governance.`
