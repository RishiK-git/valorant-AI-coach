# Next Session — Docker Setup

## Task
Add Docker support to the project.

## Decision
Containerize both the FastAPI backend and React frontend as separate services in docker-compose.

**Why:**
- `docker-compose up` runs everything in one command — good for portfolio/README
- Separate Dockerfiles per service shows understanding of separation of concerns
- Mirrors how they'll actually deploy in production (Railway for backend, Vercel for frontend)

## Steps
1. Install Docker Desktop first (not yet installed)
2. Write `Dockerfile` for the FastAPI backend (Python 3.12, install requirements, run uvicorn)
3. Write `Dockerfile` for the React frontend (Node build stage, serve static files via nginx)
4. Write `docker-compose.yml` at the project root with two services: `backend` and `frontend`
5. Handle environment variables (GEMINI_API_KEY via `.env`, VITE_API_BASE_URL pointing to backend service)
6. Update CORS in `api/main.py` to allow requests from the frontend container
7. Test with `docker-compose up` end-to-end
8. Update README with Docker setup instructions

## Notes
- Frontend Vite dev server should NOT be used inside Docker — build to static files and serve with nginx
- GEMINI_API_KEY must be passed via environment variable, never baked into the image
- The `.env` file at project root should be used by docker-compose via `env_file`
