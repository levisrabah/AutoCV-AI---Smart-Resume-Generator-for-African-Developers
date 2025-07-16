# AutoCV AI – Smart Resume Generator for African Developers

AutoCV AI is a web app that helps you generate a professional, AI-powered resume in seconds. Input your details, let AI craft your summary, and download a beautiful PDF CV. Built with Python, Streamlit, and Jinja2.

---

## 🚀 Features
- Multi-step form for personal, education, and work details
- AI-generated professional summary (OpenAI-ready, dummy for now)
- Modern, mobile-responsive resume template
- Download as PDF
- Easy deployment (Streamlit Cloud, Heroku, etc.)

---

## 🛠️ Setup

1. **Clone the repo:**
   ```bash
   git clone <repo-url>
   cd AutoCV-AI
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Install wkhtmltopdf** (for pdfkit):
   - Ubuntu: `sudo apt-get install wkhtmltopdf`
   - Mac: `brew install wkhtmltopdf`
   - [Download for other OS](https://wkhtmltopdf.org/downloads.html)

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## 📝 Customization
- Edit `resume_templates/modern.html` for your own resume style
- To use OpenAI, update `utils/ai_resume.py` with your API logic

---

## 🌍 Deployment
- Deploy on [Streamlit Cloud](https://streamlit.io/cloud) or any Python web host

---

## 📄 License
MIT 