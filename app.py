# app.py  – AutoCV AI ⸻ Smart Resume Generator
# --------------------------------------------------
import streamlit as st
from jinja2 import Environment, FileSystemLoader
import re
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher  # ← NEW import
from utils.ai_resume import generate_resume_content
from utils.pdf_export import html_to_pdf
from utils.portfolio import generate_portfolio_html

# --------------------------------------------------------------------------
# Page‑wide settings (must be the first Streamlit call)
# --------------------------------------------------------------------------
st.set_page_config(page_title="AutoCV AI – Smart Resume Builder",
                   page_icon="static/logo.png",
                   layout="centered")

# --- Authentication (Sign Up & Login) ---
if 'users' not in st.session_state:
    st.session_state['users'] = {}
if 'auth_mode' not in st.session_state:
    st.session_state['auth_mode'] = 'login'  # or 'signup'
if 'logged_in_user' not in st.session_state:
    st.session_state['logged_in_user'] = None

def signup_form():
    st.subheader('Sign Up')
    with st.form('signup_form'):
        username = st.text_input('Username')
        name = st.text_input('Full Name')
        password = st.text_input('Password', type='password')
        confirm = st.text_input('Confirm Password', type='password')
        submitted = st.form_submit_button('Create Account')
        if submitted:
            if not username or not name or not password or not confirm:
                st.error('All fields are required.')
            elif password != confirm:
                st.error('Passwords do not match.')
            elif username in st.session_state['users']:
                st.error('Username already exists.')
            else:
                st.session_state['users'][username] = {'name': name, 'password': password}
                st.success('Account created! Please log in.')
                st.session_state['auth_mode'] = 'login'

def login_form():
    st.subheader('Login')
    with st.form('login_form'):
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        submitted = st.form_submit_button('Login')
        if submitted:
            user = st.session_state['users'].get(username)
            if not user or user['password'] != password:
                st.error('Invalid username or password.')
            else:
                st.session_state['logged_in_user'] = username
                st.success(f'Welcome, {user["name"]}!')
                st.session_state['step'] = 0

if st.session_state['logged_in_user'] is None:
    st.sidebar.title('Account')
    if st.session_state['auth_mode'] == 'login':
        login_form()
        st.sidebar.write("Don't have an account?")
        if st.sidebar.button('Sign Up'):
            st.session_state['auth_mode'] = 'signup'
    else:
        signup_form()
        st.sidebar.write('Already have an account?')
        if st.sidebar.button('Back to Login'):
            st.session_state['auth_mode'] = 'login'
    st.stop()

# --------------------------------------------------------------------------
# Theme toggle (light ↔ dark)
# --------------------------------------------------------------------------
def _apply_theme():
    if hasattr(st, 'experimental_set_theme'):
        st.experimental_set_theme({'base': st.session_state['theme']})

if 'theme' not in st.session_state:
    st.session_state['theme'] = 'light'

st.sidebar.markdown("## Settings")
st.session_state['theme'] = st.sidebar.radio(
    "Theme", ["light", "dark"],
    index=0 if st.session_state['theme'] == "light" else 1
)
_apply_theme()

# --------------------------------------------------------------------------
#  State helpers
# --------------------------------------------------------------------------
if 'step' not in st.session_state:
    st.session_state.step = 0            # 0 = landing
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# --------------------------------------------------------------------------
#  Pages & components
# --------------------------------------------------------------------------
def landing_page():
    st.markdown("""
    <div style='text-align:center;'>
        <img src='static/logo.png' width='100'/>
        <h1>AutoCV AI</h1>
        <h3>Smart Resume Generator for African Developers</h3>
        <p style='color:#666;'>Create a professional, AI-powered resume in minutes. Choose a template, let AI write your summary, and download a beautiful PDF.</p>
    </div>
    <br/>
    <h4>Testimonials</h4>
    <ul>
        <li><b>Mary K.</b>: "AutoCV AI made my job search so much easier!"</li>
        <li><b>James O.</b>: "The AI summary was spot on. Highly recommended."</li>
    </ul>
    <h4>FAQ</h4>
    <b>Is it free?</b> Yes!<br/>
    <b>Can I edit my resume?</b> Absolutely.<br/>
    <b>Is my data private?</b> 100% – nothing is stored.<br/>
    <br/>
    """, unsafe_allow_html=True)
    if st.button("Start Building My Resume"):
        st.session_state.step = 1

def show_live_preview():
    templates = {"Modern": "modern.html", "Classic": "classic.html"}
    tmpl_name = st.session_state.get('selected_template', 'Modern')
    env = Environment(loader=FileSystemLoader('resume_templates'))
    preview_data = {**st.session_state.form_data, **generate_resume_content(st.session_state.form_data)}
    # Ensure all required fields exist
    for key in ["skills", "projects", "educations", "experiences"]:
        if key not in preview_data:
            preview_data[key] = "" if key in ["skills", "projects"] else []
    html = env.get_template(templates[tmpl_name]).render(**preview_data)
    st.markdown("#### Live Resume Preview")
    st.components.v1.html(html, height=500, scrolling=True)

