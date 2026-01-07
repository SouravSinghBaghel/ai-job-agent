from sentence_transformers import SentenceTransformer, util
import json

# Load AI model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load profile


with open("profile.json", "r", encoding="utf-8") as f:
    profile_data = json.load(f)

# Convert structured profile to plain text for AI
profile_text = f"""
Role: {profile_data.get('role')}
Experience: {profile_data.get('experience')}
Skills: {', '.join(profile_data.get('skills', []))}
Preferred Location: {', '.join(profile_data.get('location', []))}
Salary: {profile_data.get('salary')}
"""


# Load jobs
with open("jobs.txt", "r", encoding="utf-8") as f:
    jobs = [j.strip() for j in f.read().split("---") if j.strip()]

print(f"\nLoaded {len(jobs)} jobs\n")

results = []

for idx, job in enumerate(jobs, start=1):
    profile_emb = model.encode(profile_text, convert_to_tensor=True)
    job_emb = model.encode(job, convert_to_tensor=True)

    score = util.cos_sim(profile_emb, job_emb).item()
    results.append((round(score, 3), job))

# Sort jobs by AI score
results.sort(reverse=True, key=lambda x: x[0])

print("🔥 FINAL AI-RANKED JOBS 🔥\n")

for rank, (score, job) in enumerate(results, start=1):
    print(f"#{rank} | Match Score: {score}")
    print(job)
    print("-" * 50)
