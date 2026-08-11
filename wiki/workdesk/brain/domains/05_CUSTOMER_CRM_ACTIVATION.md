# Customer Crm Activation

> **Status:** canonical persistence candidate derived only from reconstructed source material. Historical examples remain historical; unresolved source conflicts remain unresolved.

## Canonical scope
- CDB quality
- lead funnel
- VE / virtual showroom
- BTL / exhibition / roadshow / showroom event
- customer journey / experience / loyalty

## How to use this brain
- Start from the business question, then localize the problem before diagnosing.
- Resolve requested date/currentness before applying dated standards, thresholds, program rules, or examples.
- Use [[../reference/CANONICAL_DECISION_RULE_LIBRARY|Canonical Decision Rules]] and [[../reference/CANONICAL_FORMULA_LIBRARY|Canonical Formula Library]] as shared controls.
- If evidence conflicts or authority is missing, consult [[../reference/CONTRADICTION_UNRESOLVED|Unresolved Ledger]] rather than guessing.

---

## Source-derived module — Crm Customer Intelligence Operating System
_Reconstruction module: `B07` / `CRM_CUSTOMER_INTELLIGENCE_OPERATING_SYSTEM.md`_

## Mental model

CRM in this source cluster is a closed-loop system, not a contact list:

`CDB acquisition -> 3C quality -> customer profiling/insight -> lead or retention treatment -> follow-up -> deal/service/repeat -> satisfaction/loyalty signal -> updated customer knowledge -> next treatment`.

### Why this matters

A large database with poor Correct/Complete/Clean quality can create fake scale. A large lead pool with weak dispatch/follow-up creates fake opportunity. High sales without repeat/retention signal can hide relationship weakness.

## Customer intelligence layers

1. **Identity/data** - who is the customer and how can they be contacted?
2. **Profile** - demographic/psychographic/segment context.
3. **Behavior** - purchase/service history, RO/NRO, lead source, response status.
4. **Need/job** - stated, real, unstated, delight, secret; JTBD.
5. **Experience** - convenience/action/speed/hassle-free; moments of truth; joy/pride/connection.
6. **Relationship outcome** - satisfaction -> loyalty -> advocacy, retention, repeat order, referral.

## Decision rule

Do not choose a CRM program before checking:
- data quality;
- customer segment/profile;
- lead owner/source;
- current funnel stage;
- reason for pending/not-deal;
- relevant product/program/stock;
- previous purchase/service relationship.

The treatment must fit the customer, not simply the campaign calendar.

---

## Source-derived module — Customer Focus Loyalty And Experience
_Reconstruction module: `B07` / `CUSTOMER_FOCUS_LOYALTY_AND_EXPERIENCE.md`_

## Outcome hierarchy

`Satisfaction -> Loyalty -> Advocacy`.

This means satisfaction is a floor, not the final objective.

## Customer journey

The source uses 5A:

`Aware -> Appeal -> Ask -> Act -> Advocate`.

A problem can occur at any stage. Therefore "sales down" should not automatically trigger only a closing intervention; the root may be awareness, appeal, information, experience or advocacy/referral.

## Need system

Use the five need types to avoid taking the customer's first sentence too literally:
- stated;
- real;
- unstated;
- delight;
- secret.

JTBD adds another question: **what job is the customer trying to get done?**

## Experience design

CASH expectation:
- Convenience.
- Action.
- Speed.
- Hassle Free.

Delight can be created through:
- Joy.
- Pride.
- Connection.

## Measurement

CSAT and NPS are different:
- CSAT asks whether the experience met expectations.
- NPS asks recommendation propensity and subtracts detractors from promoters.

Do not substitute one metric for the other.

## Organization implication

Customer experience crosses sales, marketing, service, maintenance, distribution and production. The source therefore requires cross-division communication, shared feedback, coordinated problem solving and shared goals/metrics.

---

## Source-derived module — Leads Management End To End
_Reconstruction module: `B07` / `LEADS_MANAGEMENT_END_TO_END.md`_

## Funnel

`touchpoint -> suspect -> validated prospect -> dispatch/assign -> follow-up -> contacted/not contacted -> pending/deal/not deal -> SPK/SO -> contribution`.

