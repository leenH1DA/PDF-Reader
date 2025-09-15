import PyPDF2
import re


def extract_resume_sections(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

    sections = {}

    name_match = re.search(r'^([^\n]+)', text)
    sections['name'] = name_match.group(1).strip() if name_match else ""

    heading_pattern = r'(?<=' + re.escape(sections['name']) + r')\s*\n([^\n]+(?:\n[^\n]+){0,2})'
    heading_match = re.search(heading_pattern, text, re.DOTALL)
    sections['headline'] = heading_match.group(1).strip() if heading_match else ""

    skills_match = re.search(r'Top Skills\s*\n(.*?)(?=Certifications|Experience|Education|Summary|$)',
                             text, re.DOTALL | re.IGNORECASE)
    skills = []
    if skills_match:
        skills_text = skills_match.group(1).strip()
        skills = [s.strip() for s in skills_text.split("\n") if s.strip()]
    sections['skills'] = skills

    exp_match = re.search(r'Experience\s*\n(.*?)(?=Education|Certifications|Summary|$)',
                          text, re.DOTALL | re.IGNORECASE)
    experiences = []
    if exp_match:
        exp_text = exp_match.group(1).strip().split("\n\n")
        for block in exp_text:
            lines = [l.strip() for l in block.split("\n") if l.strip()]
            if len(lines) >= 2:
                exp_entry = {
                    "Title": lines[0],
                    "Company": lines[1],
                    "Period": lines[2] if len(lines) > 2 else "",
                    "Bullets": lines[3:]
                }
                experiences.append(exp_entry)
    sections['experience'] = experiences

    edu_match = re.search(r'Education\s*\n(.*?)(?=Experience|Certifications|Summary|$)',
                          text, re.DOTALL | re.IGNORECASE)
    education = []
    if edu_match:
        edu_text = edu_match.group(1).strip().split("\n\n")
        for block in edu_text:
            lines = [l.strip() for l in block.split("\n") if l.strip()]
            if len(lines) >= 2:
                edu_entry = {
                    "Degree": lines[0],
                    "Institution": lines[1],
                    "Period": lines[2] if len(lines) > 2 else ""
                }
                education.append(edu_entry)
    sections['education'] = education

    cert_match = re.search(r'Certifications\s*\n(.*?)(?=Experience|Education|Summary|$)',
                           text, re.DOTALL | re.IGNORECASE)
    certifications = []
    if cert_match:
        cert_text = cert_match.group(1).strip().split("\n")
        certifications = [c.strip() for c in cert_text if c.strip()]
    sections['certifications'] = certifications

    summary_match = re.search(r'Summary\s*\n(.*?)(?=Experience|Education|Certifications|$)',
                              text, re.DOTALL | re.IGNORECASE)
    sections['summary'] = summary_match.group(1).strip() if summary_match else ""

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
    profile = build_profile_dict("Profile2.pdf")
    import pprint
    pprint.pprint(profile, width=120)