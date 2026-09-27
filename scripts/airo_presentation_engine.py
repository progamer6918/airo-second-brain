#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/airo_presentation_engine.py — Autonomous Presentation Deck Generator for AIRO Hermes.

Inspired by open-source presentation frameworks (Slideforge, pptx-generator, python-pptx).
Compiles structured presentation specifications into professional 16:9 widescreen PowerPoint decks
with dynamic modern styling, card containers, high contrast typography, and executive layouts.
"""

import os
import sys
import logging
from typing import List, Dict, Any, Optional

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

logger = logging.getLogger("airo-presentation-engine")

# ─── COLOR PALETTE & DESIGN SYSTEM (Modern Tech Dark) ─────────────────────────
COLOR_BG = RGBColor(11, 15, 25)         # Deep Space Navy (#0B0F19)
COLOR_CARD = RGBColor(22, 30, 48)       # Slate Card Container (#161E30)
COLOR_CARD_BORDER = RGBColor(40, 56, 88) # Subtle Blue Border (#283858)
COLOR_CYAN = RGBColor(0, 229, 255)      # Neon Cyan Accent (#00E5FF)
COLOR_PURPLE = RGBColor(139, 92, 246)   # Electric Violet Accent (#8B5CF6)
COLOR_EMERALD = RGBColor(16, 185, 129)  # Mint Emerald Accent (#10B981)
COLOR_TEXT_MAIN = RGBColor(248, 250, 252) # Crisp White (#F8FAFC)
COLOR_TEXT_MUTED = RGBColor(156, 163, 175) # Light Slate (#9CA3AF)
COLOR_TEXT_CYAN = RGBColor(0, 229, 255)
COLOR_WHITE = RGBColor(255, 255, 255)

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"


class PresentationEngine:
    """Compiles structured slide specifications into a high-fidelity PowerPoint deck."""

    def __init__(self, title: str = "AIRO Presentation"):
        self.prs = Presentation()
        # Set 16:9 Widescreen dimensions
        self.prs.slide_width = Inches(13.333)
        self.prs.slide_height = Inches(7.5)
        self.blank_layout = self.prs.slide_layouts[6]  # Blank slide
        self.title = title

    def _set_slide_background(self, slide, color: RGBColor = COLOR_BG):
        """Creates a solid full-bleed background shape."""
        bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, self.prs.slide_width, self.prs.slide_height
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()  # No border

    def _add_header(self, slide, category: str, title: str, subtitle: str = ""):
        """Adds a standardized top header section with a category badge and title."""
        # Top Accent Line
        top_bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.5), Inches(11.733), Inches(0.04)
        )
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = COLOR_CYAN
        top_bar.line.fill.background()

        # Category Badge
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(8.0), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = FONT_HEADING
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_CYAN

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.733), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.name = FONT_HEADING
        p_title.font.size = Pt(28)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_TEXT_MAIN

        # Optional Subtitle
        if subtitle:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.65), Inches(11.733), Inches(0.4))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle
            p_sub.font.name = FONT_BODY
            p_sub.font.size = Pt(14)
            p_sub.font.color.rgb = COLOR_TEXT_MUTED

    def _add_card(self, slide, left: Inches, top: Inches, width: Inches, height: Inches,
                  bg_color: RGBColor = COLOR_CARD, border_color: RGBColor = COLOR_CARD_BORDER):
        """Creates a modern rounded card shape container."""
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        return card

    # ─── SLIDE BUILDERS ────────────────────────────────────────────────────────

    def add_title_slide(self, badge: str, title: str, subtitle: str, author: str, highlights: List[str]):
        """Slide 1: High-impact cover/title slide."""
        slide = self.prs.slides.add_slide(self.blank_layout)
        self._set_slide_background(slide)

        # Ambient Glow Shapes (Tech aesthetic)
        glow = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.12), Inches(3.2))
        glow.fill.solid()
        glow.fill.fore_color.rgb = COLOR_CYAN
        glow.line.fill.background()

        # Category Badge Box
        badge_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.1), Inches(1.2), Inches(4.2), Inches(0.45))
        badge_card.fill.solid()
        badge_card.fill.fore_color.rgb = COLOR_CARD
        badge_card.line.color.rgb = COLOR_CYAN
        badge_card.line.width = Pt(1.2)
        tf_b = badge_card.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.text = f"⚡  {badge.upper()}"
        p_b.font.name = FONT_HEADING
        p_b.font.size = Pt(11)
        p_b.font.bold = True
        p_b.font.color.rgb = COLOR_CYAN
        p_b.alignment = PP_ALIGN.LEFT

        # Main Title
        t_box = slide.shapes.add_textbox(Inches(1.05), Inches(1.85), Inches(11.2), Inches(1.6))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(44)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_TEXT_MAIN

        # Subtitle
        s_box = slide.shapes.add_textbox(Inches(1.1), Inches(3.5), Inches(11.0), Inches(0.9))
        tf_s = s_box.text_frame
        tf_s.word_wrap = True
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle
        p_s.font.name = FONT_BODY
        p_s.font.size = Pt(20)
        p_s.font.color.rgb = COLOR_TEXT_MUTED

        # Highlights Cards
        card_w = Inches(3.64)
        card_h = Inches(1.6)
        card_y = Inches(4.7)

        for i, hl in enumerate(highlights[:3]):
            card_x = Inches(1.1) + i * Inches(3.9)
            self._add_card(slide, card_x, card_y, card_w, card_h)

            txt_box = slide.shapes.add_textbox(card_x + Inches(0.2), card_y + Inches(0.2), card_w - Inches(0.4), card_h - Inches(0.4))
            tf = txt_box.text_frame
            tf.word_wrap = True
            parts = hl.split(":", 1)
            p1 = tf.paragraphs[0]
            p1.text = parts[0].strip()
            p1.font.name = FONT_HEADING
            p1.font.size = Pt(15)
            p1.font.bold = True
            p1.font.color.rgb = COLOR_CYAN

            if len(parts) > 1:
                p2 = tf.add_paragraph()
                p2.text = parts[1].strip()
                p2.font.name = FONT_BODY
                p2.font.size = Pt(12)
                p2.font.color.rgb = COLOR_TEXT_MUTED

        # Author / Footer
        f_box = slide.shapes.add_textbox(Inches(1.1), Inches(6.6), Inches(11.0), Inches(0.4))
        p_f = f_box.text_frame.paragraphs[0]
        p_f.text = author
        p_f.font.name = FONT_BODY
        p_f.font.size = Pt(11)
        p_f.font.color.rgb = COLOR_TEXT_MUTED

    def add_three_columns_slide(self, category: str, title: str, subtitle: str,
                                columns: List[Dict[str, Any]]):
        """Standard 3-column card slide for problems, pillars, or comparisons."""
        slide = self.prs.slides.add_slide(self.blank_layout)
        self._set_slide_background(slide)
        self._add_header(slide, category, title, subtitle)

        card_w = Inches(3.64)
        card_h = Inches(4.7)
        card_y = Inches(2.2)

        for i, col in enumerate(columns[:3]):
            card_x = Inches(0.8) + i * Inches(4.04)
            card = self._add_card(slide, card_x, card_y, card_w, card_h)

            # Card Header Pill/Number
            num_str = col.get("badge", f"0{i+1}")
            c_tag = col.get("tag_color", COLOR_CYAN)

            txt_box = slide.shapes.add_textbox(card_x + Inches(0.3), card_y + Inches(0.3), card_w - Inches(0.6), card_h - Inches(0.6))
            tf = txt_box.text_frame
            tf.word_wrap = True

            # Number badge
            p_badge = tf.paragraphs[0]
            p_badge.text = num_str
            p_badge.font.name = FONT_HEADING
            p_badge.font.size = Pt(13)
            p_badge.font.bold = True
            p_badge.font.color.rgb = c_tag

            # Card Title
            p_title = tf.add_paragraph()
            p_title.text = col.get("title", "")
            p_title.font.name = FONT_HEADING
            p_title.font.size = Pt(19)
            p_title.font.bold = True
            p_title.font.color.rgb = COLOR_TEXT_MAIN
            p_title.space_before = Pt(8)
            p_title.space_after = Pt(12)

            # Bullet points or description
            points = col.get("points", [])
            for pt_text in points:
                p_pt = tf.add_paragraph()
                p_pt.text = f"•  {pt_text}"
                p_pt.font.name = FONT_BODY
                p_pt.font.size = Pt(12.5)
                p_pt.font.color.rgb = COLOR_TEXT_MUTED
                p_pt.space_after = Pt(8)

    def add_two_column_split_slide(self, category: str, title: str, subtitle: str,
                                   left_card: Dict[str, Any], right_card: Dict[str, Any]):
        """Two large comparative cards (e.g. Intelligence vs Physical Execution)."""
        slide = self.prs.slides.add_slide(self.blank_layout)
        self._set_slide_background(slide)
        self._add_header(slide, category, title, subtitle)

        card_w = Inches(5.66)
        card_h = Inches(4.7)
        card_y = Inches(2.2)

        cards_data = [(Inches(0.8), left_card, COLOR_PURPLE), (Inches(6.86), right_card, COLOR_CYAN)]
        for card_x, cdata, accent in cards_data:
            self._add_card(slide, card_x, card_y, card_w, card_h)

            txt_box = slide.shapes.add_textbox(card_x + Inches(0.4), card_y + Inches(0.35), card_w - Inches(0.8), card_h - Inches(0.7))
            tf = txt_box.text_frame
            tf.word_wrap = True

            p_badge = tf.paragraphs[0]
            p_badge.text = cdata.get("badge", "").upper()
            p_badge.font.name = FONT_HEADING
            p_badge.font.size = Pt(13)
            p_badge.font.bold = True
            p_badge.font.color.rgb = accent

            p_title = tf.add_paragraph()
            p_title.text = cdata.get("title", "")
            p_title.font.name = FONT_HEADING
            p_title.font.size = Pt(22)
            p_title.font.bold = True
            p_title.font.color.rgb = COLOR_TEXT_MAIN
            p_title.space_before = Pt(6)
            p_title.space_after = Pt(14)

            for pt_text in cdata.get("points", []):
                p_pt = tf.add_paragraph()
                p_pt.text = f"▸  {pt_text}"
                p_pt.font.name = FONT_BODY
                p_pt.font.size = Pt(13.5)
                p_pt.font.color.rgb = COLOR_TEXT_MUTED
                p_pt.space_after = Pt(10)

    def add_four_grid_slide(self, category: str, title: str, subtitle: str,
                            grid_items: List[Dict[str, Any]]):
        """2x2 Grid for Core Superpowers / Feature Showcase."""
        slide = self.prs.slides.add_slide(self.blank_layout)
        self._set_slide_background(slide)
        self._add_header(slide, category, title, subtitle)

        card_w = Inches(5.66)
        card_h = Inches(2.2)

        positions = [
            (Inches(0.8), Inches(2.2)),
            (Inches(6.86), Inches(2.2)),
            (Inches(0.8), Inches(4.7)),
            (Inches(6.86), Inches(4.7))
        ]

        accents = [COLOR_CYAN, COLOR_PURPLE, COLOR_EMERALD, COLOR_CYAN]

        for i, (gx, gy) in enumerate(positions):
            if i >= len(grid_items):
                break
            item = grid_items[i]
            acc = accents[i % len(accents)]
            self._add_card(slide, gx, gy, card_w, card_h)

            txt_box = slide.shapes.add_textbox(gx + Inches(0.35), gy + Inches(0.25), card_w - Inches(0.7), card_h - Inches(0.5))
            tf = txt_box.text_frame
            tf.word_wrap = True

            p_t = tf.paragraphs[0]
            p_t.text = item.get("title", "")
            p_t.font.name = FONT_HEADING
            p_t.font.size = Pt(17)
            p_t.font.bold = True
            p_t.font.color.rgb = acc

            p_d = tf.add_paragraph()
            p_d.text = item.get("desc", "")
            p_d.font.name = FONT_BODY
            p_d.font.size = Pt(12.5)
            p_d.font.color.rgb = COLOR_TEXT_MUTED
            p_d.space_before = Pt(6)

    def add_metrics_slide(self, category: str, title: str, subtitle: str,
                          metrics: List[Dict[str, Any]]):
        """Big Stat Numbers & ROI Slide."""
        slide = self.prs.slides.add_slide(self.blank_layout)
        self._set_slide_background(slide)
        self._add_header(slide, category, title, subtitle)

        card_w = Inches(3.64)
        card_h = Inches(4.7)
        card_y = Inches(2.2)

        accents = [COLOR_CYAN, COLOR_EMERALD, COLOR_PURPLE]

        for i, m in enumerate(metrics[:3]):
            card_x = Inches(0.8) + i * Inches(4.04)
            acc = accents[i % len(accents)]
            self._add_card(slide, card_x, card_y, card_w, card_h)

            txt_box = slide.shapes.add_textbox(card_x + Inches(0.3), card_y + Inches(0.4), card_w - Inches(0.6), card_h - Inches(0.8))
            tf = txt_box.text_frame
            tf.word_wrap = True

            # Big Stat Number
            p_stat = tf.paragraphs[0]
            p_stat.text = m.get("stat", "")
            p_stat.font.name = FONT_HEADING
            p_stat.font.size = Pt(56)
            p_stat.font.bold = True
            p_stat.font.color.rgb = acc

            # Label / Metric Name
            p_lbl = tf.add_paragraph()
            p_lbl.text = m.get("label", "").upper()
            p_lbl.font.name = FONT_HEADING
            p_lbl.font.size = Pt(15)
            p_lbl.font.bold = True
            p_lbl.font.color.rgb = COLOR_TEXT_MAIN
            p_lbl.space_before = Pt(8)
            p_lbl.space_after = Pt(12)

            # Explanation
            p_desc = tf.add_paragraph()
            p_desc.text = m.get("desc", "")
            p_desc.font.name = FONT_BODY
            p_desc.font.size = Pt(13)
            p_desc.font.color.rgb = COLOR_TEXT_MUTED

    def add_cta_slide(self, category: str, title: str, subtitle: str,
                      callout_title: str, callout_body: str, contacts: List[str]):
        """Final closing slide with prominent Call-To-Action container."""
        slide = self.prs.slides.add_slide(self.blank_layout)
        self._set_slide_background(slide)
        self._add_header(slide, category, title, subtitle)

        # Large Featured Card
        card_w = Inches(11.733)
        card_h = Inches(4.7)
        card_x = Inches(0.8)
        card_y = Inches(2.2)

        self._add_card(slide, card_x, card_y, card_w, card_h, bg_color=COLOR_CARD, border_color=COLOR_CYAN)

        txt_box = slide.shapes.add_textbox(card_x + Inches(0.8), card_y + Inches(0.6), card_w - Inches(1.6), card_h - Inches(1.2))
        tf = txt_box.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = callout_title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(28)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_CYAN

        p_b = tf.add_paragraph()
        p_b.text = callout_body
        p_b.font.name = FONT_BODY
        p_b.font.size = Pt(16)
        p_b.font.color.rgb = COLOR_TEXT_MAIN
        p_b.space_before = Pt(14)
        p_b.space_after = Pt(24)

        # Contact pills / items
        for c in contacts:
            p_c = tf.add_paragraph()
            p_c.text = f"✦  {c}"
            p_c.font.name = FONT_BODY
            p_c.font.size = Pt(14)
            p_c.font.bold = True
            p_c.font.color.rgb = COLOR_EMERALD
            p_c.space_after = Pt(6)

    def add_content_slide(self, category: str, title: str, subtitle: str, points: List[str]):
        """General high-contrast content slide with structured bullet cards."""
        slide = self.prs.slides.add_slide(self.blank_layout)
        self._set_slide_background(slide)
        self._add_header(slide, category, title, subtitle)

        card_w = Inches(11.733)
        card_h = Inches(4.7)
        card_y = Inches(2.2)
        card_x = Inches(0.8)
        self._add_card(slide, card_x, card_y, card_w, card_h)

        txt_box = slide.shapes.add_textbox(card_x + Inches(0.5), card_y + Inches(0.4), card_w - Inches(1.0), card_h - Inches(0.8))
        tf = txt_box.text_frame
        tf.word_wrap = True

        first = True
        for pt in points:
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.text = f"•  {pt}"
            p.font.name = FONT_BODY
            p.font.size = Pt(17)
            p.font.color.rgb = COLOR_TEXT_MAIN
            p.space_after = Pt(16)

    def save(self, output_path: str) -> str:
        """Saves the presentation to disk."""
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        self.prs.save(output_path)
        logger.info("Successfully generated presentation at %s", output_path)
        return output_path


# ─── DYNAMIC TOPIC PRESENTATION BUILDER ─────────────────────────────────────────

def build_dynamic_deck(output_path: str, title: str, slides: List[Dict[str, Any]], subtitle: str = "", category: str = "Executive Brief") -> str:
    """Builds a customized presentation deck from dynamic slide specifications generated by Hermes LLM."""
    engine = PresentationEngine(title=title)

    has_title_slide = False
    if slides and slides[0].get("slide_number") == 1:
        first_s = slides[0]
        pts = first_s.get("points", [])
        if len(pts) <= 3 and ("title" in first_s.get("title", "").lower() or len(slides) > 1):
            highlights = pts if pts else [
                "Disusun secara otomatis oleh AIRO Hermes Autonomous Operating System.",
                "Dibuat untuk monitor desktop dan review eksekutif.",
                "100% materi orisinal disesuaikan dengan topik yang diminta."
            ]
            engine.add_title_slide(
                badge=first_s.get("category", category),
                title=title,
                subtitle=subtitle or first_s.get("subtitle", ""),
                author="Created by AIRO Hermes | Executive OS | 2026",
                highlights=highlights
            )
            has_title_slide = True
            slides_to_render = slides[1:]
        else:
            slides_to_render = slides
    else:
        slides_to_render = slides

    if not has_title_slide:
        engine.add_title_slide(
            badge=category,
            title=title,
            subtitle=subtitle or "Presentasi Eksekutif & Strategis",
            author="Created by AIRO Hermes | Executive OS | 2026",
            highlights=[
                "Disusun secara otomatis oleh AIRO Hermes Autonomous Operating System.",
                "Dibuat untuk monitor desktop dan review eksekutif.",
                "100% materi orisinal disesuaikan dengan topik yang diminta."
            ]
        )

    for i, s in enumerate(slides_to_render):
        s_title = s.get("title", f"Slide {i+2}")
        s_cat = s.get("category", category)
        s_sub = s.get("subtitle", "")
        pts = s.get("points", [])

        if len(pts) == 2:
            engine.add_two_column_split_slide(
                category=s_cat,
                title=s_title,
                subtitle=s_sub,
                left_card={"badge": "ASPEK 1", "title": pts[0].split(":", 1)[0] if ":" in pts[0] else "Poin Utama", "points": [pts[0]]},
                right_card={"badge": "ASPEK 2", "title": pts[1].split(":", 1)[0] if ":" in pts[1] else "Poin Pendukung", "points": [pts[1]]}
            )
        elif len(pts) == 3:
            cols = []
            for c_idx, pt in enumerate(pts):
                parts = pt.split(":", 1)
                c_title = parts[0].strip() if len(parts) > 1 else f"Pilar {c_idx+1}"
                c_body = parts[1].strip() if len(parts) > 1 else pt
                cols.append({
                    "badge": f"0{c_idx+1}",
                    "tag_color": COLOR_CYAN if c_idx == 0 else (COLOR_PURPLE if c_idx == 1 else COLOR_EMERALD),
                    "title": c_title,
                    "points": [c_body]
                })
            engine.add_three_columns_slide(category=s_cat, title=s_title, subtitle=s_sub, columns=cols)
        else:
            engine.add_content_slide(category=s_cat, title=s_title, subtitle=s_sub, points=pts)

    return engine.save(output_path)


# ─── CANONICAL AIRO PITCH DECK BUILDER ─────────────────────────────────────────

def build_airo_pitch_deck(output_path: str) -> str:
    """Builds the 7-Slide AIRO Autonomous Executive OS Pitch Deck."""
    engine = PresentationEngine(title="AIRO Autonomous Executive OS Pitch Deck")

    # Slide 1: Title
    engine.add_title_slide(
        badge="Executive Operating System",
        title="AIRO: The Autonomous Executive OS",
        subtitle="The Next-Generation AI Operating Partner for High-Performance Founders & Operators",
        author="Created by Egit Aristorandas | AIRO Ecosystem v0.6 | 2026",
        highlights=[
            "Strategic Intelligence: ChatGPT + Canonical Second Brain for permanent context and long-term roadmaps.",
            "Engineering Muscle: Antigravity automation with strict multi-step verification and zero token waste.",
            "Physical Computer Use: Native Windows 11 Desktop control via mobile Telegram without friction."
        ]
    )

    # Slide 2: The Problem
    engine.add_three_columns_slide(
        category="The Industry Crisis",
        title="The Fragmentation & Context Breakdown in Modern AI",
        subtitle="Why modern AI chatbots fail high-performance leaders and operators every single day.",
        columns=[
            {
                "badge": "01 / TRAPPED",
                "tag_color": COLOR_CYAN,
                "title": "Trapped in Browser Tabs",
                "points": [
                    "Current AI models are stranded inside isolated web chat boxes.",
                    "They cannot touch your physical desktop, launch software, or interact with real Windows apps.",
                    "Users waste hours manually copy-pasting code, data, and outputs back and forth."
                ]
            },
            {
                "badge": "02 / AMNESIA",
                "tag_color": COLOR_PURPLE,
                "title": "The Memory Reset Trap",
                "points": [
                    "Chat sessions reset constantly; every conversation starts from zero context.",
                    "Past architecture decisions, business roadmaps, and personal SOPs evaporate.",
                    "Leaders are forced to re-prompt and re-teach their AI repeatedly."
                ]
            },
            {
                "badge": "03 / FATIGUE",
                "tag_color": COLOR_EMERALD,
                "title": "Severe Cognitive Fatigue",
                "points": [
                    "Managing 10+ disjointed SaaS tools creates a new chore: tool babysitting.",
                    "False claims: AI says 'I did it' when nothing actually happened on your machine.",
                    "Lack of verifiable backend truth leads to operational distrust."
                ]
            }
        ]
    )

    # Slide 3: The Architecture
    engine.add_two_column_split_slide(
        category="The Dual-Layer Solution",
        title="Unifying Strategic Intelligence with Physical Desktop Execution",
        subtitle="AIRO bridges deep contextual reasoning with physical OS actuation into one cohesive entity.",
        left_card={
            "badge": "Layer 1: Strategic Brain",
            "title": "Second Brain & Strategy Engine",
            "points": [
                "ChatGPT / Claude Strategic Intelligence layer for deep problem breakdown.",
                "Permanent Second Brain repository preserving state, PRDs, and decision logs.",
                "AIRO WorkDesk (AWD) providing instant natural language access to operational truth.",
                "Automated Finance Engine tracking accounts, credit boundaries, and burn rate."
            ]
        },
        right_card={
            "badge": "Layer 2: Physical Actuator",
            "title": "Native Desktop Computer Use",
            "points": [
                "Zero-dependency Win32 & .NET execution engine running directly on Windows 11.",
                "Controls Microsoft PowerPoint, Excel, Word, VS Code, and browsers seamlessly.",
                "Physical mouse events, typing, hotkey combinations, and system audio control.",
                "Screen Vision on Demand: Instant desktop snapshots delivered securely to Telegram."
            ]
        }
    )

    # Slide 4: Core Superpowers
    engine.add_four_grid_slide(
        category="Core Capabilities",
        title="Superpowers Engineered for Real Operational Dominance",
        subtitle="Every capability is connected to real runtime APIs and local desktop actuators.",
        grid_items=[
            {
                "title": "🖥️ Physical Computer Use Bridge",
                "desc": "Command your desktop from anywhere via Telegram. Launch apps, generate presentations, run scripts, and control Windows without being in front of your PC."
            },
            {
                "title": "📊 AIRO WorkDesk (AWD)",
                "desc": "Query complex operational business TSVs with dynamic entity resolution. Get precise numbers, ledger entries, and audit data in seconds."
            },
            {
                "title": "💳 Sovereign Financial Intelligence",
                "desc": "Direct Gmail & Telegram receipt ingress, safe-to-spend balance calculations, and multi-bank debt tracking with 100% private local storage."
            },
            {
                "title": "🔒 Air-Gapped Local Autonomy",
                "desc": "Built with strict security guardrails. All proprietary data remains on your private VPS and encrypted local PC disk—zero third-party leakage."
            }
        ]
    )

    # Slide 5: Tangible Demonstrations
    engine.add_three_columns_slide(
        category="Verified Proof of Work",
        title="Tangible Physical Execution, Not Hypothetical Text",
        subtitle="Real examples executed live on physical hardware through simple Telegram chats.",
        columns=[
            {
                "badge": "CASE 1 / MEDIA",
                "tag_color": COLOR_CYAN,
                "title": "Instant Deck & App Launch",
                "points": [
                    "Prompt: 'buat ppt menarik ttg diri lo di pc'",
                    "Result: Compiles a custom 7-slide pitch deck and opens PowerPoint on the physical monitor in <5 seconds.",
                    "No manual clicking or template wrestling required."
                ]
            },
            {
                "badge": "CASE 2 / VISION",
                "tag_color": COLOR_PURPLE,
                "title": "Live Screen Verification",
                "points": [
                    "Prompt: 'screenshot layar pc gw'",
                    "Result: Relay captures the physical Windows desktop (GDI BitBlt) and uploads a high-res photo to Telegram.",
                    "Full visual auditability from your smartphone."
                ]
            },
            {
                "badge": "CASE 3 / DEFENSE",
                "tag_color": COLOR_EMERALD,
                "title": "One-Tap Remote Lockdown",
                "points": [
                    "Prompt: 'kunci pc gw'",
                    "Result: Instantly calls Win32 LockWorkStation and mutes system audio for immediate privacy.",
                    "Complete physical security from anywhere in the world."
                ]
            }
        ]
    )

    # Slide 6: The Unfair ROI
    engine.add_metrics_slide(
        category="Measurable Business Value",
        title="Why High-Performance Leaders Choose AIRO",
        subtitle="Multiplying individual executive leverage into organizational scale.",
        metrics=[
            {
                "stat": "10x",
                "label": "Execution Velocity",
                "desc": "Eliminate hundreds of micro-tasks every week. From generating pitch decks to auditing finances, tasks execute autonomously in seconds."
            },
            {
                "stat": "100%",
                "label": "Data Sovereignty",
                "desc": "Your second brain stays entirely under your ownership. Zero cloud vendor lock-in, zero training on your private business records."
            },
            {
                "stat": "24/7",
                "label": "Autonomous Uptime",
                "desc": "Continuous queue workers on cloud infrastructure process inputs, monitor tasks, and bridge to your workstation whenever you need it."
            }
        ]
    )

    # Slide 7: Call to Action
    engine.add_cta_slide(
        category="Get Started",
        title="Transform Your Operations with AIRO Today",
        subtitle="Stop managing tools. Partner with an autonomous executive operating system.",
        callout_title="Ready to Experience True AI Computer Use?",
        callout_body="Deploy AIRO into your ecosystem. Unify your knowledge, automate your physical desktop, and scale your executive output without adding headcount.",
        contacts=[
            "Ecosystem: AIRO Second Brain Architecture v0.6",
            "Champion: Egit Aristorandas | Founder & Principal Architect",
            "Platform: Multi-Agent Tri-Layer (ChatGPT + Antigravity + Hermes + Windows 11)",
            "Status: Production Operational & Available"
        ]
    )

    return engine.save(output_path)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "AIRO_Pitch_Deck.pptx"
    print(f"Building pitch deck to {out}...")
    res = build_airo_pitch_deck(out)
    print(f"Done! Saved to {res}")
