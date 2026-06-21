# AIRO Finance V1.2 Batch D Final PASS

Generated: 2026-05-24T10:10:39+07:00

## Runtime Regression
```text
TASK=airo_finance_clarification_regression_all
DEPLOYMENT_ID=AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA
CC_R1={"ok":true,"clarification_requested":true,"clarification_type":"cc_ambiguous","amount":100928,"category":"Lainnya","account":"Credit Card"}
CC_R2={"handled":true,"cancelled":true}
DEBT_R1={"ok":true,"clarification_requested":true,"clarification_type":"debt_ambiguous","amount":100928,"category":"Hutang","account":"Unknown"}
DEBT_R2={"handled":true,"cancelled":true}
GOLD_R1={"ok":true,"clarification_requested":true,"clarification_type":"asset_gold_ambiguous","amount":0,"category":"Aset","account":"Unknown"}
GOLD_R2={"ok":true,"handled":true,"status":"ignored","clarification_type":"asset_gold_ambiguous"}
RESULT_CC=PASS
RESULT_DEBT=PASS
RESULT_ASSET_GOLD=PASS
FINAL_RESULT=PASS
```

## Deployment
```text
- AKfycbzu0Kuu9sNcCHHmZ1dj2sPW1Y4tZz9KUi8tG_ySeA-QY65yOPA9m3NYiEQcS8uKZYjuOA @178 - AIRO Finance deploy 20260524_095450
```

## Final Status
PASS. Credit Card, Debt/Hutang, and Asset/Gold ambiguous clarification flows are runtime-verified.
