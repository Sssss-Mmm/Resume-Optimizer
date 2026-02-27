from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.database import get_db
from app.db.models import Resume, JobDescription, User
from app.schemas.resume import ResumeCreate, ResumeGenerateRequest, ResumeResponse
from app.services.llm_service import generate_initial_resume

router = APIRouter()

@router.post("/generate", response_model=ResumeResponse)
async def generate_resume_draft(req: ResumeGenerateRequest, db: AsyncSession = Depends(get_db)):
    # 1. Validate JD exists
    jd_result = await db.execute(select(JobDescription).filter(JobDescription.id == req.job_description_id))
    jd = jd_result.scalars().first()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
        
    # 2. Extract keywords from JD
    keywords = jd.extracted_keywords or []
    
    # 3. Generate initial upgraded draft using LLM
    upgraded_content = await generate_initial_resume(req.original_resume_text, keywords)
    
    # 4. Save the generated resume to DB
    db_resume = Resume(
        user_id=req.user_id,
        content=upgraded_content,
        ats_score=0.0 # Will be updated in later weeks during score loop
    )
    db.add(db_resume)
    await db.commit()
    await db.refresh(db_resume)
    
    return db_resume

@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(resume_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Resume).filter(Resume.id == resume_id))
    db_obj = result.scalars().first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Resume not found")
    return db_obj
