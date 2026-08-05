# Valorant AI Coach — Roadmap

---

## Milestone 1 — Stabilize the Current Pipeline

- Fix the model name in `pipeline/analyze_frames.py` (currently `gemini-3.5-flash` which is not a valid model)
- Wire `select_frames_with_enemy_boost` into the main pipeline, or remove the unused import from `coach_video.py`
- Add a YOLO detection step before frame selection so detections feed into `select_frames_with_enemy_boost`
- Add a sensible default for `max_frames` (e.g. 20) to avoid overloading Gemini

---

## Milestone 2 — Complete the YOLO → Gemini Grounding Loop

- Run YOLO on all extracted frames and collect structured detections (class, confidence, bounding box)
- Pass detection metadata into `analyze_frames` as additional context per frame
- Augment the system prompt or frame parts so Gemini can reference YOLO output (enemy count, positions)
- Validate that grounded outputs reduce hallucinations vs. the baseline

---

## Milestone 3 — FastAPI Backend

- Wrap the pipeline in a `POST /analyze` endpoint accepting a video file upload
- Return the `CoachingReport` as JSON
- Add basic error handling, input validation, and logging
- Document the API

---

## Milestone 4 — Full Match / Multi-Round Support

- Implement round segmentation (scoreboard detection or silence/scene-change heuristics)
- Run per-round analysis in parallel using a scatter-gather pattern
- Aggregate per-round reports into a match-level summary
- Handle longer videos without hitting Gemini context limits
