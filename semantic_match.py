from sentence_transformers import SentenceTransformer, util
import json

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load profile
with open("profile.json") as f:
    profile = json.load(f)

# Load one job
with open("jd_1.json") as f:
    job = json.load(f)

# Convert profile to text
profile_text = (
    f"Target roles: {', '.join(profile['target_roles'])}. "
    f"Skills: {', '.join(profile['skills'])}. "
    f"Preferred locations: {', '.join(profile['preferred_locations'])}. "
    f"Expected salary between {profile['expected_ctc_lpa']['min']} "
    f"and {profile['expected_ctc_lpa']['max']} LPA."
)

# Convert job to text
job_text = (
    f"Role: {job['role']}. "
    f"Skills required: {', '.join(job['required_skills'])}. "
    f"Location: {job['location']}. "
    f"Salary between {job['ctc_lpa_min']} and {job['ctc_lpa_max']} LPA."
)

# Create embeddings
profile_embedding = model.encode(profile_text)
job_embedding = model.encode(job_text)

# Compute similarity
similarity = util.cos_sim(profile_embedding, job_embedding)

print("Semantic similarity score:", similarity.item())
