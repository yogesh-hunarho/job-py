from pydantic import BaseModel, Field
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

class SupportMessageRequest(BaseModel):
    subject: str
    message: str
    isRewrite: bool = False

class ResumeSummaryRequest(BaseModel):
    skills: List[str]
    summary: Optional[str] = None
    isRewrite: bool = False

class InternshipSummaryRequest(BaseModel):
    designation: str
    company: Optional[str] = None
    summary: Optional[str] = None
    isrewrite: bool = Field(False, alias="isRewrite") # Use Field for alias if client sends isRewrite

class ExperienceSummaryRequest(BaseModel):
    designation: str
    company: Optional[str] = None
    summary: Optional[str] = None
    isrewrite: bool = Field(False, alias="isRewrite")

class AccomplishmentSummaryRequest(BaseModel):
    title: str
    description: Optional[str] = None
    isrewrite: bool = Field(False, alias="isRewrite")

class JobShortDescriptionRequest(BaseModel):
    title: str
    company: str
    short_description: Optional[str] = None
    isrewrite: bool = Field(False, alias="isRewrite")

class AnnouncementBodyRequest(BaseModel):
    title: str
    body: Optional[str] = None
    isRewrite: bool = False

class AnnouncementEmailRequest(BaseModel):
    title: str
    html: Optional[str] = None
    isRewrite: bool = False
