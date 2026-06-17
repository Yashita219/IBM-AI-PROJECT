import streamlit as st
import re
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

st.set_page_config(page_title="AI Resume Builder", layout="wide")
st.title("AI Resume & Portfolio Builder")

template = st.selectbox(
    "Choose Resume Template",
    ["ATS Simple Template", "Modern Blue Template", "Two Column Professional Template"]
)

st.subheader("Personal Details")
name = st.text_input("Full Name", placeholder="Enter your full name")
role = st.text_input("Career Role / Job Title", placeholder="Example: Software Developer")
email = st.text_input("Email", placeholder="Enter your email")
phone = st.text_input("Phone Number", placeholder="Enter 10-digit phone number")
linkedin = st.text_input("LinkedIn", placeholder="Enter LinkedIn URL")
github = st.text_input("GitHub", placeholder="Enter GitHub URL")

st.subheader("Education Details")

degree = st.selectbox(
    "Select Course",
    [
        "B.Tech Computer Science Engineering (CSE)",
        "B.Tech Information Technology (IT)",
        "B.Tech Artificial Intelligence & Machine Learning (AIML)",
        "B.Tech Data Science",
        "B.Tech Electronics & Communication Engineering (ECE)",
        "B.Tech Electrical Engineering (EE)",
        "B.Tech Mechanical Engineering (ME)",
        "B.Tech Civil Engineering",
        "BCA (Bachelor of Computer Applications)",
        "MCA (Master of Computer Applications)",
        "B.Sc Computer Science",
        "M.Sc Computer Science",
        "B.Sc Information Technology",
        "B.Sc Data Science",
        "BBA",
        "MBA",
        "B.Com",
        "M.Com",
        "BA",
        "MA",
        "B.Pharm",
        "D.Pharm",
        "MBBS",
        "BDS",
        "LLB",
        "BA LLB",
        "B.Ed",
        "Diploma in Computer Science",
        "Diploma in Engineering",
        "Other"
    ]
)

if degree == "Other":
    degree = st.text_input("Enter Course Name")

college = st.selectbox(
    "Select University / College",
    [
        "Graphic Era University",
        "Graphic Era Hill University",
        "Delhi University",
        "Jawaharlal Nehru University (JNU)",
        "Banaras Hindu University (BHU)",
        "Aligarh Muslim University (AMU)",
        "Indian Institute of Technology (IIT)",
        "National Institute of Technology (NIT)",
        "IIIT Allahabad",
        "IIIT Hyderabad",
        "Amity University",
        "Lovely Professional University (LPU)",
        "Chandigarh University",
        "Sharda University",
        "Galgotias University",
        "UPES Dehradun",
        "DIT University",
        "Uttaranchal University",
        "Bennett University",
        "Manipal University",
        "VIT Vellore",
        "SRM University",
        "Anna University",
        "University of Mumbai",
        "University of Calcutta",
        "Osmania University",
        "Jadavpur University",
        "Christ University",
        "Symbiosis University",
        "Other"
    ]
)

if college == "Other":
    college = st.text_input("Enter University / College Name")

degree_year = st.text_input("Degree Year", placeholder="Example: 2023-Present")
cgpa = st.text_input("CPI / CGPA", placeholder="Example: 8.6")

school12 = st.text_input("Class XII School", placeholder="Enter school name")
year12 = st.text_input("Class XII Year", placeholder="Example: 2022")
percent12 = st.text_input("Class XII Percentage", placeholder="Example: 80.6 %")

school10 = st.text_input("Class X School", placeholder="Enter school name")
year10 = st.text_input("Class X Year", placeholder="Example: 2020")
percent10 = st.text_input("Class X Percentage", placeholder="Example: 71 %")

st.subheader("Resume Details")
summary = st.text_area("Professional Summary")
skills = st.text_area("Technical Skills")
projects = st.text_area("Projects")
experience = st.text_area("Internship / Experience")
certifications = st.text_area("Certifications")
achievements = st.text_area("Achievements")

