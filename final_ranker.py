from sentence_transformers import SentenceTransformer
import re

# =========================
# LOAD MODEL ONCE
# =========================
model = SentenceTransformer("all-MiniLM-L6-v2")


# =========================
# CLEAN JOB TEXT
# =========================
def clean_job_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+", "", text)   # remove links
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# =========================
# RULE-BASED SCORING
# =========================
def rule_score(profile: dict, job_text: str) -> float:
    score = 0.0
    text = job_text.lower()

    # Role keywords
    role_keywords = [
        "data analyst",
        "business analyst",
        "business operations analyst",
        "data scientist",
        "analytics"
    ]

    if any(role in text for role in role_keywords):
        score += 0.2

    # Skill match
    for skill in profile.get("skills", []):
        if skill.lower() in text:
            score += 0.05

    # Location preference
    for loc in profile.get("location", []):
        if loc.lower() in text:
            score += 0.1

    return min(score, 1.0)


# =========================
# DEMO / TEST (ONLY WHEN RUN DIRECTLY)
# =========================
if __name__ == "__main__":
    print("final_ranker loaded correctly. No auto execution.")
