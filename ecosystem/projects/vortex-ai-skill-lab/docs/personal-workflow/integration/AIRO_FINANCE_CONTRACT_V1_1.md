# AIRO Finance Contract v1.1

Status: implemented.

## Added coverage

- `nabung 5000 ke blu` -> Rp5.000, category `tabungan`, account/payment `BLU BCA`
- `nabung 5rb ke blu` -> Rp5.000
- `nabung 5 ribu ke blu` -> Rp5.000
- `nabung 5k ke blu` -> Rp5.000
- `tarik cash 50000 dari blu` -> Rp50.000, category `cash_withdrawal`, payment `BLU BCA`
- `topup gopay 20rb dari blu` -> Rp20.000, category `ewallet_topup`, payment `BLU BCA`

## Guardrail

All validation uses temp DB first. Production Telegram smoke is not part of this patch.
