import pdfkit
import tempfile

def html_to_pdf(html_str):
    """
    Convert HTML string to PDF bytes using pdfkit.
    """
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as html_file:
        html_file.write(html_str.encode("utf-8"))
        html_file.flush()
        pdf_bytes = pdfkit.from_file(html_file.name, False)
    return pdf_bytes 