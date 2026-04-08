from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(summary, filename="report.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    for key, value in summary.items():
        content.append(Paragraph(f"{key}: {value}", styles["Normal"]))

    doc.build(content)

    return filename