# AuditPilot

Automated inspection report generation using multimodal AI.

## Getting Started

### Frontend Setup

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
   - Copy `.env.example` to `.env.local`
   - Fill in required values (see Environment Variables section)

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `backend/.env.example` to `backend/.env`
   - Fill in required values

5. Run the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Environment Variables

### Frontend (.env.local)

- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` - Clerk publishable key for authentication
- `CLERK_SECRET_KEY` - Clerk secret key
- `NEXT_PUBLIC_SUPABASE_URL` - Supabase project URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` - Supabase anonymous key
- `NEXT_PUBLIC_APP_URL` - Frontend app URL
- `NEXT_PUBLIC_API_BASE_URL` - API base URL
- `NEXT_PUBLIC_DEFAULT_ORG_ID` - Default org for API (X-Org-Id). Create an org via `POST /organizations` first, then set this to the returned `id`.

### Backend (backend/.env)

- `DATABASE_URL` - Supabase database connection string (URI)
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase API key
- `SUPABASE_SERVICE_KEY` - Supabase service role key
- `HF_API_TOKEN` - Hugging Face API token
- `CLERK_SECRET_KEY` - Clerk secret key

## Project Structure

- `/app` - Next.js App Router pages
- `/components` - React components
  - `/ui` - shadcn/ui components
  - `/features` - Feature-specific components
- `/lib` - Utility functions and API clients
  - `/api` - API client functions
  - `/utils` - Utility functions
  - `/hooks` - React hooks
- `/types` - TypeScript type definitions
- `/backend` - FastAPI backend
  - `/app` - Application code
    - `/api/routes` - API route handlers
    - `/core` - Core configuration
    - `/models` - Database models
    - `/schemas` - Pydantic schemas
    - `/services` - Business logic services
    - `/workers` - Background workers
  - `/tests` - Test files
