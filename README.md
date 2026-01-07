# 🤖 AI Job Agent – Agentic AI Powered Job Finder

AI Job Agent is an **Agentic AI system** that automatically searches, analyzes, ranks, and surfaces the most relevant job opportunities based on a user’s profile.

Instead of manually browsing multiple job portals for hours, this system uses **AI reasoning, semantic understanding, and autonomous decision-making** to help users apply faster and smarter.

---

## 🚀 What This Project Does

- 🔍 Automatically searches the web for **newly posted jobs**
- 🧠 Uses **LLM-powered reasoning** to understand job descriptions
- 📊 Performs **semantic similarity matching** between job requirements and user skills
- 🧩 Combines **AI scoring + rule-based logic** for better ranking
- 🔗 Extracts **direct apply links**
- ⚡ Runs as a **backend AI agent** with a modern frontend UI

---

## 🧠 Agentic AI Architecture (Core Idea)

This project is built around the concept of **Agentic AI**, meaning:

- The system **acts autonomously**
- It **decides what to search**
- It **evaluates results**
- It **filters and ranks information**
- It **remembers past jobs to avoid duplicates**

The agent is not just responding to prompts — it is **executing a goal**:  
👉 *Find the best matching jobs for the user.*

---

## 🧪 AI Techniques Used

- **Semantic Embeddings**
  - Sentence Transformers to encode job descriptions and user profiles
- **Cosine Similarity**
  - Measures how closely a job matches the user’s skills
- **Hybrid Ranking**
  - AI score + rule-based filters (location, role, freshness)
- **LLM-assisted Web Search**
  - Uses AI to interpret unstructured job data from the web
- **Memory-based Filtering**
  - Avoids re-sending already seen jobs

---

## 🛠 Tech Stack

### Backend
- Python
- FastAPI
- Sentence Transformers
- Agentic AI logic
- Environment-based secret handling

### Frontend
- React (Vite)
- Responsive UI
- Modern SaaS-style design

### Other
- Git & GitHub
- REST APIs
- JSON-based profile configuration

---

## 🧩 How the System Works (Step-by-Step)

1. User provides:
   - Desired role
   - Skills
   - Preferred locations
2. AI agent:
   - Searches for jobs on the web
   - Reads and understands job descriptions
   - Converts text into embeddings
   - Scores jobs based on relevance
3. Ranked jobs are returned to the frontend
4. User sees:
   - Job title
   - Company
   - Match score
   - Apply link

---

## ▶️ How to Run Locally

### Backend
```bash
uvicorn backend.main:app --reload
