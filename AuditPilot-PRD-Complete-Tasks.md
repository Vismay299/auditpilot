# AuditPilot - Product Requirements Document (PRD)

## Document Information
- **Product Name**: AuditPilot
- **Version**: 1.0 (MVP)
- **Last Updated**: February 2026
- **Author**: Product Team
- **Status**: Ready for Development

---

## Table of Contents
1. [Product Overview](#product-overview)
2. [Objectives & Success Metrics](#objectives--success-metrics)
3. [User Personas](#user-personas)
4. [Technical Requirements](#technical-requirements)
5. [Detailed Task Breakdown](#detailed-task-breakdown)
6. [Database Schema Tasks](#database-schema-tasks)
7. [API Endpoints Tasks](#api-endpoints-tasks)
8. [Frontend Tasks](#frontend-tasks)
9. [ML Pipeline Tasks](#ml-pipeline-tasks)
10. [Authentication & Authorization Tasks](#authentication--authorization-tasks)
11. [Testing & Quality Assurance](#testing--quality-assurance)
12. [Deployment Tasks](#deployment-tasks)
13. [Documentation Tasks](#documentation-tasks)

---

## Product Overview

### Problem Statement
Field inspectors spend 70% of their time on manual report preparation instead of actual inspection work. The process involves capturing hundreds of photos, voice notes, and documents, then manually transcribing and categorizing everything into structured reports.

### Solution
AuditPilot automates the report generation pipeline using multimodal AI models to process images, audio, and documents, reducing report preparation time from 4 hours to 20 minutes.

### Target Users
- Field inspectors (construction, utilities, manufacturing)
- Safety engineers and compliance officers
- Property managers
- Quality assurance teams

---

## Objectives & Success Metrics

### Primary Objectives
1. Reduce report preparation time by 80%
2. Achieve 95%+ classification accuracy with human review
3. Process 50 files in under 5 minutes
4. Keep ML inference cost under $0.05 per inspection

### Success Metrics
- **User Adoption**: 10+ inspections per organization per month
- **Processing Speed**: < 5 minutes for 50 files
- **Accuracy**: 95%+ correct classifications after human review
- **Cost**: < $0.05 per inspection in ML costs
- **Confidence Rate**: 70-80% auto-classified without review

---

## User Personas

### Persona 1: Field Inspector (Primary User)
- **Name**: Sarah Chen
- **Role**: Safety Inspector
- **Goals**: Complete inspections quickly, ensure nothing is missed
- **Pain Points**: Hates paperwork, wants to spend time in the field
- **Technical Skill**: Medium (comfortable with mobile apps)

### Persona 2: Safety Engineer (Reviewer)
- **Name**: Michael Rodriguez
- **Role**: Lead Safety Engineer
- **Goals**: Ensure compliance, track trends, review critical findings
- **Pain Points**: Needs to review too many reports, hard to find precedents
- **Technical Skill**: High

### Persona 3: Operations Manager (Admin)
- **Name**: Lisa Thompson
- **Role**: Operations Director
- **Goals**: Monitor team performance, control costs, ensure quality
- **Pain Points**: No visibility into process efficiency, cost overruns
- **Technical Skill**: Medium

---

## Technical Requirements

### Technology Stack

**Frontend:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- shadcn/ui components
- React Hook Form
- Recharts for visualizations

**Backend:**
- FastAPI (Python 3.11+)
- SQLAlchemy ORM
- Pydantic for validation
- Python-multipart for file uploads

**Infrastructure:**
- Supabase (PostgreSQL, pgvector, Authentication, Storage)
- Local filesystem (demo file storage)
- FastAPI BackgroundTasks (job processing)

**ML/AI:**
- Hugging Face Inference API
- Models: BLIP, BART, Whisper, Sentence Transformers

**Deployment:**
- Vercel (frontend)
- Railway (backend worker)

---

## Detailed Task Breakdown

---

## PHASE 1: PROJECT SETUP & INFRASTRUCTURE

### 1.1 Initial Project Scaffolding

#### Task 1.1.1: Create Next.js Project
**Description**: Initialize Next.js 14 project with TypeScript and App Router

**Steps:**
1. Run `npx create-next-app@latest auditpilot-frontend`
2. Select options:
   - TypeScript: Yes
   - ESLint: Yes
   - Tailwind CSS: Yes
   - App Router: Yes
   - Import alias: @/*
3. Initialize git repository
4. Create initial folder structure:
   ```
   /app
     /api
     /dashboard
     /inspection/[id]
     /auth
   /components
     /ui
     /features
   /lib
     /api
     /utils
     /hooks
   /types
   ```

**Acceptance Criteria:**
- [ ] Project runs with `npm run dev`
- [ ] TypeScript compiles without errors
- [ ] Folder structure matches specification
- [ ] Git initialized with .gitignore

**Dependencies:** None

---

#### Task 1.1.2: Set Up shadcn/ui
**Description**: Install and configure shadcn/ui component library

**Steps:**
1. Run `npx shadcn-ui@latest init`
2. Configure:
   - Style: Default
   - Base color: Slate
   - CSS variables: Yes
3. Install initial components:
   ```bash
   npx shadcn-ui@latest add button
   npx shadcn-ui@latest add card
   npx shadcn-ui@latest add dropdown-menu
   npx shadcn-ui@latest add input
   npx shadcn-ui@latest add label
   npx shadcn-ui@latest add select
   npx shadcn-ui@latest add table
   npx shadcn-ui@latest add badge
   npx shadcn-ui@latest add dialog
   npx shadcn-ui@latest add toast
   npx shadcn-ui@latest add progress
   npx shadcn-ui@latest add tabs
   ```
4. Create `components/ui/index.ts` barrel export

**Acceptance Criteria:**
- [ ] shadcn/ui configured in components.json
- [ ] All listed components installed
- [ ] Test component renders successfully
- [ ] Tailwind theme extended with shadcn colors

**Dependencies:** Task 1.1.1

---

#### Task 1.1.3: Create FastAPI Backend
**Description**: Initialize FastAPI backend with project structure

**Steps:**
1. Create `/backend` directory in project root
2. Create Python virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
3. Create `requirements.txt`:
   ```
   fastapi==0.109.0
   uvicorn[standard]==0.27.0
   python-multipart==0.0.6
   sqlalchemy==2.0.25
   pydantic==2.5.3
   python-dotenv==1.0.0
   httpx>=0.24,<0.26
   pypdf==3.17.4
   pillow==10.2.0
   supabase==2.3.4
   pgvector==0.2.4
   psycopg2-binary==2.9.9
   ```
4. Install dependencies: `pip install -r requirements.txt`
5. Create folder structure:
   ```
   /backend
     /app
       /api
         /routes
       /core
       /models
       /schemas
       /services
       /workers
     /tests
     main.py
   ```
6. Create `main.py`:
   ```python
   from fastapi import FastAPI
   from fastapi.middleware.cors import CORSMiddleware
   
   app = FastAPI(title="AuditPilot API")
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   
   @app.get("/health")
   def health_check():
       return {"status": "healthy"}
   ```
7. Test server runs: `uvicorn main:app --reload`

**Acceptance Criteria:**
- [ ] Backend server starts on port 8000
- [ ] /health endpoint returns 200
- [ ] CORS configured for frontend
- [ ] Virtual environment documented in README

**Dependencies:** None

---

#### Task 1.1.4: Set Up Environment Variables
**Description**: Create environment variable structure for all services

**Steps:**
1. Create `/frontend/.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_SUPABASE_URL=
   NEXT_PUBLIC_SUPABASE_ANON_KEY=
   ```
2. Create `/backend/.env`:
   ```
   # Supabase
   SUPABASE_URL=
   SUPABASE_KEY=
   SUPABASE_SERVICE_KEY=
   
   # Hugging Face
   HF_API_TOKEN=
   ```
3. Create `.env.example` files (without values)
4. Add `.env*` to `.gitignore`
5. Document all required environment variables in README

**Acceptance Criteria:**
- [ ] Environment files created
- [ ] .env files in .gitignore
- [ ] .env.example files committed
- [ ] README documents all variables

**Dependencies:** Task 1.1.1, 1.1.3

---

### 1.2 Third-Party Service Setup

#### Task 1.2.1: Set Up Supabase Project
**Description**: Create and configure Supabase project for PostgreSQL + pgvector

**Steps:**
1. Go to supabase.com and create account
2. Create new project:
   - Name: auditpilot
   - Database password: Generate strong password (save securely)
   - Region: Choose closest to users
3. Wait for project provisioning (~2 minutes)
4. Enable pgvector extension:
   - Go to Database → Extensions
   - Search for "vector"
   - Enable "vector" extension
5. Copy credentials:
   - Project URL
   - Anon public key
   - Service role key (keep secret)
6. Add to environment variables
7. Install Supabase client:
   - Frontend: `npm install @supabase/supabase-js`
   - Backend: `pip install supabase`
8. Create Supabase client files:
   - Frontend: `/lib/supabase.ts`
   - Backend: `/app/core/supabase.py`

**Acceptance Criteria:**
- [ ] Supabase project created
- [ ] pgvector extension enabled
- [ ] Credentials saved securely
- [ ] Client libraries installed
- [ ] Connection test successful

**Dependencies:** Task 1.1.4

---

#### Task 1.2.2: Set Up Local File Storage
**Description**: Configure local directory for file uploads
**Status**: [x] Completed

**Steps:**
1. Create `storage_service.py` to handle local file saving
2. Configure `LOCAL_UPLOAD_DIR` environment variable
3. Ensure directory exists on startup
4. Return local file paths instead of presigned URLs for MVP

**Acceptance Criteria:**
- [x] Files save locally
- [x] Service returns correct local paths

**Dependencies:** Task 1.1.1

---

#### Task 1.2.3: Set Up Background Tasks
**Description**: Configure FastAPI BackgroundTasks for async processing
**Status**: [x] Completed

**Steps:**
1. Use FastAPI's built-in `BackgroundTasks` in routes
2. Create synchronous wrapper `process_file_background` in worker
3. Pass file IDs to background task instead of full payloads
4. Handle database sessions within the background task

**Acceptance Criteria:**
- [x] Background processing works
- [x] DB sessions handled correctly
- [x] No external queue dependencies needed

**Dependencies:** Task 1.1.1

---

#### Task 1.2.4: Set Up Supabase Auth
**Description**: Configure Supabase Authentication

**Steps:**
1. Enable Email/Password Auth in Supabase Dashboard
2. Get Project URL and Anon Key
3. Add to `.env.local` as `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`
4. Install `@supabase/ssr` in frontend
5. Install `supabase` python client in backend

**Acceptance Criteria:**
- [ ] Supabase Auth configured
- [ ] Environment variables set
- [ ] Clients installed

**Dependencies:** Task 1.1.4

---

#### Task 1.2.5: Set Up Hugging Face Account
**Description**: Get API access for ML models

**Steps:**
1. Sign up at huggingface.co
2. Go to Settings → Access Tokens
3. Create new token:
   - Name: auditpilot-inference
   - Type: Read
4. Copy token
5. Add to environment variables
6. Install Hugging Face client:
   - Backend: `pip install huggingface-hub`
7. Test API access with simple inference call
8. Review rate limits (free tier: 30 requests/minute)

**Acceptance Criteria:**
- [ ] Hugging Face account created
- [ ] API token generated
- [ ] Token in environment variables
- [ ] Test inference call successful
- [ ] Rate limits documented

**Dependencies:** Task 1.1.4

---

## PHASE 2: DATABASE SCHEMA & MODELS

### 2.1 Database Schema Implementation

#### Task 2.1.1: Create Organizations Table
**Description**: Implement organizations table for multi-tenancy

**Steps:**
1. Create migration file: `/backend/migrations/001_create_organizations.sql`
2. Write SQL:
   ```sql
   CREATE TABLE organizations (
       id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
       name TEXT NOT NULL,
       slug TEXT UNIQUE NOT NULL,
       settings JSONB DEFAULT '{"confidence_threshold": 0.65, "categories": []}'::jsonb,
       created_at TIMESTAMP DEFAULT NOW(),
       updated_at TIMESTAMP DEFAULT NOW()
   );
   
   CREATE INDEX idx_organizations_slug ON organizations(slug);
   ```
3. Run migration in Supabase SQL Editor
4. Create SQLAlchemy model: `/backend/app/models/organization.py`
5. Create Pydantic schema: `/backend/app/schemas/organization.py`
6. Verify table created with `SELECT * FROM organizations`

**Acceptance Criteria:**
- [ ] Table exists in Supabase
- [ ] SQLAlchemy model defined
- [ ] Pydantic schemas created
- [ ] Indexes created
- [ ] Test insert/select works

**Dependencies:** Task 1.2.1

---

#### Task 2.1.2: Create Users Table
**Description**: Implement users table linked to Clerk

**Steps:**
1. Create migration: `/backend/migrations/002_create_users.sql`
2. Write SQL:
   ```sql
   CREATE TABLE users (
       id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
       clerk_user_id TEXT UNIQUE NOT NULL,
       org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
       role TEXT NOT NULL CHECK (role IN ('admin', 'inspector', 'reviewer', 'viewer')),
       name TEXT NOT NULL,
       email TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT NOW(),
       updated_at TIMESTAMP DEFAULT NOW()
   );
   
   CREATE INDEX idx_users_clerk_id ON users(clerk_user_id);
   CREATE INDEX idx_users_org_id ON users(org_id);
   ```
3. Run migration
4. Create SQLAlchemy model: `/backend/app/models/user.py`
5. Create Pydantic schemas: `/backend/app/schemas/user.py`

**Acceptance Criteria:**
- [ ] Table exists with foreign key to organizations
- [ ] Role constraint enforced
- [ ] Indexes created
- [ ] Models and schemas defined

**Dependencies:** Task 2.1.1

---

#### Task 2.1.3: Create Inspections Table
**Description**: Core table for inspection records

**Steps:**
1. Create migration: `/backend/migrations/003_create_inspections.sql`
2. Write SQL:
   ```sql
   CREATE TABLE inspections (
       id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
       org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
       name TEXT NOT NULL,
       site_location TEXT,
       site_address TEXT,
       inspector_id UUID REFERENCES users(id),
       status TEXT DEFAULT 'processing' CHECK (status IN ('processing', 'review', 'completed', 'failed')),
       risk_level TEXT CHECK (risk_level IN ('critical', 'high', 'medium', 'low', 'clear')),
       report_narrative TEXT,
       total_findings INTEGER DEFAULT 0,
       total_files INTEGER DEFAULT 0,
       processing_started_at TIMESTAMP,
       processing_completed_at TIMESTAMP,
       created_at TIMESTAMP DEFAULT NOW(),
       updated_at TIMESTAMP DEFAULT NOW()
   );
   
   CREATE INDEX idx_inspections_org_id ON inspections(org_id);
   CREATE INDEX idx_inspections_inspector_id ON inspections(inspector_id);
   CREATE INDEX idx_inspections_status ON inspections(status);
   CREATE INDEX idx_inspections_created_at ON inspections(created_at DESC);
   ```
3. Run migration
4. Create model and schemas

**Acceptance Criteria:**
- [ ] Table created with constraints
- [ ] All indexes created
- [ ] Foreign keys work
- [ ] Status enum validated

**Dependencies:** Task 2.1.1, 2.1.2

---

#### Task 2.1.4: Create Files Table
**Description**: Track uploaded files for each inspection

**Steps:**
1. Create migration: `/backend/migrations/004_create_files.sql`
2. Write SQL:
   ```sql
   CREATE TABLE files (
       id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
       inspection_id UUID REFERENCES inspections(id) ON DELETE CASCADE,
       file_type TEXT NOT NULL CHECK (file_type IN ('image', 'audio', 'pdf', 'other')),
       file_name TEXT NOT NULL,
       storage_url TEXT NOT NULL,
       storage_key TEXT NOT NULL,
       file_size INTEGER,
       mime_type TEXT,
       status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
       error_message TEXT,
       processed_at TIMESTAMP,
       created_at TIMESTAMP DEFAULT NOW()
   );
   
   CREATE INDEX idx_files_inspection_id ON files(inspection_id);
   CREATE INDEX idx_files_status ON files(status);
   CREATE INDEX idx_files_file_type ON files(file_type);
   ```
3. Run migration
4. Create model and schemas

**Acceptance Criteria:**
- [ ] Table created
- [ ] File type validation works
- [ ] Cascade delete configured
- [ ] Model and schemas created

**Dependencies:** Task 2.1.3

---

#### Task 2.1.5: Create Findings Table with pgvector
**Description**: Store AI-processed findings with vector embeddings

**Steps:**
1. Create migration: `/backend/migrations/005_create_findings.sql`
2. Write SQL:
   ```sql
   CREATE TABLE findings (
       id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
       inspection_id UUID REFERENCES inspections(id) ON DELETE CASCADE,
       file_id UUID REFERENCES files(id) ON DELETE CASCADE,
       category TEXT NOT NULL,
       severity TEXT CHECK (severity IN ('critical', 'high', 'medium', 'low', 'clear')),
       confidence_score FLOAT CHECK (confidence_score >= 0 AND confidence_score <= 1),
       needs_review BOOLEAN DEFAULT false,
       description TEXT,
       ai_caption TEXT,
       transcription TEXT,
       location_code TEXT,
       equipment_id TEXT,
       metadata JSONB DEFAULT '{}'::jsonb,
       embedding VECTOR(384),  -- pgvector column
       created_at TIMESTAMP DEFAULT NOW(),
       updated_at TIMESTAMP DEFAULT NOW()
   );
   
   CREATE INDEX idx_findings_inspection_id ON findings(inspection_id);
   CREATE INDEX idx_findings_file_id ON findings(file_id);
   CREATE INDEX idx_findings_category ON findings(category);
   CREATE INDEX idx_findings_severity ON findings(severity);
   CREATE INDEX idx_findings_needs_review ON findings(needs_review) WHERE needs_review = true;
   
   -- Vector similarity index (HNSW for fast approximate search)
   CREATE INDEX idx_findings_embedding ON findings USING hnsw (embedding vector_cosine_ops);
   ```
3. Run migration
4. Verify pgvector index created
5. Create model and schemas

**Acceptance Criteria:**
- [ ] Table created with VECTOR column
- [ ] All indexes including HNSW created
- [ ] Constraint checks work
- [ ] Test embedding insert/query

**Dependencies:** Task 2.1.3, 2.1.4, Task 1.2.1 (pgvector enabled)

---

#### Task 2.1.6: Create Human Reviews Table
**Description**: Track manual corrections of AI classifications

**Steps:**
1. Create migration: `/backend/migrations/006_create_human_reviews.sql`
2. Write SQL:
   ```sql
   CREATE TABLE human_reviews (
       id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
       finding_id UUID REFERENCES findings(id) ON DELETE CASCADE,
       reviewer_id UUID REFERENCES users(id),
       original_category TEXT NOT NULL,
       corrected_category TEXT NOT NULL,
       original_severity TEXT,
       corrected_severity TEXT,
       notes TEXT,
       review_duration_seconds INTEGER,
       reviewed_at TIMESTAMP DEFAULT NOW()
   );
   
   CREATE INDEX idx_human_reviews_finding_id ON human_reviews(finding_id);
   CREATE INDEX idx_human_reviews_reviewer_id ON human_reviews(reviewer_id);
   CREATE INDEX idx_human_reviews_reviewed_at ON human_reviews(reviewed_at DESC);
   ```
3. Run migration
4. Create model and schemas

**Acceptance Criteria:**
- [ ] Table created
- [ ] Foreign keys work
- [ ] Can track before/after corrections

**Dependencies:** Task 2.1.5, 2.1.2

---

#### Task 2.1.7: Create Usage Logs Table
**Description**: Track ML inference costs per inspection

**Steps:**
1. Create migration: `/backend/migrations/007_create_usage_logs.sql`
2. Write SQL:
   ```sql
   CREATE TABLE usage_logs (
       id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
       inspection_id UUID REFERENCES inspections(id) ON DELETE CASCADE,
       file_id UUID REFERENCES files(id) ON DELETE SET NULL,
       model_name TEXT NOT NULL,
       task_type TEXT NOT NULL,
       input_tokens INTEGER,
       output_tokens INTEGER,
       processing_time_ms INTEGER,
       cost_usd DECIMAL(10, 6),
       timestamp TIMESTAMP DEFAULT NOW()
   );
   
   CREATE INDEX idx_usage_logs_inspection_id ON usage_logs(inspection_id);
   CREATE INDEX idx_usage_logs_timestamp ON usage_logs(timestamp DESC);
   CREATE INDEX idx_usage_logs_model_name ON usage_logs(model_name);
   ```
3. Run migration
4. Create model and schemas
5. Create cost calculation utility

**Acceptance Criteria:**
- [ ] Table created
- [ ] Can log ML usage
- [ ] Can calculate costs per inspection
- [ ] Indexes support analytics queries

**Dependencies:** Task 2.1.3, 2.1.4

---

#### Task 2.1.8: Set Up Row Level Security (RLS)
**Description**: Implement multi-tenant data isolation

**Steps:**
1. Create migration: `/backend/migrations/008_setup_rls.sql`
2. Enable RLS on all tables:
   ```sql
   ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
   ALTER TABLE users ENABLE ROW LEVEL SECURITY;
   ALTER TABLE inspections ENABLE ROW LEVEL SECURITY;
   ALTER TABLE files ENABLE ROW LEVEL SECURITY;
   ALTER TABLE findings ENABLE ROW LEVEL SECURITY;
   ALTER TABLE human_reviews ENABLE ROW LEVEL SECURITY;
   ALTER TABLE usage_logs ENABLE ROW LEVEL SECURITY;
   ```
3. Create RLS policies for each table (example for inspections):
   ```sql
   CREATE POLICY inspections_org_isolation ON inspections
       USING (org_id = current_setting('app.current_org_id')::uuid);
   ```
4. Create policies for all tables
5. Test data isolation between orgs

**Acceptance Criteria:**
- [ ] RLS enabled on all tables
- [ ] Policies prevent cross-org access
- [ ] Service role can bypass RLS
- [ ] Test confirms isolation

**Dependencies:** All previous database tasks

---

### 2.2 Database Utilities & Services

#### Task 2.2.1: Create Database Connection Manager
**Description**: Set up database connection pooling

**Steps:**
1. Create `/backend/app/core/database.py`
2. Implement SQLAlchemy engine and session:
   ```python
   from sqlalchemy import create_engine
   from sqlalchemy.ext.declarative import declarative_base
   from sqlalchemy.orm import sessionmaker
   
   SQLALCHEMY_DATABASE_URL = os.getenv("SUPABASE_URL")
   
   engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   Base = declarative_base()
   
   def get_db():
       db = SessionLocal()
       try:
           yield db
       finally:
           db.close()
   ```
3. Create context manager for org-scoped queries
4. Test connection pooling

**Acceptance Criteria:**
- [ ] Connection pool configured
- [ ] get_db dependency works
- [ ] Connections properly closed
- [ ] Pool size appropriate

**Dependencies:** Task 2.1.1-2.1.7

---

#### Task 2.2.2: Create Repository Pattern Classes
**Description**: Implement data access layer

**Steps:**
1. Create `/backend/app/repositories/base.py` with base repository
2. Create specific repositories:
   - `/backend/app/repositories/organization_repository.py`
   - `/backend/app/repositories/user_repository.py`
   - `/backend/app/repositories/inspection_repository.py`
   - `/backend/app/repositories/file_repository.py`
   - `/backend/app/repositories/finding_repository.py`
3. Implement CRUD operations for each
4. Add org_id scoping to all queries
5. Create vector search method in finding_repository

**Acceptance Criteria:**
- [ ] All repositories implemented
- [ ] CRUD operations work
- [ ] Queries scoped by org_id
- [ ] Vector search function works

**Dependencies:** Task 2.2.1

---

## PHASE 3: FILE UPLOAD & STORAGE

### 3.1 File Upload Backend

#### Task 3.1.1: Create R2 Storage Service
**Description**: Implement file upload/download service

**Steps:**
1. Create `/backend/app/services/storage_service.py`
2. Implement methods:
   ```python
   class StorageService:
       def __init__(self):
           self.s3_client = boto3.client(
               's3',
               endpoint_url=f'https://{ACCOUNT_ID}.r2.cloudflarestorage.com',
               aws_access_key_id=ACCESS_KEY_ID,
               aws_secret_access_key=SECRET_ACCESS_KEY
           )
       
       async def upload_file(self, file: UploadFile, org_id: str, inspection_id: str):
           # Generate unique key
           # Upload to R2
           # Return storage URL
           pass
       
       async def download_file(self, storage_key: str):
           # Download from R2
           # Return file bytes
           pass
       
       async def delete_file(self, storage_key: str):
           pass
       
       async def generate_presigned_url(self, storage_key: str):
           pass
   ```
3. Add error handling
4. Test upload/download

**Acceptance Criteria:**
- [ ] Can upload files to R2
- [ ] Can download files from R2
- [ ] Unique keys generated
- [ ] Error handling works

**Dependencies:** Task 1.2.2

---

#### Task 3.1.2: Create File Upload Endpoint
**Description**: API endpoint for multipart file uploads

**Steps:**
1. Create `/backend/app/api/routes/files.py`
2. Implement POST endpoint:
   ```python
   @router.post("/inspections/{inspection_id}/files")
   async def upload_files(
       inspection_id: str,
       files: List[UploadFile] = File(...),
       db: Session = Depends(get_db),
       current_user: User = Depends(get_current_user)
   ):
       # Validate file types and sizes
       # Upload to R2
       # Create file records in database
       # Queue processing jobs
       # Return file IDs
       pass
   ```
3. Add file validation:
   - Max size: 50MB per file
   - Allowed types: jpg, png, mp3, m4a, wav, pdf
4. Implement chunked upload for large files
5. Add rate limiting

**Acceptance Criteria:**
- [ ] Endpoint accepts multiple files
- [ ] File validation works
- [ ] Files uploaded to R2
- [ ] Database records created
- [ ] Proper error responses

**Dependencies:** Task 3.1.1

---

#### Task 3.1.3: Create File Metadata Endpoint
**Description**: Get file status and metadata

**Steps:**
1. Add GET endpoint to `/backend/app/api/routes/files.py`:
   ```python
   @router.get("/files/{file_id}")
   async def get_file(
       file_id: str,
       db: Session = Depends(get_db),
       current_user: User = Depends(get_current_user)
   ):
       # Get file record
       # Check org access
       # Return metadata and status
       pass
   ```
2. Add list files for inspection endpoint
3. Add file download endpoint with presigned URLs

**Acceptance Criteria:**
- [ ] Can retrieve file metadata
- [ ] Can list all files for inspection
- [ ] Presigned URLs work for downloads
- [ ] Org isolation enforced

**Dependencies:** Task 3.1.2

---

### 3.2 File Upload Frontend

#### Task 3.2.1: Create File Upload Component
**Description**: Drag-and-drop file upload UI

**Steps:**
1. Create `/components/features/FileUpload.tsx`
2. Implement drag-and-drop:
   ```typescript
   export function FileUpload({ inspectionId }: { inspectionId: string }) {
     const [files, setFiles] = useState<File[]>([]);
     const [uploading, setUploading] = useState(false);
     
     const onDrop = useCallback((acceptedFiles: File[]) => {
       setFiles(prev => [...prev, ...acceptedFiles]);
     }, []);
     
     const { getRootProps, getInputProps } = useDropzone({
       onDrop,
       accept: {
         'image/*': ['.jpg', '.jpeg', '.png'],
         'audio/*': ['.mp3', '.m4a', '.wav'],
         'application/pdf': ['.pdf']
       },
       maxSize: 50 * 1024 * 1024 // 50MB
     });
     
     // Upload logic
   }
   ```
3. Add file preview thumbnails
4. Show upload progress per file
5. Display file validation errors
6. Add remove file button

**Acceptance Criteria:**
- [ ] Drag-and-drop works
- [ ] File type validation
- [ ] Size validation
- [ ] Upload progress shown
- [ ] Error handling

**Dependencies:** Task 3.1.2

---

#### Task 3.2.2: Implement File Upload Logic
**Description**: Connect upload component to API

**Steps:**
1. Create `/lib/api/files.ts` with API functions:
   ```typescript
   export async function uploadFiles(
     inspectionId: string,
     files: File[]
   ): Promise<FileUploadResponse> {
     const formData = new FormData();
     files.forEach(file => formData.append('files', file));
     
     const response = await fetch(
       `${API_URL}/inspections/${inspectionId}/files`,
       {
         method: 'POST',
         body: formData,
         headers: {
           'Authorization': `Bearer ${token}`
         }
       }
     );
     
     return response.json();
   }
   ```
2. Add upload queue (upload 3 files at a time)
3. Implement retry logic for failed uploads
4. Add pause/resume functionality
5. Store uploaded file IDs in state

**Acceptance Criteria:**
- [ ] Files upload successfully
- [ ] Progress tracked per file
- [ ] Failed uploads retry
- [ ] Can handle 50+ files
- [ ] Proper error messages

**Dependencies:** Task 3.2.1

---

#### Task 3.2.3: Create File Status Display
**Description**: Show real-time processing status

**Steps:**
1. Create `/components/features/FileStatusList.tsx`
2. Display files with status badges:
   - Pending (gray)
   - Processing (blue, animated)
   - Completed (green)
   - Failed (red)
3. Connect to Supabase real-time subscriptions:
   ```typescript
   useEffect(() => {
     const subscription = supabase
       .channel('files')
       .on('postgres_changes', {
         event: 'UPDATE',
         schema: 'public',
         table: 'files',
         filter: `inspection_id=eq.${inspectionId}`
       }, (payload) => {
         // Update file status in state
       })
       .subscribe();
     
     return () => subscription.unsubscribe();
   }, [inspectionId]);
   ```
4. Show processing progress bar
5. Display error messages for failed files

**Acceptance Criteria:**
- [ ] Real-time status updates
- [ ] Status badges display correctly
- [ ] Progress indicators work
- [ ] Error messages shown
- [ ] Auto-refreshes on updates

**Dependencies:** Task 3.2.2, Task 1.2.1

---

## PHASE 4: ASYNC FILE PROCESSING

### 4.1 Background processing setup

#### Task 4.1.1: Configure FastAPI BackgroundTasks
**Description**: Set up built-in async task execution
**Status**: [x] Completed

**Steps:**
1. Import `BackgroundTasks` from FastAPI
2. Inject into upload endpoints
3. Add processing function to background tasks after saving file record

**Acceptance Criteria:**
- [x] BackgroundTasks used in routes
- [x] API returns immediately while processing happens

**Dependencies:** Task 3.2.1

---

#### Task 4.1.2: Create File Dispatcher
**Description**: Route files to correct processing pipeline
**Status**: [x] Completed

**Steps:**
1. Create `/backend/app/workers/file_processor.py`
2. Implement synchronous entry point `process_file_background` that handles its own DB session
3. Implement async dispatcher `_process_file` that calls correct ML models
4. Handle status updates (processing → completed/failed)
5. Add error handling and logging

**Acceptance Criteria:**
- [x] Files routed by type
- [x] DB sessions handled correctly per task
- [x] Status updates working
- [x] Errors caught and logged

**Dependencies:** Task 4.1.1

---

#### Task 4.1.3: Create Job Status Tracker
**Description**: Track job progress and status

**Steps:**
1. Create `/backend/app/services/job_tracker.py`
2. Implement status tracking:
   ```python
   class JobTracker:
       def update_file_status(self, file_id: str, status: str, error: str = None):
           # Update files table
           pass
       
       def update_inspection_progress(self, inspection_id: str):
           # Calculate total files vs processed
           # Update inspection status if all complete
           pass
       
       def log_processing_step(self, file_id: str, step: str, duration: float):
           # Log for analytics
           pass
   ```
3. Add websocket notifications for real-time updates
4. Create inspection completion trigger

**Acceptance Criteria:**
- [ ] File status updates work
- [ ] Inspection status auto-updates
- [ ] Real-time notifications sent
- [ ] Processing logs captured

**Dependencies:** Task 4.1.2

---

## PHASE 5: ML PROCESSING PIPELINE

### 5.1 Hugging Face Integration

#### Task 5.1.1: Create HF Inference Client
**Description**: Client for Hugging Face Inference API

**Steps:**
1. Create `/backend/app/services/hf_client.py`
2. Implement base client:
   ```python
   import httpx
   
   class HFInferenceClient:
       def __init__(self):
           self.api_url = "https://api-inference.huggingface.co/models"
           self.headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
           self.client = httpx.AsyncClient(timeout=60.0)
       
       async def inference(self, model: str, inputs: dict):
           response = await self.client.post(
               f"{self.api_url}/{model}",
               headers=self.headers,
               json=inputs
           )
           return response.json()
       
       async def close(self):
           await self.client.aclose()
   ```
3. Add rate limiting (30 req/min)
4. Implement retry with exponential backoff
5. Add response caching for identical inputs

**Acceptance Criteria:**
- [ ] Can call HF models
- [ ] Rate limiting works
- [ ] Retries on failures
- [ ] Proper error handling

**Dependencies:** Task 1.2.5

---

#### Task 5.1.2: Implement Image Captioning
**Description**: Generate descriptions from images

**Steps:**
1. Create `/backend/app/services/image_processor.py`
2. Implement image captioning:
   ```python
   async def generate_caption(self, image_bytes: bytes) -> str:
       # Encode image to base64
       image_b64 = base64.b64encode(image_bytes).decode()
       
       # Call BLIP model
       result = await self.hf_client.inference(
           "Salesforce/blip-image-captioning-large",
           {"inputs": image_b64}
       )
       
       caption = result[0]["generated_text"]
       return caption
   ```
3. Add image preprocessing (resize if > 2MB)
4. Handle various image formats
5. Add caption quality validation

**Acceptance Criteria:**
- [ ] Generates accurate captions
- [ ] Handles all image formats
- [ ] Preprocessing works
- [ ] Error handling

**Dependencies:** Task 5.1.1

---

#### Task 5.1.3: Implement Zero-Shot Classification
**Description**: Categorize findings without training

**Steps:**
1. Add to `/backend/app/services/image_processor.py`
2. Implement classification:
   ```python
   DEFECT_CATEGORIES = [
       "structural damage",
       "electrical hazard",
       "water damage",
       "fire risk",
       "equipment issue",
       "fall hazard",
       "clear/no defect"
   ]
   
   async def classify_finding(self, caption: str) -> dict:
       result = await self.hf_client.inference(
           "facebook/bart-large-mnli",
           {
               "inputs": caption,
               "parameters": {
                   "candidate_labels": DEFECT_CATEGORIES
               }
           }
       )
       
       # Extract top prediction and confidence
       category = result["labels"][0]
       confidence = result["scores"][0]
       
       return {
           "category": category,
           "confidence": confidence,
           "all_scores": dict(zip(result["labels"], result["scores"]))
       }
   ```
3. Add confidence threshold check (0.65)
4. Map categories to severity levels
5. Return alternative predictions

**Acceptance Criteria:**
- [ ] Classification works
- [ ] Confidence scores accurate
- [ ] Threshold check works
- [ ] Returns all alternatives

**Dependencies:** Task 5.1.2

---

#### Task 5.1.4: Implement Audio Transcription
**Description**: Convert audio to text using Whisper

**Steps:**
1. Create `/backend/app/services/audio_processor.py`
2. Implement transcription:
   ```python
   async def transcribe_audio(self, audio_bytes: bytes, mime_type: str) -> str:
       # Convert to compatible format if needed
       audio_b64 = base64.b64encode(audio_bytes).decode()
       
       result = await self.hf_client.inference(
           "openai/whisper-large-v3",
           {"inputs": audio_b64}
       )
       
       transcription = result["text"]
       return transcription
   ```
3. Add audio format conversion (ffmpeg)
4. Handle long audio files (chunk if > 5 min)
5. Add timestamps for long recordings

**Acceptance Criteria:**
- [ ] Transcribes audio accurately
- [ ] Handles multiple formats
- [ ] Chunks long audio
- [ ] Returns timestamps

**Dependencies:** Task 5.1.1

---

#### Task 5.1.5: Implement Named Entity Recognition
**Description**: Extract structured data from transcriptions

**Steps:**
1. Add to `/backend/app/services/audio_processor.py`
2. Implement NER:
   ```python
   async def extract_entities(self, text: str) -> dict:
       result = await self.hf_client.inference(
           "dslim/bert-base-NER",
           {"inputs": text}
       )
       
       entities = {
           "equipment_ids": [],
           "locations": [],
           "people": [],
           "dates": [],
           "standards": []
       }
       
       # Parse NER results and categorize
       for entity in result:
           if entity["entity_group"] == "ORG":
               entities["equipment_ids"].append(entity["word"])
           # ... more parsing logic
       
       return entities
   ```
3. Add custom patterns for inspection-specific entities
4. Extract OSHA/standard references
5. Clean and normalize extracted entities

**Acceptance Criteria:**
- [ ] Extracts relevant entities
- [ ] Categorizes correctly
- [ ] Handles inspection jargon
- [ ] Returns structured data

**Dependencies:** Task 5.1.4

---

#### Task 5.1.6: Implement PDF Text Extraction
**Description**: Extract text from PDF documents

**Steps:**
1. Create `/backend/app/services/pdf_processor.py`
2. Implement text extraction:
   ```python
   from pypdf import PdfReader
   
   async def extract_text(self, pdf_bytes: bytes) -> str:
       reader = PdfReader(BytesIO(pdf_bytes))
       
       text = ""
       for page in reader.pages:
           text += page.extract_text() + "\n\n"
       
       return text
   ```
3. Add OCR fallback for scanned PDFs (Tesseract)
4. Clean extracted text (remove artifacts)
5. Chunk text for embeddings

**Acceptance Criteria:**
- [ ] Extracts text from PDFs
- [ ] OCR works for scanned docs
- [ ] Text cleaning works
- [ ] Chunks appropriately

**Dependencies:** None (uses pypdf)

---

#### Task 5.1.7: Implement Document QA
**Description**: Answer questions about uploaded documents

**Steps:**
1. Add to `/backend/app/services/pdf_processor.py`
2. Implement QA:
   ```python
   async def answer_question(self, context: str, question: str) -> str:
       result = await self.hf_client.inference(
           "deepset/roberta-base-squad2",
           {
               "inputs": {
                   "question": question,
                   "context": context
               }
           }
       )
       
       answer = result["answer"]
       confidence = result["score"]
       
       return {
           "answer": answer,
           "confidence": confidence,
           "context": context[result["start"]:result["end"]]
       }
   ```
3. Add context retrieval (find relevant sections)
4. Cache common queries
5. Handle "no answer" cases

**Acceptance Criteria:**
- [ ] Answers questions accurately
- [ ] Retrieves relevant context
- [ ] Confidence scoring works
- [ ] Handles unanswerable questions

**Dependencies:** Task 5.1.6

---

#### Task 5.1.8: Implement Summarization
**Description**: Generate inspection report narratives

**Steps:**
1. Create `/backend/app/services/summarization_service.py`
2. Implement summarization:
   ```python
   async def generate_inspection_summary(
       self,
       findings: List[dict],
       transcriptions: List[str],
       inspection_data: dict
   ) -> str:
       # Compile all inputs
       context = self._compile_context(findings, transcriptions, inspection_data)
       
       # Generate summary
       result = await self.hf_client.inference(
           "facebook/bart-large-cnn",
           {
               "inputs": context,
               "parameters": {
                   "max_length": 500,
                   "min_length": 200,
                   "do_sample": False
               }
           }
       )
       
       summary = result[0]["summary_text"]
       
       # Structure into paragraphs
       structured = self._structure_narrative(summary, findings)
       
       return structured
   ```
3. Create summary template with sections
4. Include key findings and recommendations
5. Add severity-based prioritization

**Acceptance Criteria:**
- [ ] Generates coherent narratives
- [ ] Includes all critical findings
- [ ] Proper structure (3 paragraphs)
- [ ] Prioritizes by severity

**Dependencies:** Task 5.1.1

---

#### Task 5.1.9: Implement Embedding Generation
**Description**: Generate vectors for semantic search

**Steps:**
1. Create `/backend/app/services/embedding_service.py`
2. Implement embedding generation:
   ```python
   async def generate_embedding(self, text: str) -> List[float]:
       result = await self.hf_client.inference(
           "sentence-transformers/all-MiniLM-L6-v2",
           {"inputs": text}
       )
       
       # Returns 384-dimensional vector
       embedding = result[0]
       return embedding
   ```
3. Add batch embedding generation
4. Implement caching for identical texts
5. Normalize embeddings

**Acceptance Criteria:**
- [ ] Generates 384-dim embeddings
- [ ] Batch processing works
- [ ] Caching improves performance
- [ ] Vectors normalized

**Dependencies:** Task 5.1.1

---

### 5.2 Processing Pipeline Orchestration

#### Task 5.2.1: Create Image Processing Pipeline
**Description**: Orchestrate image analysis workflow

**Steps:**
1. Update `/backend/app/workers/file_processor.py`
2. Implement image pipeline:
   ```python
   async def process_image(self, file_id: str):
       # 1. Download image from R2
       file_record = self.db.get_file(file_id)
       image_bytes = await self.storage.download_file(file_record.storage_key)
       
       # 2. Generate caption
       caption = await self.image_processor.generate_caption(image_bytes)
       
       # 3. Classify finding
       classification = await self.image_processor.classify_finding(caption)
       
       # 4. Generate embedding
       embedding = await self.embedding_service.generate_embedding(caption)
       
       # 5. Determine if needs review
       needs_review = classification["confidence"] < 0.65
       
       # 6. Create finding record
       finding = self.db.create_finding({
           "file_id": file_id,
           "inspection_id": file_record.inspection_id,
           "ai_caption": caption,
           "category": classification["category"],
           "confidence_score": classification["confidence"],
           "needs_review": needs_review,
           "embedding": embedding
       })
       
       # 7. Log usage
       await self.log_usage(file_id, "image-captioning", "BLIP")
       await self.log_usage(file_id, "classification", "BART")
       
       # 8. Update file status
       self.db.update_file_status(file_id, "completed")
   ```
3. Add error handling for each step
4. Implement step-level retries
5. Log processing time for each step

**Acceptance Criteria:**
- [ ] Full pipeline executes
- [ ] Each step completes successfully
- [ ] Error handling works
- [ ] Usage logged correctly
- [ ] Processing time tracked

**Dependencies:** Tasks 5.1.2, 5.1.3, 5.1.9

---

#### Task 5.2.2: Create Audio Processing Pipeline
**Description**: Orchestrate audio analysis workflow

**Steps:**
1. Implement audio pipeline:
   ```python
   async def process_audio(self, file_id: str):
       # 1. Download audio from R2
       file_record = self.db.get_file(file_id)
       audio_bytes = await self.storage.download_file(file_record.storage_key)
       
       # 2. Transcribe audio
       transcription = await self.audio_processor.transcribe_audio(
           audio_bytes,
           file_record.mime_type
       )
       
       # 3. Extract entities
       entities = await self.audio_processor.extract_entities(transcription)
       
       # 4. Create finding record
       finding = self.db.create_finding({
           "file_id": file_id,
           "inspection_id": file_record.inspection_id,
           "transcription": transcription,
           "location_code": entities.get("locations", [None])[0],
           "equipment_id": entities.get("equipment_ids", [None])[0],
           "metadata": entities
       })
       
       # 5. Log usage
       await self.log_usage(file_id, "transcription", "Whisper")
       
       # 6. Update file status
       self.db.update_file_status(file_id, "completed")
   ```
2. Add audio format validation
3. Handle transcription errors
4. Extract timestamp information

**Acceptance Criteria:**
- [ ] Audio transcribed correctly
- [ ] Entities extracted
- [ ] Finding created with metadata
- [ ] Usage logged

**Dependencies:** Tasks 5.1.4, 5.1.5

---

#### Task 5.2.3: Create PDF Processing Pipeline
**Description**: Orchestrate PDF analysis workflow

**Steps:**
1. Implement PDF pipeline:
   ```python
   async def process_pdf(self, file_id: str):
       # 1. Download PDF from R2
       file_record = self.db.get_file(file_id)
       pdf_bytes = await self.storage.download_file(file_record.storage_key)
       
       # 2. Extract text
       text = await self.pdf_processor.extract_text(pdf_bytes)
       
       # 3. Chunk text
       chunks = self._chunk_text(text, max_length=500)
       
       # 4. Generate embeddings for each chunk
       embeddings = []
       for chunk in chunks:
           emb = await self.embedding_service.generate_embedding(chunk)
           embeddings.append(emb)
       
       # 5. Store PDF metadata
       self.db.update_file({
           "id": file_id,
           "metadata": {
               "text": text,
               "chunks": chunks,
               "embeddings": embeddings
           }
       })
       
       # 6. Update file status
       self.db.update_file_status(file_id, "completed")
   ```
2. Add OCR for scanned PDFs
3. Handle multi-page documents
4. Extract tables if present

**Acceptance Criteria:**
- [ ] Text extracted from PDFs
- [ ] Chunking works correctly
- [ ] Embeddings generated
- [ ] Metadata stored

**Dependencies:** Tasks 5.1.6, 5.1.9

---

#### Task 5.2.4: Create Inspection Completion Handler
**Description**: Finalize inspection after all files processed

**Steps:**
1. Create `/backend/app/services/inspection_completion_service.py`
2. Implement completion handler:
   ```python
   async def finalize_inspection(self, inspection_id: str):
       # 1. Check all files processed
       files = self.db.get_inspection_files(inspection_id)
       if any(f.status != "completed" for f in files):
           return  # Not ready yet
       
       # 2. Get all findings
       findings = self.db.get_inspection_findings(inspection_id)
       
       # 3. Calculate overall risk level
       risk_level = self._calculate_risk_level(findings)
       
       # 4. Generate summary narrative
       summary = await self.summarization.generate_inspection_summary(
           findings=findings,
           transcriptions=[f.transcription for f in findings if f.transcription],
           inspection_data={"name": inspection.name, "location": inspection.site_location}
       )
       
       # 5. Update inspection record
       self.db.update_inspection({
           "id": inspection_id,
           "status": "completed" if not any(f.needs_review for f in findings) else "review",
           "risk_level": risk_level,
           "report_narrative": summary,
           "total_findings": len(findings),
           "processing_completed_at": datetime.utcnow()
       })
       
       # 6. Send notification (optional)
       await self.notify_completion(inspection_id)
   ```
3. Add risk calculation logic
4. Implement notification system
5. Calculate total processing time

**Acceptance Criteria:**
- [ ] Triggers when all files done
- [ ] Risk level calculated correctly
- [ ] Summary generated
- [ ] Inspection status updated
- [ ] Notifications sent

**Dependencies:** Tasks 5.2.1, 5.2.2, 5.2.3, 5.1.8

---

#### Task 5.2.5: Implement Cost Tracking
**Description**: Log and calculate ML inference costs

**Steps:**
1. Create `/backend/app/services/cost_tracker.py`
2. Define model costs:
   ```python
   MODEL_COSTS = {
       "Salesforce/blip-image-captioning-large": 0.0003,  # per image
       "facebook/bart-large-mnli": 0.0001,  # per classification
       "openai/whisper-large-v3": 0.006,  # per minute
       "facebook/bart-large-cnn": 0.0002,  # per summary
       "sentence-transformers/all-MiniLM-L6-v2": 0.0001  # per embedding
   }
   ```
3. Implement logging:
   ```python
   async def log_model_usage(
       self,
       inspection_id: str,
       file_id: str,
       model_name: str,
       task_type: str,
       processing_time_ms: int
   ):
       cost = MODEL_COSTS.get(model_name, 0)
       
       self.db.create_usage_log({
           "inspection_id": inspection_id,
           "file_id": file_id,
           "model_name": model_name,
           "task_type": task_type,
           "processing_time_ms": processing_time_ms,
           "cost_usd": cost
       })
   ```
4. Create cost calculation queries
5. Add monthly cost aggregation

**Acceptance Criteria:**
- [ ] Usage logged for all models
- [ ] Costs calculated accurately
- [ ] Can query total cost per inspection
- [ ] Can query monthly costs

**Dependencies:** Task 2.1.7

---

## PHASE 6: AUTHENTICATION & AUTHORIZATION

### 6.1 Supabase Auth Frontend Integration

#### Task 6.1.1: Set Up Supabase Auth in Next.js
**Description**: Configure Supabase Auth UI and SSR helpers

**Steps:**
1. Create `/lib/supabase.ts` for browser client:
   ```typescript
   import { createBrowserClient } from '@supabase/ssr'
   
   export function createClient() {
     return createBrowserClient(
       process.env.NEXT_PUBLIC_SUPABASE_URL!,
       process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
     )
   }
   ```
2. Create `/middleware.ts` to protect routes:
   ```typescript
   import { createServerClient } from '@supabase/ssr'
   import { NextResponse } from 'next/server'
   
   export async function middleware(request) {
     let response = NextResponse.next({
       request: { headers: request.headers },
     })
     
     // Create SSR client and refresh session
     const supabase = createServerClient(...)
     const { data: { user } } = await supabase.auth.getUser()
     
     // Protect all routes except /login and /signup
     if (!user && !request.nextUrl.pathname.startsWith('/login') && !request.nextUrl.pathname.startsWith('/signup')) {
       return NextResponse.redirect(new URL('/login', request.url))
     }
     return response
   }
   ```
3. Create `/app/login/page.tsx` and `/app/signup/page.tsx` using manual forms or `@supabase/auth-ui-react`
4. Update `client.ts` to append the Supabase session token to API requests automatically

**Acceptance Criteria:**
- [ ] Supabase SSR clients configured
- [ ] Auth pages work (login, signup, logout)
- [ ] Protected routes redirect to `/login`
- [ ] API client attaches `Authorization: Bearer <token>`

**Dependencies:** Task 1.2.4

---

### 6.2 Authorization & Access Control

#### Task 6.2.1: Create Backend Auth Middleware
**Description**: Verify Supabase JWTs and extract user context in FastAPI

**Steps:**
1. Create `/backend/app/core/auth.py`
2. Implement auth dependency:
   ```python
   from supabase import create_client, Client
   from fastapi.security import HTTPBearer
   
   security = HTTPBearer()
   
   async def get_current_user(
       token: HTTPAuthorizationCredentials = Depends(security),
       db: Session = Depends(get_db)
   ) -> User:
       try:
           # Supabase client handles JWT verification automatically if configured properly
           # Or manual verification using PyJWT and the Supabase JWT secret
           user = supabase.auth.get_user(token.credentials)
           if not user:
               raise HTTPException(status_code=401)
       except Exception:
           raise HTTPException(status_code=401, detail="Invalid token")
       
       # Fetch actual user record from DB by auth_id (UUID)
       db_user = db.query(User).filter(User.auth_id == user.user.id).first()
       return db_user
   ```
3. Update `User` model to link to Supabase `auth.users` UUID
4. Replace hardcoded `X-Org-Id` dependency with `get_current_user` in all endpoints

**Acceptance Criteria:**
- [ ] Token verification works
- [ ] User context extracted correctly
- [ ] `X-Org-Id` removed from frontend tracking
- [ ] All endpoints protected via bearer token

**Dependencies:** Task 6.1.1

---

## PHASE 7: FRONTEND PAGES & FEATURES

### 7.1 Dashboard Page

#### Task 7.1.1: Create Dashboard Layout
**Description**: Main dashboard structure

**Steps:**
1. Create `/app/dashboard/page.tsx`
2. Implement layout:
   ```typescript
   export default function DashboardPage() {
     return (
       <div className="container mx-auto py-8">
         <div className="mb-8">
           <h1 className="text-3xl font-bold">Dashboard</h1>
           <p className="text-muted-foreground">Overview of your inspections</p>
         </div>
         
         <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
           <StatsCard />
           <StatsCard />
           <StatsCard />
           <StatsCard />
         </div>
         
         <div className="grid gap-6 md:grid-cols-2 mt-6">
           <FindingsChart />
           <RecentInspections />
         </div>
         
         <div className="mt-6">
           <ReviewQueue />
         </div>
       </div>
     );
   }
   ```
3. Create responsive grid layout
4. Add navigation sidebar
5. Create header with org switcher

**Acceptance Criteria:**
- [ ] Layout renders correctly
- [ ] Responsive design works
- [ ] Navigation functional
- [ ] Org switcher visible

**Dependencies:** Task 6.1.1

---

#### Task 7.1.2: Create Stats Cards
**Description**: Display key metrics

**Steps:**
1. Create `/components/features/StatsCard.tsx`
2. Implement cards:
   ```typescript
   interface StatsCardProps {
     title: string;
     value: string | number;
     change?: number;
     icon?: React.ReactNode;
   }
   
   export function StatsCard({ title, value, change, icon }: StatsCardProps) {
     return (
       <Card>
         <CardHeader className="flex flex-row items-center justify-between pb-2">
           <CardTitle className="text-sm font-medium">{title}</CardTitle>
           {icon}
         </CardHeader>
         <CardContent>
           <div className="text-2xl font-bold">{value}</div>
           {change && (
             <p className="text-xs text-muted-foreground">
               {change > 0 ? '+' : ''}{change}% from last month
             </p>
           )}
         </CardContent>
       </Card>
     );
   }
   ```
3. Create API endpoint for dashboard stats
4. Fetch and display:
   - Total inspections this month
   - Pending reviews
   - Total findings
   - Average processing time
5. Add loading states

**Acceptance Criteria:**
- [ ] Cards display data correctly
- [ ] Real data from API
- [ ] Loading states work
- [ ] Change percentages calculated

**Dependencies:** Task 7.1.1

---

#### Task 7.1.3: Create Findings Chart
**Description**: Visualize findings breakdown

**Steps:**
1. Create `/components/features/FindingsChart.tsx`
2. Implement donut chart with Recharts:
   ```typescript
   import { PieChart, Pie, Cell, ResponsiveContainer, Legend } from 'recharts';
   
   export function FindingsChart() {
     const data = [
       { name: 'Structural', value: 12, color: '#ef4444' },
       { name: 'Electrical', value: 8, color: '#f59e0b' },
       { name: 'Water', value: 5, color: '#3b82f6' },
       { name: 'Fire', value: 3, color: '#dc2626' },
       { name: 'Clear', value: 22, color: '#10b981' }
     ];
     
     return (
       <Card>
         <CardHeader>
           <CardTitle>Findings by Category</CardTitle>
         </CardHeader>
         <CardContent>
           <ResponsiveContainer width="100%" height={300}>
             <PieChart>
               <Pie
                 data={data}
                 dataKey="value"
                 nameKey="name"
                 cx="50%"
                 cy="50%"
                 innerRadius={60}
                 outerRadius={80}
               >
                 {data.map((entry, index) => (
                   <Cell key={index} fill={entry.color} />
                 ))}
               </Pie>
               <Legend />
             </PieChart>
           </ResponsiveContainer>
         </CardContent>
       </Card>
     );
   }
   ```
3. Create API endpoint for findings aggregation
4. Add date range selector
5. Make chart interactive (click to filter)

**Acceptance Criteria:**
- [ ] Chart displays correctly
- [ ] Real data from API
- [ ] Interactive elements work
- [ ] Date range filtering

**Dependencies:** Task 7.1.1

---

#### Task 7.1.4: Create Recent Inspections List
**Description**: Show latest inspection activity

**Steps:**
1. Create `/components/features/RecentInspections.tsx`
2. Implement list:
   ```typescript
   export function RecentInspections() {
     const { data: inspections, isLoading } = useQuery({
       queryKey: ['inspections', 'recent'],
       queryFn: () => api.getRecentInspections(10)
     });
     
     return (
       <Card>
         <CardHeader>
           <CardTitle>Recent Inspections</CardTitle>
         </CardHeader>
         <CardContent>
           <div className="space-y-4">
             {inspections?.map(inspection => (
               <div key={inspection.id} className="flex items-center justify-between">
                 <div>
                   <p className="font-medium">{inspection.name}</p>
                   <p className="text-sm text-muted-foreground">
                     {formatDistanceToNow(inspection.created_at)} ago
                   </p>
                 </div>
                 <Badge variant={getBadgeVariant(inspection.status)}>
                   {inspection.status}
                 </Badge>
               </div>
             ))}
           </div>
         </CardContent>
       </Card>
     );
   }
   ```
3. Add click to view inspection
4. Show status badges
5. Add "View All" link

**Acceptance Criteria:**
- [ ] List displays recent inspections
- [ ] Status badges correct
- [ ] Click navigates to detail
- [ ] Relative timestamps work

**Dependencies:** Task 7.1.1

---

#### Task 7.1.5: Create Review Queue Widget
**Description**: Show findings needing human review

**Steps:**
1. Create `/components/features/ReviewQueue.tsx`
2. Implement queue display:
   ```typescript
   export function ReviewQueue() {
     const { data: findings } = useQuery({
       queryKey: ['findings', 'needs-review'],
       queryFn: () => api.getFindingsNeedingReview()
     });
     
     return (
       <Card>
         <CardHeader>
           <CardTitle>Pending Reviews ({findings?.length || 0})</CardTitle>
         </CardHeader>
         <CardContent>
           <Table>
             <TableHeader>
               <TableRow>
                 <TableHead>Inspection</TableHead>
                 <TableHead>Finding</TableHead>
                 <TableHead>AI Suggestion</TableHead>
                 <TableHead>Confidence</TableHead>
                 <TableHead>Action</TableHead>
               </TableRow>
             </TableHeader>
             <TableBody>
               {findings?.map(finding => (
                 <TableRow key={finding.id}>
                   <TableCell>{finding.inspection.name}</TableCell>
                   <TableCell className="max-w-xs truncate">
                     {finding.ai_caption}
                   </TableCell>
                   <TableCell>
                     <Badge>{finding.category}</Badge>
                   </TableCell>
                   <TableCell>
                     {(finding.confidence_score * 100).toFixed(1)}%
                   </TableCell>
                   <TableCell>
                     <Button size="sm" onClick={() => reviewFinding(finding.id)}>
                       Review
                     </Button>
                   </TableCell>
                 </TableRow>
               ))}
             </TableBody>
           </Table>
         </CardContent>
       </Card>
     );
   }
   ```
3. Add inline review functionality
4. Show aging indicators (time since flagged)
5. Add bulk review actions

**Acceptance Criteria:**
- [ ] Shows all flagged findings
- [ ] Inline review works
- [ ] Aging indicators visible
- [ ] Can mark as reviewed

**Dependencies:** Task 7.1.1

---

#### Task 7.1.6: Add Cost Tracker Widget
**Description**: Display ML processing costs

**Steps:**
1. Create `/components/features/CostTracker.tsx`
2. Implement cost display:
   ```typescript
   export function CostTracker() {
     const { data: costs } = useQuery({
       queryKey: ['costs', 'monthly'],
       queryFn: () => api.getMonthlyUsage()
     });
     
     return (
       <Card>
         <CardHeader>
           <CardTitle>ML Cost This Month</CardTitle>
         </CardHeader>
         <CardContent>
           <div className="text-3xl font-bold">
             ${costs?.total.toFixed(2)}
           </div>
           <div className="mt-4 space-y-2">
             <div className="flex justify-between text-sm">
               <span>Average per inspection:</span>
               <span className="font-medium">
                 ${costs?.avgPerInspection.toFixed(3)}
               </span>
             </div>
             <div className="flex justify-between text-sm">
               <span>Total inspections:</span>
               <span className="font-medium">{costs?.totalInspections}</span>
             </div>
           </div>
         </CardContent>
       </Card>
     );
   }
   ```
3. Add monthly trend chart
4. Show breakdown by model
5. Add cost projection

**Acceptance Criteria:**
- [ ] Displays current month cost
- [ ] Shows average per inspection
- [ ] Breakdown by model available
- [ ] Trend chart works

**Dependencies:** Task 7.1.1, Task 5.2.5

---

### 7.2 New Inspection Flow

#### Task 7.2.1: Create New Inspection Modal
**Description**: Dialog to start new inspection

**Steps:**
1. Create `/components/features/NewInspectionDialog.tsx`
2. Implement form:
   ```typescript
   export function NewInspectionDialog({ open, onOpenChange, onSuccess }) {
     const form = useForm<InspectionFormData>({
       defaultValues: {
         name: '',
         site_location: '',
         site_address: ''
       }
     });
     
     const onSubmit = async (data: InspectionFormData) => {
       const inspection = await api.createInspection(data);
       onSuccess(inspection.id);
     };
     
     return (
       <Dialog open={open} onOpenChange={onOpenChange}>
         <DialogContent>
           <DialogHeader>
             <DialogTitle>New Inspection</DialogTitle>
           </DialogHeader>
           <form onSubmit={form.handleSubmit(onSubmit)}>
             <div className="space-y-4">
               <div>
                 <Label>Inspection Name</Label>
                 <Input {...form.register('name')} placeholder="Building 3 Safety Audit" />
               </div>
               <div>
                 <Label>Site Location</Label>
                 <Input {...form.register('site_location')} placeholder="Main Campus" />
               </div>
               <div>
                 <Label>Address</Label>
                 <Input {...form.register('site_address')} />
               </div>
             </div>
             <DialogFooter className="mt-6">
               <Button type="submit">Create Inspection</Button>
             </DialogFooter>
           </form>
         </DialogContent>
       </Dialog>
     );
   }
   ```
3. Add validation
4. Auto-navigate to upload page on creation
5. Add template selection (optional)

**Acceptance Criteria:**
- [ ] Modal opens/closes correctly
- [ ] Form validation works
- [ ] Creates inspection via API
- [ ] Navigates to upload page
- [ ] Error handling

**Dependencies:** Task 7.1.1

---

#### Task 7.2.2: Create Upload Page
**Description**: Dedicated page for file uploads

**Steps:**
1. Create `/app/inspection/[id]/upload/page.tsx`
2. Implement upload interface:
   ```typescript
   export default function UploadPage({ params }) {
     const inspectionId = params.id;
     
     return (
       <div className="container mx-auto py-8">
         <div className="mb-8">
           <h1 className="text-2xl font-bold">Upload Files</h1>
           <p className="text-muted-foreground">
             Add photos, audio recordings, and documents
           </p>
         </div>
         
         <div className="grid md:grid-cols-2 gap-6">
           <Card>
             <CardHeader>
               <CardTitle>Upload Files</CardTitle>
             </CardHeader>
             <CardContent>
               <FileUpload inspectionId={inspectionId} />
             </CardContent>
           </Card>
           
           <Card>
             <CardHeader>
               <CardTitle>Processing Status</CardTitle>
             </CardHeader>
             <CardContent>
               <FileStatusList inspectionId={inspectionId} />
             </CardContent>
           </Card>
         </div>
         
         <div className="mt-6 flex justify-end">
           <Button onClick={() => router.push(`/inspection/${inspectionId}`)}>
             View Report
           </Button>
         </div>
       </div>
     );
   }
   ```
3. Add progress tracking
4. Show real-time status updates
5. Add "Upload Complete" notification

**Acceptance Criteria:**
- [ ] Upload interface works
- [ ] Status updates in real-time
- [ ] Can navigate to report
- [ ] Progress clearly visible

**Dependencies:** Task 3.2.1, Task 3.2.3

---

### 7.3 Inspection Report Page

#### Task 7.3.1: Create Report Page Layout
**Description**: Main inspection report view

**Steps:**
1. Create `/app/inspection/[id]/page.tsx`
2. Implement layout:
   ```typescript
   export default async function InspectionPage({ params }) {
     const inspection = await api.getInspection(params.id);
     const findings = await api.getInspectionFindings(params.id);
     
     return (
       <div className="container mx-auto py-8">
         <ReportHeader inspection={inspection} />
         
         <Tabs defaultValue="report">
           <TabsList>
             <TabsTrigger value="report">Report</TabsTrigger>
             <TabsTrigger value="findings">Findings</TabsTrigger>
             <TabsTrigger value="files">Files</TabsTrigger>
             <TabsTrigger value="activity">Activity</TabsTrigger>
           </TabsList>
           
           <TabsContent value="report">
             <ReportSummary inspection={inspection} findings={findings} />
           </TabsContent>
           
           <TabsContent value="findings">
             <FindingsGrid findings={findings} />
           </TabsContent>
           
           <TabsContent value="files">
             <FilesView inspectionId={params.id} />
           </TabsContent>
           
           <TabsContent value="activity">
             <ActivityLog inspectionId={params.id} />
           </TabsContent>
         </Tabs>
       </div>
     );
   }
   ```
3. Add export button
4. Add share functionality
5. Add edit inspection details

**Acceptance Criteria:**
- [ ] Layout renders correctly
- [ ] Tabs work properly
- [ ] Data loads correctly
- [ ] Navigation functional

**Dependencies:** Task 7.2.2

---

#### Task 7.3.2: Create Report Header Component
**Description**: Display inspection overview

**Steps:**
1. Create `/components/features/ReportHeader.tsx`
2. Implement header:
   ```typescript
   export function ReportHeader({ inspection }) {
     return (
       <div className="mb-8">
         <div className="flex items-start justify-between">
           <div>
             <h1 className="text-3xl font-bold">{inspection.name}</h1>
             <p className="text-muted-foreground">{inspection.site_location}</p>
             <p className="text-sm text-muted-foreground">
               {format(inspection.created_at, 'PPP')}
             </p>
           </div>
           
           <div className="flex items-center gap-2">
             <Badge variant={getRiskVariant(inspection.risk_level)} className="text-lg">
               {inspection.risk_level?.toUpperCase() || 'PENDING'}
             </Badge>
             
             <DropdownMenu>
               <DropdownMenuTrigger asChild>
                 <Button variant="outline">Actions</Button>
               </DropdownMenuTrigger>
               <DropdownMenuContent>
                 <DropdownMenuItem onClick={exportPDF}>
                   Export PDF
                 </DropdownMenuItem>
                 <DropdownMenuItem onClick={share}>
                   Share Report
                 </DropdownMenuItem>
                 <DropdownMenuItem onClick={edit}>
                   Edit Details
                 </DropdownMenuItem>
               </DropdownMenuContent>
             </DropdownMenu>
           </div>
         </div>
         
         <div className="mt-4 grid grid-cols-4 gap-4">
           <MetricCard label="Total Findings" value={inspection.total_findings} />
           <MetricCard label="Files Processed" value={inspection.total_files} />
           <MetricCard label="Processing Time" value={formatDuration(inspection.processing_time)} />
           <MetricCard label="ML Cost" value={`$${inspection.ml_cost?.toFixed(3)}`} />
         </div>
       </div>
     );
   }
   ```
3. Add inspector info
4. Add status badge
5. Add action buttons

**Acceptance Criteria:**
- [ ] Header displays all info
- [ ] Risk badge colored correctly
- [ ] Metrics accurate
- [ ] Actions work

**Dependencies:** Task 7.3.1

---

#### Task 7.3.3: Create Report Summary Component
**Description**: Display AI-generated narrative

**Steps:**
1. Create `/components/features/ReportSummary.tsx`
2. Implement summary:
   ```typescript
   export function ReportSummary({ inspection, findings }) {
     return (
       <div className="space-y-6">
         <Card>
           <CardHeader>
             <CardTitle>Executive Summary</CardTitle>
           </CardHeader>
           <CardContent>
             <div className="prose max-w-none">
               {inspection.report_narrative?.split('\n').map((para, i) => (
                 <p key={i}>{para}</p>
               ))}
             </div>
           </CardContent>
         </Card>
         
         <Card>
           <CardHeader>
             <CardTitle>Critical Findings</CardTitle>
           </CardHeader>
           <CardContent>
             <div className="space-y-4">
               {findings
                 .filter(f => f.severity === 'critical')
                 .map(finding => (
                   <FindingCard key={finding.id} finding={finding} />
                 ))}
             </div>
           </CardContent>
         </Card>
         
         <Card>
           <CardHeader>
             <CardTitle>Recommendations</CardTitle>
           </CardHeader>
           <CardContent>
             <ul className="list-disc pl-6 space-y-2">
               {getRecommendations(findings).map((rec, i) => (
                 <li key={i}>{rec}</li>
               ))}
             </ul>
           </CardContent>
         </Card>
       </div>
     );
   }
   ```
3. Add loading skeleton
4. Regenerate summary option
5. Edit summary capability

**Acceptance Criteria:**
- [ ] Summary displays correctly
- [ ] Critical findings highlighted
- [ ] Recommendations shown
- [ ] Can regenerate

**Dependencies:** Task 7.3.1

---

#### Task 7.3.4: Create Findings Grid Component
**Description**: Display all findings with filters

**Steps:**
1. Create `/components/features/FindingsGrid.tsx`
2. Implement grid:
   ```typescript
   export function FindingsGrid({ findings }) {
     const [filters, setFilters] = useState({
       category: 'all',
       severity: 'all',
       needsReview: false
     });
     
     const filteredFindings = findings.filter(f => {
       if (filters.category !== 'all' && f.category !== filters.category) return false;
       if (filters.severity !== 'all' && f.severity !== filters.severity) return false;
       if (filters.needsReview && !f.needs_review) return false;
       return true;
     });
     
     return (
       <div className="space-y-4">
         <div className="flex gap-4">
           <Select value={filters.category} onValueChange={v => setFilters({...filters, category: v})}>
             <SelectTrigger className="w-48">
               <SelectValue placeholder="Category" />
             </SelectTrigger>
             <SelectContent>
               <SelectItem value="all">All Categories</SelectItem>
               <SelectItem value="structural damage">Structural</SelectItem>
               <SelectItem value="electrical hazard">Electrical</SelectItem>
               <SelectItem value="water damage">Water</SelectItem>
               <SelectItem value="fire risk">Fire</SelectItem>
             </SelectContent>
           </Select>
           
           <Select value={filters.severity} onValueChange={v => setFilters({...filters, severity: v})}>
             <SelectTrigger className="w-48">
               <SelectValue placeholder="Severity" />
             </SelectTrigger>
             <SelectContent>
               <SelectItem value="all">All Severities</SelectItem>
               <SelectItem value="critical">Critical</SelectItem>
               <SelectItem value="high">High</SelectItem>
               <SelectItem value="medium">Medium</SelectItem>
               <SelectItem value="low">Low</SelectItem>
             </SelectContent>
           </Select>
           
           <label className="flex items-center gap-2">
             <input
               type="checkbox"
               checked={filters.needsReview}
               onChange={e => setFilters({...filters, needsReview: e.target.checked})}
             />
             Needs Review Only
           </label>
         </div>
         
         <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
           {filteredFindings.map(finding => (
             <FindingCard key={finding.id} finding={finding} />
           ))}
         </div>
       </div>
     );
   }
   ```
3. Add sorting options
4. Add search functionality
5. Add "Export Findings" button

**Acceptance Criteria:**
- [ ] Grid displays all findings
- [ ] Filters work correctly
- [ ] Sorting functional
- [ ] Search works
- [ ] Can export

**Dependencies:** Task 7.3.1

---

#### Task 7.3.5: Create Finding Card Component
**Description**: Individual finding display

**Steps:**
1. Create `/components/features/FindingCard.tsx`
2. Implement card:
   ```typescript
   export function FindingCard({ finding }) {
     return (
       <Card className={finding.needs_review ? 'border-yellow-500' : ''}>
         <CardContent className="p-4">
           {finding.file?.file_type === 'image' && (
             <div className="relative aspect-video mb-3">
               <Image
                 src={finding.file.storage_url}
                 alt={finding.ai_caption}
                 fill
                 className="object-cover rounded"
               />
             </div>
           )}
           
           <div className="space-y-2">
             <div className="flex items-start justify-between">
               <Badge variant={getSeverityVariant(finding.severity)}>
                 {finding.category}
               </Badge>
               {finding.needs_review && (
                 <Badge variant="outline" className="bg-yellow-50">
                   Review Needed
                 </Badge>
               )}
             </div>
             
             <p className="text-sm">{finding.ai_caption || finding.transcription}</p>
             
             {finding.confidence_score && (
               <div className="flex items-center gap-2 text-xs text-muted-foreground">
                 <span>Confidence:</span>
                 <div className="flex-1">
                   <div className="h-1.5 bg-gray-200 rounded-full overflow-hidden">
                     <div
                       className="h-full bg-blue-500"
                       style={{ width: `${finding.confidence_score * 100}%` }}
                     />
                   </div>
                 </div>
                 <span>{(finding.confidence_score * 100).toFixed(1)}%</span>
               </div>
             )}
             
             {finding.location_code && (
               <p className="text-xs text-muted-foreground">
                 Location: {finding.location_code}
               </p>
             )}
             
             {finding.needs_review && (
               <Button
                 size="sm"
                 className="w-full"
                 onClick={() => openReviewDialog(finding)}
               >
                 Review Finding
               </Button>
             )}
           </div>
         </CardContent>
       </Card>
     );
   }
   ```
3. Add click to expand modal
4. Show all metadata
5. Add edit capability

**Acceptance Criteria:**
- [ ] Card displays finding info
- [ ] Image preview works
- [ ] Confidence bar accurate
- [ ] Review button functional
- [ ] Expandable modal works

**Dependencies:** Task 7.3.4

---

#### Task 7.3.6: Create Review Dialog Component
**Description**: Modal for correcting AI classifications

**Steps:**
1. Create `/components/features/ReviewDialog.tsx`
2. Implement review form:
   ```typescript
   export function ReviewDialog({ finding, open, onOpenChange, onSubmit }) {
     const [category, setCategory] = useState(finding.category);
     const [severity, setSeverity] = useState(finding.severity);
     const [notes, setNotes] = useState('');
     
     const handleSubmit = async () => {
       await api.reviewFinding(finding.id, {
         corrected_category: category,
         corrected_severity: severity,
         notes
       });
       onSubmit();
     };
     
     return (
       <Dialog open={open} onOpenChange={onOpenChange}>
         <DialogContent className="max-w-2xl">
           <DialogHeader>
             <DialogTitle>Review Finding</DialogTitle>
           </DialogHeader>
           
           <div className="space-y-4">
             {finding.file?.file_type === 'image' && (
               <div className="relative aspect-video">
                 <Image src={finding.file.storage_url} alt="" fill />
               </div>
             )}
             
             <div>
               <Label>AI Caption</Label>
               <p className="text-sm text-muted-foreground">{finding.ai_caption}</p>
             </div>
             
             <div>
               <Label>AI Suggestion (Confidence: {(finding.confidence_score * 100).toFixed(1)}%)</Label>
               <Badge>{finding.category}</Badge>
             </div>
             
             <div>
               <Label>Correct Category</Label>
               <Select value={category} onValueChange={setCategory}>
                 <SelectTrigger>
                   <SelectValue />
                 </SelectTrigger>
                 <SelectContent>
                   <SelectItem value="structural damage">Structural Damage</SelectItem>
                   <SelectItem value="electrical hazard">Electrical Hazard</SelectItem>
                   <SelectItem value="water damage">Water Damage</SelectItem>
                   <SelectItem value="fire risk">Fire Risk</SelectItem>
                   <SelectItem value="equipment issue">Equipment Issue</SelectItem>
                   <SelectItem value="fall hazard">Fall Hazard</SelectItem>
                   <SelectItem value="clear">Clear/No Defect</SelectItem>
                 </SelectContent>
               </Select>
             </div>
             
             <div>
               <Label>Severity</Label>
               <Select value={severity} onValueChange={setSeverity}>
                 <SelectTrigger>
                   <SelectValue />
                 </SelectTrigger>
                 <SelectContent>
                   <SelectItem value="critical">Critical</SelectItem>
                   <SelectItem value="high">High</SelectItem>
                   <SelectItem value="medium">Medium</SelectItem>
                   <SelectItem value="low">Low</SelectItem>
                 </SelectContent>
               </Select>
             </div>
             
             <div>
               <Label>Notes (Optional)</Label>
               <Textarea
                 value={notes}
                 onChange={e => setNotes(e.target.value)}
                 placeholder="Additional context or reasoning..."
               />
             </div>
           </div>
           
           <DialogFooter>
             <Button variant="outline" onClick={() => onOpenChange(false)}>
               Cancel
             </Button>
             <Button onClick={handleSubmit}>
               Submit Review
             </Button>
           </DialogFooter>
         </DialogContent>
       </Dialog>
     );
   }
   ```
3. Add keyboard shortcuts
4. Show alternative predictions
5. Track review time

**Acceptance Criteria:**
- [ ] Dialog displays finding
- [ ] Can correct category/severity
- [ ] Notes field works
- [ ] Submits review correctly
- [ ] Updates finding status

**Dependencies:** Task 7.3.5

---

#### Task 7.3.7: Create PDF Export
**Description**: Generate downloadable PDF reports

**Steps:**
1. Create `/lib/pdf-export.ts`
2. Implement PDF generation using react-pdf:
   ```typescript
   import { Document, Page, Text, View, Image, StyleSheet } from '@react-pdf/renderer';
   
   const styles = StyleSheet.create({
     page: { padding: 30 },
     header: { fontSize: 24, marginBottom: 20 },
     section: { marginBottom: 10 },
     // ... more styles
   });
   
   export const InspectionReport = ({ inspection, findings }) => (
     <Document>
       <Page size="A4" style={styles.page}>
         <Text style={styles.header}>{inspection.name}</Text>
         
         <View style={styles.section}>
           <Text>Site: {inspection.site_location}</Text>
           <Text>Date: {format(inspection.created_at, 'PPP')}</Text>
           <Text>Risk Level: {inspection.risk_level}</Text>
         </View>
         
         <View style={styles.section}>
           <Text style={styles.subtitle}>Executive Summary</Text>
           <Text>{inspection.report_narrative}</Text>
         </View>
         
         <View style={styles.section}>
           <Text style={styles.subtitle}>Findings ({findings.length})</Text>
           {findings.map(f => (
             <View key={f.id} style={styles.finding}>
               {f.file?.storage_url && (
                 <Image src={f.file.storage_url} style={styles.image} />
               )}
               <Text>Category: {f.category}</Text>
               <Text>Severity: {f.severity}</Text>
               <Text>{f.ai_caption}</Text>
             </View>
           ))}
         </View>
       </Page>
     </Document>
   );
   ```
3. Add export endpoint
4. Include charts in PDF
5. Add company branding options

**Acceptance Criteria:**
- [ ] PDF generates successfully
- [ ] Includes all sections
- [ ] Images embedded
- [ ] Professional formatting
- [ ] Downloads correctly

**Dependencies:** Task 7.3.3

---

### 7.4 Semantic Search Feature

#### Task 7.4.1: Create Search Bar Component
**Description**: Search interface for historical findings

**Steps:**
1. Create `/components/features/SearchBar.tsx`
2. Implement search:
   ```typescript
   export function SearchBar() {
     const [query, setQuery] = useState('');
     const [results, setResults] = useState([]);
     const [loading, setLoading] = useState(false);
     
     const handleSearch = async () => {
       setLoading(true);
       const results = await api.searchFindings(query);
       setResults(results);
       setLoading(false);
     };
     
     return (
       <div className="w-full">
         <div className="flex gap-2">
           <Input
             placeholder="Search past inspections... e.g., 'concrete spalling on columns'"
             value={query}
             onChange={e => setQuery(e.target.value)}
             onKeyDown={e => e.key === 'Enter' && handleSearch()}
             className="flex-1"
           />
           <Button onClick={handleSearch} disabled={loading}>
             {loading ? <Loader2 className="animate-spin" /> : <Search />}
             Search
           </Button>
         </div>
         
         {results.length > 0 && (
           <Card className="mt-4">
             <CardHeader>
               <CardTitle>Similar Findings ({results.length})</CardTitle>
             </CardHeader>
             <CardContent>
               <div className="space-y-4">
                 {results.map(result => (
                   <SearchResult key={result.id} result={result} />
                 ))}
               </div>
             </CardContent>
           </Card>
         )}
       </div>
     );
   }
   ```
3. Add recent searches
4. Add search suggestions
5. Add filters (date range, severity)

**Acceptance Criteria:**
- [ ] Search bar works
- [ ] Results display correctly
- [ ] Loading state shown
- [ ] Enter key triggers search
- [ ] Recent searches saved

**Dependencies:** Task 7.1.1

---

#### Task 7.4.2: Create Search Result Component
**Description**: Display individual search results

**Steps:**
1. Create `/components/features/SearchResult.tsx`
2. Implement result card:
   ```typescript
   export function SearchResult({ result }) {
     return (
       <div className="flex gap-4 p-4 border rounded hover:bg-accent cursor-pointer">
         {result.file?.file_type === 'image' && (
           <div className="relative w-32 h-24 flex-shrink-0">
             <Image
               src={result.file.storage_url}
               alt=""
               fill
               className="object-cover rounded"
             />
           </div>
         )}
         
         <div className="flex-1 space-y-2">
           <div className="flex items-center gap-2">
             <Badge variant={getSeverityVariant(result.severity)}>
               {result.category}
             </Badge>
             <span className="text-sm text-muted-foreground">
               Similarity: {(result.similarity_score * 100).toFixed(1)}%
             </span>
           </div>
           
           <p className="text-sm">{result.ai_caption || result.description}</p>
           
           <div className="flex items-center gap-4 text-xs text-muted-foreground">
             <span>
               From: <Link href={`/inspection/${result.inspection_id}`} className="underline">
                 {result.inspection.name}
               </Link>
             </span>
             <span>{format(result.created_at, 'PP')}</span>
             {result.location_code && <span>Location: {result.location_code}</span>}
           </div>
           
           {result.human_review && (
             <p className="text-xs">
               <strong>Resolution:</strong> {result.human_review.notes}
             </p>
           )}
         </div>
       </div>
     );
   }
   ```
3. Add click to view full inspection
4. Show similarity score
5. Highlight relevant text

**Acceptance Criteria:**
- [ ] Results display all info
- [ ] Similarity score shown
- [ ] Links to inspection work
- [ ] Resolution notes visible
- [ ] Images show if available

**Dependencies:** Task 7.4.1

---

#### Task 7.4.3: Create Search API Endpoint
**Description**: Backend semantic search implementation

**Steps:**
1. Create `/backend/app/api/routes/search.py`
2. Implement search endpoint:
   ```python
   @router.post("/search/findings")
   async def search_findings(
       request: SearchRequest,
       current_user: User = Depends(get_current_user),
       db: Session = Depends(get_db)
   ):
       # 1. Generate embedding for query
       query_embedding = await embedding_service.generate_embedding(request.query)
       
       # 2. Perform vector similarity search
       results = db.execute("""
           SELECT 
               f.*,
               i.name as inspection_name,
               fi.storage_url,
               (f.embedding <=> %s::vector) as similarity_score
           FROM findings f
           JOIN inspections i ON f.inspection_id = i.id
           LEFT JOIN files fi ON f.file_id = fi.id
           WHERE i.org_id = %s
           ORDER BY f.embedding <=> %s::vector
           LIMIT %s
       """, (query_embedding, current_user.org_id, query_embedding, request.limit or 10))
       
       # 3. Format results
       findings = []
       for row in results:
           findings.append({
               "id": row.id,
               "ai_caption": row.ai_caption,
               "category": row.category,
               "severity": row.severity,
               "similarity_score": 1 - row.similarity_score,  # Convert distance to similarity
               "inspection": {"id": row.inspection_id, "name": row.inspection_name},
               "file": {"storage_url": row.storage_url} if row.storage_url else None,
               "created_at": row.created_at
           })
       
       return {"results": findings, "query": request.query}
   ```
3. Add caching for common queries
4. Add filters (date, severity, category)
5. Log search queries for analytics

**Acceptance Criteria:**
- [ ] Semantic search works
- [ ] Returns relevant results
- [ ] Similarity scores accurate
- [ ] Scoped to organization
- [ ] Performance acceptable (<500ms)

**Dependencies:** Task 5.1.9, Task 2.1.5

---

## PHASE 8: DEPLOYMENT & PRODUCTION

### 8.1 Frontend Deployment

#### Task 8.1.1: Configure Vercel Deployment
**Description**: Deploy Next.js app to Vercel

**Steps:**
1. Connect GitHub repo to Vercel
2. Configure build settings:
   - Framework: Next.js
   - Build command: `npm run build`
   - Output directory: `.next`
3. Add environment variables in Vercel dashboard
4. Configure custom domain (optional)
5. Set up preview deployments for branches
6. Configure deployment hooks
7. Test deployed app

**Acceptance Criteria:**
- [ ] App deployed to Vercel
- [ ] Environment variables set
- [ ] Build successful
- [ ] App accessible via URL
- [ ] Preview deployments work

**Dependencies:** All frontend tasks complete

---

#### Task 8.1.2: Set Up Error Tracking
**Description**: Implement error monitoring

**Steps:**
1. Sign up for Sentry
2. Install Sentry SDK:
   ```bash
   npm install @sentry/nextjs
   ```
3. Configure Sentry:
   ```typescript
   // sentry.client.config.ts
   import * as Sentry from "@sentry/nextjs";
   
   Sentry.init({
     dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
     tracesSampleRate: 1.0,
   });
   ```
4. Add error boundary components
5. Test error reporting

**Acceptance Criteria:**
- [ ] Sentry configured
- [ ] Errors tracked
- [ ] Source maps uploaded
- [ ] Notifications working

**Dependencies:** Task 8.1.1

---

### 8.2 Backend Deployment

#### Task 8.2.1: Deploy Worker to Railway
**Description**: Deploy FastAPI worker process

**Steps:**
1. Create Railway account
2. Create new project from GitHub repo
3. Configure build:
   - Root directory: `/backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `python -m app.workers.file_processor`
4. Add environment variables
5. Configure health checks
6. Set up auto-deploy on push
7. Monitor logs

**Acceptance Criteria:**
- [ ] Worker deployed to Railway
- [ ] Environment variables set
- [ ] Worker runs continuously
- [ ] Processes jobs successfully
- [ ] Logs accessible

**Dependencies:** All backend tasks complete

---

#### Task 8.2.2: Set Up API Service (Optional)
**Description**: Deploy FastAPI REST API separately

**Steps:**
1. Create separate Railway service for API
2. Configure build for API:
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Add environment variables
4. Configure custom domain
5. Set up HTTPS
6. Test API endpoints

**Acceptance Criteria:**
- [ ] API deployed
- [ ] Endpoints accessible
- [ ] HTTPS enabled
- [ ] CORS configured
- [ ] Rate limiting works

**Dependencies:** Task 8.2.1

---

### 8.3 Database & Storage

#### Task 8.3.1: Configure Production Database
**Description**: Set up production Supabase instance

**Steps:**
1. Create production Supabase project
2. Run all migrations
3. Enable pgvector
4. Set up RLS policies
5. Configure backups (automatic in Supabase)
6. Set up connection pooling
7. Test connections from deployed services

**Acceptance Criteria:**
- [ ] Production DB created
- [ ] Schema matches development
- [ ] RLS policies active
- [ ] Backups configured
- [ ] Connection pool optimized

**Dependencies:** Task 2.1.1-2.1.8

---

#### Task 8.3.2: Configure Production File Storage
**Description**: Set up production file storage

**Steps:**
1. Create Supabase Storage bucket for production
2. Configure CORS:
   ```json
   [
     {
       "AllowedOrigins": ["https://yourdomain.com"],
       "AllowedMethods": ["GET", "PUT", "POST"],
       "AllowedHeaders": ["*"]
     }
   ]
   ```
3. Update `storage_service.py` backend logic to use Supabase Storage instead of local files for production environments
4. Test upload/download from production

**Acceptance Criteria:**
- [ ] Production bucket created
- [ ] CORS configured
- [ ] Files accessible
- [ ] Upload/download works

**Dependencies:** Task 8.3.1

---

### 8.4 Monitoring & Analytics

#### Task 8.4.1: Set Up Application Monitoring
**Description**: Monitor app performance and usage

**Steps:**
1. Configure Vercel Analytics
2. Add custom events:
   - Inspection created
   - Files uploaded
   - Report generated
   - Search performed
3. Set up uptime monitoring (UptimeRobot)
4. Configure alerts for:
   - High error rates
   - Slow response times
   - Queue backlog
5. Create monitoring dashboard

**Acceptance Criteria:**
- [ ] Analytics tracking events
- [ ] Uptime monitoring active
- [ ] Alerts configured
- [ ] Dashboard accessible

**Dependencies:** Task 8.1.1, 8.2.1

---

#### Task 8.4.2: Implement Usage Analytics
**Description**: Track feature usage and costs

**Steps:**
1. Create analytics dashboard queries:
   - Daily active users
   - Inspections per day
   - Files processed per day
   - ML costs per day
   - Search queries per day
2. Build analytics page in app
3. Add export functionality
4. Set up automated reports (optional)

**Acceptance Criteria:**
- [ ] Analytics queries work
- [ ] Dashboard displays metrics
- [ ] Can export data
- [ ] Historical trends visible

**Dependencies:** Task 7.1.1

---

## PHASE 9: SEED DATA & DEMO

### 9.1 Demo Data Creation

#### Task 9.1.1: Create Seed Script
**Description**: Script to populate demo data

**Steps:**
1. Create `/backend/scripts/seed_demo_data.py`
2. Implement seeding:
   ```python
   async def seed_demo_data():
       # 1. Create 2 demo organizations
       org1 = await create_organization("Acme Construction")
       org2 = await create_organization("BuildRight Industries")
       
       # 2. Create demo users for each org
       await create_demo_users(org1.id)
       await create_demo_users(org2.id)
       
       # 3. Create inspections with processed findings
       for org in [org1, org2]:
           for i in range(4):
               inspection = await create_inspection(org.id, DEMO_INSPECTION_DATA[i])
               await create_demo_findings(inspection.id)
       
       # 4. Generate embeddings for all findings
       await generate_all_embeddings()
       
       print("Demo data seeded successfully!")
   ```
3. Create demo inspection templates
4. Add realistic finding descriptions
5. Include sample images/audio/PDFs

**Acceptance Criteria:**
- [ ] Script creates 2 orgs
- [ ] 8 complete inspections
- [ ] 50+ findings with embeddings
- [ ] Realistic data
- [ ] Runs without errors

**Dependencies:** All database and ML tasks

---

#### Task 9.1.2: Gather Sample Files
**Description**: Collect realistic sample files

**Steps:**
1. Download construction/industrial images from:
   - Unsplash
   - Pexels
   - OpenImages dataset
2. Create demo categories:
   - 10 images of structural damage
   - 8 images of electrical hazards
   - 6 images of water damage
   - 5 images of fire risks
   - 15 images of clear/safe conditions
3. Record 5 voice memos with inspection notes
4. Download sample OSHA/building code PDFs
5. Organize in `/backend/demo_files/`

**Acceptance Criteria:**
- [ ] 40+ sample images collected
- [ ] 5 audio files recorded
- [ ] 3 PDF documents
- [ ] Properly categorized
- [ ] Realistic content

**Dependencies:** None

---

#### Task 9.1.3: Pre-process Demo Files
**Description**: Process demo files and store results

**Steps:**
1. Upload demo files to local storage (`demo_files/`)
2. Run through ML pipeline
3. Generate embeddings
4. Store all findings in database
5. Generate inspection summaries
6. Create human reviews for some findings
7. Verify vector search works with demo data

**Acceptance Criteria:**
- [ ] All files processed
- [ ] Findings stored
- [ ] Embeddings generated
- [ ] Summaries created
- [ ] Search returns results

**Dependencies:** Task 9.1.2, All ML tasks

---

### 9.2 Demo Video & Documentation

#### Task 9.2.1: Record Demo Video
**Description**: Create walkthrough video

**Steps:**
1. Script demo flow:
   - Sign in
   - Dashboard overview
   - Create new inspection
   - Upload files
   - Watch processing
   - View report
   - Review flagged finding
   - Search similar findings
   - Export PDF
2. Record screen with Loom/OBS
3. Add voiceover explaining features
4. Edit for clarity (< 90 seconds)
5. Upload to YouTube/Vimeo
6. Add to portfolio

**Acceptance Criteria:**
- [ ] Video under 90 seconds
- [ ] Shows all key features
- [ ] Clear audio
- [ ] Professional quality
- [ ] Uploaded and accessible

**Dependencies:** Task 9.1.3, All UI complete

---

#### Task 9.2.2: Write README Documentation
**Description**: Comprehensive project README

**Steps:**
1. Create detailed README.md:
   - Project overview
   - Features list
   - Tech stack
   - Architecture diagram
   - Setup instructions
   - Deployment guide
   - API documentation
   - Screenshots
   - Demo video embed
   - License
2. Add architecture diagram (draw.io)
3. Include screenshots of each page
4. Document environment variables
5. Add troubleshooting section

**Acceptance Criteria:**
- [ ] README complete
- [ ] Architecture diagram included
- [ ] Screenshots added
- [ ] Setup instructions clear
- [ ] Professional presentation

**Dependencies:** All tasks complete

---

## PHASE 10: TESTING & POLISH

### 10.1 Testing

#### Task 10.1.1: Write Unit Tests
**Description**: Test core functionality

**Steps:**
1. Backend tests (`/backend/tests/`):
   - Test ML processing functions
   - Test database operations
   - Test API endpoints
   - Test authentication
2. Frontend tests:
   - Test components render
   - Test form submissions
   - Test API integration
3. Run tests in CI/CD
4. Aim for 70%+ coverage

**Acceptance Criteria:**
- [ ] 70%+ test coverage
- [ ] All tests pass
- [ ] CI/CD runs tests
- [ ] Critical paths covered

**Dependencies:** All feature tasks

---

#### Task 10.1.2: End-to-End Testing
**Description**: Test complete user flows

**Steps:**
1. Set up Playwright
2. Write E2E tests:
   - Sign up flow
   - Create inspection
   - Upload files
   - View report
   - Review finding
   - Search similar
   - Export PDF
3. Run in CI/CD
4. Test on multiple browsers

**Acceptance Criteria:**
- [ ] E2E tests written
- [ ] All flows pass
- [ ] Multi-browser tested
- [ ] Runs in CI

**Dependencies:** Task 10.1.1

---

### 10.2 Performance Optimization

#### Task 10.2.1: Optimize Load Times
**Description**: Improve app performance

**Steps:**
1. Analyze with Lighthouse
2. Optimize images (Next.js Image)
3. Implement lazy loading
4. Add loading skeletons
5. Optimize database queries
6. Minimize bundle size
7. Test improvements

**Acceptance Criteria:**
- [ ] Lighthouse score >90
- [ ] First paint <1.5s
- [ ] Interactive <3s
- [ ] Bundle size optimized

**Dependencies:** All features complete

---

### 10.3 Final Polish

#### Task 10.3.1: UI/UX Refinement
**Description**: Polish user interface

**Steps:**
1. Consistent spacing/padding
2. Smooth transitions
3. Loading states everywhere
4. Error states styled
5. Empty states designed
6. Tooltips added
7. Keyboard shortcuts
8. Mobile responsive check

**Acceptance Criteria:**
- [ ] UI consistent
- [ ] Animations smooth
- [ ] Mobile works well
- [ ] Accessibility improved

**Dependencies:** All UI tasks

---

#### Task 10.3.2: Add Onboarding
**Description**: Help new users get started

**Steps:**
1. Create welcome screen
2. Add product tour (intro.js)
3. Create sample inspection button
4. Add helpful tooltips
5. Link to documentation
6. Add video tutorial

**Acceptance Criteria:**
- [ ] Onboarding flow works
- [ ] Product tour helpful
- [ ] Sample inspection created
- [ ] Users can get started easily

**Dependencies:** All features complete

---

## Task Summary by Phase

### Phase 1 (Setup): ~6-8 hours
- Project scaffolding
- Third-party services
- Environment configuration

### Phase 2 (Database): ~4-6 hours
- Schema creation
- Models and repositories
- RLS policies

### Phase 3 (File Upload): ~4-5 hours
- Backend upload API
- Frontend upload UI
- Status tracking

### Phase 4 (Async Processing): ~3-4 hours
- BackgroundTasks setup
- Worker process routing
- Status tracking

### Phase 5 (ML Pipeline): ~12-15 hours
- HF integration
- All ML models
- Pipeline orchestration

### Phase 6 (Auth): ~3-4 hours
- Supabase Auth integration
- Authorization middleware
- Multi-tenancy access control

### Phase 7 (Frontend): ~15-20 hours
- Dashboard
- Report pages
- Search feature
- All UI components

### Phase 8 (Deployment): ~4-6 hours
- Production deployment
- Monitoring setup
- DNS configuration

### Phase 9 (Demo): ~4-5 hours
- Seed data
- Sample files
- Demo video

### Phase 10 (Testing): ~6-8 hours
- Unit tests
- E2E tests
- Performance optimization
- Final polish

**Total Estimated Time: 60-80 hours** (across 2-3 weekends with focused work)

---

## Priority for Weekend Build

For a weekend build, focus on these tasks in order:

**Friday Night (Critical Setup):**
- Tasks 1.1.1 - 1.1.4
- Tasks 1.2.1 - 1.2.5

**Saturday Morning (Core Backend):**
- Tasks 2.1.1 - 2.1.7
- Tasks 3.1.1 - 3.1.2
- Tasks 4.1.1 - 4.1.2

**Saturday Afternoon (ML Pipeline):**
- Tasks 5.1.1 - 5.1.3
- Tasks 5.1.4 - 5.1.5
- Tasks 5.2.1 - 5.2.2

**Saturday Evening (Basic Frontend):**
- Task 6.1.1
- Tasks 7.1.1 - 7.1.2
- Tasks 7.2.1 - 7.2.2

**Sunday Morning (Report & Search):**
- Tasks 7.3.1 - 7.3.5
- Tasks 7.4.1 - 7.4.3
- Task 5.1.9

**Sunday Afternoon (Deploy & Demo):**
- Tasks 8.1.1
- Tasks 8.2.1
- Tasks 9.1.1 - 9.1.3
- Task 9.2.1

**Nice-to-haves (if time):**
- Task 7.3.6 (Review dialog)
- Task 7.3.7 (PDF export)
- Task 7.1.6 (Cost tracker)
- Task 5.2.5 (Cost tracking backend)
