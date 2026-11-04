#!/usr/bin/env python3
"""Render the Paper 5 Markdown manuscript as a reviewable preprint PDF."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

from reportlab.graphics.shapes import Drawing, Line, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "MANUSCRIPT.md"
DEFAULT_OUTPUT = ROOT.parents[1] / "output" / "pdf" / "paper-5-preprint-candidate.pdf"

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#2E6F9E")
PALE = colors.HexColor("#EEF5F9")
MID = colors.HexColor("#687784")
RULE = colors.HexColor("#B9C7D1")


def ascii_pdf(text: str) -> str:
    replacements = {
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "--",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
        "\u00a0": " ",
        "\u2260": "!=",
        "\u2264": "<=",
        "\u2265": ">=",
        "\u2192": "->",
        "\u21d2": "=>",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return text


def inline_markup(text: str) -> str:
    text = ascii_pdf(text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    links: list[tuple[str, str]] = []

    def hold_link(match: re.Match[str]) -> str:
        token = f"@@LINK{len(links)}@@"
        links.append((match.group(1), match.group(2)))
        return token

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", hold_link, text)
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    for i, (label, url) in enumerate(links):
        replacement = f'<link href="{html.escape(url)}" color="#2E6F9E">{html.escape(label)}</link>'
        text = text.replace(f"@@LINK{i}@@", replacement)
    return text


class PreprintDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
            id="normal",
        )
        self.addPageTemplates(PageTemplate(id="body", frames=[frame], onPage=self._decorate))

    def _decorate(self, canvas, doc):
        canvas.saveState()
        canvas.setTitle("Where Does AI Continuity Live?")
        canvas.setAuthor("Branden Laskowski")
        canvas.setSubject("ADI Research Series Paper 5 - preprint candidate")
        canvas.setKeywords("Artificial Deterministic Intelligence, ADI, governed memory, continuity, model substitution")
        width, height = letter
        if doc.page > 1:
            canvas.setStrokeColor(RULE)
            canvas.setLineWidth(0.5)
            canvas.line(0.72 * inch, height - 0.54 * inch, width - 0.72 * inch, height - 0.54 * inch)
            canvas.setFont("Helvetica", 7.5)
            canvas.setFillColor(MID)
            canvas.drawString(0.72 * inch, height - 0.43 * inch, "ADI Research Series - Paper 5 - Preprint candidate")
            canvas.drawRightString(width - 0.72 * inch, height - 0.43 * inch, "Evidence review - not released")
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MID)
        canvas.drawCentredString(width / 2, 0.42 * inch, str(doc.page))
        canvas.restoreState()


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "PaperTitle", parent=base["Title"], fontName="Helvetica-Bold", fontSize=24,
            leading=28, alignment=TA_CENTER, textColor=NAVY, spaceAfter=14,
        ),
        "subtitle": ParagraphStyle(
            "PaperSubtitle", parent=base["Heading2"], fontName="Helvetica", fontSize=13,
            leading=18, alignment=TA_CENTER, textColor=BLUE, spaceAfter=20,
        ),
        "author": ParagraphStyle(
            "Author", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=11,
            leading=16, alignment=TA_CENTER, textColor=NAVY,
        ),
        "meta": ParagraphStyle(
            "Meta", parent=base["Normal"], fontName="Helvetica", fontSize=9.5,
            leading=14, alignment=TA_CENTER, textColor=MID,
        ),
        "question": ParagraphStyle(
            "Question", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=13,
            leading=18, alignment=TA_LEFT, textColor=NAVY, backColor=PALE,
            borderColor=BLUE, borderWidth=0.8, borderPadding=12, spaceBefore=8, spaceAfter=12,
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=15,
            leading=19, textColor=NAVY, spaceBefore=13, spaceAfter=7, keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "H3", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=11.5,
            leading=15, textColor=BLUE, spaceBefore=10, spaceAfter=5, keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontName="Times-Roman", fontSize=9.4,
            leading=13.2, alignment=TA_JUSTIFY, textColor=colors.HexColor("#1D252B"),
            spaceAfter=6, splitLongWords=True,
        ),
        "small": ParagraphStyle(
            "Small", parent=base["BodyText"], fontName="Helvetica", fontSize=7.8,
            leading=10.3, alignment=TA_LEFT, textColor=colors.HexColor("#26333B"),
        ),
        "table_header": ParagraphStyle(
            "TableHeader", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=7.5,
            leading=9.5, alignment=TA_LEFT, textColor=colors.white,
        ),
        "quote": ParagraphStyle(
            "Quote", parent=base["BodyText"], fontName="Times-BoldItalic", fontSize=10.2,
            leading=14.2, leftIndent=18, rightIndent=10, borderColor=BLUE,
            borderWidth=0, borderLeft=2, borderPadding=8, textColor=NAVY,
            spaceBefore=5, spaceAfter=8,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["BodyText"], fontName="Times-Roman", fontSize=9.2,
            leading=12.7, leftIndent=17, firstLineIndent=-8, spaceAfter=3,
        ),
        "code": ParagraphStyle(
            "Code", parent=base["Code"], fontName="Courier", fontSize=6.5,
            leading=8.1, leftIndent=7, rightIndent=7, backColor=colors.HexColor("#F4F6F7"),
            borderPadding=7, spaceBefore=4, spaceAfter=7,
        ),
        "caption": ParagraphStyle(
            "Caption", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=7.8,
            leading=10.5, alignment=TA_CENTER, textColor=MID, spaceAfter=8,
        ),
    }


def continuity_figure() -> Drawing:
    drawing = Drawing(468, 118)
    boxes = [
        (8, 34, 118, 52, "Models and clients", "Variable reasoning layer"),
        (174, 24, 128, 72, "Governed substrate", "Deterministic authority"),
        (350, 34, 110, 52, "Continuity state", "Provenance + receipts"),
    ]
    for x, y, w, h, title, sub in boxes:
        drawing.add(Rect(x, y, w, h, rx=7, ry=7, fillColor=PALE if x != 174 else NAVY, strokeColor=BLUE, strokeWidth=1.2))
        drawing.add(String(x + w / 2, y + h / 2 + 5, title, textAnchor="middle", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.white if x == 174 else NAVY))
        drawing.add(String(x + w / 2, y + h / 2 - 10, sub, textAnchor="middle", fontName="Helvetica", fontSize=7.2, fillColor=colors.white if x == 174 else MID))
    drawing.add(Line(126, 60, 174, 60, strokeColor=BLUE, strokeWidth=1.8))
    drawing.add(Line(302, 60, 350, 60, strokeColor=BLUE, strokeWidth=1.8))
    drawing.add(String(150, 69, "request", textAnchor="middle", fontName="Helvetica", fontSize=6.8, fillColor=MID))
    drawing.add(String(326, 69, "governed transition", textAnchor="middle", fontName="Helvetica", fontSize=6.8, fillColor=MID))
    drawing.add(String(234, 106, "REPLACEMENT TEST: change the reasoning layer; measure what remains invariant", textAnchor="middle", fontName="Helvetica-Bold", fontSize=8.5, fillColor=NAVY))
    return drawing


def table_flowable(lines: list[str], st: dict) -> Table:
    rows: list[list[Paragraph]] = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            continue
        cell_style = st["table_header"] if not rows else st["small"]
        rows.append([Paragraph(inline_markup(cell), cell_style) for cell in cells])
    columns = max(len(row) for row in rows)
    for row in rows:
        while len(row) < columns:
            row.append(Paragraph("", st["small"]))
    width = 468
    if columns == 2:
        col_widths = [width * 0.38, width * 0.62]
    elif columns == 3:
        col_widths = [width * 0.29, width * 0.17, width * 0.54]
    else:
        col_widths = [width / columns] * columns
    table = Table(rows, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, RULE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9FA")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def parse_body(lines: list[str], st: dict) -> list:
    story: list = []
    paragraph: list[str] = []
    code: list[str] = []
    in_code = False
    table_lines: list[str] = []

    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            text = " ".join(part.strip() for part in paragraph).strip()
            if text:
                story.append(Paragraph(inline_markup(text), st["body"]))
            paragraph = []

    def flush_table():
        nonlocal table_lines
        if table_lines:
            story.append(table_flowable(table_lines, st))
            story.append(Spacer(1, 7))
            table_lines = []

    for raw in lines:
        line = raw.rstrip("\n")
        if line.startswith("```"):
            flush_paragraph()
            flush_table()
            if in_code:
                story.append(Preformatted(ascii_pdf("\n".join(code)), st["code"], maxLineLength=105))
                code = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code.append(line)
            continue
        if line.startswith("|") and line.rstrip().endswith("|"):
            flush_paragraph()
            table_lines.append(line)
            continue
        flush_table()
        if not line.strip():
            flush_paragraph()
            continue
        if line.startswith("![Figure"):
            flush_paragraph()
            story.append(Spacer(1, 5))
            story.append(continuity_figure())
            continue
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            flush_paragraph()
            heading = line[3:].strip()
            if heading.startswith("Appendix") or heading in {"References", "Declarations"}:
                story.append(PageBreak())
            story.append(Paragraph(inline_markup(heading), st["h2"]))
            continue
        if line.startswith("### "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line[4:].strip()), st["h3"]))
            continue
        if line.startswith("> "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line[2:].strip()), st["quote"]))
            continue
        if re.match(r"^[-*] ", line):
            flush_paragraph()
            story.append(Paragraph("- " + inline_markup(line[2:].strip()), st["bullet"]))
            continue
        numbered = re.match(r"^(\d+)\.\s+(.*)", line)
        if numbered:
            flush_paragraph()
            story.append(Paragraph(f"{numbered.group(1)}. " + inline_markup(numbered.group(2)), st["bullet"]))
            continue
        if line.strip() in {"\\[", "\\]"}:
            flush_paragraph()
            continue
        if line.strip().startswith("\\") or re.fullmatch(r"[A-Za-z].*=.*", line.strip()):
            paragraph.append(line)
            continue
        if line.startswith("*Figure "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line.strip("*")), st["caption"]))
            continue
        paragraph.append(line)
    flush_paragraph()
    flush_table()
    if code:
        story.append(Preformatted(ascii_pdf("\n".join(code)), st["code"], maxLineLength=105))
    return story


def build(source: Path, output: Path) -> None:
    text = source.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = ascii_pdf(next(line[2:] for line in lines if line.startswith("# ")))
    subtitle = ascii_pdf(next(line[3:] for line in lines if line.startswith("## ")))
    abstract_index = next(i for i, line in enumerate(lines) if line.strip() == "### Abstract")
    st = styles()
    story: list = [
        Spacer(1, 0.72 * inch),
        Paragraph(inline_markup(title), st["title"]),
        Paragraph(inline_markup(subtitle), st["subtitle"]),
        Spacer(1, 0.18 * inch),
        Paragraph("Branden Laskowski", st["author"]),
        Paragraph("Cortex Agentics Global", st["meta"]),
        Paragraph("ADI Research Series - Paper 5", st["meta"]),
        Paragraph("Preprint candidate v0.9 - Evidence review - 4 November 2026", st["meta"]),
        Spacer(1, 0.38 * inch),
        Paragraph(
            "When the model, client, machine, or runtime changes, can one governed memory substrate preserve the exact continuity of work without transferring authority over memory to the replacement model?",
            st["question"],
        ),
        Spacer(1, 0.16 * inch),
        Paragraph(
            "Research lineage: an empirical extension of Artificial Deterministic Intelligence (ADI), introduced in Artificial Deterministic Intelligence: Probabilistic Reasoning, Deterministic Authority (DOI 10.5281/zenodo.23265200). Cortex Continuum is the evaluated memory substrate; ADI supplies the governing scientific theory.",
            st["meta"],
        ),
        Spacer(1, 0.18 * inch),
        Paragraph(
            "Status: first-party synthetic evidence; independent replication, production readiness, security certification, and universal provider portability are not claimed.",
            st["meta"],
        ),
        PageBreak(),
        Paragraph("Abstract", st["h2"]),
    ]
    story.extend(parse_body(lines[abstract_index + 1 :], st))
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = PreprintDocTemplate(
        str(output),
        pagesize=letter,
        rightMargin=0.72 * inch,
        leftMargin=0.72 * inch,
        topMargin=0.68 * inch,
        bottomMargin=0.68 * inch,
        title=title,
        author="Branden Laskowski",
    )
    doc.build(story)


if __name__ == "__main__":
    destination = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_OUTPUT
    build(SOURCE, destination)
    print(destination)
