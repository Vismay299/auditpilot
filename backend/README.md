# AuditPilot Backend

FastAPI backend for AuditPilot.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (copy `.env.example` to `.env` and fill in values).
   - **DATABASE_URL**: Supabase → Project Settings → Database → Connection string (URI).

4. Run migrations in Supabase SQL Editor (run `backend/migrations/*.sql` in order).

5. Run the API server:
```bash
uvicorn main:app --reload
```
API: `http://localhost:8000` — docs at `http://localhost:8000/docs`.

File processing runs automatically in the background after upload (via FastAPI BackgroundTasks).

## API overview

- **Health**: `GET /health`
- **Organizations**: `POST /organizations`, `GET /organizations/{org_id}` — create an org, then use its `id` as `X-Org-Id` header.
- **Inspections**: `POST /inspections`, `GET /inspections/{id}` — require `X-Org-Id`.
- **Files**: `POST /inspections/{inspection_id}/files` (multipart), `GET /inspections/{inspection_id}/files`, `GET /files/{file_id}` — require `X-Org-Id`.
