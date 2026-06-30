from pathlib import Path
from datetime import datetime

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    HRFlowable,
)

BASE_DIR = Path(__file__).resolve().parent

FONT_DIR = BASE_DIR / "fonts"

pdfmetrics.registerFont(
    TTFont(
        "Times",
        str(FONT_DIR / "TIMES.TTF"),
    )
)

pdfmetrics.registerFont(
    TTFont(
        "Times-Bold",
        str(FONT_DIR / "TIMESBD.TTF"),
    )
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "Title",
    parent=styles["Heading1"],
    fontName="Times-Bold",
    fontSize=26,
    alignment=TA_CENTER,
    textColor=HexColor("#2563EB"),
    spaceAfter=18,
)

subtitle_style = ParagraphStyle(
    "Subtitle",
    parent=styles["Heading2"],
    fontName="Times",
    fontSize=13,
    alignment=TA_CENTER,
    textColor=HexColor("#555555"),
    spaceAfter=25,
)

heading_style = ParagraphStyle(
    "Heading",
    parent=styles["Heading2"],
    fontName="Times-Bold",
    fontSize=18,
    textColor=HexColor("#111827"),
    spaceBefore=18,
    spaceAfter=8,
)

text_style = ParagraphStyle(
    "Text",
    parent=styles["BodyText"],
    fontName="Times",
    fontSize=12,
    leading=18,
    spaceAfter=8,
)

footer_style = ParagraphStyle(
    "Footer",
    parent=styles["Normal"],
    fontName="Times",
    fontSize=9,
    alignment=TA_CENTER,
    textColor=HexColor("#999999"),
)


def _parse_markdown(text: str):

    story = []

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            story.append(Spacer(1, 4))
            continue

        if line.startswith("# "):
            story.append(
                Paragraph(
                    line[2:],
                    heading_style,
                )
            )
            continue

        if line.startswith("## "):
            story.append(
                Paragraph(
                    line[3:],
                    heading_style,
                )
            )
            continue

        if line.startswith("### "):
            story.append(
                Paragraph(
                    line[4:],
                    heading_style,
                )
            )
            continue

        line = (
            line
            .replace("**", "<b>")
        )

        count = line.count("<b>")

        if count % 2 == 0:
            opened = False

            result = ""

            i = 0

            while i < len(line):

                if line[i:i + 3] == "<b>":

                    if opened:
                        result += "</b>"
                    else:
                        result += "<b>"

                    opened = not opened
                    i += 3
                    continue

                result += line[i]
                i += 1

            line = result

        story.append(
            Paragraph(
                line,
                text_style,
            )
        )

    return story


def create_pdf(
    specification: str,
    filename: str,
):

    output_dir = BASE_DIR.parent.parent / "generated"

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    pdf_path = output_dir / filename

    doc = SimpleDocTemplate(
        str(pdf_path),
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    story = []

    story.append(
        Paragraph(
            "TechSpec AI",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Автоматическая генерация технического задания",
            subtitle_style,
        )
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=HexColor("#D1D5DB"),
        )
    )

    story.append(
        Spacer(
            1,
            15,
        )
    )

    story.append(
        Paragraph(
            "<b>Документ:</b> Техническое задание",
            text_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Дата создания:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}",
            text_style,
        )
    )

    story.append(
        Spacer(
            1,
            10,
        )
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=HexColor("#D1D5DB"),
        )
    )

    story.append(
        Spacer(
            1,
            20,
        )
    )

    story.extend(
        _parse_markdown(
            specification,
        )
    )

    story.append(
        Spacer(
            1,
            25,
        )
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=HexColor("#D1D5DB"),
        )
    )

    story.append(
        Spacer(
            1,
            10,
        )
    )

    story.append(
        Paragraph(
            "Документ автоматически создан TechSpec AI",
            footer_style,
        )
    )

    doc.build(story)

    return str(pdf_path)