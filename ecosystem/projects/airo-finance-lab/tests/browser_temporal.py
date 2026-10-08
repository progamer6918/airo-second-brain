import sys, json, tempfile, threading, importlib.util, contextlib, io
from pathlib import Path
from http.server import ThreadingHTTPServer
from playwright.sync_api import sync_playwright
import argparse

args_parser = argparse.ArgumentParser()
args_parser.add_argument("--chrome", required=True)
args_parser.add_argument("--output", required=True)
args = args_parser.parse_args()
r = Path(__file__).resolve().parents[1]
base = Path(args.output)
base.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(r / "src"))
spec = importlib.util.spec_from_file_location("finance_dashboard", r / "web/app.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)
from airo_finance_core import temporal as t

checks = []
errors = []
with tempfile.TemporaryDirectory() as tmp:
    e = app.get_engine(tmp + "/db.sqlite")
    app.DashboardRequestHandler.engine = e
    acc = next(a for a in e.list_accounts() if a.account_class != "LIABILITY")
    cat = e.list_categories()[0]
    clock = dict(
        occurred_at="2026-01-07T17:30:00+07:00",
        time_precision="MINUTE",
        time_accuracy="CONFIRMED",
        time_source="OWNER",
    )
    tx = e.create_transaction(
        acc.id,
        12000,
        "EXPENSE",
        category_id=cat.id,
        note="Browser Fixture",
        tx_date="2026-01-07",
        temporal_context=clock,
    )
    cc = e.create_credit_card("Fixture Card", "Fixture Issuer", 1000000)
    stmt = e.create_credit_card_statement(
        cc.id, "2026-01", "2026-01-01", "2026-01-20", 10000, 1000
    )
    liab = e.create_liability(
        "Fixture Loan", "PERSONAL_LOAN", 100000, 100000, 10000, 10
    )
    unknown = e.create_transaction(
        acc.id,
        12000,
        "EXPENSE",
        category_id=cat.id,
        note="Unknown Fixture",
        tx_date="2026-01-07",
    )
    proposal = t.preview(
        e.db,
        [dict(id=unknown.id, temporal=dict(clock, time_accuracy="ESTIMATED"))],
        "Browser recovery preview",
    )
    server = ThreadingHTTPServer(("127.0.0.1", 0), app.DashboardRequestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}"
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=args.chrome, args=["--no-sandbox"])
        for zone in ["Asia/Shanghai", "America/New_York"]:
            ctx = browser.new_context(
                timezone_id=zone,
                viewport=(
                    {"width": 390, "height": 844}
                    if zone == "Asia/Shanghai"
                    else {"width": 1360, "height": 900}
                ),
            )
            page = ctx.new_page()
            page.on("pageerror", lambda err: errors.append(str(err)))
            page.goto(url)
            page.wait_for_function("connection==='ready'")
            label = page.evaluate(
                "(row)=>eventTime(row)", dict(date="2026-01-07", **t.normalize(clock))
            )
            assert "17.30 WIB" in label, label
            checks.append("WIB_display_" + zone)
            page.evaluate("navigate('transactions')")
            page.locator("[data-action=new-tx]").click()
            page.locator("[name=time_mode]").select_option("UNKNOWN")
            page.locator("[name=date]").fill("2026-01-07")
            page.locator("[name=time_mode]").select_option("INPUT")
            page.locator("[name=event_clock]").fill("17:31:12")
            page.locator("[name=time_accuracy]").select_option("ESTIMATED")
            page.locator("[name=amount]").fill("12345")
            page.locator("[name=account_id]").select_option(acc.id)
            page.locator("[name=category_id]").select_option(cat.id)
            page.locator("[name=note]").fill("Browser new " + zone)
            page.locator("#modal button[type=submit]").click()
            page.wait_for_function("!document.querySelector('#modal').open")
            saved = (
                e.db.get_connection()
                .execute(
                    "SELECT * FROM transactions WHERE note=?", ("Browser new " + zone,)
                )
                .fetchone()
            )
            assert saved["time_accuracy"] == "ESTIMATED"
            assert saved["time_precision"] == "SECOND"
            checks.append("manual_create_" + zone)
            page.evaluate("navigate('transactions')")
            page.locator("[data-tx]").filter(has_text="Browser Fixture").first.click()
            assert page.locator("#modal").inner_text().find("Waktu kejadian") >= 0
            page.locator("[data-time-edit]").click()
            page.locator("[name=time_mode]").select_option("INPUT")
            page.locator("[name=event_clock]").fill("18:05")
            page.locator("[name=time_accuracy]").select_option("CONFIRMED")
            balance = e.get_account(acc.id).balance
            page.locator("#modal button[type=submit]").click()
            page.wait_for_function(
                "document.querySelector('#modal-title').textContent.includes('Rekapan waktu')"
            )
            assert e.get_account(acc.id).balance == balance
            page.locator("#modal button[type=submit]").click()
            page.wait_for_function("!document.querySelector('#modal').open")
            assert e.get_account(acc.id).balance == balance
            checks.append("metadata_edit_preview_" + zone)
            page.evaluate("navigate('transactions')")
            page.locator("[data-time-recovery]").click()
            page.locator('[data-time-proposal="' + proposal["id"] + '"]').click()
            page.wait_for_function(
                "document.querySelector('#modal-title').textContent.includes('Rekapan waktu')"
            )
            assert (
                page.locator("#modal").inner_text().find("Browser recovery preview")
                >= 0
            )
            checks.append("historical_preview_" + zone)
            page.screenshot(
                path=str(base / ("browser-" + zone.replace("/", "-") + ".png")),
                full_page=True,
            )
            ctx.close()
        ctx = browser.new_context(timezone_id="America/New_York")
        page = ctx.new_page()
        page.goto(url)
        page.wait_for_function("connection==='ready'")
        page.evaluate("(id)=>manageCreditLineModal(id)", cc.id)
        page.wait_for_function("currentCreditLineData!==null")
        page.evaluate("(args)=>payStatementModal(args[0],args[1])", [cc.id, stmt.id])
        page.locator("[name=payment_date]").fill("2026-01-07")
        page.locator("[name=time_mode]").select_option("INPUT")
        page.locator("[name=event_clock]").fill("17:32")
        page.locator("[name=time_accuracy]").select_option("CONFIRMED")
        page.locator("[name=source_account_id]").select_option(acc.id)
        page.locator("#modal button[type=submit]").click()
        page.wait_for_function(
            "!document.querySelector('#modal').open || document.querySelector('#modal-title').textContent.includes('Kelola')"
        )
        pay = (
            e.db.get_connection()
            .execute(
                "SELECT * FROM credit_card_payments WHERE statement_id=?", (stmt.id,)
            )
            .fetchone()
        )
        assert pay and pay["time_accuracy"] == "CONFIRMED"
        ledger = (
            e.db.get_connection()
            .execute("SELECT * FROM transactions WHERE id=?", (pay["transaction_id"],))
            .fetchone()
        )
        assert ledger["occurred_at"] == pay["occurred_at"]
        checks.append("statement_payment_browser_links_core")
        ctx.close()
        browser.close()
    server.shutdown()
    server.server_close()
    e.db.close()
report = {"checks": checks, "page_errors": errors}
(base / "browser-tests.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report))
assert not errors
