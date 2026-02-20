import os
from uuid import UUID
import uuid
import hashlib
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.models.organization import Organization
security = HTTPBearer()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_ANON_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None

class UserContext(BaseModel):
    id: str
    email: str

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserContext:
    """
    Verify the JWT token from the Authorization header using Supabase.
    """
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Supabase client not configured",
        )

    try:
        # get_user automatically verifies the JWT
        response = supabase.auth.get_user(credentials.credentials)
        if not response or not response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = response.user
        return UserContext(
            id=user.id,
            email=user.email or "",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_org_id(user: UserContext = Depends(get_current_user), db: Session = Depends(get_db)) -> UUID:
    """
    Extract the organization ID from the authenticated user.
    For MVP without a separate orgs table, we generate a deterministic 
    UUID based on the user's ID to isolate their data.
    Ensures the organization exists in the DB to satisfy foreign key constraints.
    """
    hash_obj = hashlib.md5(user.id.encode())
    org_uuid = uuid.UUID(hash_obj.hexdigest())
    
    # Auto-upsert into organizations table
    slug = f"workspace-{hash_obj.hexdigest()[:8]}"
    db.execute(text("""
        INSERT INTO organizations (id, name, slug) 
        VALUES (:id, :name, :slug) 
        ON CONFLICT (id) DO NOTHING
    """), {"id": org_uuid, "name": "Personal Workspace", "slug": slug})
    db.commit()

    return org_uuid
