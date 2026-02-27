from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ResumeCreate(BaseModel):
    user_id: int
    content: str

class ResumeGenerateRequest(BaseModel):
    user_id: int
    job_description_id: int
    original_resume_text: str

class ResumeResponse(BaseModel):
    id: int
    user_id: int
    content: str
    ats_score: float
    created_at: datetime

    class Config:
        from_attributes = True
