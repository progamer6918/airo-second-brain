import re
from typing import Optional, Dict, Any, List
from .insights import FinanceInsightsService
from .telegram_capture import format_idr

class FinanceHermesReadAdapter:
    """
    Read-Only Adapter bridging AIRO Hermes with Finance Intelligence Read Layer.
    STRICT DATA BOUNDARY:
    - Zero write authority (No INSERT, UPDATE, DELETE).
    - Stateless: does not maintain separate state.
    - Pure fact provider for Hermes reasoning and presentation.
    """
    INTENT_MONTHLY_SUMMARY = "MONTHLY_SPENDING_SUMMARY"
    INTENT_TOP_CATEGORY = "TOP_CATEGORY_SPENDING"
    INTENT_SPENDING_ANOMALY = "SPENDING_ANOMALY_CHECK"
    INTENT_COMPARATIVE_ANALYSIS = "COMPARATIVE_ANALYSIS"
    INTENT_SAFE_TO_SPEND = "SAFE_TO_SPEND"
    INTENT_WEEKLY_RECAP = "WEEKLY_RECAP"
    INTENT_NET_WORTH = "NET_WORTH"
    INTENT_ASSETS = "ASSETS_SUMMARY"
    INTENT_LIABILITIES = "LIABILITIES_SUMMARY"
    INTENT_UPCOMING_COMMITMENTS = "UPCOMING_COMMITMENTS"
    INTENT_SUBCATEGORY_SPENDING = "SUBCATEGORY_SPENDING"
    INTENT_CREDIT_CARD_STATUS = "CREDIT_CARD_STATUS"
    INTENT_FINANCIAL_POSITION = "FINANCIAL_POSITION"
    INTENT_UNKNOWN = "UNKNOWN_INTENT"

    SUPPORTED_INTENTS = [
        INTENT_MONTHLY_SUMMARY,
        INTENT_TOP_CATEGORY,
        INTENT_SPENDING_ANOMALY,
        INTENT_COMPARATIVE_ANALYSIS,
        INTENT_SAFE_TO_SPEND,
        INTENT_WEEKLY_RECAP,
        INTENT_NET_WORTH,
        INTENT_ASSETS,
        INTENT_LIABILITIES,
        INTENT_UPCOMING_COMMITMENTS,
        INTENT_SUBCATEGORY_SPENDING,
        INTENT_CREDIT_CARD_STATUS,
        INTENT_FINANCIAL_POSITION
    ]


    def __init__(self, insights_service: FinanceInsightsService):
        self.insights = insights_service

    # ====================================================
    # 1. Intent Resolution
    # ====================================================
    def resolve_intent(self, query_text: str) -> str:
        """
        Deterministically maps natural language query to supported finance intents.
        """
        text = (query_text or "").lower().strip()
        if not text:
            return self.INTENT_UNKNOWN

        # Comparative Intent Patterns
        comparison_patterns = [
            r"bandingkan",
            r"komparasi",
            r"perbandingan"
        ]
        for pat in comparison_patterns:
            if re.search(pat, text):
                return self.INTENT_COMPARATIVE_ANALYSIS

        # Anomaly Intent Patterns
        anomaly_patterns = [
            r"tidak\s+biasa",
            r"anomali",
            r"mencurigakan",
            r"boros\s+tidak\s+wajar",
            r"tak\s+biasa",
            r"kejanggalan"
        ]
        for pat in anomaly_patterns:
            if re.search(pat, text):
                return self.INTENT_SPENDING_ANOMALY

        # Top Category Intent Patterns
        top_cat_patterns = [
            r"kategori.*(terbesar|paling\s+besar|besar|paling\s+boros|tertinggi|utama)",
            r"top\s+kategori",
            r"belanja\s+terbanyak",
            r"pengeluaran\s+terbanyak"
        ]
        for pat in top_cat_patterns:
            if re.search(pat, text):
                return self.INTENT_TOP_CATEGORY

        # Safe-to-Spend Intent Patterns (Phase 2.2)
        safe_to_spend_patterns = [
            r"uang\s+aman",
            r"aman.*gajian",
            r"safe\s*to\s*spend",
            r"sisa\s+aman",
            r"jatah\s+harian",
            r"bisa\s+belanja\s+berapa",
            r"boleh\s+jajan\s+berapa",
            r"uang\s+bebas",
            r"/safetospend"
        ]
        for pat in safe_to_spend_patterns:
            if re.search(pat, text):
                return self.INTENT_SAFE_TO_SPEND

        # Weekly Finance Recap Intent Patterns (Phase 2.3 Package B)
        weekly_recap_patterns = [
            r"rekap\s+minggu\s+ini",
            r"evaluasi\s+mingguan",
            r"pengeluaran\s+7\s+hari\s+terakhir",
            r"belanja\s+7\s+hari\s+terakhir",
            r"pengeluaran\s+minggu\s+ini",
            r"pengeluaran\s+mingguan",
            r"belanja\s+minggu\s+ini",
            r"rekap\s+mingguan",
            r"weekly\s*recap",
            r"/rekap",
            r"/weekly"
        ]
        for pat in weekly_recap_patterns:
            if re.search(pat, text):
                return self.INTENT_WEEKLY_RECAP

        # Net Worth Intent Patterns (Phase 3 Foundation)
        net_worth_patterns = [
            r"kekayaan\s+bersih",
            r"net\s*worth",
            r"total\s+kekayaan",
            r"posisi\s+kekayaan",
            r"nilai\s+bersih",
            r"/networth"
        ]
        for pat in net_worth_patterns:
            if re.search(pat, text):
                return self.INTENT_NET_WORTH

        # Assets Intent Patterns
        assets_patterns = [
            r"(daftar|ringkasan|total|posisi)\s+aset",
            r"aset\s+(saya|dimiliki)",
            r"harta\s+(benda|saya|tetap)",
            r"/assets"
        ]
        for pat in assets_patterns:
            if re.search(pat, text):
                return self.INTENT_ASSETS

        # Liabilities Intent Patterns
        liabilities_patterns = [
            r"(daftar|ringkasan|total|posisi)\s+(utang|hutang|liabilitas|pinjaman|cicilan)",
            r"kewajiban\s+finansial",
            r"/liabilities"
        ]
        for pat in liabilities_patterns:
            if re.search(pat, text):
                return self.INTENT_LIABILITIES

        # Upcoming Commitments Intent Patterns
        commitments_patterns = [
            r"(komitmen|tagihan)\s+(mendatang|rutin|bulan\s+ini|siklus\s+ini)",
            r"daftar\s+tagihan",
            r"upcoming\s+commitments",
            r"/commitments",
            r"/tagihan"
        ]
        for pat in commitments_patterns:
            if re.search(pat, text):
                return self.INTENT_UPCOMING_COMMITMENTS

        # Subcategory Spending Intent Patterns
        subcat_patterns = [
            r"subkategori",
            r"detail\s+belanja",
            r"rincian\s+kategori",
            r"pengeluaran\s+subkategori",
            r"/subkategori"
        ]
        for pat in subcat_patterns:
            if re.search(pat, text):
                return self.INTENT_SUBCATEGORY_SPENDING

        # Credit Card Status Intent Patterns
        cc_patterns = [
            r"kartu\s+kredit",
            r"tagihan\s+cc",
            r"limit\s+cc",
            r"status\s+cc",
            r"/cc",
            r"credit\s*card"
        ]
        for pat in cc_patterns:
            if re.search(pat, text):
                return self.INTENT_CREDIT_CARD_STATUS

        # Financial Position Patterns
        position_patterns = [
            r"posisi\s+keuangan",
            r"ringkasan\s+keuangan",
            r"financial\s+position",
            r"/position"
        ]
        for pat in position_patterns:
            if re.search(pat, text):
                return self.INTENT_FINANCIAL_POSITION

        # Monthly Spending Summary Patterns
        summary_patterns = [
            r"pengeluaran\s+(bulan\s+ini|saat\s+ini)",
            r"berapa\s+pengeluaran",
            r"total\s+belanja",
            r"rekap\s+bulan\s+ini",
            r"summary\s+bulan\s+ini",
            r"cashflow\s+bulan\s+ini",
            r"sisa\s+uang\s+bulan\s+ini",
            r"kondisi\s+(finansial|keuangan)"
        ]
        for pat in summary_patterns:
            if re.search(pat, text):
                return self.INTENT_MONTHLY_SUMMARY

        return self.INTENT_UNKNOWN

    # ====================================================
    # 2. Intent Handlers (Facts & Context for Hermes)
    # ====================================================
    def get_monthly_spending_summary(self, year: Optional[int] = None, month: Optional[int] = None) -> Dict[str, Any]:
        summary = self.insights.get_monthly_summary(year, month)
        data = {
            "period": summary.period,
            "total_expense": summary.total_expense,
            "total_income": summary.total_income,
            "net_cashflow": summary.net_cashflow,
            "transaction_count": summary.transaction_count,
            "formatted_expense": format_idr(summary.total_expense),
            "formatted_income": format_idr(summary.total_income),
            "formatted_cashflow": format_idr(summary.net_cashflow)
        }
        context_str = (
            f"Fakta Finansial Periode {summary.period}: "
            f"Total pengeluaran tercatat {format_idr(summary.total_expense)} "
            f"dari {summary.transaction_count} transaksi, "
            f"total pemasukan {format_idr(summary.total_income)}, "
            f"sehingga net cashflow saat ini {format_idr(summary.net_cashflow)}."
        )
        return {
            "intent": self.INTENT_MONTHLY_SUMMARY,
            "status": "SUCCESS",
            "data": data,
            "context_for_hermes": context_str
        }

    def get_top_category_spending(self, year: Optional[int] = None, month: Optional[int] = None) -> Dict[str, Any]:
        report = self.insights.get_category_spending(year, month)
        
        if not report.categories or report.total_expense == 0.0:
            return {
                "intent": self.INTENT_TOP_CATEGORY,
                "status": "SUCCESS",
                "data": {
                    "period": report.period,
                    "top_category": None,
                    "amount": 0.0,
                    "percentage": 0.0,
                    "transaction_count": 0,
                    "formatted_amount": format_idr(0.0),
                    "all_categories_count": 0
                },
                "context_for_hermes": f"Belum ada transaksi pengeluaran tercatat pada periode {report.period}."
            }

        # Categories are already sorted by total_amount DESC in FinanceInsightsService
        top = report.categories[0]
        data = {
            "period": report.period,
            "top_category": top.category_name,
            "amount": top.total_amount,
            "percentage": top.percentage,
            "transaction_count": top.transaction_count,
            "formatted_amount": format_idr(top.total_amount),
            "all_categories_count": len(report.categories)
        }
        context_str = (
            f"Kategori pengeluaran terbesar periode {report.period} adalah "
            f"'{top.category_name}' dengan nominal {format_idr(top.total_amount)} "
            f"({top.percentage}% dari total pengeluaran {format_idr(report.total_expense)})."
        )
        return {
            "intent": self.INTENT_TOP_CATEGORY,
            "status": "SUCCESS",
            "data": data,
            "context_for_hermes": context_str
        }

    def get_spending_anomaly_check(self, year: Optional[int] = None, month: Optional[int] = None) -> Dict[str, Any]:
        anomalies = self.insights.get_spending_anomalies(year, month)
        period_str = self.insights._format_period(year, month)
        
        anomaly_dicts = [a.to_dict() for a in anomalies]
        has_anomaly = len(anomalies) > 0

        if has_anomaly:
            descriptions = "; ".join(a.description for a in anomalies)
            context_str = (
                f"Ditemukan {len(anomalies)} indikasi anomali pada periode {period_str}: {descriptions}"
            )
        else:
            context_str = (
                f"Pemeriksaan anomali periode {period_str} menunjukkan pola belanja normal, "
                "tidak ditemukan transaksi tunggal ekstrem atau dominasi kategori yang melebihi ambang batas."
            )

        return {
            "intent": self.INTENT_SPENDING_ANOMALY,
            "status": "SUCCESS",
            "data": {
                "period": period_str,
                "has_anomaly": has_anomaly,
                "anomaly_count": len(anomalies),
                "anomalies": anomaly_dicts
            },
            "context_for_hermes": context_str
        }

    def get_comparative_analysis(self, year: Optional[int] = None, month: Optional[int] = None) -> Dict[str, Any]:
        summary = self.insights.get_monthly_summary(year, month)
        accounts = self.insights.get_account_overview()
        
        data = {
            "available_facts": {
                "current_period": summary.period,
                "total_expense": summary.total_expense,
                "total_income": summary.total_income,
                "net_cashflow": summary.net_cashflow,
                "total_liquid_balance": accounts.total_liquid_balance,
                "formatted_expense": format_idr(summary.total_expense),
                "formatted_income": format_idr(summary.total_income),
                "formatted_liquid_balance": format_idr(accounts.total_liquid_balance)
            },
            "limitations": [
                "Data historis perbandingan antar-bulan (multi-month historical data) belum tersedia.",
                "Benchmark komparatif eksternal tidak diintegrasikan untuk menjaga kemurnian fakta tanpa asumsi."
            ]
        }
        context_str = (
            f"Fakta yang tersedia untuk periode {summary.period}: "
            f"Total pengeluaran {format_idr(summary.total_expense)}, "
            f"pemasukan {format_idr(summary.total_income)}, dan total saldo likuid {format_idr(accounts.total_liquid_balance)}. "
            "Batasan: Data perbandingan historis antar-bulan masa lalu belum tersedia di sistem saat ini, "
            "sehingga perbandingan komparatif belum dapat dilakukan tanpa membuat asumsi atau tebakan."
        )
        return {
            "intent": self.INTENT_COMPARATIVE_ANALYSIS,
            "status": "LIMITATION_STATED",
            "data": data,
            "context_for_hermes": context_str
        }

    def get_safe_to_spend_report(self, as_of: Optional[str] = None) -> Dict[str, Any]:
        """
        Deterministically retrieves Safe-to-Spend calculations from FinanceInsightsService.
        ZERO LLM arithmetic, ZERO database writes, pure factual reporting.
        """
        report = self.insights.get_safe_to_spend_report(as_of)
        data = {
            "as_of_date": report.as_of_date,
            "liquid_balance": report.total_liquid_balance,
            "unpaid_obligations": report.unpaid_obligations_this_cycle,
            "safety_floor": report.safety_floor,
            "safe_to_spend": report.safe_to_spend,
            "payday_runway": report.payday_runway_days,
            "daily_allowance": report.daily_safe_allowance,
            "days_to_payday": report.days_to_payday,
            "next_payday_date": report.next_payday_date,
            "payday_day": report.payday_day,
            "status": report.status,
            "deficit_amount": report.deficit_amount,
            "total_active_obligations": report.total_active_obligations,
            "paid_obligations": report.paid_obligations_this_cycle,
            "formatted_liquid_balance": format_idr(report.total_liquid_balance),
            "formatted_unpaid_obligations": format_idr(report.unpaid_obligations_this_cycle),
            "formatted_safety_floor": format_idr(report.safety_floor),
            "formatted_safe_to_spend": format_idr(report.safe_to_spend),
            "formatted_daily_allowance": format_idr(report.daily_safe_allowance),
            "obligations": [o.to_dict() for o in report.obligations]
        }

        if report.status == "SAFE":
            context_str = (
                f"Fakta Posisi Kas & Safe-to-Spend (per {report.as_of_date}): "
                f"Total saldo kas likuid {format_idr(report.total_liquid_balance)}, "
                f"komitmen tagihan belum dibayar siklus ini {format_idr(report.unpaid_obligations_this_cycle)}, "
                f"dan batas cadangan aman (safety floor) {format_idr(report.safety_floor)}. "
                f"Dana aman belanja (Safe-to-Spend) Anda saat ini adalah {format_idr(report.safe_to_spend)}, "
                f"dengan jatah harian aman {format_idr(report.daily_safe_allowance)}/hari "
                f"untuk {report.days_to_payday} hari menuju gajian ({report.next_payday_date}). "
                f"Estimasi payday runway adalah {report.payday_runway_days} hari."
            )
        else:
            context_str = (
                f"Fakta Posisi Kas & Safe-to-Spend (per {report.as_of_date}): "
                f"Total saldo kas likuid {format_idr(report.total_liquid_balance)}, "
                f"komitmen tagihan belum dibayar siklus ini {format_idr(report.unpaid_obligations_this_cycle)}, "
                f"dan batas cadangan aman (safety floor) {format_idr(report.safety_floor)}. "
                f"Status kas saat ini mengalami DEFISIT sebesar {format_idr(report.deficit_amount)}, "
                f"sehingga dana aman belanja (Safe-to-Spend) adalah {format_idr(0.0)} "
                f"dan jatah harian aman adalah {format_idr(0.0)}/hari. "
                f"Sisa {report.days_to_payday} hari menuju gajian ({report.next_payday_date})."
            )

        return {
            "intent": self.INTENT_SAFE_TO_SPEND,
            "status": "SUCCESS",
            "data": data,
            "context_for_hermes": context_str
        }

    # ====================================================
    # 3. Telegram Single Response Card Formatting
    # ====================================================
    def format_safe_to_spend_telegram_card(self, as_of: Optional[str] = None) -> str:
        """
        Formats deterministic Safe-to-Spend calculations into a single Telegram HTML card.
        """
        report = self.insights.get_safe_to_spend_report(as_of)
        if report.status == "SAFE":
            status_badge = "🟢 <b>STATUS: AMAN (SAFE)</b>"
            main_line = f"✨ <b>Safe-to-Spend:</b> {format_idr(report.safe_to_spend)}"
        else:
            status_badge = f"🔴 <b>STATUS: DEFISIT ({format_idr(report.deficit_amount)})</b>"
            main_line = f"⚠️ <b>Safe-to-Spend:</b> {format_idr(0.0)} (Defisit: {format_idr(report.deficit_amount)})"

        runway_desc = f"{report.payday_runway_days} hari" if report.payday_runway_days < 999 else "Aman (>30 hari)"

        card = (
            f"🛡️ <b>Safe-to-Spend Report</b>\n"
            f"{status_badge}\n"
            f"───────────────────\n"
            f"💰 <b>Saldo Kas Likuid:</b> {format_idr(report.total_liquid_balance)}\n"
            f"📌 <b>Tagihan Siklus Ini:</b> {format_idr(report.unpaid_obligations_this_cycle)}\n"
            f"🛑 <b>Safety Floor:</b> {format_idr(report.safety_floor)}\n"
            f"───────────────────\n"
            f"{main_line}\n"
            f"💵 <b>Jatah Harian:</b> {format_idr(report.daily_safe_allowance)} / hari\n"
            f"📅 <b>Sisa Hari s.d. Gajian:</b> {report.days_to_payday} hari ({report.next_payday_date})\n"
            f"⏳ <b>Payday Runway:</b> {runway_desc}\n"
            f"───────────────────\n"
            f"<i>Kalkulasi deterministik Python murni • Nol halusinasi LLM.</i>"
        )
        return card

    def get_weekly_recap_report(self, as_of: Optional[str] = None) -> Dict[str, Any]:
        """
        Deterministically retrieves Weekly Finance Recap calculations from FinanceInsightsService.
        ZERO LLM arithmetic, ZERO database writes, pure factual reporting.
        """
        report = self.insights.get_weekly_recap_report(as_of)
        
        largest_dict = report.largest_expense.to_dict() if report.largest_expense else None
        
        data = {
            "as_of_date": report.as_of_date,
            "start_date": report.start_date,
            "end_date": report.end_date,
            "period": f"{report.start_date} s.d. {report.end_date}",
            "total_expense": report.total_expense,
            "total_income": report.total_income,
            "net_cashflow": report.net_cashflow,
            "daily_burn_rate": report.daily_burn_rate,
            "expense_count": report.expense_count,
            "income_count": report.income_count,
            "transfer_count": report.transfer_count,
            "top_category_name": report.top_category_name,
            "top_category_amount": report.top_category_amount,
            "top_category_percentage": report.top_category_percentage,
            "largest_expense": largest_dict,
            "total_liquid_balance": report.total_liquid_balance,
            "safe_to_spend": report.safe_to_spend,
            "days_to_payday": report.days_to_payday,
            "daily_safe_allowance": report.daily_safe_allowance,
            "safe_to_spend_status": report.safe_to_spend_status,
            "formatted_total_expense": format_idr(report.total_expense),
            "formatted_total_income": format_idr(report.total_income),
            "formatted_net_cashflow": format_idr(report.net_cashflow),
            "formatted_daily_burn_rate": format_idr(report.daily_burn_rate),
            "formatted_liquid_balance": format_idr(report.total_liquid_balance),
            "formatted_safe_to_spend": format_idr(report.safe_to_spend),
            "categories": [c.to_dict() for c in report.categories]
        }

        top_cat_desc = f"{report.top_category_name} ({format_idr(report.top_category_amount)}, {report.top_category_percentage}%)" if report.top_category_name else "Belum ada pengeluaran"
        largest_desc = f"{format_idr(report.largest_expense.amount)} ({report.largest_expense.note or report.largest_expense.category_name})" if report.largest_expense else "-"

        context_str = (
            f"Fakta Rekap Finansial Mingguan (Periode {report.start_date} s.d. {report.end_date}): "
            f"Total belanja 7 hari terakhir {format_idr(report.total_expense)} ({report.expense_count} transaksi), "
            f"total pemasukan {format_idr(report.total_income)}, "
            f"sehingga net cashflow mingguan {format_idr(report.net_cashflow)}. "
            f"Rata-rata pengeluaran harian (daily burn rate) {format_idr(report.daily_burn_rate)}/hari. "
            f"Kategori belanja terbesar: {top_cat_desc}. "
            f"Transaksi pengeluaran terbesar: {largest_desc}. "
            f"Snapshot saldo kas likuid saat ini {format_idr(report.total_liquid_balance)}, "
            f"dengan Safe-to-Spend aktif {format_idr(report.safe_to_spend)} ({report.days_to_payday} hari s.d. gajian)."
        )

        return {
            "intent": self.INTENT_WEEKLY_RECAP,
            "status": "SUCCESS",
            "data": data,
            "context_for_hermes": context_str
        }

    def format_weekly_recap_telegram_card(self, as_of: Optional[str] = None) -> str:
        """
        Formats deterministic Weekly Finance Recap into a single Telegram HTML card.
        """
        report = self.insights.get_weekly_recap_report(as_of)
        
        top_cat_str = f"{report.top_category_name} ({format_idr(report.top_category_amount)} • {report.top_category_percentage}%)" if report.top_category_name else "-"
        
        if report.largest_expense:
            note_str = f" ({report.largest_expense.note})" if report.largest_expense.note else ""
            largest_str = f"{format_idr(report.largest_expense.amount)}{note_str}"
        else:
            largest_str = "-"

        sts_badge = "🟢 AMAN" if report.safe_to_spend_status == "SAFE" else "🔴 DEFISIT"
        net_cashflow_badge = f"+{format_idr(report.net_cashflow)}" if report.net_cashflow >= 0 else f"-{format_idr(abs(report.net_cashflow))}"

        card = (
            f"📊 <b>Weekly Finance Recap</b>\n"
            f"🗓️ <code>{report.start_date} s.d. {report.end_date}</code> (7 Hari)\n"
            f"───────────────────\n"
            f"💸 <b>Total Belanja:</b> {format_idr(report.total_expense)} ({report.expense_count} tx)\n"
            f"💰 <b>Pemasukan:</b> {format_idr(report.total_income)}\n"
            f"⚖️ <b>Net Cashflow:</b> {net_cashflow_badge}\n"
            f"🔥 <b>Rata-rata Harian:</b> {format_idr(report.daily_burn_rate)} / hari\n"
            f"───────────────────\n"
            f"🏷️ <b>Kategori Terbesar:</b> {top_cat_str}\n"
            f"📌 <b>Transaksi Terbesar:</b> {largest_str}\n"
            f"───────────────────\n"
            f"🏦 <b>Saldo Kas Likuid:</b> {format_idr(report.total_liquid_balance)}\n"
            f"🛡️ <b>Safe-to-Spend:</b> {format_idr(report.safe_to_spend)} ({sts_badge}, {report.days_to_payday} hari s.d. gajian)\n"
            f"───────────────────\n"
            f"<i>Kalkulasi deterministik Python murni • Nol halusinasi LLM.</i>"
        )
        return card

    # ====================================================
    # Phase 3 Foundation: Net Worth, Assets, Liabilities, Commitments Handlers
    # ====================================================
    def get_net_worth(self, as_of: Optional[str] = None) -> Dict[str, Any]:
        report = self.insights.get_net_worth_report(as_of)
        data = {
            "as_of_date": report.as_of_date,
            "total_liquid_balance": report.total_liquid_balance,
            "total_assets_value": report.total_assets_value,
            "total_liabilities_remaining": report.total_liabilities_remaining,
            "net_worth": report.net_worth,
            "active_accounts_count": report.active_accounts_count,
            "active_assets_count": report.active_assets_count,
            "active_liabilities_count": report.active_liabilities_count,
            "monthly_liability_payments": report.monthly_liability_payments,
            "formatted_liquid_balance": format_idr(report.total_liquid_balance),
            "formatted_assets_value": format_idr(report.total_assets_value),
            "formatted_liabilities_remaining": format_idr(report.total_liabilities_remaining),
            "formatted_net_worth": format_idr(report.net_worth),
            "formatted_monthly_payments": format_idr(report.monthly_liability_payments)
        }
        context_str = (
            f"Fakta Posisi Kekayaan Bersih (Net Worth per {report.as_of_date}): "
            f"Total saldo kas likuid {format_idr(report.total_liquid_balance)} ({report.active_accounts_count} akun), "
            f"total estimasi nilai aset fisik/tetap {format_idr(report.total_assets_value)} ({report.active_assets_count} item), "
            f"total sisa pokok liabilitas/utang {format_idr(report.total_liabilities_remaining)} ({report.active_liabilities_count} kewajiban). "
            f"Total Kekayaan Bersih (Net Worth) adalah {format_idr(report.net_worth)}. "
            f"Beban cicilan bulanan tercatat {format_idr(report.monthly_liability_payments)}/bulan."
        )
        return {
            "intent": self.INTENT_NET_WORTH,
            "status": "SUCCESS",
            "data": data,
            "context_for_hermes": context_str
        }

    def format_net_worth_telegram_card(self, as_of: Optional[str] = None) -> str:
        report = self.insights.get_net_worth_report(as_of)
        card = (
            f"🏛️ <b>Net Worth Report</b>\n"
            f"🗓️ <code>Per {report.as_of_date}</code>\n"
            f"───────────────────\n"
            f"💵 <b>Kas Likuid:</b> {format_idr(report.total_liquid_balance)} ({report.active_accounts_count} akun)\n"
            f"🏠 <b>Total Aset:</b> {format_idr(report.total_assets_value)} ({report.active_assets_count} aset)\n"
            f"💳 <b>Total Liabilitas:</b> {format_idr(report.total_liabilities_remaining)} ({report.active_liabilities_count} kewajiban)\n"
            f"───────────────────\n"
            f"💎 <b>Kekayaan Bersih:</b> {format_idr(report.net_worth)}\n"
            f"📅 <b>Beban Cicilan Bulanan:</b> {format_idr(report.monthly_liability_payments)} / bulan\n"
            f"───────────────────\n"
            f"<i>Kalkulasi deterministik Python murni • Nol halusinasi LLM.</i>"
        )
        return card

    def get_assets_summary(self) -> Dict[str, Any]:
        summary = self.insights.get_assets_summary()
        summary["formatted_total_assets_value"] = format_idr(summary["total_assets_value"])
        for a in summary["assets"]:
            a["formatted_value"] = format_idr(a["current_value"])
        context_str = (
            f"Fakta Registry Aset: Terdaftar {summary['asset_count']} aset non-kas "
            f"dengan total estimasi nilai {format_idr(summary['total_assets_value'])}."
        )
        return {
            "intent": self.INTENT_ASSETS,
            "status": "SUCCESS",
            "data": summary,
            "context_for_hermes": context_str
        }

    def format_assets_telegram_card(self) -> str:
        summary = self.insights.get_assets_summary()
        lines = [
            "🏠 <b>Daftar & Ringkasan Aset</b>",
            "───────────────────"
        ]
        if not summary["assets"]:
            lines.append("<i>Belum ada data aset non-kas yang dicatat.</i>")
        else:
            for a in summary["assets"]:
                lines.append(f"• <b>{a['name']}</b> ({a['type']}): {format_idr(a['current_value'])}")
        lines.append("───────────────────")
        lines.append(f"💎 <b>Total Estimasi Nilai Aset:</b> {format_idr(summary['total_assets_value'])}")
        lines.append("<i>Data metadata non-transaksional • Tidak mengubah buku kas.</i>")
        return "\n".join(lines)

    def get_liabilities_summary(self) -> Dict[str, Any]:
        summary = self.insights.get_liabilities_summary()
        summary["formatted_total_liabilities_remaining"] = format_idr(summary["total_liabilities_remaining"])
        summary["formatted_total_monthly_payment"] = format_idr(summary["total_monthly_payment"])
        for l in summary["liabilities"]:
            l["formatted_remaining"] = format_idr(l["remaining_amount"])
            l["formatted_monthly"] = format_idr(l["monthly_payment"])
        context_str = (
            f"Fakta Registry Liabilitas: Terdaftar {summary['liability_count']} kewajiban jangka panjang "
            f"dengan total sisa pokok {format_idr(summary['total_liabilities_remaining'])} "
            f"dan total beban cicilan bulanan {format_idr(summary['total_monthly_payment'])}/bulan."
        )
        return {
            "intent": self.INTENT_LIABILITIES,
            "status": "SUCCESS",
            "data": summary,
            "context_for_hermes": context_str
        }

    def format_liabilities_telegram_card(self) -> str:
        summary = self.insights.get_liabilities_summary()
        lines = [
            "💳 <b>Daftar & Ringkasan Liabilitas</b>",
            "───────────────────"
        ]
        if not summary["liabilities"]:
            lines.append("<i>Tidak ada liabilitas/kewajiban aktif yang tercatat.</i>")
        else:
            for l in summary["liabilities"]:
                due_info = f"tgl {l['due_day']}" if l.get("due_day") else "-"
                lines.append(f"• <b>{l['name']}</b>: sisa {format_idr(l['remaining_amount'])} (cicilan {format_idr(l['monthly_payment'])}, jatuh tempo {due_info})")
        lines.append("───────────────────")
        lines.append(f"📌 <b>Total Sisa Pokok:</b> {format_idr(summary['total_liabilities_remaining'])}")
        lines.append(f"📅 <b>Total Cicilan per Bulan:</b> {format_idr(summary['total_monthly_payment'])}")
        lines.append("<i>Data kewajiban jangka panjang • Dilunasi via pencatatan transaksi manual/rutin.</i>")
        return "\n".join(lines)

    def get_upcoming_commitments(self, as_of: Optional[str] = None) -> Dict[str, Any]:
        report = self.insights.get_safe_to_spend_report(as_of)
        data = {
            "as_of_date": report.as_of_date,
            "next_payday_date": report.next_payday_date,
            "days_to_payday": report.days_to_payday,
            "unpaid_obligations": report.unpaid_obligations_this_cycle,
            "total_obligations": report.total_active_obligations,
            "formatted_unpaid_obligations": format_idr(report.unpaid_obligations_this_cycle),
            "formatted_total_obligations": format_idr(report.total_active_obligations),
            "obligations": [o.to_dict() for o in report.obligations]
        }
        context_str = (
            f"Fakta Upcoming Commitments (siklus s.d. {report.next_payday_date}): "
            f"Total komitmen tagihan terdaftar {format_idr(report.total_active_obligations)}, "
            f"dengan tagihan belum dibayar sebesar {format_idr(report.unpaid_obligations_this_cycle)} "
            f"menuju gajian dalam {report.days_to_payday} hari."
        )
        return {
            "intent": self.INTENT_UPCOMING_COMMITMENTS,
            "status": "SUCCESS",
            "data": data,
            "context_for_hermes": context_str
        }

    def format_upcoming_commitments_telegram_card(self, as_of: Optional[str] = None) -> str:
        report = self.insights.get_safe_to_spend_report(as_of)
        lines = [
            "📅 <b>Upcoming Commitments (Tagihan Rutin)</b>",
            f"🗓️ <code>Siklus s.d. Gajian ({report.next_payday_date})</code>",
            "───────────────────"
        ]
        if not report.obligations:
            lines.append("<i>Belum ada komitmen/tagihan rutin terdaftar.</i>")
        else:
            for o in report.obligations:
                status_icon = "✅" if o.is_paid_this_cycle else "⏳"
                status_text = "LUNAS" if o.is_paid_this_cycle else "BELUM BAYAR"
                lines.append(f"{status_icon} <b>{o.name}</b>: {format_idr(o.amount)} (tgl {o.due_day}) - {status_text}")
        lines.append("───────────────────")
        lines.append(f"📌 <b>Belum Dibayar Siklus Ini:</b> {format_idr(report.unpaid_obligations_this_cycle)}")
        lines.append(f"💰 <b>Total Komitmen Rutin:</b> {format_idr(report.total_active_obligations)}")
        lines.append("<i>Sinkron dengan Safe-to-Spend engine.</i>")
        return "\n".join(lines)

    # ====================================================
    # Phase 3.1: Subcategory, Credit Card & Financial Position Handlers
    # ====================================================
    def get_spending_by_subcategory(self, period: Optional[str] = None) -> Dict[str, Any]:
        report = self.insights.get_spending_by_subcategory(period)
        for item in report["breakdown"]:
            item["formatted_amount"] = format_idr(item["total_amount"])
        context_str = (
            f"Fakta Subkategori Periode {report['period']}: "
            f"Total pengeluaran tercatat {format_idr(report['total_expense'])} "
            f"terdistribusi ke dalam {report['breakdown_count']} subkategori."
        )
        return {
            "intent": self.INTENT_SUBCATEGORY_SPENDING,
            "status": "SUCCESS",
            "data": report,
            "context_for_hermes": context_str
        }

    def format_subcategory_telegram_card(self, period: Optional[str] = None) -> str:
        res = self.get_spending_by_subcategory(period)
        report = res["data"]
        lines = [
            f"📂 <b>Rincian Pengeluaran Subkategori</b>",
            f"🗓️ <code>Periode: {report['period']}</code>",
            "───────────────────"
        ]
        if not report["breakdown"]:
            lines.append("<i>Belum ada data pengeluaran dengan subkategori pada periode ini.</i>")
        else:
            for b in report["breakdown"][:8]:
                lines.append(f"• <b>{b['category_name']} / {b['subcategory_name']}</b>: {b['formatted_amount']} ({b['percentage']}%)")
        lines.append("───────────────────")
        lines.append(f"💰 <b>Total Pengeluaran:</b> {format_idr(report['total_expense'])}")
        return "\n".join(lines)

    def get_credit_card_status(self) -> Dict[str, Any]:
        summary = self.insights.get_credit_card_summary()
        context_str = (
            f"Fakta Kartu Kredit: {summary['card_count']} kartu terdaftar, "
            f"total limit {format_idr(summary['total_limit'])}, "
            f"saldo terpakai {format_idr(summary['total_balance'])} ({summary['overall_utilization_rate']}%), "
            f"sisa limit tersedia {format_idr(summary['total_available_credit'])}, "
            f"dan {summary['unpaid_statements_count']} tagihan belum dibayar senilai {format_idr(summary['total_unpaid_statement_amount'])}."
        )
        return {
            "intent": self.INTENT_CREDIT_CARD_STATUS,
            "status": "SUCCESS",
            "data": summary,
            "context_for_hermes": context_str
        }

    def format_credit_card_telegram_card(self) -> str:
        summary = self.insights.get_credit_card_summary()
        lines = [
            "💳 <b>Status Portofolio Kartu Kredit</b>",
            "───────────────────"
        ]
        if not summary["cards"]:
            lines.append("<i>Tidak ada kartu kredit yang terdaftar.</i>")
        else:
            for c in summary["cards"]:
                lines.append(
                    f"• <b>{c['name']} ({c['bank_name']})</b>\n"
                    f"  Terpakai: {format_idr(c['current_balance'])} / {format_idr(c['credit_limit'])} ({c['utilization_rate']}%)\n"
                    f"  Sisa Limit: {format_idr(c['available_credit'])} (Jatuh tempo tgl {c['payment_due_day']})"
                )
        lines.append("───────────────────")
        lines.append(f"📊 <b>Total Limit:</b> {format_idr(summary['total_limit'])}")
        lines.append(f"📉 <b>Total Terpakai:</b> {format_idr(summary['total_balance'])} ({summary['overall_utilization_rate']}%)")
        lines.append(f"💰 <b>Tersedia:</b> {format_idr(summary['total_available_credit'])}")
        if summary["unpaid_statements"]:
            lines.append(f"⚠️ <b>Tagihan Belum Lunas:</b> {format_idr(summary['total_unpaid_statement_amount'])} ({summary['unpaid_statements_count']} lembar)")
        return "\n".join(lines)

    def get_financial_position(self, as_of: Optional[str] = None) -> Dict[str, Any]:
        data = self.insights.get_financial_position(as_of)
        nw = data["net_worth"]
        sts = data["safe_to_spend"]
        cc = data["credit_cards"]
        context_str = (
            f"Fakta Posisi Keuangan per {data['as_of']}: "
            f"Kekayaan Bersih {format_idr(nw['net_worth'])} (Saldo Likuid: {format_idr(nw['total_liquid_balance'])}), "
            f"Safe-to-Spend {format_idr(sts.get('safe_to_spend', 0.0))} (Jatah Harian: {format_idr(sts.get('daily_safe_allowance', 0.0))}), "
            f"dan Saldo Kartu Kredit Terpakai {format_idr(cc['total_balance'])}."
        )
        return {
            "intent": self.INTENT_FINANCIAL_POSITION,
            "status": "SUCCESS",
            "data": data,
            "context_for_hermes": context_str
        }

    def format_financial_position_telegram_card(self, as_of: Optional[str] = None) -> str:
        data = self.insights.get_financial_position(as_of)
        nw = data["net_worth"]
        sts = data["safe_to_spend"]
        cc = data["credit_cards"]
        lines = [
            "🧭 <b>Ringkasan Posisi Keuangan AIRO</b>",
            f"🗓️ <code>As of: {data['as_of']}</code>",
            "───────────────────",
            f"🏛️ <b>Kekayaan Bersih (Net Worth):</b> {format_idr(nw['net_worth'])}",
            f"  • Saldo Likuid: {format_idr(nw['total_liquid_balance'])}",
            f"  • Nilai Aset: {format_idr(nw['total_assets_value'])}",
            f"  • Sisa Liabilitas: {format_idr(nw['total_liabilities_remaining'])}",
            "───────────────────",
            f"🛡️ <b>Safe-to-Spend (s.d. Gajian):</b> {format_idr(sts.get('safe_to_spend', 0.0))}",
            f"  • Jatah Harian: {format_idr(sts.get('daily_safe_allowance', 0.0))}/hari ({sts.get('days_to_payday', 0)} hari lagi)",
            f"  • Tagihan Belum Dibayar: {format_idr(sts.get('unpaid_obligations_this_cycle', 0.0))}",
            "───────────────────",
            f"💳 <b>Kartu Kredit:</b>",
            f"  • Terpakai: {format_idr(cc['total_balance'])} ({cc['overall_utilization_rate']}%)",
            f"  • Sisa Limit: {format_idr(cc['total_available_credit'])}",
            "───────────────────",
            "<i>Semua angka diverifikasi secara deterministic dari ledger AIRO Finance.</i>"
        ]
        return "\n".join(lines)

    # ====================================================
    # 4. Main Query Dispatcher
    # ====================================================
    def handle_query(self, query_text: str, year: Optional[int] = None, month: Optional[int] = None) -> Dict[str, Any]:
        """
        High-level dispatcher for Hermes to pass user question and retrieve
        factual financial context.
        """
        intent = self.resolve_intent(query_text)
        
        if intent == self.INTENT_MONTHLY_SUMMARY:
            return self.get_monthly_spending_summary(year, month)
        elif intent == self.INTENT_TOP_CATEGORY:
            return self.get_top_category_spending(year, month)
        elif intent == self.INTENT_SPENDING_ANOMALY:
            return self.get_spending_anomaly_check(year, month)
        elif intent == self.INTENT_COMPARATIVE_ANALYSIS:
            return self.get_comparative_analysis(year, month)
        elif intent == self.INTENT_SAFE_TO_SPEND:
            return self.get_safe_to_spend_report()
        elif intent == self.INTENT_WEEKLY_RECAP:
            return self.get_weekly_recap_report()
        elif intent == self.INTENT_NET_WORTH:
            return self.get_net_worth()
        elif intent == self.INTENT_ASSETS:
            return self.get_assets_summary()
        elif intent == self.INTENT_LIABILITIES:
            return self.get_liabilities_summary()
        elif intent == self.INTENT_UPCOMING_COMMITMENTS:
            return self.get_upcoming_commitments()
        elif intent == self.INTENT_SUBCATEGORY_SPENDING:
            return self.get_spending_by_subcategory()
        elif intent == self.INTENT_CREDIT_CARD_STATUS:
            return self.get_credit_card_status()
        elif intent == self.INTENT_FINANCIAL_POSITION:
            return self.get_financial_position()
        else:
            return {
                "intent": self.INTENT_UNKNOWN,
                "status": "UNSUPPORTED",
                "data": {},
                "supported_intents": self.SUPPORTED_INTENTS,
                "context_for_hermes": (
                    "Pertanyaan tidak cocok dengan query finansial yang didukung saat ini. "
                    "Query yang didukung: Net worth (kekayaan bersih), posisi keuangan, ringkasan aset, ringkasan liabilitas, kartu kredit, subkategori, "
                    "upcoming commitments / tagihan, Safe-to-Spend / uang aman, rekap mingguan 7 hari, rekap bulanan, kategori terbesar, atau cek anomali belanja."
                )
            }

    # ====================================================
    # 5. Hermes Tool Specification Metadata
    # ====================================================
    def get_hermes_tool_spec(self) -> Dict[str, Any]:
        """
        Returns formal JSON schema representation for AIRO Hermes tool binding.
        """
        return {
            "name": "get_finance_insights",
            "description": (
                "Query authoritative, read-only personal finance facts from Finance Core. "
                "Supports: net-worth (kekayaan bersih), financial-position (posisi keuangan), credit-card-status, subcategory-spending, "
                "assets-summary, liabilities-summary, upcoming-commitments (tagihan), safe-to-spend (uang aman belanja), weekly-recap, monthly spending summary, top category, and spending anomaly check."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "User question or inquiry regarding finance"
                    },
                    "year": {
                        "type": "integer",
                        "description": "Target 4-digit year (optional, defaults to current year)"
                    },
                    "month": {
                        "type": "integer",
                        "description": "Target 1-12 month (optional, defaults to current month)"
                    }
                },
                "required": ["query"]
            }
        }

