from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from services.ai_service import generate_profile_summary, generate_Internship_summary, generate_Experience_summary, generate_Accomplishment_summary, generate_JobShort_Description, generate_Job_Description, generate_Support_Message,generate_Announcement_Body, generate_Announcement_Email
from schemas.validation import ResumeSummaryRequest, InternshipSummaryRequest, ExperienceSummaryRequest, AccomplishmentSummaryRequest, JobShortDescriptionRequest, AnnouncementBodyRequest, AnnouncementEmailRequest, JobDescriptionRequest, SupportMessageRequest

router = APIRouter()

@router.post("/summary")
async def resume_summary(payload: ResumeSummaryRequest):
    if payload.isRewrite and not payload.summary:
        raise HTTPException(
            status_code=400,
            detail="Summary is required when isRewrite is true"
        )
    try:
        summaries = generate_profile_summary(payload.skills, payload.summary, payload.isRewrite)
        return JSONResponse({"data": summaries, "message": True},status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/internship-summary")
async def Internship_summary(payload: InternshipSummaryRequest):
    if payload.isrewrite and not payload.summary:
        raise HTTPException(status_code=400, detail="Summary is required when rewriting.")
    
    try:
        summaries = generate_Internship_summary(payload.designation, payload.company, payload.summary, payload.isrewrite)
        return JSONResponse({"data":summaries, "message":True},status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/experience-summary")
async def Experience_summary(payload: ExperienceSummaryRequest):
    if payload.isrewrite and not payload.summary:
        raise HTTPException(status_code=400, detail="Summary is required when rewriting.")
    
    try:
        summaries = generate_Experience_summary(payload.designation, payload.company, payload.summary, payload.isrewrite)
        return JSONResponse({"data": summaries, "message": True}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/accomplishment-summary")
async def Accomplishment_summary(payload: AccomplishmentSummaryRequest):
    if payload.isrewrite and not payload.description:
        raise HTTPException(status_code=400, detail="Description is required when rewriting.")
    
    try:
        summaries = generate_Accomplishment_summary(payload.title, payload.description, payload.isrewrite)
        return JSONResponse({"data": summaries, "message": True}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/job-short-description")
async def Job_short_Description(payload: JobShortDescriptionRequest):
    if payload.isrewrite and not payload.short_description:
        raise HTTPException(status_code=400, detail="Short description is required when rewriting.")
    
    try:
        summaries = generate_JobShort_Description(payload.company, payload.title, payload.short_description, payload.isrewrite)
        return JSONResponse({"data": summaries, "message": True}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/job-description")
async def job_description(payload: JobDescriptionRequest):

    if payload.isRewrite and not payload.description:
        raise HTTPException(
            status_code=400,
            detail="Description is required when rewriting"
        )

    try:
        summaries = generate_Job_Description(
            payload.company,
            payload.title,
            payload.skills,
            payload.education,
            payload.industry,
            payload.work_type,
            payload.location,
            payload.description,
            payload.isRewrite
        )

        return {
            "success": True,
            "data": summaries
        }

    except Exception as e:
        # Log e here if needed
        raise HTTPException(
            status_code=500,
            detail="Failed to generate job description"
        )

@router.post("/support_message")
async def support_message(payload: SupportMessageRequest):

    if payload.isRewrite and not payload.message:
        raise HTTPException(
            status_code=400,
            detail="Message is required when rewriting"
        )

    try:
        message = generate_Support_Message(payload.subject, payload.message, payload.isRewrite)

        return {
            "success": True,
            "data": message
        }

    except Exception as e:
        # Log e here if needed
        raise HTTPException(
            status_code=500,
            detail="Failed to generate support message"
        )

@router.post("/announcement_body")
async def announcement_body(payload: AnnouncementBodyRequest):
    if payload.isRewrite and not payload.body:
        raise HTTPException(status_code=400, detail="Body is required when rewriting.")
    
    try:
        message = generate_Announcement_Body(payload.title, payload.body, payload.isRewrite)

        return {
            "success": True,
            "data": message
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate announcement body"
        )

@router.post("/announcement_email")
async def announcement_email(payload: AnnouncementEmailRequest):
    if payload.isRewrite and not payload.html:
        raise HTTPException(status_code=400, detail="HTML content is required when rewriting.")
    
    try:
        message = generate_Announcement_Email(payload.title, payload.html, payload.isRewrite)

        return {
            "success": True,
            "data": message
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate announcement email"
        )
