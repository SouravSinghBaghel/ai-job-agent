import json

with open("profile.json") as f:
    profile = json.load(f)

jobs = []

for i in [1, 2]:
    with open(f"jd_{i}.json") as f:
        jobs.append(json.load(f))

def score_job(profile, job):
    score = 0

    if job["role"] in profile["target_roles"]:
        score += 5

    common_skills = set(profile["skills"]) & set(job["required_skills"])
    score += len(common_skills) * 2

    if job["location"] in profile["preferred_locations"]:
        score += 3

    return score

ranked_jobs = sorted(jobs, key=lambda j: score_job(profile, j), reverse=True)

print("Job ranking:\n")
for job in ranked_jobs:
    print(job["role"], "→ Score:", score_job(profile, job))
