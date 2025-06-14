import spacy
import re

nlp = spacy.load("en_core_web_sm")

COMMON_SKILLS1 = {"react", "node.js", "typescript", "python", "flutter", "docker", "aws", "next.js", "graphql"}

# Example list of common tech skills for filtering
COMMON_SKILLS = {
  # Programming Languages
  "python", "javascript", "typescript", "java", "c#", "c++", "go", "rust", "kotlin", "swift",

  # Web Development
  "html", "css", "react.js", "react", "next.js", "vue.js", "angular", "tailwind css", "sass", "bootstrap",

  # Backend Development
  "node.js", "express.js", "django", "flask", "spring boot", "nestjs", "fastapi", "ruby on rails",

  # Databases
  "postgresql", "mysql", "mongodb", "sqlite", "redis", "firebase", "supabase", "elasticsearch",

  # DevOps & Cloud
  "docker", "kubernetes", "ci/cd", "aws", "gcp", "azure", "nginx", "terraform", "linux", "bash",

  # Testing
  "jest", "mocha", "chai", "cypress", "playwright", "selenium", "junit", "pytest",

  # Version Control
  "git", "github", "gitlab", "bitbucket",

  # Mobile Development
  "react native", "flutter", "swift (ios)", "kotlin (android)", "ionic", "capacitor",

  # Software Architecture
  "microservices", "rest", "graphql", "event-driven architecture", "design patterns",

  # Project & Collaboration Tools
  "jira", "trello", "slack", "notion", "confluence",

  # Soft Skills
  "problem solving", "critical thinking", "communication", "agile/scrum", "time management",

  # Others (important & growing)
  "ai/ml", "data structures & algorithms", "websockets", "oauth2", "openapi", "webrtc", "webassembly"
}


def extract_entities(text: str):
    doc = nlp(text)

    name = ""
    email = ""
    phone = ""
    skills = set()
    education = []
    experience = []

    # Name (first PERSON entity)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    # Email + Phone using regex
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phone_match = re.search(r"\+?\d[\d \-\(\)]{7,}", text)

    if email_match:
        email = email_match.group()
    if phone_match:
        phone = phone_match.group()

    # Skills (match lowercase words against COMMON_SKILLS)
    for token in doc:
        word = token.text.lower()
        if word in COMMON_SKILLS:
            skills.add(token.text)

    # Education (simple rule: lines with degree keywords)
    for line in text.split("\n"):
        if any(keyword in line.lower() for keyword in ["bsc", "msc", "university", "degree", "diploma"]):
            education.append(line.strip())

    # Experience (lines with keywords or patterns)
    for line in text.split("\n"):
        if any(word in line.lower() for word in ["developer", "engineer", "intern", "lead", "manager"]):
            experience.append(line.strip())

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": list(skills),
        "education": education,
        "experience": experience
    }