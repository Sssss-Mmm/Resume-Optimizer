from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routers import job_descriptions, resumes

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(job_descriptions.router, prefix=f"{settings.API_V1_STR}/job-descriptions", tags=["Job Descriptions"])
app.include_router(resumes.router, prefix=f"{settings.API_V1_STR}/resumes", tags=["Resumes"])

@app.get("/health-check")
async def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}