The source distinguishes **owner**, **processor** and **executor** roles. That prevents the common failure where everyone can see a lead but nobody owns the next action.

## Diagnostic matrix

### Leads high, contacted low
Check data validity, duplicate/redundant data, assignment, FLP capacity, SLA and contact-attempt execution.

### Contacted high, deal low
Check probing quality, customer fit, product/price/financing/stock, reason codes, follow-up timing and alternative offer.

### Deal exists, reported contribution low
Check status update, frame/SPK/SO linkage and source attribution before blaming sales execution.

### Pending pool grows
Split Hot/Medium/Low/Inden; inspect promised next follow-up date, stock/color, financing rejection and customer readiness.

### Not-deal pool grows
Do not treat as dead automatically. Source explicitly supports retargeting/re-follow-up when the original barrier changes.

## Metrics

- Contacted Rate = Contacted / Prospect.
- Success Rate = Deal / Contacted.
- Conversion Rate = Deal / Total Leads.
- Contribution to Sales = Deal / Total Sales.
- SLA = time from upstream upload/dispatch to first dealer follow-up (exact definition depends on source/process version).

## Currentness

Exact 2024 tool names, daily lead allocations and contact sequence are historical process guidance. Use current system policy if a newer source exists.

---

## Source-derived module — Btl Activity Operating System
_Reconstruction module: `B06` / `BTL_ACTIVITY_OPERATING_SYSTEM.md`_

## L0 - What it is

BTL is not simply "doing an event". The reconstructed sources define an operating loop that connects territory coverage, customer attraction, sales execution, evidence, and evaluation.

## L1 - Core loop

`coverage need -> choose activity type -> plan location/content/target -> approval -> execute -> capture visitor/prospect/sales -> evidence/LPJ -> evaluate -> improve next activity`.

## L2 - Choose the activity intentionally

- **Exhibition:** persistent display/dealing presence in a potential location.
- **Roadshow:** activation with hard-selling/crowd content and riding-test experience.
- **Showroom Event:** event at dealer premises; useful for invited customers/community/thematic activation.

Do not classify an ordinary static display as Roadshow just because it happened outside the dealer.

## L3 - Diagnose weak activity

### Problem: event happened but sales weak
Check in order:
1. Was the location chosen for coverage/potential or convenience?
2. Did the event format match the objective?
3. Was there enough crowd/customer activity?
4. Were sales people actively serving and prospecting?
5. Were riding test / product focus / finance support available where relevant?
6. Were prospects captured in the proper system?
7. Did hot prospects convert?
8. Did event sales actually occur in the defined event window/location?
9. Was cost proportional to output?

### Problem: LPJ looks good but field execution may be weak
Use evidence triangulation:
- geotag/time;
- whole setup;
- crowd;
- sales interaction;
- riding test;
- cost receipts;
- system prospect/sales record.

A photo of a tent is not proof of effective BTL.

## L4 - Metrics from the source

Source-supported event fields:
- visitors;
- sales;
- riding-test participants;
- hot prospects;
- sales from hot prospects;
- conversion from hot prospects;
- actual cost.

**Analytical extensions (derived, not explicit source KPI):** cost/visitor, cost/hot-prospect and cost/deal can be calculated when the source fields exist. Use them as diagnostic ratios, not as historical mandated thresholds.

## Currentness

2022/2023 event frequencies, sponsorship values and old operational details are historical. For current 2026 BTL standards, use NOS BTL 2026 + BEST 2026 first, then use these historical sources for design intent, evidence logic and comparison.

---

## Source-derived module — Btl Ve Customer Activation Synthesis
_Reconstruction module: `B06` / `BTL_VE_CUSTOMER_ACTIVATION_SYNTHESIS.md`_

The BTL, VE, showroom, CRM and survey sources can be compiled into one customer-activation system:

`territory opportunity`  
`-> choose physical/digital activation`  
`-> create relevant experience/promo`  
`-> generate visitor/traffic`  
`-> capture unique lead/prospect`  
`-> assign and follow up`  
`-> manage stock/finance/pending barriers`  
`-> verify deal`  
`-> measure contribution/cost`  
`-> preserve evidence`  
`-> learn and redesign next activation`.

## Physical vs digital are not separate brains

