# Currentness & Supersession Model

Some WorkDesk knowledge is stable; some is only valid for a specific period.

## Memory classes

### STABLE_FRAMEWORK
Examples: PDCA/PICA reasoning structures, when supported by source and not superseded.

### VERSIONED_STANDARD
Examples: NOS version/year, current formal operating standards.

### TIME_BOUND_OPERATIONAL_FACT
Examples: monthly sales-support/MSW, price list, campaign eligibility, claim deadlines.

### HISTORICAL_BUSINESS_DATA
Examples: prior-month Polreg, retail, stock snapshot, historical program.

### CURRENT_SNAPSHOT
Latest available operational state, always tagged with `as_of`.

## Resolver rule

For a query about period `T`:

1. resolve the requested period explicitly;
2. select only sources effective for `T`;
3. apply revisions/updates that supersede overlapping earlier versions;
4. reject files explicitly marked not applicable / not valid;
5. prefer the highest-authority applicable source;
6. if a conflict remains, return `UNRESOLVED`;
7. never use today's program to explain an older period unless the source proves continuity.

## Fast-reference rule

Quick-reference images may help humans sell/remember a program, but formal Juklak/official source controls when there is a conflict.
