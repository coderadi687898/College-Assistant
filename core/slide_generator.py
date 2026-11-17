"""
Visual Slide Generation Engine
Renders high-definition (1920x1080, 16:9) presentation slides from RAG-synthesized content
using Pillow (PIL). Produces modern dark-themed slides with clear cards, typography,
and source citations.
"""

import os
from pathlib import Path
from typing import List
from PIL import Image, ImageDraw, ImageFont

from .rag_engine import SlideContent


class SlideGenerator:
    """
    Renders 1920x1080 presentation slides for explainer videos.
    """

    def __init__(self):
        self.width = 1920
        self.height = 1080
        self._load_fonts()

    def _load_fonts(self):
        """Loads clean system fonts with fallback."""
        font_candidates = [
            ("segoeui.ttf", "segoeuib.ttf"),
            ("arial.ttf", "arialbd.ttf"),
            ("calibri.ttf", "calibrib.ttf")
        ]
        windir = os.environ.get("WINDIR", "C:\\Windows")
        fdir = Path(windir) / "Fonts"

        reg_path = "arial.ttf"
        bold_path = "arialbd.ttf"
        for r, b in font_candidates:
            if (fdir / r).exists() and (fdir / b).exists():
                reg_path = str(fdir / r)
                bold_path = str(fdir / b)
                break

        try:
            self.font_brand = ImageFont.truetype(bold_path, 22)
            self.font_badge = ImageFont.truetype(bold_path, 24)
            self.font_title = ImageFont.truetype(bold_path, 52)
            self.font_bullet = ImageFont.truetype(reg_path, 32)
            self.font_takeaway_label = ImageFont.truetype(bold_path, 22)
            self.font_takeaway_body = ImageFont.truetype(reg_path, 28)
            self.font_footer = ImageFont.truetype(reg_path, 22)
        except Exception:
            def_font = ImageFont.load_default()
            self.font_brand = def_font
            self.font_badge = def_font
            self.font_title = def_font
            self.font_bullet = def_font
            self.font_takeaway_label = def_font
            self.font_takeaway_body = def_font
            self.font_footer = def_font

    def _wrap_text(self, text: str, font: ImageFont.ImageFont, max_width: int, draw: ImageDraw.ImageDraw) -> List[str]:
        words = text.split()
        if not words:
            return []
        lines = []
        current = []
        for word in words:
            test_line = " ".join(current + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if (bbox[2] - bbox[0]) <= max_width:
                current.append(word)
            else:
                if current:
                    lines.append(" ".join(current))
                    current = [word]
                else:
                    lines.append(word)
        if current:
            lines.append(" ".join(current))
        return lines

    def render_slide(self, slide: SlideContent, total_slides: int, output_path: str) -> str:
        """Renders an individual slide to a PNG image file."""
        img = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(img)

        # 1. Dark Slate Gradient Background
        c_top = (11, 15, 25)
        c_bot = (19, 29, 49)
        for y in range(self.height):
            ratio = y / float(self.height)
            r = int(c_top[0] * (1 - ratio) + c_bot[0] * ratio)
            g = int(c_top[1] * (1 - ratio) + c_bot[1] * ratio)
            b = int(c_top[2] * (1 - ratio) + c_bot[2] * ratio)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))

        # 2. Header Branding & Slide Progress
        draw.text((90, 50), "DOCUVIDEO RAG | EXPLAINER PRESENTATION", font=self.font_brand, fill=(148, 163, 184))
        progress_text = f"SLIDE {slide.slide_index} OF {total_slides}"
        p_bbox = draw.textbbox((0, 0), progress_text, font=self.font_brand)
        draw.text((self.width - 90 - (p_bbox[2] - p_bbox[0]), 50), progress_text, font=self.font_brand, fill=(56, 189, 248))

        # 3. Category Badge Pill
        badge_text = f"  {slide.category.upper()}  "
        b_bbox = draw.textbbox((0, 0), badge_text, font=self.font_badge)
        bw = b_bbox[2] - b_bbox[0] + 16
        bh = b_bbox[3] - b_bbox[1] + 12
        draw.rounded_rectangle([90, 95, 90 + bw, 95 + bh], radius=8, fill=(30, 58, 102), outline=(51, 65, 85), width=1)
        draw.text((98, 101), badge_text, font=self.font_badge, fill=(56, 189, 248))

        # 4. Slide Title
        title_y = 95 + bh + 20
        title_lines = self._wrap_text(slide.title, self.font_title, max_width=1700, draw=draw)
        for t_line in title_lines[:2]:
            draw.text((90, title_y), t_line, font=self.font_title, fill=(248, 250, 252))
            title_y += 65

        # 5. Main Card Container
        card_x1 = 90
        card_y1 = max(title_y + 15, 260)
        card_x2 = self.width - 90
        card_y2 = self.height - 110
        draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=18, fill=(26, 37, 61), outline=(51, 65, 85), width=2)

        # 6. Bullet Points
        bullet_y = card_y1 + 45
        max_bullet_width = (card_x2 - card_x1) - 120
        for b_text in slide.bullet_points[:3]:
            # Glowing cyan bullet icon
            dot_x = card_x1 + 55
            dot_y = bullet_y + 12
            draw.ellipse([dot_x - 7, dot_y - 7, dot_x + 7, dot_y + 7], fill=(56, 189, 248))

            b_lines = self._wrap_text(b_text, self.font_bullet, max_bullet_width, draw)
            for bline in b_lines:
                draw.text((card_x1 + 80, bullet_y), bline, font=self.font_bullet, fill=(226, 232, 240))
                bullet_y += 44
            bullet_y += 20

        # 7. Key Takeaway Callout Box
        callout_y1 = card_y2 - 135
        callout_y2 = card_y2 - 25
        draw.rounded_rectangle([card_x1 + 40, callout_y1, card_x2 - 40, callout_y2], radius=12, fill=(30, 41, 59), outline=(251, 191, 36), width=2)
        draw.text((card_x1 + 65, callout_y1 + 16), "KEY TAKEAWAY", font=self.font_takeaway_label, fill=(251, 191, 36))
        
        takeaway_lines = self._wrap_text(slide.key_takeaway, self.font_takeaway_body, max_width=(card_x2 - card_x1 - 130), draw=draw)
        if takeaway_lines:
            draw.text((card_x1 + 65, callout_y1 + 55), takeaway_lines[0][:130] + ("..." if len(takeaway_lines[0]) > 130 else ""), font=self.font_takeaway_body, fill=(254, 243, 199))

        # 8. Footer & Citations
        pages_str = ", ".join(str(p) for p in slide.source_pages) if slide.source_pages else "1"
        draw.text((90, self.height - 85), f"Source Grounding: Extracted from Document Page(s) {pages_str}", font=self.font_footer, fill=(148, 163, 184))

        # 9. Bottom Progress Bar
        bar_w = int(self.width * (slide.slide_index / float(total_slides)))
        draw.rectangle([0, self.height - 6, bar_w, self.height], fill=(56, 189, 248))

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path, "PNG", quality=95)
        return output_path

    def render_deck(self, slides: List[SlideContent], output_dir: str = "output/slides") -> List[str]:
        """Renders all slides in the deck to PNGs."""
        os.makedirs(output_dir, exist_ok=True)
        paths = []
        for s in slides:
            p = os.path.join(output_dir, f"slide_{s.slide_index:02d}.png")
            self.render_slide(s, len(slides), p)
            paths.append(p)
        return paths
