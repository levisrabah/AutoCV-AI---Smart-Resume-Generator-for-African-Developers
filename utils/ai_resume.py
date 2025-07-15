import os
import random

try:
    import openai
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
    else:
        openai = None
except ImportError:
    openai = None


def generate_resume_content(form_data):
    """
    Generate AI-powered summaries for work experience, education, and skills.
    Uses OpenAI if available, otherwise falls back to dummy content.
    """
    skills = form_data.get('skills', '')
    name = form_data.get('name', 'This candidate')
    experience = form_data.get('experience', '')
    education = form_data.get('education', '')

    if openai:
        prompt = f"""
        You are a professional resume writer. Given the following information, write a concise, impactful professional summary for a resume. Use 2-3 sentences.\n\nName: {name}\nEducation: {education}\nExperience: {experience}\nSkills: {skills}\n\nProfessional Summary:
        """
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=100,
                temperature=0.7,
                n=1,
                stop=None
            )
            summary = response.choices[0].text.strip()
        except Exception as e:
            summary = f"[OpenAI error: {e}] {name} is a highly motivated professional with experience in {skills}."
    else:
        summary = (
            f"{name} is a highly motivated professional with experience in "
            f"{random.choice(['software development', 'data analysis', 'project management', 'web development'])}. "
            "They have demonstrated strong skills in {skills} and have contributed to impactful projects."
        ).format(skills=skills)

    return {
        'experience_summary': summary,
        'ai_generated': bool(openai)
    } 