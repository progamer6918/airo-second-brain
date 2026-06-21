# AIRO Finance Language Contract v1.0

Status: active.

## Amount units

Bare numbers:

- `1` through `999` mean thousands.
  - `5` = `5000`
  - `50` = `50000`
  - `500` = `500000`
- `1000` and above are exact rupiah.
  - `5000` = `5000`
  - `15000` = `15000`

Suffixes:

- `rb`, `ribu`, `k` mean x1000.
- `jt`, `juta`, `m` mean x1000000.

Decimal/thousands notation:

- `1,5 juta` = `1500000`
- `1.5 juta` = `1500000`
- `1.250.000` = `1250000`

## Accounts

Official accounts:

- BCA
- BLU BCA
- Mandiri
- GoPay
- ShopeePay
- Cash

## Routing

Savings:

- `nabung 5000 ke blu`
- target: `💸 Transactions` and `🥇 Aset`
- category: `tabungan`
- cashflow_treatment: `asset_transfer`
- not `uncategorized`

Internal transfer:

- `transfer 10000 dari bca ke blu`
- not expense
- cashflow_treatment: `internal_transfer`

Cash withdrawal:

- `tarik 5000 dari blu ke cash`
- default: internal transfer BLU BCA -> Cash

Topup:

- default internal transfer unless explicit consumption purpose exists.

Gold:

- gram is canonical quantity.
- gold without price goes to Review Queue.

Ambiguous parser cases go to Review Queue.
