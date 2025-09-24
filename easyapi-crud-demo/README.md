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

Override API base if needed:

```bash
VITE_API_BASE=http://localhost:8000 npm run dev
```

## Deploy on Render via Blueprint

This repo includes `render.yaml` defining two services:
- Web service: FastAPI backend (Python), started with `uvicorn app.main:app`
- Static site: Vite frontend, built with `npm ci && npm run build`, served from `dist`

Steps:
1. Push this repo to GitHub.
2. In Render, New → Blueprint, pick this repo.
3. After first deploy, set env vars:
   - Backend: `allowed_origins` = your frontend URL.
   - Frontend: `VITE_API_BASE` = your backend URL.
4. Redeploy both services.

Notes:
- Default DB is SQLite file `app.db`. For production, set `database_url` to Postgres.
- CORS origin is controlled by `allowed_origins` env.
