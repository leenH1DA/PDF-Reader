import PyPDF2
import re


def extract_resume_sections(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

    sections = {}

    headline_match = re.search(r'^([^\n]+(?:\n[^\n]+)?)', text)
    sections['headline'] = headline_match.group(1).strip() if headline_match else ""

    skills_match = re.search(r'(Top Skills|أفضل المهارات)\s*\n(.*?)(?=Certifications|Experience|Education|Summary|الخبرة|التعليم|موجز|$)',
                             text, re.DOTALL | re.IGNORECASE)
    skills = []
    if skills_match:
        skills_text = skills_match.group(2).strip()
        skills = [s.strip() for s in skills_text.split("\n") if s.strip()]
    sections['skills'] = skills

    exp_match = re.search(r'(Experience|الخبرة)\s*\n(.*?)(?=Education|Certifications|Summary|أفضل المهارات|التعليم|موجز|$)',
                          text, re.DOTALL | re.IGNORECASE)
    experiences = []
    if exp_match:
        exp_text = exp_match.group(2).strip().split("\n\n")
        for block in exp_text:
            lines = [l.strip() for l in block.split("\n") if l.strip()]
            if len(lines) >= 1:
                exp_entry = {
                    "Title/Role": lines[0],
                    "Org/Company": lines[1] if len(lines) > 1 else "",
                    "Period": lines[2] if len(lines) > 2 else "",
                    "Details": lines[3:] if len(lines) > 3 else []
                }
                experiences.append(exp_entry)
    sections['experience'] = experiences

    # -----------------------------
    # Education (Education / التعليم)
    # -----------------------------
    edu_match = re.search(r'(Education|التعليم)\s*\n(.*?)(?=Experience|Certifications|Summary|أفضل المهارات|الخبرة|موجز|$)',
                          text, re.DOTALL | re.IGNORECASE)
    education = []
    if edu_match:
        edu_text = edu_match.group(2).strip().split("\n\n")
        for block in edu_text:
            lines = [l.strip() for l in block.split("\n") if l.strip()]
            if len(lines) >= 1:
                edu_entry = {
                    "Degree/Program": lines[0],
                    "Institution": lines[1] if len(lines) > 1 else "",
                    "Period": lines[2] if len(lines) > 2 else ""
                }
                education.append(edu_entry)
    sections['education'] = education

    cert_match = re.search(r'Certifications\s*\n(.*?)(?=Experience|Education|Summary|أفضل المهارات|الخبرة|التعليم|موجز|$)',
                           text, re.DOTALL | re.IGNORECASE)
    certifications = []
    if cert_match:
        cert_text = cert_match.group(1).strip().split("\n")
        certifications = [c.strip() for c in cert_text if c.strip()]
    sections['certifications'] = certifications

    summary_match = re.search(r'(Summary|موجز)\s*\n(.*?)(?=Experience|Education|Certifications|أفضل المهارات|الخبرة|التعليم|$)',
                              text, re.DOTALL | re.IGNORECASE)
    sections['summary'] = summary_match.group(2).strip() if summary_match else ""

    return sections


def build_profile_dict(file_path):
    sections = extract_resume_sections(file_path)

    parsed_profile = {
        "Headline": sections['headline'],
        "Summary": sections['summary'],
        "Experience": sections['experience'],
        "Education": sections['education'],
        "Skills": sections['skills'],
        "Certifications": sections['certifications']
    }

    return parsed_profile


if __name__ == "__main__":
    profile = build_profile_dict("Profile3.pdf")
    import pprint
    pprint.pprint(profile, width=120)
