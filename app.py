# app.py – AutoCV AI — Smart Resume Generator
# --------------------------------------------------
import streamlit as st
from jinja2 import Environment, FileSystemLoader
import re
import json
import os
from utils.ai_resume import generate_resume_content
from utils.pdf_export import generate_pdf
from utils.portfolio import generate_portfolio_html
from datetime import datetime

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------
USERS_FILE = "users.json"
RESUME_TEMPLATES = {
    "Modern Professional": "modern.html",
    "Classic Elegant": "classic.html", 
    "Tech Minimalist": "minimalist.html"
}

# --------------------------------------------------------------------------
# Authentication Functions
# --------------------------------------------------------------------------
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# --------------------------------------------------------------------------
# Page Setup (must be first Streamlit command)
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="AutoCV AI – Smart Resume Builder",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------------------------------
# Session State Initialization
# --------------------------------------------------------------------------
if 'users' not in st.session_state:
    st.session_state.users = load_users()
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'login'
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}
if 'selected_template' not in st.session_state:
    st.session_state.selected_template = "Modern Professional"

# --------------------------------------------------------------------------
# Authentication UI
# --------------------------------------------------------------------------
def show_auth_ui():
    st.sidebar.title("Account")
    
    if st.session_state.auth_mode == 'login':
        with st.sidebar.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                user = st.session_state.users.get(username)
                if user and user['password'] == password:
                    st.session_state.logged_in_user = username
                    st.session_state.step = 0
                    st.rerun()
                else:
                    st.sidebar.error("Invalid credentials")
        st.sidebar.write("Don't have an account?")
        if st.sidebar.button("Sign Up"):
            st.session_state.auth_mode = 'signup'
            
    else:  # Signup mode
        with st.sidebar.form("signup_form"):
            username = st.text_input("Username")
            name = st.text_input("Full Name")
            password = st.text_input("Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")
            if st.form_submit_button("Create Account"):
                if password != confirm:
                    st.sidebar.error("Passwords don't match")
                elif username in st.session_state.users:
                    st.sidebar.error("Username already exists")
                else:
                    st.session_state.users[username] = {
                        'name': name,
                        'password': password,
                        'created_at': datetime.now().isoformat()
                    }
                    save_users(st.session_state.users)
                    st.session_state.auth_mode = 'login'
                    st.sidebar.success("Account created! Please log in")
        st.sidebar.write("Already have an account?")
        if st.sidebar.button("Back to Login"):
            st.session_state.auth_mode = 'login'

