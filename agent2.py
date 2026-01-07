import requests
import json
import hashlib
import smtplib
from email.mime.text import MIMEText

from config import (
    PERPLEXITY_API_KEY,
    JOB_QUERY,
    EMAIL_SENDER,
    EMAIL_PASSWORD,
    EMAIL_RECEIVER,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID
)

MEMORY_FILE = "memory.json"


# ---------------- MEMORY ----------------
def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"seen_jobs": []}


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


# ---------------- UTIL ----------------
def make_job_id(job):
    return hashlib.md5(job["apply_link"].encode()).hexdigest()


def score_job(job):
    score = 0
    if "Remote" in job["location"]:
        score += 2
    if "Intern" in job["role"] or "Fresher" in job["role"]:
        score += 1
    if "Today" in job["posted"] or "Just now" in job["posted"]:
        score += 3
    return score


# ---------------- EMAIL ----------------
def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)


# ---------------- TELEGRAM ----------------
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload)


# ---------------- SEARCH ----------------
def search_jobs(retries=2):
    url = "https://api.perplexity.ai/chat/completions"

    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "sonar-pro",
        "messages": [
            {"role": "system", "content": "You are an autonomous job search agent."},
            {"role": "user", "content": JOB_QUERY}
        ]
    }

    for _ in range(retries):
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return json.loads(content)
        except Exception as e:
            print("Retrying search...", e)

    return {"jobs": []}


# ---------------- FILTER ----------------
def filter_jobs(jobs):
    return [job for job in jobs if job.get("apply_link")]

def clean_job_text(job_text: str) -> str:
    keywords = [
        "Responsibilities",
        "Requirements",
        "What You Bring",
        "Skills",
        "Qualifications"
    ]

    lines = job_text.splitlines()
    cleaned = []

    for line in lines:
        if any(k.lower() in line.lower() for k in keywords):
            cleaned.append(line)

    # fallback: if nothing matched, keep first 15 lines
    if not cleaned:
        cleaned = lines[:15]

    return " ".join(cleaned)

# ---------------- NOTIFY ----------------
def notify_new_jobs(data):
    jobs = filter_jobs(data.get("jobs", []))

    if not jobs:
        print("No open jobs found.")
        return

    jobs.sort(key=score_job, reverse=True)

    memory = load_memory()
    seen = memory["seen_jobs"]

    for job in jobs:
        job_id = make_job_id(job)

        if job_id not in seen:
            message = (
                f"🔥 NEW JOB ALERT 🔥\n\n"
                f"🏢 Company: {job['company']}\n"
                f"💼 Role: {job['role']}\n"
                f"📍 Location: {job['location']}\n"
                f"⏱ Posted: {job['posted']}\n"
                f"🌐 Source: {job['source']}\n"
                f"🔗 Apply: {job['apply_link']}"
            )

            send_email("🔥 New Job Opportunity", message)
            send_telegram(message)

            seen.append(job_id)

    save_memory(memory)


# ---------------- RUN ----------------
def run_agent():
    print("🤖 Agentic Job Finder running...")
    data = search_jobs()
    notify_new_jobs(data)
    print("✅ Scan complete.")


if __name__ == "__main__":
    run_agent()
