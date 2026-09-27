#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/airo_office_engine.py — Unified Autonomous Office Suite Engine for AIRO Hermes.

Provides programmatic compilation of structured data into executive-grade Office documents:
- PowerPoint (.pptx) via python-pptx / airo_presentation_engine
- Excel (.xlsx) via openpyxl with executive styling, auto-fit columns, zebra stripes, and number formatting
- Word (.docx) via python-docx with typographic hierarchy, callout boxes, and executive tables
"""

import os
import sys
import logging
from typing import List, Dict, Any, Optional, Union

# Re-export PowerPoint builder from canonical presentation engine
from airo_presentation_engine import (
    PresentationEngine,
    build_dynamic_deck,
    build_airo_pitch_deck
)

logger = logging.getLogger("airo-office-engine")


# ─── EXCEL ENGINE (openpyxl) ──────────────────────────────────────────────────

def build_dynamic_xlsx(
    output_path: str,
    title: str,
    headers: List[str],
    rows: List[List[Any]],
    sheet_name: str = "Executive Summary",
    summary: Optional[Dict[str, Any]] = None
) -> str:
    """
    Builds a beautifully styled, executive-grade Excel spreadsheet (.xlsx).
    Features:
    - Dark Navy (#161E30) header row with crisp white bold text
    - Subtle zebra striping on alternating rows
    - Professional thin grid borders (#D1D5DB)
    - Auto-detection and formatting of numeric / currency values
    - Dynamic column width auto-fitting
    - Top title banner with metadata
    """
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet_name[:31]  # Excel limits sheet names to 31 chars

    # Palette
    NAVY_FILL = PatternFill(start_color="161E30", end_color="161E30", fill_type="solid")
    ACCENT_FILL = PatternFill(start_color="00E5FF", end_color="00E5FF", fill_type="solid")
    ZEBRA_FILL = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    WHITE_FILL = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

    FONT_TITLE = Font(name="Segoe UI", size=14, bold=True, color="161E30")
    FONT_SUBTITLE = Font(name="Segoe UI", size=10, italic=True, color="6B7280")
    FONT_HEADER = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    FONT_BODY = Font(name="Segoe UI", size=10, color="1F2937")
    FONT_BODY_BOLD = Font(name="Segoe UI", size=10, bold=True, color="1F2937")

    THIN_BORDER_SIDE = Side(border_style="thin", color="E2E8F0")
    BORDER_CELL = Border(left=THIN_BORDER_SIDE, right=THIN_BORDER_SIDE, top=THIN_BORDER_SIDE, bottom=THIN_BORDER_SIDE)

    current_row = 1

    # 1. Title Banner
    ws.cell(row=current_row, column=1, value=title).font = FONT_TITLE
    current_row += 1
    ws.cell(row=current_row, column=1, value="Disusun secara otomatis oleh AIRO Hermes Autonomous Operating System").font = FONT_SUBTITLE
    current_row += 2  # Blank row separation

    # 2. Optional Key Metrics / Summary Cards
    if summary and isinstance(summary, dict):
        ws.cell(row=current_row, column=1, value="IKHTISAR UTAMA").font = Font(name="Segoe UI", size=10, bold=True, color="00E5FF")
        current_row += 1
        for k, v in summary.items():
            ws.cell(row=current_row, column=1, value=str(k)).font = FONT_BODY_BOLD
            ws.cell(row=current_row, column=2, value=str(v)).font = FONT_BODY
            current_row += 1
        current_row += 1

    # 3. Table Headers
    header_row_idx = current_row
    num_cols = len(headers)
    for col_idx, h_text in enumerate(headers, start=1):
        cell = ws.cell(row=header_row_idx, column=col_idx, value=str(h_text))
        cell.font = FONT_HEADER
        cell.fill = NAVY_FILL
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER_CELL

    ws.row_dimensions[header_row_idx].height = 28
    current_row += 1

    # 4. Table Data Rows
    for r_idx, row_data in enumerate(rows):
        is_even = (r_idx % 2 == 1)
        row_fill = ZEBRA_FILL if is_even else WHITE_FILL
        ws.row_dimensions[current_row].height = 20

        for col_idx in range(1, num_cols + 1):
            val = row_data[col_idx - 1] if col_idx - 1 < len(row_data) else ""
            cell = ws.cell(row=current_row, column=col_idx)

            # Smart formatting for numbers, percentages, currency
            if isinstance(val, (int, float)):
                cell.value = val
                cell.alignment = Alignment(horizontal="right", vertical="center")
                if isinstance(val, float) and 0 < val <= 1.0:
                    cell.number_format = '0.0%'
                elif isinstance(val, int) and val >= 1000:
                    cell.number_format = '#,##0'
                elif isinstance(val, float):
                    cell.number_format = '#,##0.00'
            else:
                str_val = str(val).strip()
                # Check if string is formatted number/currency
                if str_val.replace(".", "").replace(",", "").replace("-", "").isdigit():
                    try:
                        clean_num = float(str_val.replace(".", "").replace(",", "."))
                        cell.value = clean_num
                        cell.alignment = Alignment(horizontal="right", vertical="center")
                        cell.number_format = '#,##0'
                    except Exception:
                        cell.value = str_val
                        cell.alignment = Alignment(horizontal="left", vertical="center")
                else:
                    cell.value = str_val
                    cell.alignment = Alignment(horizontal="left", vertical="center")

            cell.font = FONT_BODY
            cell.fill = row_fill
            cell.border = BORDER_CELL

        current_row += 1

    # 5. Column Width Auto-Fitting
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            # Skip title row from calculation to avoid bloated width
            if cell.row < header_row_idx:
                continue
            if cell.value:
                val_str = str(cell.value)
                max_len = max(max_len, len(val_str))
        ws.column_dimensions[col_letter].width = max(max_len + 4, 14)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    wb.save(output_path)
    logger.info("Successfully generated Excel workbook at %s", output_path)
    return output_path


# ─── WORD ENGINE (python-docx) ────────────────────────────────────────────────

def build_dynamic_docx(
    output_path: str,
    title: str,
    sections: List[Dict[str, Any]],
    subtitle: Optional[str] = None,
    author: str = "Created by AIRO Hermes | Executive OS"
) -> str:
    """
    Builds a beautifully structured, executive-grade Word document (.docx).
    Features:
    - Clean cover banner with category, title, subtitle, and metadata
    - Visual section hierarchy with customized headings
    - Formatted callout boxes / quote blocks for key insights
    - Executive styled tables for structured data
    - High-readability typography (Segoe UI / Calibri)
    """
    import docx
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
    from docx.oxml import OxmlElement, parse_xml
    from docx.oxml.ns import nsdecls, qn

    doc = docx.Document()

    # Set standard 1-inch margins
    sections_layout = doc.sections
    for s in sections_layout:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # Helper: Set background color of a table cell
    def set_cell_background(cell, fill_hex: str):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    # 1. Title & Header Block
    p_badge = doc.add_paragraph()
    p_badge.paragraph_format.space_before = Pt(0)
    p_badge.paragraph_format.space_after = Pt(4)
    run_badge = p_badge.add_run("⚡  AIRO EXECUTIVE BRIEF")
    run_badge.font.name = "Segoe UI"
    run_badge.font.size = Pt(10)
    run_badge.font.bold = True
    run_badge.font.color.rgb = RGBColor(0, 180, 216)

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(8)
    run_title = p_title.add_run(title)
    run_title.font.name = "Segoe UI"
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(17, 24, 39)

    if subtitle:
        p_sub = doc.add_paragraph()
        p_sub.paragraph_format.space_before = Pt(0)
        p_sub.paragraph_format.space_after = Pt(8)
        run_sub = p_sub.add_run(subtitle)
        run_sub.font.name = "Segoe UI"
        run_sub.font.size = Pt(13)
        run_sub.font.color.rgb = RGBColor(75, 85, 99)

    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(18)
    run_meta = p_meta.add_run(f"{author} • 2026")
    run_meta.font.name = "Segoe UI"
    run_meta.font.size = Pt(9.5)
    run_meta.font.italic = True
    run_meta.font.color.rgb = RGBColor(107, 114, 128)

    # Divider Line
    p_hr = doc.add_paragraph()
    p_hr.paragraph_format.space_before = Pt(0)
    p_hr.paragraph_format.space_after = Pt(16)
    r_hr = p_hr.add_run("―" * 48)
    r_hr.font.color.rgb = RGBColor(229, 231, 235)

    # 2. Process Content Sections
    for sec_idx, sec in enumerate(sections, start=1):
        s_title = sec.get("title", f"Bagian {sec_idx}")
        s_content = sec.get("content", "")
        s_points = sec.get("points", [])
        s_callout = sec.get("callout", "")
        s_table = sec.get("table", None)

        # Section Heading
        p_h1 = doc.add_paragraph()
        p_h1.paragraph_format.space_before = Pt(16)
        p_h1.paragraph_format.space_after = Pt(6)
        r_h1 = p_h1.add_run(f"{sec_idx}. {s_title}")
        r_h1.font.name = "Segoe UI"
        r_h1.font.size = Pt(16)
        r_h1.font.bold = True
        r_h1.font.color.rgb = RGBColor(22, 30, 48)

        # Paragraph text
        if s_content:
            p_c = doc.add_paragraph()
            p_c.paragraph_format.space_before = Pt(0)
            p_c.paragraph_format.space_after = Pt(8)
            p_c.paragraph_format.line_spacing = 1.15
            r_c = p_c.add_run(s_content)
            r_c.font.name = "Segoe UI"
            r_c.font.size = Pt(11)
            r_c.font.color.rgb = RGBColor(31, 41, 55)

        # Bullet points
        if s_points:
            for pt in s_points:
                p_pt = doc.add_paragraph(style='List Bullet')
                p_pt.paragraph_format.space_before = Pt(2)
                p_pt.paragraph_format.space_after = Pt(4)
                r_pt = p_pt.add_run(pt)
                r_pt.font.name = "Segoe UI"
                r_pt.font.size = Pt(10.5)
                r_pt.font.color.rgb = RGBColor(55, 65, 81)

        # Callout Box (Shaded Table container)
        if s_callout:
            tbl_box = doc.add_table(rows=1, cols=1)
            tbl_box.alignment = WD_TABLE_ALIGNMENT.CENTER
            cell = tbl_box.cell(0, 0)
            cell.width = Inches(6.5)
            set_cell_background(cell, "F0F9FF")  # Subtle Sky Blue
            p_box = cell.paragraphs[0]
            p_box.paragraph_format.space_before = Pt(8)
            p_box.paragraph_format.space_after = Pt(8)
            p_box.paragraph_format.left_indent = Inches(0.15)
            p_box.paragraph_format.right_indent = Inches(0.15)
            r_box = p_box.add_run(f"💡 Poin Penting: {s_callout}")
            r_box.font.name = "Segoe UI"
            r_box.font.size = Pt(10.5)
            r_box.font.bold = True
            r_box.font.color.rgb = RGBColor(12, 74, 110)

        # Optional Data Table
        if s_table and isinstance(s_table, dict):
            t_headers = s_table.get("headers", [])
            t_rows = s_table.get("rows", [])
            if t_headers and t_rows:
                tbl = doc.add_table(rows=len(t_rows) + 1, cols=len(t_headers))
                tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
                tbl.autofit = True

                # Format Header
                for col_idx, h_text in enumerate(t_headers):
                    c = tbl.cell(0, col_idx)
                    set_cell_background(c, "161E30")
                    p = c.paragraphs[0]
                    p.paragraph_format.space_before = Pt(6)
                    p.paragraph_format.space_after = Pt(6)
                    r = p.add_run(str(h_text))
                    r.font.name = "Segoe UI"
                    r.font.size = Pt(10)
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(255, 255, 255)

                # Format Rows
                for row_idx, r_data in enumerate(t_rows, start=1):
                    bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
                    for col_idx in range(len(t_headers)):
                        c = tbl.cell(row_idx, col_idx)
                        set_cell_background(c, bg_color)
                        val = r_data[col_idx] if col_idx < len(r_data) else ""
                        p = c.paragraphs[0]
                        p.paragraph_format.space_before = Pt(4)
                        p.paragraph_format.space_after = Pt(4)
                        r = p.add_run(str(val))
                        r.font.name = "Segoe UI"
                        r.font.size = Pt(9.5)
                        r.font.color.rgb = RGBColor(31, 41, 55)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc.save(output_path)
    logger.info("Successfully generated Word document at %s", output_path)
    return output_path


# ─── UNIFIED DISPATCH ROUTER ──────────────────────────────────────────────────

def generate_office_document(app_type: str, output_path: str, spec: Dict[str, Any]) -> str:
    """
    Unified entry point for dynamic office document generation.
    Supports:
    - POWERPOINT / PPT: spec={"title": str, "slides": list, "subtitle": str}
    - EXCEL / XLSX: spec={"title": str, "headers": list, "rows": list, "sheet_name": str}
    - WORD / DOCX: spec={"title": str, "sections": list, "subtitle": str}
    """
    t = app_type.strip().upper()
    if t in ("PPT", "POWERPOINT", "PRESENTATION"):
        return build_dynamic_deck(
            output_path=output_path,
            title=spec.get("title", "AIRO Executive Presentation"),
            slides=spec.get("slides", []),
            subtitle=spec.get("subtitle", ""),
            category=spec.get("category", "Executive Brief")
        )
    elif t in ("EXCEL", "XLSX", "SPREADSHEET"):
        return build_dynamic_xlsx(
            output_path=output_path,
            title=spec.get("title", "AIRO Business Model & Analysis"),
            headers=spec.get("headers", ["Item", "Kategori", "Nilai"]),
            rows=spec.get("rows", []),
            sheet_name=spec.get("sheet_name", "Data Eksekutif"),
            summary=spec.get("summary")
        )
    elif t in ("WORD", "DOCX", "DOCUMENT"):
        return build_dynamic_docx(
            output_path=output_path,
            title=spec.get("title", "Laporan Eksekutif AIRO"),
            sections=spec.get("sections", []),
            subtitle=spec.get("subtitle")
        )
    else:
        raise ValueError(f"Unsupported Office document type: {app_type}")


if __name__ == "__main__":
    print("Testing airo_office_engine...")
    test_xlsx = "/tmp/test_office.xlsx"
    build_dynamic_xlsx(
        test_xlsx,
        title="Strategi Mobil Listrik Indonesia 2026",
        headers=["Pilar", "Target", "Status", "Alokasi Budget (IDR)"],
        rows=[
            ["Infrastruktur SPKLU", "15.000 Unit", "On Track", 45000000000],
            ["Insentif Subsidi", "50.000 Unit", "Active", 120000000000],
            ["R&D Baterai Nikel", "Konsorsium Nasional", "Accelerating", 85000000000]
        ]
    )
    print(f"Excel test generated: {test_xlsx}")

    test_docx = "/tmp/test_office.docx"
    build_dynamic_docx(
        test_docx,
        title="Strategi Penetrasi Mobil Listrik Indonesia",
        subtitle="Analisis Eksekutif & Roadmap Pertumbuhan 2026-2030",
        sections=[
            {
                "title": "Latar Belakang & Potensi Pasar",
                "content": "Adopsi kendaraan listrik di Indonesia mencatatkan lonjakan signifikan seiring dengan insentif fiskal pemerintah dan percepatan rantai pasok hilirisasi nikel.",
                "points": ["Kapasitas baterai lokal melonjak 40%", "Permintaan mobil keluarga EV meningkat"],
                "callout": "Subsidi PPN-DTP 1% menjadi katalis terbesar adopsi konsumen kelas menengah."
            }
        ]
    )
    print(f"Word test generated: {test_docx}")
    print("All engine self-tests passed!")