# --------------------------------------------------------------------------
# Resume Generation Pages
# --------------------------------------------------------------------------
def landing_page():
    st.markdown("""
        <style>
        .landing-container {
            max-width: 700px;
            margin: 0 auto;
            text-align: center;
            padding-top: 2rem;
        }
        .feature-card {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="landing-container">', unsafe_allow_html=True)
        st.image("https://via.placeholder.com/150", width=150)
        st.title("AutoCV AI")
        st.markdown("""
            ### Smart Resume Generator for Developers
            Create a professional, ATS-friendly resume in minutes with AI-powered suggestions
        """)
        
        cols = st.columns(3)
        with cols[0]:
            st.markdown("""
                <div class="feature-card">
                <h4>🚀 AI-Powered</h4>
                <p>Get optimized content suggestions</p>
                </div>
            """, unsafe_allow_html=True)
        with cols[1]:
            st.markdown("""
                <div class="feature-card">
                <h4>🎨 Multiple Templates</h4>
                <p>Choose from professional designs</p>
                </div>
            """, unsafe_allow_html=True)
        with cols[2]:
            st.markdown("""
                <div class="feature-card">
                <h4>📄 Perfect PDFs</h4>
                <p>Print-ready resumes every time</p>
                </div>
            """, unsafe_allow_html=True)
        
        if st.button("Start Building My Resume →", type="primary"):
            st.session_state.step = 1
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def personal_info_form():
    st.header("Step 1: Personal Information")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        with st.form("personal_info"):
            st.session_state.form_data['name'] = st.text_input(
                "Full Name", 
                value=st.session_state.form_data.get('name', '')
            )
            st.session_state.form_data['email'] = st.text_input(
                "Email", 
                value=st.session_state.form_data.get('email', '')
            )
            st.session_state.form_data['phone'] = st.text_input(
                "Phone", 
                value=st.session_state.form_data.get('phone', '')
            )
            st.session_state.form_data['location'] = st.text_input(
                "Location", 
                value=st.session_state.form_data.get('location', '')
            )
            st.session_state.form_data['linkedin'] = st.text_input(
                "LinkedIn URL", 
                value=st.session_state.form_data.get('linkedin', '')
            )
            st.session_state.form_data['github'] = st.text_input(
                "GitHub URL", 
                value=st.session_state.form_data.get('github', '')
            )
            st.session_state.form_data['headline'] = st.text_input(
                "Professional Headline", 
                value=st.session_state.form_data.get('headline', '')
            )
            
            if st.form_submit_button("Next →"):
                if not st.session_state.form_data['name']:
                    st.error("Please enter your name")
                elif not re.match(r"[^@]+@[^@]+\.[^@]+", st.session_state.form_data['email']):
                    st.error("Please enter a valid email")
                else:
                    st.session_state.step = 2
                    st.rerun()
    
    with col2:
        show_live_preview()

def experience_education_form():
    st.header("Step 2: Experience & Education")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Education Section
        st.subheader("Education")
        if 'educations' not in st.session_state.form_data:
            st.session_state.form_data['educations'] = []
            
        for i, edu in enumerate(st.session_state.form_data['educations']):
            with st.expander(f"{edu.get('degree', '')} at {edu.get('institution', '')}"):
                st.session_state.form_data['educations'][i]['degree'] = st.text_input(
                    "Degree", 
                    value=edu.get('degree', ''),
                    key=f"edu_degree_{i}"
                )
                st.session_state.form_data['educations'][i]['institution'] = st.text_input(
                    "Institution", 
                    value=edu.get('institution', ''),
                    key=f"edu_institution_{i}"
                )
                st.session_state.form_data['educations'][i]['year'] = st.text_input(
                    "Year", 
                    value=edu.get('year', ''),
                    key=f"edu_year_{i}"
                )
                if st.button("Remove", key=f"remove_edu_{i}"):
                    st.session_state.form_data['educations'].pop(i)
                    st.rerun()
        
        with st.form("add_education"):
            new_degree = st.text_input("Degree (e.g., BSc Computer Science)", key="new_degree")
            new_institution = st.text_input("Institution", key="new_institution")
            new_year = st.text_input("Year", key="new_year")
            if st.form_submit_button("Add Education"):
                if new_degree and new_institution and new_year:
                    st.session_state.form_data['educations'].append({
                        'degree': new_degree,
                        'institution': new_institution,
                        'year': new_year
                    })
                    st.rerun()
        
        # Experience Section
        st.subheader("Work Experience")
        if 'experiences' not in st.session_state.form_data:
            st.session_state.form_data['experiences'] = []
            
        for i, exp in enumerate(st.session_state.form_data['experiences']):
            with st.expander(f"{exp.get('role', '')} at {exp.get('company', '')}"):
                st.session_state.form_data['experiences'][i]['role'] = st.text_input(
                    "Job Title", 
                    value=exp.get('role', ''),
                    key=f"exp_role_{i}"
                )
                st.session_state.form_data['experiences'][i]['company'] = st.text_input(
                    "Company", 
                    value=exp.get('company', ''),
                    key=f"exp_company_{i}"
                )
                st.session_state.form_data['experiences'][i]['years'] = st.text_input(
                    "Years", 
                    value=exp.get('years', ''),
                    key=f"exp_years_{i}"
                )
                st.session_state.form_data['experiences'][i]['achievements'] = st.text_area(
                    "Achievements (one per line)", 
                    value=exp.get('achievements', ''),
                    key=f"exp_achievements_{i}"
                )
                if st.button("Remove", key=f"remove_exp_{i}"):
                    st.session_state.form_data['experiences'].pop(i)
                    st.rerun()
        
        with st.form("add_experience"):
            new_role = st.text_input("Job Title", key="new_role")
            new_company = st.text_input("Company", key="new_company")
            new_years = st.text_input("Years (e.g., 2020-2023)", key="new_years")
            new_achievements = st.text_area("Achievements (one per line)", key="new_achievements")
            if st.form_submit_button("Add Experience"):
                if new_role and new_company and new_years:
                    st.session_state.form_data['experiences'].append({
                        'role': new_role,
                        'company': new_company,
                        'years': new_years,
                        'achievements': new_achievements
                    })
                    st.rerun()
        
        # Skills Section
        st.subheader("Skills")
        st.session_state.form_data['skills'] = st.text_area(
            "List your skills (comma separated)",
            value=st.session_state.form_data.get('skills', ''),
            height=100
        )
        
        if st.button("Continue to Final Step →"):
            if not st.session_state.form_data.get('educations'):
                st.error("Please add at least one education entry")
            elif not st.session_state.form_data.get('experiences'):
                st.error("Please add at least one work experience")
            else:
                st.session_state.step = 3
                st.rerun()
    
    with col2:
        show_live_preview()

def show_live_preview():
    st.subheader("Live Preview")
    env = Environment(loader=FileSystemLoader('resume_templates'))
    try:
        html = env.get_template(
            RESUME_TEMPLATES[st.session_state.selected_template]
        ).render(**st.session_state.form_data)
        st.components.v1.html(html, height=600, scrolling=True)
    except Exception as e:
        st.error(f"Preview error: {str(e)}")

def generate_resume_page():
    st.header("Step 3: Generate Your Resume")
    
    st.session_state.use_ai = st.checkbox(
        "Enable AI Enhancements", 
        value=True,
        help="Get AI-powered improvements to your resume content"
    )
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.session_state.selected_template = st.selectbox(
            "Choose Template",
            list(RESUME_TEMPLATES.keys()),
            index=list(RESUME_TEMPLATES.keys()).index(st.session_state.selected_template)
        )
        
        # Customization options
        with st.expander("Design Options"):
            st.session_state.form_data['font_size'] = st.slider(
                "Font Size", 10, 14, 12
            )
            st.session_state.form_data['primary_color'] = st.color_picker(
                "Primary Color", "#0a6"
            )
            st.session_state.form_data['line_spacing'] = st.slider(
                "Line Spacing", 1.0, 2.0, 1.6, 0.1
            )
    
    with col2:
        show_live_preview()
    
    # Generate final output
    if st.button("Generate Resume PDF", type="primary"):
        with st.spinner("Creating your professional resume..."):
            try:
                # Generate AI content if enabled
                if st.session_state.use_ai:
                    st.session_state.form_data.update(
                        generate_resume_content(st.session_state.form_data)
                    )

                # Render HTML
                env = Environment(loader=FileSystemLoader('resume_templates'))
                html = env.get_template(
                    RESUME_TEMPLATES[st.session_state.selected_template]
                ).render(**st.session_state.form_data)

                # Generate PDF
                pdf_bytes = generate_pdf(html)

                # Show download button
                st.success("Resume generated successfully!")
                st.download_button(
                    "💾 Download PDF",
                    pdf_bytes,
                    file_name=f"{st.session_state.form_data.get('name', 'resume')}.pdf",
                    mime="application/pdf"
                )

                # Show HTML option
                with st.expander("Advanced Options"):
                    st.download_button(
                        "📄 Download HTML",
                        html.encode('utf-8'),
                        file_name="resume.html",
                        mime="text/html"
                    )

            except Exception as e:
                st.error(f"Error generating resume: {str(e)}")

# --------------------------------------------------------------------------
# Main App Router
# --------------------------------------------------------------------------
if not st.session_state.logged_in_user:
    show_auth_ui()
    st.stop()

# Main pages
match st.session_state.step:
    case 0: landing_page()
    case 1: personal_info_form()
    case 2: experience_education_form()
    case 3: generate_resume_page()

# --------------------------------------------------------------------------
# Footer
# --------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 0.9em;">
    AutoCV AI • Professional Resume Generator • 
    <a href="#" style="color: #666;">Terms</a> • 
    <a href="#" style="color: #666;">Privacy</a>
    </div>
    """,
    unsafe_allow_html=True
)