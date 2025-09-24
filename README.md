# easyapi-crud-demo

FastAPI backend + Vite TypeScript frontend CRUD demo.

## Local development

Backend (Python 3.12):

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Frontend:

```bash
cd frontend
npm ci
npm run dev
```

Set frontend to talk to backend in dev by using default `VITE_API_BASE` (http://localhost:8000). You can override with:

```bash
VITE_API_BASE=http://localhost:8000 npm run dev
```

## Deploy on Render via Blueprint

This repo includes `render.yaml` defining two services:
- Web service: FastAPI backend (Python), started with `uvicorn app.main:app`
- Static site: Vite frontend, built with `npm ci && npm run build`, served from `dist`

Steps:
1. Push this repo to GitHub (public or private).
2. Go to Render and choose "New +" → "Blueprint".
3. Connect your GitHub repo and select it; Render reads `render.yaml`.
4. First deploy will create both services.
5. After both have URLs, update allowed origins and API base:
   - In backend service → Environment → set `allowed_origins` to the frontend URL (e.g., `https://easyapi-crud-frontend.onrender.com`).
   - In frontend static site → Environment → set `VITE_API_BASE` to the backend URL (e.g., `https://easyapi-crud-backend.onrender.com`).
6. Trigger a redeploy on both services.

Notes:
- Backend uses SQLite (`app.db`) by default. For production, consider a managed Postgres; update `database_url` accordingly.
- CORS is controlled via `allowed_origins` in backend env.
- Local `.env` is supported by Pydantic Settings (see `backend/app/config.py`).

## Project structure

```
backend/  # FastAPI app
frontend/ # Vite TS app
render.yaml
```
