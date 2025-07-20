# AutoCV AI – Smart Resume Generator for Developers

AutoCV AI is a modern web app that helps you generate a professional, AI-powered resume in seconds. Input your details, let AI craft your summary, and download a beautiful PDF CV or a personal portfolio website. Built with Python, Streamlit, and Jinja2.

---

## 🚀 Features
- Multi-step form for personal, education, and work details
- AI-generated professional summary (OpenAI integration or fallback to dummy content)
- Multiple modern, mobile-responsive resume templates
- Live preview as you fill in your details
- Add/remove multiple education and experience entries
- Download as PDF or HTML portfolio website
- Dark mode toggle and beautiful, branded UI
- User authentication (sign up & login, persistent across sessions)
- Easy deployment (Streamlit Cloud, Heroku, etc.)

---

## 🛠️ Setup

1. **Clone the repo:**
   ```bash
   git clone https://github.com/levisrabah/AutoCV-AI---Smart-Resume-Generator-for-African-Developers.git
   cd AutoCV-AI
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Install wkhtmltopdf** (for PDF export):
   - Ubuntu: `sudo apt-get install wkhtmltopdf`
   - Mac: `brew install wkhtmltopdf`
   - [Download for other OS](https://wkhtmltopdf.org/downloads.html)

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

---

## 🤖 OpenAI Integration (Optional)
- To enable real AI-powered summaries, get your API key from [OpenAI](https://platform.openai.com/account/api-keys).
- Set your key in the terminal before running the app:
  ```bash
  export OPENAI_API_KEY=sk-...
  streamlit run app.py
  ```
- If you have no key or quota, the app will use a dummy summary.

---

## 📝 Customization
- Edit `resume_templates/modern.html` and `resume_templates/classic.html` for your own resume style.
- Add more templates by placing new HTML files in `resume_templates/`.
- Update branding by replacing `static/logo.png` with your own logo.
- To use a database for user accounts, replace the file-based `users.json` logic in `app.py`.

---

## 🛡️ Troubleshooting
- **Logo not showing?** Ensure your logo is at `static/logo.png`.
- **PDF export not working?** Make sure `wkhtmltopdf` is installed and on your PATH.
- **OpenAI errors?** Check your API key, quota, and model version (see [OpenAI migration guide](https://github.com/openai/openai-python/discussions/742)).
- **User accounts not persisting?** Make sure `users.json` is present and writable.

---

## 🌍 Deployment
- Deploy on [Streamlit Cloud](https://streamlit.io/cloud) or any Python web host.
- For production, consider using a real database for user accounts and HTTPS for security.

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License
MIT 

## Demo

[Watch the demo video](https://drive.google.com/file/d/19nYCiGnB6IIkfJyEFqUUvhQRs77Stm72/view?usp=drivesdk) 