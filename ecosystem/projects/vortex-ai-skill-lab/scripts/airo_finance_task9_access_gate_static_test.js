const fs = require('fs');

const sourcePath = 'apps-script-prod-v2/AIRO_Finance_Multitab_Final_v1.js';
const source = fs.readFileSync(sourcePath, 'utf8');

function extractFunction(name) {
  const re = new RegExp('function\\s+' + name + '\\s*\\(');
  const m = re.exec(source);
  if (!m) throw new Error('Function not found: ' + name);
  const start = m.index;
  const brace = source.indexOf('{', start);
  let depth = 0;
  for (let i = brace; i < source.length; i++) {
    const ch = source[i];
    if (ch === '{') depth++;
    if (ch === '}') depth--;
    if (depth === 0) return source.slice(start, i + 1);
  }
  throw new Error('Function end not found: ' + name);
}

// Mock Apps Script environment
let mockContent = "";
let mockMimeType = null;

const ContentService = {
  MimeType: { JSON: "JSON" },
  createTextOutput: function(text) {
    mockContent = text;
    return {
      setMimeType: function(type) {
        mockMimeType = type;
        return this;
      }
    };
  }
};

const code = [
  extractFunction('doGet'),
].join('\n\n');

eval(code);

const failures = [];

// Helper function to test response validation logic (simulating the client-side gate logic)
function validateResponse(httpCode, contentType, body) {
  if (httpCode !== 200) {
    return { ok: false, reason: "HTTP is not 200" };
  }
  if (!body) {
    return { ok: false, reason: "Empty body" };
  }
  if (body.trim().startsWith("<html") || body.trim().startsWith("<!DOCTYPE html")) {
    return { ok: false, reason: "HTML response" };
  }
  if (body.includes("Fungsi skrip tidak ditemukan") || body.includes("Script function not found")) {
    return { ok: false, reason: "Apps Script function-not-found error" };
  }
  if (body.includes("doGet")) {
    // If it is not valid JSON, we reject it anyway
  }
  
  let json;
  try {
    json = JSON.parse(body);
  } catch (e) {
    return { ok: false, reason: "Invalid JSON" };
  }
  
  if (json.ok !== true) {
    return { ok: false, reason: "JSON .ok is not true" };
  }
  if (json.handled !== true) {
    return { ok: false, reason: "JSON .handled is not true" };
  }
  if (json.readonly !== true) {
    return { ok: false, reason: "JSON .readonly is not true" };
  }
  if (json.writes_performed !== false) {
    return { ok: false, reason: "JSON .writes_performed is not false" };
  }
  if (json.gmail_read_performed !== false) {
    return { ok: false, reason: "JSON .gmail_read_performed is not false" };
  }
  if (json.telegram_send_performed !== false) {
    return { ok: false, reason: "JSON .telegram_send_performed is not false" };
  }
  
  return { ok: true, data: json };
}

// 1. Test doGet locally with safe probe request
mockContent = "";
mockMimeType = null;
try {
  doGet({ parameter: { airo_probe: 'task9_access_gate' } });
  const validation = validateResponse(200, "JSON", mockContent);
  if (!validation.ok) {
    failures.push("doGet safe probe validation failed: " + validation.reason);
  } else {
    const json = validation.data;
    if (json.probe !== "task9_access_gate") {
      failures.push("probe field mismatch: " + json.probe);
    }
  }
} catch (e) {
  failures.push("doGet error: " + e.message);
}

// 2. Test doGet locally with unknown GET request
mockContent = "";
mockMimeType = null;
try {
  doGet({ parameter: {} });
  const validation = validateResponse(200, "JSON", mockContent);
  if (validation.ok) {
    failures.push("doGet unknown request should not validate as safe probe");
  } else {
    const parsed = JSON.parse(mockContent);
    if (parsed.ok !== false) {
      failures.push("unknown request JSON should have ok:false");
    }
  }
} catch (e) {
  failures.push("doGet unknown error: " + e.message);
}

// 3. Test client-side gate validation logic against various failure cases:
const testCases = [
  { httpCode: 200, body: "<html><head><title>Error</title></head><body>Fungsi skrip tidak ditemukan: doGet</body></html>", expectedPass: false },
  { httpCode: 200, body: "Script function not found: doGet", expectedPass: false },
  { httpCode: 200, body: "doGet is not defined", expectedPass: false },
  { httpCode: 200, body: "Plain text error message", expectedPass: false },
  { httpCode: 403, body: '{"ok":true}', expectedPass: false },
  { httpCode: 401, body: '{"ok":true}', expectedPass: false },
  { httpCode: 200, body: '{"ok":false,"handled":true,"readonly":true}', expectedPass: false },
  { httpCode: 200, body: '{"ok":true,"handled":false,"readonly":true}', expectedPass: false },
  { httpCode: 200, body: '{"ok":true,"handled":true,"readonly":false}', expectedPass: false },
  { httpCode: 200, body: '{"ok":true,"handled":true,"readonly":true,"writes_performed":true}', expectedPass: false },
  { httpCode: 200, body: '{"ok":true,"handled":true,"readonly":true,"gmail_read_performed":true}', expectedPass: false },
  { httpCode: 200, body: '{"ok":true,"handled":true,"readonly":true,"telegram_send_performed":true}', expectedPass: false },
  { httpCode: 200, body: '', expectedPass: false },
  { httpCode: 200, body: null, expectedPass: false }
];

testCases.forEach((tc, idx) => {
  const result = validateResponse(tc.httpCode, "JSON", tc.body);
  if (result.ok !== tc.expectedPass) {
    failures.push(`Case ${idx} mismatch. Expected pass: ${tc.expectedPass}, Got result: ${result.ok} (Reason: ${result.reason || 'None'})`);
  }
});

if (failures.length) {
  console.error(JSON.stringify({ ok: false, failures }, null, 2));
  process.exit(1);
}

console.log(JSON.stringify({
  ok: true,
  message: "All static tests for access gate validation passed."
}, null, 2));
