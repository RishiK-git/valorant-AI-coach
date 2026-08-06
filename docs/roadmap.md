# Valorant AI Coach — Roadmap

---

## Milestone 1 — Stabilize the Current Pipeline ✅

- ✅ Wire `select_frames_with_enemy_boost` into the main pipeline
- ✅ Add a YOLO detection step before frame selection
- ✅ Add `max_frames` default (20) to avoid overloading Gemini
- ⚠️ Fix Gemini model name — `gemini-3.5-flash` is still invalid, needs updating to the correct current flash model ID

---

## Milestone 2 — YOLO Integration ✅

- ✅ Run YOLO on all extracted frames at 1s fine interval
- ✅ Collect structured detections (class, confidence) per frame
- ✅ Drive frame selection with enemy-boost logic (base grid + enemy appearance events)
- ✅ Guarantee last 5 seconds of clip are always included (outcome/death frames)
- ✅ Tune timeline prompt: prioritize decision-changing events, require final frames, bump limit to 4–8
- ✅ Add `models/valorant_yolo11s_collapsed.pt` — collapsed ally/enemy model, more accurate than per-agent
- ❌ Grounding Gemini with per-frame YOLO context was deprioritized — YOLO class detections (enemy/ally)
  don't help with map position or movement hallucinations which are the main issue

---

## Milestone 3 — FastAPI Backend ✅

- ✅ `POST /analyze` — video upload, format validation, async job creation
- ✅ `GET /status/{job_id}` — polling endpoint returning status + result
- ✅ In-memory job store with thread pool execution
- ✅ CORS configured for local development (`localhost:5173`)
- ✅ Auto-generated API docs at `/docs`

---

## Milestone 4 — React + TypeScript Frontend ✅

- ✅ Vite + React + TypeScript + Tailwind CSS
- ✅ Dark theme UI
- ✅ Video upload with drag-and-drop and format validation
- ✅ Async polling with progress indicator (queued → analyzing → done)
- ✅ Coaching report display: summary, confidence badge, key moment, timeline, coaching cards
- ✅ Error state with try again flow
- ✅ "Start over" to reset without page reload

---

## Next Up

### Performance Improvements
- Fix the Gemini model name to the correct current flash model
- Investigate pipeline parallelism: YOLO inference while FFmpeg is still extracting frames
- Consider Gemini native video API (upload video directly, skip frame extraction for Gemini step)
- Consider streaming Gemini response so UI shows results as they arrive

### Milestone 5 — Full Match / Multi-Round Support
- Round segmentation (scoreboard detection or scene-change heuristics)
- Per-round analysis in parallel (scatter-gather)
- Aggregate per-round reports into a match-level summary
- Handle longer videos without hitting Gemini context limits

### Milestone 5.5 — Docker ✅
- ✅ Dockerfile.backend: Python 3.12-slim + ffmpeg + CPU-only PyTorch (avoids CUDA bloat)
- ✅ Dockerfile.frontend: Node build stage + nginx serving static files
- ✅ docker-compose.yml: single command spins up both services
- ✅ Tested end-to-end locally — full pipeline works in containers
- ⚠️ Backend image is ~6GB due to PyTorch — future improvement: switch YOLO to ONNX runtime

### Milestone 6 — Deployment
- Deploy FastAPI backend (Railway or Fly.io)
- Deploy React frontend (Vercel)
- Configure `VITE_API_BASE_URL` env var for production
- Update CORS origins for production frontend URL
