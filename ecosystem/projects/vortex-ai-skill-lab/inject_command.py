from pathlib import Path

path = Path("scripts/personal-workflow/apps-script/airo_finance_multitab_final_v1.gs")
text = path.read_text(encoding="utf-8")

old = """function handleSpecialFinanceCommand_(rawText, chatId) {
  const text = String(rawText || '').toLowerCase().trim();"""

new = """function handleSpecialFinanceCommand_(rawText, chatId) {
  const text = String(rawText || '').toLowerCase().trim();

  if (/^admin\\s+read\\s+live\\s+audit\\s+split/i.test(text)) {
    const ss = SpreadsheetApp.openById(getProp_('SPREADSHEET_ID'));
    const needles = ["test cash umum", "test cash bensin"];
    const tabs = ["💵 Cash Ledger", "📒 Account Ledger"];
    const result = {};

    tabs.forEach(tab => {
      const sheet = getSheetLoose_(ss, tab);
      if (!sheet) {
        result[tab] = { error: "NOT_FOUND" };
        return;
      }
      const values = sheet.getDataRange().getValues();
      const headers = values[0] || [];
      const matching = [];

      for (let r = 1; r < values.length; r++) {
        const row = values[r];
        const joined = row.map(v => String(v || '').toLowerCase()).join(' ');
        if (needles.some(n => joined.indexOf(n) >= 0)) {
          matching.push({
            row: r + 1,
            values: row.map(v => String(v || '').trim())
          });
        }
      }
      result[tab] = {
        headers: headers.map(v => String(v || '').trim()),
        matching: matching
      };
    });

    return {
      handled: true,
      ok: true,
      command: 'admin_read_live_audit_split',
      result: result
    };
  }"""

if old not in text:
    raise SystemExit("ABORT: handleSpecialFinanceCommand_ not found")

text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
print("SUCCESSFULLY_INJECTED")