job_description = st.text_area("Paste Job Description for ATS Check")


def safe(text):
    return escape(str(text)).replace("\n", "<br/>")


def make_bullets(text):
    lines = [line.strip() for line in str(text).split("\n") if line.strip()]
    return "<br/>".join([f"• {safe(line)}" for line in lines])


resume_text = f"""
{name} {role} {email} {phone} {linkedin} {github}
Education {degree} {college} {degree_year} {cgpa}
XII {school12} {year12} {percent12}
X {school10} {year10} {percent10}
Summary {summary}
Skills {skills}
Projects {projects}
Experience {experience}
Certifications {certifications}
Achievements {achievements}
"""


def resume_word_count():
    return len(resume_text.split())


def ats_score(resume_text, job_description):
    score = 0
    suggestions = []

    resume = resume_text.lower()
    job = job_description.lower()

    resume_words = set(re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.]*\b", resume))
    job_words = set(re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.]*\b", job))

    stop_words = {
        "the", "and", "is", "are", "to", "of", "in", "for", "with",
        "a", "an", "on", "at", "by", "or", "be", "as", "from"
    }

    resume_words -= stop_words
    job_words -= stop_words

    if job_words:
        matched = resume_words.intersection(job_words)
        score += min(int((len(matched) / len(job_words)) * 40), 40)

        missing = list(job_words - resume_words)
        if missing:
            suggestions.append("Add job keywords: " + ", ".join(missing[:10]))
    else:
        suggestions.append("Paste job description for accurate ATS score.")

    if re.search(r"\S+@\S+\.\S+", resume_text):
        score += 5
    else:
        suggestions.append("Add valid email address.")

    if re.search(r"\b\d{10}\b", resume_text):
        score += 5
    else:
        suggestions.append("Add valid 10-digit phone number.")

    for section in ["education", "skills", "projects", "experience"]:
        if section in resume:
            score += 5
        else:
            suggestions.append(f"Add {section.capitalize()} section.")

    tech_skills = [
        "python", "java", "c++", "html", "css", "javascript",
        "mysql", "firebase", "git", "github", "flask", "django",
        "react", "ai", "machine learning", "sql", "api"
    ]

    found = [s for s in tech_skills if s in resume]
    score += min(len(found) * 2, 15)

    if len(found) < 5:
        suggestions.append("Add more technical skills related to the job.")

    words = resume_word_count()

    if 250 <= words <= 800:
        score += 15
    elif words < 250:
        score += 8
        suggestions.append("Resume is short. Add more project and experience details.")
    else:
        score += 8
        suggestions.append("Resume is too long. Keep it within 1–2 pages.")

    if words > 650:
        suggestions.append("Resume may cover 2 pages. Use Two Column Professional Template.")

    if len(projects.split()) > 250:
        suggestions.append("Projects section is lengthy. Use short bullet points.")

    if len(experience.split()) > 200:
        suggestions.append("Experience section is lengthy. Use achievement-focused bullets.")

    if len(projects.strip()) < 100:
        suggestions.append("Describe projects with tools, features, and outcomes.")

    if not certifications.strip():
        suggestions.append("Add certifications.")

    if not achievements.strip():
        suggestions.append("Add achievements or coding profile details.")

    return min(score, 100), suggestions