def personal_info_form():
    st.header("Step 1: Personal Information")
    c1, c2 = st.columns(2)

    with c1:
        with st.form("personal_info"):
            name      = st.text_input("Full Name",  value=st.session_state.form_data.get('name', ''))
            email     = st.text_input("Email",      value=st.session_state.form_data.get('email', ''))
            phone     = st.text_input("Phone",      value=st.session_state.form_data.get('phone', ''))
            location  = st.text_input("Location",   value=st.session_state.form_data.get('location', ''))
            linkedin  = st.text_input("LinkedIn",   value=st.session_state.form_data.get('linkedin', ''))
            github    = st.text_input("GitHub",     value=st.session_state.form_data.get('github', ''))
            if st.form_submit_button("Next"):
                if not name or not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
                    st.error("Please provide a valid name and email.")
                else:
                    st.session_state.form_data.update(
                        dict(name=name, email=email, phone=phone,
                             location=location, linkedin=linkedin, github=github))
                    st.session_state.step = 2
    with c2:
        show_live_preview()

def experience_education_form():
    st.header("Step 2: Experience & Education")
    cols = st.columns([1, 1])
    with cols[0]:
        # --- Education Section ---
        if 'educations' not in st.session_state.form_data:
            st.session_state.form_data['educations'] = []
        st.markdown("**Education**")
        edu_to_remove = st.selectbox(
            "Remove education entry:",
            ["None"] + [f"{e['degree']} at {e['institution']}" for e in st.session_state.form_data['educations']],
            key="edu_remove_selectbox"
        )
        if edu_to_remove != "None":
            st.session_state.form_data['educations'] = [e for e in st.session_state.form_data['educations'] if f"{e['degree']} at {e['institution']}" != edu_to_remove]
        with st.form("add_edu_form"):
            degree = st.text_input("Degree (e.g., BSc Computer Science)", key="degree_input")
            institution = st.text_input("Institution (e.g., University of Nairobi)", key="institution_input")
            year = st.text_input("Year (e.g., 2022)", key="year_input")
            add_edu = st.form_submit_button("Add Education")
            if add_edu and degree and institution and year:
                st.session_state.form_data['educations'].append({"degree": degree, "institution": institution, "year": year})
        # --- Experience Section ---
        if 'experiences' not in st.session_state.form_data:
            st.session_state.form_data['experiences'] = []
        st.markdown("**Work Experience**")
        exp_to_remove = st.selectbox(
            "Remove experience entry:",
            ["None"] + [f"{e['role']} at {e['company']}" for e in st.session_state.form_data['experiences']],
            key="exp_remove_selectbox"
        )
        if exp_to_remove != "None":
            st.session_state.form_data['experiences'] = [e for e in st.session_state.form_data['experiences'] if f"{e['role']} at {e['company']}" != exp_to_remove]
        with st.form("add_exp_form"):
            role = st.text_input("Role (e.g., Software Engineer)", key="role_input")
            company = st.text_input("Company (e.g., Google)", key="company_input")
            years = st.text_input("Years (e.g., 2020-2023)", key="years_input")
            achievements = st.text_area("Achievements (comma-separated)", key="achievements_input")
            add_exp = st.form_submit_button("Add Experience")
            if add_exp and role and company and years:
                st.session_state.form_data['experiences'].append({"role": role, "company": company, "years": years, "achievements": achievements})
        # --- Skills & Projects ---
        skills = st.text_area("Skills (comma-separated)", value=st.session_state.form_data.get('skills', ''), key="skills_input")
        projects = st.text_area("Projects (optional)", value=st.session_state.form_data.get('projects', ''), key="projects_input")
        submitted = st.button("Next", key="next_button")
        if submitted:
            if not st.session_state.form_data['educations'] or not st.session_state.form_data['experiences'] or not skills:
                st.error("Please add at least one education, one experience, and skills.")
            else:
                st.session_state.form_data['skills'] = skills
                st.session_state.form_data['projects'] = projects
                st.session_state.step = 3
    with cols[1]:
        show_live_preview()

def generate_resume():
    st.header("Step 3: Generate & Download Resume")
    templates = {"Modern": "modern.html", "Classic": "classic.html"}
    if 'selected_template' not in st.session_state:
        st.session_state.selected_template = "Modern"
    st.session_state.selected_template = st.selectbox(
        "Choose a template", list(templates.keys()),
        index=list(templates.keys()).index(st.session_state.selected_template))
    with st.spinner("Crafting your AI‑powered resume…"):
        fd = st.session_state.form_data
        fd.update(generate_resume_content(fd))
        # Ensure all required fields exist
        for key in ["skills", "projects", "educations", "experiences"]:
            if key not in fd:
                fd[key] = "" if key in ["skills", "projects"] else []
        tmpl = Environment(loader=FileSystemLoader('resume_templates')) \
               .get_template(templates[st.session_state.selected_template])
        html_resume = tmpl.render(**fd)
        st.components.v1.html(html_resume, height=850, scrolling=True)
        # PDF
        pdf_bytes = html_to_pdf(html_resume)
        st.download_button("Download PDF", pdf_bytes,
                           file_name="AutoCV_Resume.pdf", mime="application/pdf")
        # Portfolio
        portfolio_html = generate_portfolio_html(fd)
        st.download_button("Download Portfolio HTML", portfolio_html,
                           file_name="portfolio.html", mime="text/html")
    st.success("All set! 🎉 Download your resume or portfolio above.")

# --------------------------------------------------------------------------
#  Page router
# --------------------------------------------------------------------------
match st.session_state.step:
    case 0: landing_page()
    case 1: personal_info_form()
    case 2: experience_education_form()
    case _: generate_resume()

# --------------------------------------------------------------------------
#  Footer
# --------------------------------------------------------------------------
st.markdown(
    """
    <hr/>
    <div style='text-align:center;font-size:0.9em;color:#888;'>
        © 2025 AutoCV AI — Smart Resume Generator for African Developers
    </div>
    """,
    unsafe_allow_html=True
)
