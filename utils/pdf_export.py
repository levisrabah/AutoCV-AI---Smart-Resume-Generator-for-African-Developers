from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import tempfile

def generate_pdf(html_content, styles=None):
    """Generate PDF with WeasyPrint with enhanced settings"""
    try:
        font_config = FontConfiguration()
        
        # Base CSS for print optimization
        base_css = CSS(string='''
            @page {
                size: A4;
                margin: 1.5cm;
                @top-right {
                    content: "Page " counter(page);
                    font-size: 10pt;
                }
            }
            body {
                font-kerning: normal;
                text-rendering: optimizeLegibility;
                hyphenate: auto;
            }
            a {
                text-decoration: none;
                color: inherit;
            }
        ''', font_config=font_config)
        
        # Additional custom styles if provided
        custom_css = CSS(string=styles, font_config=font_config) if styles else None
        
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tmp:
            HTML(string=html_content).write_pdf(
                tmp.name,
                stylesheets=[base_css, custom_css] if custom_css else [base_css],
                font_config=font_config
            )
            with open(tmp.name, "rb") as f:
                return f.read()
                
    except Exception as e:
        raise RuntimeError(f"Professional PDF generation failed: {str(e)}")