def create_resume_pdf():
    file_name = "Professional_Resume.pdf"

    doc = SimpleDocTemplate(
        file_name,
        pagesize=A4,
        rightMargin=38,
        leftMargin=38,
        topMargin=28,
        bottomMargin=28
    )

    styles = getSampleStyleSheet()
    main_color = colors.HexColor("#1F4E79") if template != "ATS Simple Template" else colors.black

    name_style = ParagraphStyle(
        "NameStyle",
        parent=styles["Title"],
        fontSize=21,
        alignment=1,
        textColor=main_color,
        spaceAfter=4
    )

    role_style = ParagraphStyle(
        "RoleStyle",
        parent=styles["Normal"],
        fontSize=10.5,
        alignment=1,
        spaceAfter=4
    )

    contact_style = ParagraphStyle(
        "ContactStyle",
        parent=styles["Normal"],
        fontSize=9,
        alignment=1,
        leading=12,
        spaceAfter=10
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontSize=12,
        textColor=main_color,
        spaceBefore=10,
        spaceAfter=3
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontSize=9.5,
        leading=14,
        spaceAfter=5
    )

    white_heading = ParagraphStyle(
        "WhiteHeading",
        parent=styles["Heading2"],
        fontSize=11,
        textColor=colors.white,
        spaceBefore=8,
        spaceAfter=4
    )

    white_text = ParagraphStyle(
        "WhiteText",
        parent=styles["Normal"],
        fontSize=8.8,
        leading=12,
        textColor=colors.white
    )

    story = []

    story.append(Paragraph(safe(name.upper()), name_style))
    story.append(Paragraph(safe(role), role_style))
    story.append(Paragraph(
        f"{safe(email)} | {safe(phone)}<br/>{safe(linkedin)} | {safe(github)}",
        contact_style
    ))

    story.append(HRFlowable(width="100%", thickness=1, color=main_color))
    story.append(Spacer(1, 8))
    education_data = [
        [
            Paragraph("<b>Examination</b>", normal_style),
            Paragraph("<b>University</b>", normal_style),
            Paragraph("<b>Year</b>", normal_style),
            Paragraph("<b>CPI/%</b>", normal_style),
        ],
        [
            Paragraph(safe(degree), normal_style),
            Paragraph(safe(college), normal_style),
            Paragraph(safe(degree_year), normal_style),
            Paragraph(safe(cgpa), normal_style),
        ],
        [
            Paragraph("XII", normal_style),
            Paragraph(safe(school12), normal_style),
            Paragraph(safe(year12), normal_style),
            Paragraph(safe(percent12), normal_style),
        ],
        [
            Paragraph("X", normal_style),
            Paragraph(safe(school10), normal_style),
            Paragraph(safe(year10), normal_style),
            Paragraph(safe(percent10), normal_style),
        ]
    ]

    education_table = Table(
        education_data,
        colWidths=[190, 190, 75, 65]
    )

    education_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (1, -1), "LEFT"),
        ("ALIGN", (2, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
    ]))

    if template == "Two Column Professional Template":
        left_content = [
            Paragraph("CONTACT", white_heading),
            Paragraph(
                f"Email: {safe(email)}<br/>Phone: {safe(phone)}<br/>LinkedIn: {safe(linkedin)}<br/>GitHub: {safe(github)}",
                white_text
            ),
            Spacer(1, 8),
            Paragraph("SKILLS", white_heading),
            Paragraph(make_bullets(skills), white_text),
            Spacer(1, 8),
            Paragraph("CERTIFICATIONS", white_heading),
            Paragraph(make_bullets(certifications), white_text),
            Spacer(1, 8),
            Paragraph("ACHIEVEMENTS", white_heading),
            Paragraph(make_bullets(achievements), white_text)
        ]

        right_content = []

        right_sections = [
            ("PROFESSIONAL SUMMARY", safe(summary)),
            ("EDUCATION", "education_table"),
            ("PROJECTS", make_bullets(projects)),
            ("INTERNSHIP / EXPERIENCE", make_bullets(experience)),
        ]

        for title, content in right_sections:
            if title == "EDUCATION" or content.strip():
                right_content.append(Paragraph(title, heading_style))
                right_content.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
                right_content.append(Spacer(1, 4))

                if title == "EDUCATION":
                    right_content.append(education_table)
                else:
                    right_content.append(Paragraph(content, normal_style))

                right_content.append(Spacer(1, 7))

        main_table = Table([[left_content, right_content]], colWidths=[160, 355])
        main_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#1F4E79")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (0, 0), 10),
            ("RIGHTPADDING", (0, 0), (0, 0), 10),
            ("TOPPADDING", (0, 0), (0, 0), 10),
            ("BOTTOMPADDING", (0, 0), (0, 0), 10),
            ("LEFTPADDING", (1, 0), (1, 0), 14),
        ]))

        story.append(main_table)

    else:
        sections = [
            ("PROFESSIONAL SUMMARY", safe(summary)),
            ("EDUCATION", "education_table"),
            ("TECHNICAL SKILLS", make_bullets(skills)),
            ("PROJECTS", make_bullets(projects)),
            ("INTERNSHIP / EXPERIENCE", make_bullets(experience)),
            ("CERTIFICATIONS", make_bullets(certifications)),
            ("ACHIEVEMENTS", make_bullets(achievements)),
        ]

        for title, content in sections:
            if title == "EDUCATION" or content.strip():
                story.append(Paragraph(title, heading_style))
                story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
                story.append(Spacer(1, 4))

                if title == "EDUCATION":
                    story.append(education_table)
                else:
                    story.append(Paragraph(content, normal_style))

                story.append(Spacer(1, 7))

    doc.build(story)
    return file_name


