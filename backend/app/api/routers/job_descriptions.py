from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.db.models import JobDescription, User
from app.schemas.job_description import JobDescriptionCreate, JobDescriptionResponse
from app.services.llm_service import extract_keywords_from_jd
from sqlalchemy.future import select

router = APIRouter()

@router.post("/", response_model=JobDescriptionResponse)
async def create_job_description(jd_in: JobDescriptionCreate, db: AsyncSession = Depends(get_db)):
    # Verify user exists
    user_result = await db.execute(select(User).filter(User.id == jd_in.user_id))
    user = user_result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Analyze JD using LLM service
    keywords = await extract_keywords_from_jd(jd_in.raw_text)
    
    db_obj = JobDescription(
        user_id=jd_in.user_id,
        raw_text=jd_in.raw_text,
        extracted_keywords=keywords
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    
    return db_obj

@router.get("/{jd_id}", response_model=JobDescriptionResponse)
async def get_job_description(jd_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JobDescription).filter(JobDescription.id == jd_id))
    db_obj = result.scalars().first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Job description not found")
    return db_obj
