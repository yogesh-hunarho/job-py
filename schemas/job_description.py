from pydantic import BaseModel
from typing import List, Optional

class JobDescriptionRequest(BaseModel):
    title: str
    company: str
    description: Optional[str] = None
    isRewrite: bool = False
    work_type: List[str]
    location: List[str]
    skills: List[str]
    education: List[str]
    industry: List[str]
