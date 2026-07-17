---
project_id: DREADY
project_name: D-READY
repository_visibility: PUBLIC
content_policy: PUBLIC_SAFE_SANITIZED_ONLY
last_updated: 2026-07-17
---
document_status: ACTIVE_REFERENCE_CANDIDATE

# D-READY Data Contract

## 1. Canonical Grains

### Sales

```text
Report Date × Dealer × Type × Base Color
```

### Stock

```text
Snapshot Date × Dealer × Type × Base Color
```

### Monthly Target

```text
Month × Dealer × Type
```

### Historical Color Sales

```text
Historical Period × Dealer × Type × Base Color
```

### Color Contribution

```text
Contribution Profile × Dealer Scope × Type × Base Color
```

## 2. Keys

### Dealer

Use a governed dealer code. Dealer name is a display attribute.

### Product

Use type code as the stable product key.

### Color

Use governed base-color code after raw source mapping.

### Date

Store report date, target month, and stock snapshot date explicitly.

## 3. Required Fields

Every fact row must identify its source, reporting period, grain keys, numeric value, and load timestamp.

## 4. Null and Zero

- zero is a valid business value;
- blank means unavailable or not applicable;
- unmapped is not equivalent to zero;
- missing source total must fail validation rather than silently becoming zero.

## 5. Duplicate Rule

A duplicate at the canonical fact grain is an error unless the source contract explicitly permits additive rows and the transformation groups them deterministically.

## 6. Unmapped Rule

Unmapped dealer, type, or color records must be surfaced in a data-quality output with raw value, source, period, and record count.

## 7. Reconciliation Rule

Mapped color detail must reconcile to the authoritative type total. Variance beyond the approved tolerance blocks promotion.

## 8. All Dealer

All Dealer is a filter context, not a physical dealer member in the target model.

## 9. Public Safety

This contract intentionally excludes real dealer identities, internal file paths, commercial values, and raw source samples.
