# Valorant AI Coach

An AI-powered coaching system that analyzes Valorant gameplay footage and provides structured coaching feedback using computer vision and multimodal large language models.

## Overview

The goal of this project is to automatically analyze recorded Valorant gameplay and generate coaching similar to what a human coach would provide.

The current pipeline:

1. Upload a gameplay video via the React frontend
2. Extract frames at 1s intervals using FFmpeg
3. Run a custom YOLO11 model on every frame to detect allies and enemies
4. Select the most informative frames using enemy-boost logic (base grid + enemy appearance events + guaranteed last 5s)
5. Send selected frames with timestamps to Google Gemini
6. Return structured coaching feedback as validated JSON
7. Display results in a dark-themed React UI with timeline, key moment, and coaching cards

The long-term goal is to support full match analysis while keeping inference efficient through intelligent frame selection and parallel processing.

---

# Features

## Working

- Video frame extraction using FFmpeg
- Custom YOLO11 ally/enemy detector (`models/valorant_yolo11s_collapsed.pt`)
- Event-driven frame selection with enemy-boost and guaranteed tail frames
- Gemini-powered multi-image coaching analysis
- Structured JSON responses using Pydantic (`CoachingReport` schema)
- FastAPI backend with async job queue (`POST /analyze`, `GET /status/{job_id}`)
- React + TypeScript frontend with dark theme
- Progress indicator with polling during analysis
- Coaching report UI: summary, confidence, timeline, key moment, coaching cards

## Planned

- Fix Gemini model name (`gemini-3.5-flash` is invalid — update to current flash model)
- Grounding Gemini with per-frame YOLO detection counts as structured context
- Pipeline parallelism (YOLO while FFmpeg extracts)
- Full match / multi-round support with round segmentation
- Parallel scatter-gather inference per round
- Persistent analysis storage
- Deployment (FastAPI + React, likely Railway + Vercel)

---

# Tech Stack

## AI

- Google Gemini (multimodal, structured JSON output)
- YOLO11 (Ultralytics) — custom trained on Valorant footage, collapsed to ally/enemy classes

## Backend

- Python 3.12
- FastAPI + Uvicorn
- Pydantic

## Frontend

- React + TypeScript
- Vite
- Tailwind CSS
- Lucide React (icons)

## Video Processing

- FFmpeg

---

# Project Structure

```
valorant-coach-poc/
├── coach_video.py              # Main pipeline entry point
├── api/                        # FastAPI backend
│   ├── main.py                 # Routes: POST /analyze, GET /status/{job_id}
│   ├── jobs.py                 # In-memory job store
│   └── models.py               # API response schemas
├── pipeline/                   # Pipeline stages
│   ├── extract_frames.py       # FFmpeg frame extraction
│   ├── detect_frames.py        # YOLO batch inference
│   ├── select_frames.py        # Naive chronological selection
│   ├── select_frames_with_enemy_boost.py  # YOLO-informed selection
│   ├── analyze_frames.py       # Gemini API call
│   └── report.py               # CoachingReport schema + system prompt
├── frontend/                   # React + TypeScript UI
│   └── src/
│       ├── App.tsx
│       ├── api.ts
│       ├── types.ts
│       └── components/
│           ├── UploadForm.tsx
│           ├── AnalysisProgress.tsx
│           └── CoachingReport.tsx
├── models/
│   └── valorant_yolo11s_collapsed.pt   # Trained YOLO weights
├── scripts/                    # Utility and training scripts (not part of pipeline)
└── docs/
    └── roadmap.md
```

---

# Running Locally

**Backend:**
```bash
.venv/bin/uvicorn api.main:app --reload
```

**Frontend:**
```bash
cd frontend && npm run dev
```

Frontend: `http://localhost:5173`
API docs: `http://localhost:8000/docs`

Requires a `.env` file at the project root with:
```
GEMINI_API_KEY=your_key_here
```
