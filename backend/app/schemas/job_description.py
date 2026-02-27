from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class JobDescriptionCreate(BaseModel):
    user_id: int
    raw_text: str

class JobDescriptionResponse(BaseModel):
    id: int
    user_id: int
    raw_text: str
    extracted_keywords: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True

class KeywordExtractionResult(BaseModel):
    keywords: List[str] = Field(description="The extracted key skills and requirements from the job description.")
