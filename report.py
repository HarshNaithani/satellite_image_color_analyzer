from __future__ import annotations

from io import BytesIO
from typing import Dict

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image as RLImage,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def _pil_to_png_bytes(image: Image.Image) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def build_report(
    original: Image.Image,
    classified: Image.Image,
    chart: bytes,
    result: Dict,
    source_name: str,
) -> bytes:
    """Build a concise PDF report for the current prototype."""
    output = BytesIO()
    doc = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Satellite Image Color Analyzer", styles["Title"]))
    story.append(
        Paragraph(
            "RGB/HSV rule-based prototype for pixel-based land-cover analysis",
            styles["Heading2"],
        )
    )
    story.append(Spacer(1, 10))

    story.append(Paragraph(f"<b>Input:</b> {source_name}", styles["BodyText"]))
    story.append(
        Paragraph(
            f"<b>Processed image size:</b> "
            f"{result['processed_size'][0]} × {result['processed_size'][1]} pixels",
            styles["BodyText"],
        )
    )
    story.append(
        Paragraph(
            f"<b>Total analyzed pixels:</b> {result['total_pixels']:,}",
            styles["BodyText"],
        )
    )
    story.append(Spacer(1, 12))

    data = [["Category", "Pixel Count", "Percentage"]]
    for category in result["counts"]:
        data.append(
            [
                category,
                f"{result['counts'][category]:,}",
                f"{result['percentages'][category]:.2f}%",
            ]
        )

    table = Table(data, colWidths=[2.7 * inch, 1.5 * inch, 1.5 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 16))

    original_bytes = _pil_to_png_bytes(original)
    classified_bytes = _pil_to_png_bytes(classified)

    story.append(Paragraph("Original Image", styles["Heading2"]))
    story.append(RLImage(BytesIO(original_bytes), width=5.8 * inch, height=3.8 * inch))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Classified Image", styles["Heading2"]))
    story.append(
        RLImage(BytesIO(classified_bytes), width=5.8 * inch, height=3.8 * inch)
    )
    story.append(Spacer(1, 10))

    story.append(Paragraph("Distribution Chart", styles["Heading2"]))
    story.append(RLImage(BytesIO(chart), width=5.8 * inch, height=3.3 * inch))
    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "<b>Technical limitation:</b> The current prototype classifies "
            "pixels using RGB/HSV color rules. Percentages represent the "
            "proportion of analyzed image pixels and are not geographic area "
            "measurements. Actual NDVI, NDWI, NDBI, georeferencing, or "
            "hectare/m² calculations require suitable remote-sensing bands "
            "and spatial metadata.",
            styles["BodyText"],
        )
    )

    doc.build(story)
    return output.getvalue()