words = resume_word_count()
if words > 650:
    st.warning("Resume may cover 2 pages. Recommended: Two Column Professional Template.")
elif words > 450:
    st.info("Resume is lengthy. Two-column layout is recommended.")
else:
    st.success("Resume length is suitable.")

col1, col2 = st.columns(2)

with col1:
    if st.button("Check ATS Score"):
        score, suggestions = ats_score(resume_text, job_description)

        st.subheader("ATS Analysis")
        st.progress(score / 100)
        st.success(f"ATS Score: {score}%")

        st.subheader("Suggestions")
        for i, s in enumerate(suggestions, 1):
            st.write(f"{i}. {s}")

with col2:

    if st.button("Generate Resume PDF"):
        pdf_file = create_resume_pdf()

        with open(pdf_file, "rb") as file:
            st.download_button(
                label="Download Resume PDF",
                data=file,
                file_name="Professional_Resume.pdf",
                mime="application/pdf"
            )

    if st.button("Generate Portfolio Website"):
        portfolio_file = create_portfolio_html()

        with open(portfolio_file, "rb") as file:
            st.download_button(
                label="Download Portfolio Website",
                data=file,
                file_name="Portfolio_Website.html",
                mime="text/html"
            )
def create_portfolio_html():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{name} Portfolio</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background: #f4f6f9;
                color: #333;
            }}

            .container {{
                max-width: 1000px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            }}

            h1 {{
                color: #1F4E79;
            }}

            h2 {{
                color: #1F4E79;
                border-bottom: 2px solid #1F4E79;
                padding-bottom: 5px;
            }}

            .contact {{
                margin-bottom: 20px;
            }}

            ul {{
                line-height: 1.8;
            }}
        </style>
    </head>
    <body>
        <div class="container">

            <h1>{name}</h1>
            <h3>{role}</h3>

            <div class="contact">
                <p><b>Email:</b> {email}</p>
                <p><b>Phone:</b> {phone}</p>
                <p><b>LinkedIn:</b> <a href="{linkedin}">{linkedin}</a></p>
                <p><b>GitHub:</b> <a href="{github}">{github}</a></p>
            </div>

            <h2>Professional Summary</h2>
            <p>{summary}</p>

            <h2>Education</h2>
            <ul>
                <li>
                    <b>{degree}</b><br>
                    {college} ({degree_year})<br>
                    CGPA: {cgpa}
                </li>
            </ul>

            <h2>Skills</h2>
            <p>{skills.replace(chr(10), '<br>')}</p>

            <h2>Projects</h2>
            <p>{projects.replace(chr(10), '<br>')}</p>

            <h2>Experience</h2>
            <p>{experience.replace(chr(10), '<br>')}</p>

            <h2>Certifications</h2>
            <p>{certifications.replace(chr(10), '<br>')}</p>

            <h2>Achievements</h2>
            <p>{achievements.replace(chr(10), '<br>')}</p>

        </div>
    </body>
    </html>
    """

    file_name = "Portfolio_Website.html"

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html)

    return file_name
