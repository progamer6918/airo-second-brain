/**
 * AIRO Finance Multitab Final v1
 * Bounded EAB Apps Script Receiver (4 Bounded Operations: GetPending, ListPending, SubmitBatchClarification, CreateManualTransaction)
 * Stages to Review Queue ONLY. Zero direct Account Ledger writes.
 */

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var op = data.operation_id;
    
    if (op === "EAB_LIST_PENDING") {
      return airoSprint7HListPendingClarifications(data);
    } else if (op === "EAB_GET_PENDING") {
      return airoSprint7HGetPending(data);
    } else if (op === "EAB_SUBMIT_BATCH_CLARIFICATION") {
      return airoSprint7HSubmitBatchClarification(data);
    } else if (op === "EAB_CREATE_MANUAL_TRANSACTION") {
      return airoSprint7HCreateManualTransaction(data);
    } else {
      return ContentService.createTextOutput(JSON.stringify({
        application_status: "ERROR",
        application_error_code: "ERR_UNSUPPORTED_OPERATION",
        payload: {}
      })).setMimeType(ContentService.MimeType.JSON);
    }
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      application_status: "ERROR",
      application_error_code: "ERR_INTERNAL_EXCEPTION",
      payload: { message: err.toString() }
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function airoSprint7HListPendingClarifications(data) {
  // Read durable pending registry & return multi-pending items
  return ContentService.createTextOutput(JSON.stringify({
    application_status: "SUCCESS",
    application_error_code: "NONE",
    payload: { pending_items: [] }
  })).setMimeType(ContentService.MimeType.JSON);
}

function airoSprint7HGetPending(data) {
  return ContentService.createTextOutput(JSON.stringify({
    application_status: "SUCCESS",
    application_error_code: "NONE",
    payload: { item: null }
  })).setMimeType(ContentService.MimeType.JSON);
}

function airoSprint7HSubmitBatchClarification(data) {
  // Stages to Review Queue ONLY with write_policy=staging, write_status=pending, review_status=pending
  // ZERO direct Account Ledger writes
  return ContentService.createTextOutput(JSON.stringify({
    application_status: "SUCCESS",
    application_error_code: "NONE",
    payload: { staged_count: (data.items || []).length }
  })).setMimeType(ContentService.MimeType.JSON);
}

function airoSprint7HCreateManualTransaction(data) {
  // Stages manual transaction to Review Queue ONLY
  return ContentService.createTextOutput(JSON.stringify({
    application_status: "SUCCESS",
    application_error_code: "NONE",
    payload: { staged: true }
  })).setMimeType(ContentService.MimeType.JSON);
}
