# Stock News Agent

A real-time, AI-powered market intelligence dashboard. This agent autonomously monitors stock news for your watchlist, evaluates its potential market impact using Llama 3.1 (via Groq), and provides concise summaries.

## Features
- **Autonomy**: Runs as a background "agent" cycling every 10 minutes.
- **AI-Powered**: Uses Llama 3.1 to score news impact (1-5) and sentiment.
- **Real-time UI**: Aesthetic React dashboard with live updates.
- **Visual Intelligence**: Automatically extracts and displays news thumbnails.
- **Persistent Memory**: Saves results to Supabase (PostgreSQL).

## Tech Stack
- **Backend**: FastAPI, SQLModel, Groq, APScheduler.
- **Frontend**: React (Vite), TailwindCSS, Framer Motion.
- **Database**: Supabase (PostgreSQL).

---

## Deployment Guide

### 1. Backend (Hugging Face Spaces)
1. Create a new **Docker Space** on Hugging Face.
2. Upload the `backend/` folder.
3. Set the following **Repository Secrets**:
   - `DATABASE_URL`: Your Supabase connection string.
   - `GROQ_API_KEY`: Your Groq API key.
4. Hugging Face will automatically build and deploy via the provided `Dockerfile`.

### 2. Frontend (Vercel)
1. Connect your GitHub repository to Vercel.
2. Set the **Root Directory** to `frontend`.
3. Set the following **Environment Variable**:
   - `VITE_API_URL`: The public URL of your Hugging Face Space (e.g., `https://[username]-[space-name].hf.space`).
4. Build and Deploy

---

## Local Setup

### Backend
1. `cd backend`
2. `python -m venv venv`
3. `venv/Scripts/activate`
4. `pip install -r requirements.txt`
5. Create `.env` with `DATABASE_URL` and `GROQ_API_KEY`.
6. `uvicorn app.main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. Create `.env` with `VITE_API_URL=http://localhost:8000`.
4. `npm run dev`
