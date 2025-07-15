def generate_portfolio_html(form_data):
    name = form_data.get('name', '')
    email = form_data.get('email', '')
    location = form_data.get('location', '')
    linkedin = form_data.get('linkedin', '')
    github = form_data.get('github', '')
    skills = form_data.get('skills', '')
    projects = form_data.get('projects', '')
    educations = form_data.get('educations', [])
    experiences = form_data.get('experiences', [])
    summary = form_data.get('experience_summary', '')
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{name} - Portfolio</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f7f7f7; margin: 0; }}
            .container {{ max-width: 800px; margin: 30px auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px #0001; padding: 32px; }}
            .header {{ text-align: center; }}
            .name {{ font-size: 2.2em; font-weight: bold; color: #222; }}
            .contact {{ color: #555; margin-top: 8px; font-size: 1em; }}
            .section {{ margin-top: 32px; }}
            .section-title {{ color: #0a6; font-size: 1.2em; font-weight: bold; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }}
            .skills {{ display: flex; flex-wrap: wrap; gap: 8px; }}
            .skill {{ background: #e0f7fa; color: #00796b; padding: 4px 12px; border-radius: 12px; font-size: 0.95em; }}
            .projects {{ margin-top: 8px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="name">{name}</div>
                <div class="contact">
                    {email} | {location}<br>
                    <a href="{linkedin}">LinkedIn</a> | <a href="{github}">GitHub</a>
                </div>
            </div>
            <div class="section">
                <div class="section-title">About Me</div>
                <div>{summary}</div>
            </div>
            <div class="section">
                <div class="section-title">Education</div>
                {''.join([f'<div><b>{e['degree']}</b>, {e['institution']} ({e['year']})</div>' for e in educations])}
            </div>
            <div class="section">
                <div class="section-title">Work Experience</div>
                {''.join([f'<div><b>{e['role']}</b>, {e['company']} ({e['years']})<ul>' + ''.join([f'<li>{a.strip()}</li>' for a in e['achievements'].split(',')]) + '</ul></div>' for e in experiences])}
            </div>
            <div class="section">
                <div class="section-title">Skills</div>
                <div class="skills">
                    {''.join([f'<span class="skill">{s.strip()}</span>' for s in skills.split(',')])}
                </div>
            </div>
            {f'<div class="section"><div class="section-title">Projects</div><div class="projects">{projects}</div></div>' if projects else ''}
        </div>
    </body>
    </html>
    '''
    return html 