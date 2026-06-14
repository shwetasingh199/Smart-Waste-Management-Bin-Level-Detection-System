from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd


def generate_report(df):

    doc = SimpleDocTemplate(
        "outputs/waste_report.pdf"
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Smart Waste Monitoring Report",
            styles["Title"]
        )
    )

    content.append(
        Paragraph(
            f"Total Records: {len(df)}",
            styles["BodyText"]
        )
    )

    doc.build(content)

    return "outputs/waste_report.pdf"