from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from app.config import settings

router = APIRouter(tags=["Health"])

class HealthResponse(BaseModel):
    status: str
    app: str
    environment: str
    database: str
    llm_provider: str

@router.get("/health", response_model=HealthResponse)
@router.get("/api/v1/health", response_model=HealthResponse)
async def check_health():
    db_status = "disconnected"
    try:
        engine = create_engine(settings.DATABASE_URL, connect_args={"connect_timeout": 2})
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return HealthResponse(
        status="ok",
        app=settings.PROJECT_NAME,
        environment=settings.ENVIRONMENT,
        database=db_status,
        llm_provider=settings.LLM_PROVIDER
    )