- Physical BTL uses location, crowd, sales people, riding test and evidence.
- VE uses navigation, product/promo information, lead capture, assignment and digital follow-up.
- Showroom/virtual showroom extends the same customer journey across H1/H2/H3.

The shared professional question is:

> **Where exactly did customer momentum break?**

## Diagnostic matrix

| Signal | Likely layer to inspect first |
|---|---|
| low visitors/traffic | location, promotion, campaign reach, source activation |
| visitors high, leads low | proposition, customer capture, CTA, lead-form friction |
| leads high, contacted low | data quality, assignment, follow-up SLA/discipline |
| contacted high, prospect low | customer fit, product/program communication |
| prospect high, deal low | price/finance, stock/indent, competitor, follow-up quality |
| deal high, reported contribution low | system coding, SPK/SO/chassis verification, data rejection |
| cost high, sales low | event design, location, crowd quality, conversion chain |

This matrix is a cross-source synthesis. It does not create new historical thresholds.

---

## Source-derived module — Ve Customer Insight 2025
_Reconstruction module: `B06` / `VE_CUSTOMER_INSIGHT_2025.md`_

## What customers appear to value

From the 124-response survey:
- promotion and product information are equally strong stated reasons for using VE (48 respondents each);
- promo/discount is the largest named attractive content category (44 respondents);
- credit simulation is smaller but meaningful (14 respondents);
- direct discounts and lighter installment/DP are more desired than accessory bonus among the listed promo categories.

## Acquisition insight

The report says offline dealer visit (49) is still the largest named awareness source, while social media (40) is close behind. WhatsApp blast is much smaller (9).

This means "digital exhibition" does not imply purely digital acquisition. Dealer offline contact and social media can both feed the digital journey.

## Friction insight

Reported weak points:
- navigation/ease: 43;
- slow response: 27;
- design appearance: 21.

A campaign can therefore fail after customer interest is already present. The correct intervention may be UX or response process rather than more traffic.

## Data-quality caution

Some category totals in the source do not sum to the stated n=124. Do not normalise or invent missing respondents. When using the figures, quote the category counts/percentages as source-reported and treat them as directional customer research rather than a perfectly reconciled analytical dataset.

---

## Source-derived module — Ve Customer Journey And Platform
_Reconstruction module: `B06` / `VE_CUSTOMER_JOURNEY_AND_PLATFORM.md`_

## Why this matters

The platform sources show that VE is not merely a digital event banner. It attempts to connect the full customer journey across product, finance, service and dealer interaction.

## Customer journey layers

### Entry
- landing page;
- domicile/dealer selection;
- registration/login/promo code;
- terms and welcome guidance.

### Product discovery
- category/zone;
- 360 product;
- feature hotspots;
- variants;
- brochure/price list;
- promo;
- price/credit tools;
- trade-in.

### Experience/action
- riding-test registration;
- contact/lead form;
- live chat;
- dealer/finance-company path.

### H2/H3 extension
- AHASS booking/service information;
- service tips/technical education;
- AHASS program;
- parts/accessories/apparel/oil.

### Back end
- data capture;
- lead allocation;
- report/monitoring;
- CRM/NMS integration.

## Diagnostic rule

When VE conversion is weak, do not jump directly to "promo kurang menarik". Diagnose the specific journey friction:

`awareness -> access -> navigation -> information -> interest -> lead capture -> response -> deal verification`.

The 2025 customer survey specifically reports navigation/ease and slow response as major frictions, validating this stage-based approach.

---

## Source-derived module — Virtual Exhibition Leads Operating System
_Reconstruction module: `B06` / `VIRTUAL_EXHIBITION_LEADS_OPERATING_SYSTEM.md`_

## Mental model

VE performance is a chain, not a traffic number:

`event/source -> visitor -> unique lead -> contacted -> prospect -> deal -> verified SPK/SO -> retail contribution`.

Every break in that chain has a different cause and therefore a different action.

## Source integrity first

Before analysing performance:
- distinguish Independent, FINCOY and Product Launch event sources;
- separate invited and non-invited acquisition;
- prevent multiple event sources from collapsing into one code;
- deduplicate repeated customer actions before calling them unique leads.

If source coding is wrong, campaign comparison is invalid even if total lead count is correct.

## Stage diagnostics

