# Virtual Exhibition Leads Operating System

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
