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
    INTENT_UNKNOWN = "UNKNOWN_INTENT"

    SUPPORTED_INTENTS = [
        INTENT_MONTHLY_SUMMARY,
        INTENT_TOP_CATEGORY,
        INTENT_SPENDING_ANOMALY,
        INTENT_COMPARATIVE_ANALYSIS
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

        # Monthly Spending Summary Patterns
        summary_patterns = [
            r"pengeluaran\s+(bulan\s+ini|minggu\s+ini|saat\s+ini)",
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

    # ====================================================
    # 3. Main Query Dispatcher
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
        else:
            return {
                "intent": self.INTENT_UNKNOWN,
                "status": "UNSUPPORTED",
                "data": {},
                "supported_intents": self.SUPPORTED_INTENTS,
                "context_for_hermes": (
                    "Pertanyaan tidak cocok dengan query finansial yang didukung saat ini. "
                    "Query yang didukung: rekap pengeluaran bulanan, kategori terbesar, atau cek anomali belanja."
                )
            }

    # ====================================================
    # 4. Hermes Tool Specification Metadata
    # ====================================================
    def get_hermes_tool_spec(self) -> Dict[str, Any]:
        """
        Returns formal JSON schema representation for AIRO Hermes tool binding.
        """
        return {
            "name": "get_finance_insights",
            "description": (
                "Query authoritative, read-only personal finance facts from Finance Core. "
                "Supports: monthly spending summary, top category, and spending anomaly check."
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