### Leads low
Check:
- event frequency/campaign reach;
- database blast execution;
- social/offline promotion;
- promo attractiveness;
- access/navigation friction.

### Leads high, contacted low
Check:
- contact-number quality;
- assignment/distribution delay;
- follow-up discipline;
- repeated contact at different times/days.

### Contacted high, deal low
Check:
- customer need/product fit;
- stock/color/indent;
- program competitiveness;
- finance offer;
- response quality;
- re-follow-up of pending/not-deal.

### Deal exists but system contribution looks low
Check:
- deal update completeness;
- SPK/SO process;
- historical 2025 rule that VE deal is verified by chassis number rather than phone number;
- source-code accuracy.

## Integration evolution

The sources show the system moving from MonitorMu/manual reporting toward MDMS/NMS and CRM integration. Therefore, a modern analysis should distinguish **customer behaviour problem** from **data-pipeline/rejection problem**.

## Dated benchmarks

Keep old benchmarks as historical references only:
- 2023 VE Success Rate target 40%; Contribution to RS 0.55%.
- 2024 plan: Success Rate 40%, Contribution to RS 0.83%, Conversion Rate 25%, 2x VE/month.
- 2025 slide: minimum 3 deals/event for weak dealers.

No supplied 2026 VE authority confirms these as current targets.

---

## Source-derived module — Customer Centric Leadership And Moments
_Reconstruction module: `B08` / `CUSTOMER_CENTRIC_LEADERSHIP_AND_MOMENTS.md`_

## Customer centricity is tension management

Three tensions from the source:
- stability vs change;
- openness vs privacy;
- close vs professional.

A strong customer system resolves these tensions deliberately rather than choosing one extreme.

## Trust foundations

`Empathy + Effective Communication + Psychological Safety`.

Operational translation:
- understand need/emotion before designing treatment;
- communicate clearly and verify understanding;
- create an environment where customer/team can surface truth without fear.

## Satisfaction is not the end state

NPS distinguishes Promoter, Passive and Detractor. The source also emphasizes emotional + rational/business needs and CASH expectations:
`Convenience, Action, Speed, Hassle Free`.

## Power moments

Design customer/dealer/people experience around critical moments:
- **Elevation** - make ordinary interaction noticeably better.
- **Insight** - help someone realize something important quickly.
- **Pride** - recognize achievement/identity.
- **Connection** - create shared meaning/relationship.

Potential dealer moments:
- first inquiry;
- test ride;
- credit approval/problem;
- unit delivery;
- first service;
- complaint recovery;
- loyalty milestone;
- staff/dealer achievement.

## Decision rule

Do not optimize every touchpoint equally. Find moments with disproportionate effect on confidence, loyalty, action or advocacy, then design the mechanism and evidence.

---

## Deep module files

- [[../modules/B07__CRM_CUSTOMER_INTELLIGENCE_OPERATING_SYSTEM|CRM CUSTOMER INTELLIGENCE OPERATING SYSTEM]]
- [[../modules/B07__CUSTOMER_FOCUS_LOYALTY_AND_EXPERIENCE|CUSTOMER FOCUS LOYALTY AND EXPERIENCE]]
- [[../modules/B07__LEADS_MANAGEMENT_END_TO_END|LEADS MANAGEMENT END TO END]]
- [[../modules/B06__BTL_ACTIVITY_OPERATING_SYSTEM|BTL ACTIVITY OPERATING SYSTEM]]
- [[../modules/B06__BTL_VE_CUSTOMER_ACTIVATION_SYNTHESIS|BTL VE CUSTOMER ACTIVATION SYNTHESIS]]
- [[../modules/B06__VE_CUSTOMER_INSIGHT_2025|VE CUSTOMER INSIGHT 2025]]
- [[../modules/B06__VE_CUSTOMER_JOURNEY_AND_PLATFORM|VE CUSTOMER JOURNEY AND PLATFORM]]
- [[../modules/B06__VIRTUAL_EXHIBITION_LEADS_OPERATING_SYSTEM|VIRTUAL EXHIBITION LEADS OPERATING SYSTEM]]
- [[../modules/B08__CUSTOMER_CENTRIC_LEADERSHIP_AND_MOMENTS|CUSTOMER CENTRIC LEADERSHIP AND MOMENTS]]
