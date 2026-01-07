from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import ProfileInput
from .agent_core import run_agent

app = FastAPI(title="AI Job Agent Backend")

# 🔥 CORS FIX (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "Backend is running"}

@app.post("/run-agent")
def run_agent_endpoint(profile: ProfileInput):
    results = run_agent(profile.dict())
    return {
        "matched_jobs": results,
        "count": len(results)
    }
