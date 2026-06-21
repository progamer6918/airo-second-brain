const fs = require("fs");
const vm = require("vm");

const source = fs.readFileSync(
  "apps-script-live/AIRO_Finance_Multitab_Final_v1.js",
  "utf8"
);

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function functionBlock(name) {
  const marker = new RegExp(
    "\\bfunction\\s+" +
    name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") +
    "\\s*\\([^)]*\\)\\s*\\{"
  );

  const match = marker.exec(source);

  assert(match, `Function not found: ${name}`);

  const braceStart = source.indexOf("{", match.index);
  let depth = 0;
  let quote = null;
  let escaped = false;

  for (let i = braceStart; i < source.length; i++) {
    const char = source[i];

    if (quote) {
      if (escaped) {
        escaped = false;
      } else if (char === "\\") {
        escaped = true;
      } else if (char === quote) {
        quote = null;
      }
      continue;
    }

    if (["'", '"', "`"].includes(char)) {
      quote = char;
      continue;
    }

    if (char === "{") depth++;
    if (char === "}") depth--;

    if (depth === 0) {
      return source.slice(match.index, i + 1);
    }
  }

  throw new Error(`Unclosed function: ${name}`);
}

assert(
  source.includes("AIRO_TASK614_APPROVAL_STABLE_ID_V1"),
  "Task 6.14 marker missing"
);

const fallback = functionBlock(
  "airoSprint7HResolveToReviewQueueFallback_"
);

assert(
  (
    fallback.match(
      /airoTask614StoreDirectApproval_/g
    ) || []
  ).length === 2,
  "Direct approval target must be stored in both fallback branches"
);

assert(
  fallback.includes(
    "Balas /approval untuk langsung menyetujui transaksi ini."
  ),
  "Fallback reply still uses old approval copy"
);

const list = functionBlock(
  "airoSprint7HApprovalList_"
);

assert(
  list.includes(
    "airoTask614StoreApprovalSnapshot_"
  ),
  "Approval list does not create stable snapshot"
);

const approve = functionBlock(
  "airoSprint7HApprovalApprove_"
);

assert(
  approve.includes(
    "airoTask614FindReviewItemByQueueId_"
  ),
  "Approve cannot resolve exact queue_id"
);

const route = functionBlock(
  "airoSprint7HApprovalCommandMaybeHandleRoute_"
);

assert(
  route.includes(
    "airoTask614GetDirectApprovalQueueId_"
  ),
  "Bare /approval is not direct approval"
);

assert(
  route.includes(
    "airoTask614ResolveApprovalArg_"
  ),
  "Numeric approval does not use snapshot"
);

assert(
  route.includes(
    'command: "approval_" + (cmd || "direct")'
  ),
  "Bare /approval is still reported as help"
);

const memory = {};

global.PropertiesService = {
  getScriptProperties() {
    return {
      getProperty(key) {
        return Object.prototype.hasOwnProperty.call(
          memory,
          key
        )
          ? memory[key]
          : null;
      },
      setProperty(key, value) {
        memory[key] = String(value);
      },
      deleteProperty(key) {
        delete memory[key];
      }
    };
  }
};

[
  "airoTask614DirectApprovalPropertyKey_",
  "airoTask614SnapshotPropertyKey_",
  "airoTask614ReadJsonProperty_",
  "airoTask614StoreDirectApproval_",
  "airoTask614GetDirectApprovalQueueId_",
  "airoTask614StoreApprovalSnapshot_",
  "airoTask614ResolveApprovalArg_"
].forEach((name) => {
  vm.runInThisContext(
    functionBlock(name),
    {
      filename:
        "task614-helper-" + name + ".js"
    }
  );
});

const queue1 = "review:emc:first";
const queue2 = "review:emc:second";

assert(
  airoTask614StoreDirectApproval_(
    "8482041086",
    queue1,
    3
  ) === true,
  "Failed to store direct approval target"
);

assert(
  airoTask614GetDirectApprovalQueueId_(
    "8482041086"
  ) === queue1,
  "Direct approval queue_id mismatch"
);

airoTask614StoreApprovalSnapshot_(
  "8482041086",
  [
    { queue_id: queue1 },
    { queue_id: queue2 }
  ]
);

assert(
  airoTask614ResolveApprovalArg_(
    "8482041086",
    "1"
  ) === queue1,
  "Snapshot item 1 mismatch"
);

assert(
  airoTask614ResolveApprovalArg_(
    "8482041086",
    "1"
  ) === queue1,
  "Repeated item 1 changed target"
);

assert(
  airoTask614ResolveApprovalArg_(
    "8482041086",
    "2"
  ) === queue2,
  "Snapshot item 2 mismatch"
);

assert(
  airoTask614ResolveApprovalArg_(
    "unknown-chat",
    "1"
  ) === "__AIRO_TASK614_SNAPSHOT_REQUIRED__",
  "Numeric approval without list must be blocked"
);

console.log(
  JSON.stringify({
    ok: true,
    task: "6.14",
    mode: "approval_ux_static_test",
    bare_approval_stable_id: true,
    numeric_snapshot_stable: true,
    repeated_numeric_safe: true,
    write_performed: false
  })
);
