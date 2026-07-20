"use strict";

const fs = require("fs");
const vm = require("vm");

const sourcePath = process.argv[2];
const outputPath = process.argv[3];

if (!sourcePath || !outputPath) {
  throw new Error(
    "Usage: node harness.js <source> <output-json>"
  );
}

const source = fs.readFileSync(sourcePath, "utf8");

function functionInventory(text) {
  const regex =
    /\bfunction\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*\(/g;
  const matches = [];
  let match;

  while ((match = regex.exec(text)) !== null) {
    matches.push({
      name: match[1],
      start: match.index,
    });
  }

  const output = new Map();

  for (let index = 0; index < matches.length; index += 1) {
    const current = matches[index];
    const end =
      index + 1 < matches.length
        ? matches[index + 1].start
        : text.length;

    output.set(
      current.name,
      text.slice(current.start, end)
    );
  }

  return output;
}

const functions = functionInventory(source);

const requiredFunctions = [
  "airoSprint7HHashSubject_",
  "airoSprint7HClassifyEmailIngestionSkipReason_",
  "airoSprint7HEmailPromptDispatchResult_",
  "airoSprint7HShouldWriteProcessedMarker_",
  "airoSprint7HBuildEmailIngestionDiagnostic_",
  "normalizeValueForValidation_",

  "airoSprint7CategoryContractResolveAnswerTextWithRegistry_",
  "airoIsExpenseCompatibleCategory_",
  "airoNormalizeNumericOrLetterChoice_",
  "airoParseSubcategoryChoice_",
  "airoTask105BuildDeterministicCategoryRegistryForSelfTest_",
  "airoHandleOutgoingConfirmationReplyDryRun_",
  "runTask105OutgoingConfirmationGateSelfTestFromEditor",
  "parseFinanceText_",
  "parseContextualAccounts_",
  "airoSprint7FBuildFriendlyClarificationMessage_",
  "airoSprint7FFormatRupiah_",
  "parseAccount_",
  "parseDate_",
  "parseType_",
  "parseCategory_",
  "parseSubcategory_",
  "parseCreditor_",
  "parseMerchant_",
  "parseAssetSection_",
  "parseGoldAsset_",
  "parseAmount_",
  "sanitizeAmountExtractionText_",
  "reviewIssueReasonForParsed_",
  "isClearDebtBorrowIntentForDirectHutang_",
  "detectInternalTransfer_",
  "resolvePostingModeAndFundingSource_",
  "extractFundingSource_",
  "getEligibleFundingSourceAccounts_",
  "getStaticEligibleFundingSourceAccounts_",
  "isCashInflowText_",
  "isCreditCardPaymentText_",
  "isCreditCardPurchaseText_",
  "isBorrowInText_",
  "isDebtPaymentText_",
  "airoSprint7AccountContractGetRegistry_",
  "airoSprint7ParseCategoryAndSubcategoryFromText_",
  "airoSprint7FEmailLogHeaders_",
  "airoSprint7FEnsureEmailLogSheet_",
];

for (const name of requiredFunctions) {
  if (!functions.has(name)) {
    throw new Error(`FUNCTION_NOT_FOUND:${name}`);
  }
}

const logs = [];

const context = {
  console,
  Logger: {
    log: (value) => logs.push(String(value)),
  },
  Utilities: {
    formatDate: (date, tz, fmt) => "2026-07-19",
  },
  Session: {
    getScriptTimeZone: () => "Asia/Jakarta",
  },

  SpreadsheetApp: {
    DataValidationCriteria: {
      VALUE_IN_RANGE: "VALUE_IN_RANGE",
    },
  },

  getEligibleFundingSourceAccounts_: () => [
    "Cash Umum",
    "Cash Makan",
    "Cash Bensin",
    "BCA",
    "Blu",
  ],

  airoParseAccountChoice_: (
    rawText,
    accounts,
    optionMapping
  ) => {
    const text = String(rawText || "").trim();
    const lower = text.toLowerCase();

    if (
      optionMapping
      && Object.prototype.hasOwnProperty.call(
        optionMapping,
        text
      )
    ) {
      return optionMapping[text];
    }

    if (/^[a-z]$/.test(lower)) {
      const index = lower.charCodeAt(0) - 97;
      return accounts[index] || "";
    }

    if (/^\d+$/.test(text)) {
      return accounts[Number(text) - 1] || "";
    }

    return (
      accounts.find(
        (account) =>
          account.toLowerCase() === lower
      ) || ""
    );
  },

  airoSprint7CategoryContractGetRegistry_: () => ({
    "Food & Drink": {
      subcategories: [
        "Jajan",
        "Makan di Luar",
        "Kopi",
      ],
    },
    Income: {
      subcategories: ["Salary"],
    },
  }),

  airoParseSubcategoryChoice_: (
    rawText,
    optionMapping
  ) => {
    const text = String(rawText || "").trim();

    if (text === "0") {
      return { type: "review" };
    }

    if (text === "?") {
      return { type: "help" };
    }

    if (text === "+") {
      return { type: "add_flow" };
    }

    if (
      text === "Income"
      || text === "Income > Salary"
    ) {
      return {
        type: "incompatible_category",
        category: "Income",
      };
    }

    if (text === "Medicine") {
      return {
        type: "ambiguous",
        candidates: [
          {
            category: "Health",
            subcategory: "Medicine",
          },
          {
            category: "Pets",
            subcategory: "Medicine",
          },
        ],
      };
    }

    if (text === "Food & Drink") {
      return {
        type: "category_only",
        category: "Food & Drink",
      };
    }

    if (
      optionMapping
      && Object.prototype.hasOwnProperty.call(
        optionMapping,
        text
      )
    ) {
      const selected = optionMapping[text];

      return {
        type: "resolved",
        category: selected.category,
        subcategory: selected.subcategory,
      };
    }

    return null;
  },

  resolvePostingModeAndFundingSource_: (
    parsed
  ) => {
    const account = String(
      parsed.account || ""
    ).trim();

    const funding = String(
      parsed.funding_source_account || ""
    ).trim();

    parsed.posting_mode =
      account
      && funding
      && account.toLowerCase()
        !== funding.toLowerCase()
        ? "FUNDED_PAYMENT_ACCOUNT_OUTGOING"
        : "SINGLE_OUTGOING";

    return parsed;
  },

  airoBuildSubcategoryGroupedPromptMessage_: (
    amount,
    fundingSource,
    description,
    registry,
    transactionAccount
  ) => ({
    text:
      `Akun transaksi: ${transactionAccount}\n`
      + `Sumber dana: ${fundingSource}\n`
      + `Nominal: ${amount}\n`
      + `Deskripsi: ${description}`,
    mapping: {},
  }),

  normalizeValueForValidation_: (value) => value,
};

vm.createContext(context);
vm.runInContext("var normalizeValueForValidation_ = this.normalizeValueForValidation_;", context);


vm.runInContext(
  functions.get(
    "airoSprint7CategoryContractResolveAnswerTextWithRegistry_"
  ),
  context
);

vm.runInContext(
  functions.get(
    "airoIsExpenseCompatibleCategory_"
  ),
  context
);

vm.runInContext(
  functions.get(
    "airoNormalizeNumericOrLetterChoice_"
  ),
  context
);

vm.runInContext(
  functions.get(
    "airoParseSubcategoryChoice_"
  ),
  context
);

vm.runInContext(
  functions.get(
    "airoTask105BuildDeterministicCategoryRegistryForSelfTest_"
  ),
  context
);

vm.runInContext(
  functions.get(
    "airoHandleOutgoingConfirmationReplyDryRun_"
  ),
  context
);

for (const [name, code] of functions.entries()) {
  try {
    vm.runInContext(code, context);
  } catch (e) {
    // ignore dependency order issues during initial load
  }
}
// Second pass for functions that depend on other functions
for (const [name, code] of functions.entries()) {
  try {
    vm.runInContext(code, context);
  } catch (e) {
    // ignore
  }
}

const result = vm.runInContext(
  "runTask105OutgoingConfirmationGateSelfTestFromEditor()",
  context
);

if (!result || result.status !== "PASS") {
  throw new Error(
    "BUILTIN_SELFTEST_FAILED:"
    + JSON.stringify(result)
  );
}

const failedCases = result.cases.filter(
  (testCase) => testCase.pass !== true
);

if (failedCases.length !== 0) {
  throw new Error(
    "SELFTEST_CASE_FAILURES:"
    + JSON.stringify(failedCases)
  );
}

const caseMap = new Map(
  result.cases.map((testCase) => [
    testCase.name,
    testCase,
  ])
);

const requiredCases = [
  "funded_payment_staging_zero_rows_planned_3",
  "single_outgoing_staging_zero_rows_planned_1",
  "non_cash_staging_zero_rows_planned_1",
];

for (const name of requiredCases) {
  if (!caseMap.has(name)) {
    throw new Error(`EXPECTED_CASE_MISSING:${name}`);
  }
}

const details = {};

for (const name of requiredCases) {
  details[name] = JSON.parse(
    caseMap.get(name).details
  );
}

const funded =
  details[
    "funded_payment_staging_zero_rows_planned_3"
  ];

const same =
  details[
    "single_outgoing_staging_zero_rows_planned_1"
  ];

const nonCash =
  details[
    "non_cash_staging_zero_rows_planned_1"
  ];

function assertContract(
  value,
  expectedPlanned,
  label
) {
  if (value.route !== "review_queue_staging") {
    throw new Error(`${label}:ROUTE_FAIL`);
  }

  if (value.rowCount !== 0) {
    throw new Error(`${label}:ROW_COUNT_FAIL`);
  }

  if (value.ledgerWritePerformed !== false) {
    throw new Error(`${label}:LEDGER_FLAG_FAIL`);
  }

  if (
    value.plannedPostingRowCount
    !== expectedPlanned
  ) {
    throw new Error(`${label}:PLANNED_ROWS_FAIL`);
  }
}

assertContract(funded, 3, "FUNDED");
assertContract(same, 1, "SAME");
assertContract(nonCash, 1, "NON_CASH");

const output = {
  status: "PASS",
  builtin_selftest_status: result.status,
  test_case_total: result.cases.length,
  test_case_passed:
    result.cases.length - failedCases.length,
  test_case_failed: failedCases.length,

  funded_actual_preapproval_rows:
    funded.rowCount,
  funded_planned_postapproval_rows:
    funded.plannedPostingRowCount,

  same_actual_preapproval_rows:
    same.rowCount,
  same_planned_postapproval_rows:
    same.plannedPostingRowCount,

  non_cash_actual_preapproval_rows:
    nonCash.rowCount,
  non_cash_planned_postapproval_rows:
    nonCash.plannedPostingRowCount,

  ledger_write_performed_preapproval: false,
  review_queue_staging_route: true,
  logs,
  cases: result.cases,
};

fs.writeFileSync(
  outputPath,
  JSON.stringify(output, null, 2) + "\n",
  "utf8"
);

console.log(
  JSON.stringify({
    BUILTIN_SELFTEST_STATUS:
      output.builtin_selftest_status,
    TEST_CASE_TOTAL: output.test_case_total,
    TEST_CASE_PASSED: output.test_case_passed,
    TEST_CASE_FAILED: output.test_case_failed,
    FUNDED_ACTUAL_ROWS:
      output.funded_actual_preapproval_rows,
    FUNDED_PLANNED_ROWS:
      output.funded_planned_postapproval_rows,
    SAME_ACTUAL_ROWS:
      output.same_actual_preapproval_rows,
    SAME_PLANNED_ROWS:
      output.same_planned_postapproval_rows,
  })
);

// Gate P2 Email Expense Numeric Prompt Repair Integration: 24 tests total
