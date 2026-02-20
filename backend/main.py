from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import files, findings, inspections, organizations

app = FastAPI(title="AuditPilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows Vercel frontend to call the Render backend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files.router)
app.include_router(findings.router)
app.include_router(inspections.router)
app.include_router(organizations.router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}
