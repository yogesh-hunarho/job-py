from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from services.ai_service import generate_profile_summary, generate_Internship_summary, generate_Experience_summary, generate_Accomplishment_summary, generate_JobShort_Description, generate_Job_Description, generate_Support_Message,generate_Announcement_Body, generate_Announcement_Email
from schemas.job_description import JobDescriptionRequest
from schemas.support_message import SupportMessageRequest

router = APIRouter()

@router.post("/summary")
async def resume_summary(request: Request):
    body = await request.json()
    skills = body.get("skills")
    summary= body.get("summary")
    isRewrite=body.get("isRewrite")

    if not skills or not isinstance(skills, list):
        return JSONResponse({"error": "Skills must be a list"}, status_code=400)
    if isRewrite and not summary:
        return JSONResponse(
            {"error": "Summary is required when isRewrite is true"},
            status_code=400
        )
    try:
        summaries = generate_profile_summary(skills,summary,isRewrite)
        return JSONResponse({"data": summaries, "message": True},status_code=200)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@router.post("/internship-summary")
async def Internship_summary(request: Request):
    body = await request.json()
    designation = body.get("designation")
    company = body.get("company")
    summary = body.get("summary")
    isRewrite= body.get("isrewrite", False)

    if not designation or (not summary and isRewrite):
        return JSONResponse({"error": "Designation and Summary are required."}, status_code=400)
    
    try:
        summaries = generate_Internship_summary(designation,company,summary,isRewrite)
        return JSONResponse({"data":summaries, "message":True},status_code=200)
    except Exception as e:
        return JSONResponse({"error":str(e)},status_code=500)


@router.post("/experience-summary")
async def Experience_summary(request: Request):
    body = await request.json()
    designation = body.get("designation")
    company = body.get("company")
    summary = body.get("summary")
    isRewrite = body.get("isrewrite", False)

    if not designation or (isRewrite and not summary):
        return JSONResponse({"error": "Designation and (if rewriting) Summary are required."}, status_code=400)
    
    try:
        summaries = generate_Experience_summary(designation, company, summary, isRewrite)
        return JSONResponse({"data": summaries, "message": True}, status_code=200)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@router.post("/accomplishment-summary")
async def Accomplishment_summary(request: Request):
    body = await request.json()
    title = body.get("title")
    description = body.get("description")
    isRewrite = body.get("isrewrite", False)

    if not title or (isRewrite and not description):
        return JSONResponse({"error": "Title and (if rewriting) Description are required."}, status_code=400)
    
    try:
        summaries = generate_Accomplishment_summary(title, description, isRewrite)
        return JSONResponse({"data": summaries, "message": True}, status_code=200)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@router.post("/job-short-description")
async def Job_short_Description(request: Request):
    body = await request.json()
    title = body.get("title")
    company = body.get("company")
    description = body.get("short_description")
    isRewrite = body.get("isrewrite", False)

    if not company or not title or (isRewrite and not description):
        return JSONResponse({"error": "company or title and (if rewriting) Description are required."}, status_code=400)
    
    try:
        summaries = generate_JobShort_Description(company, title, description, isRewrite)
        return JSONResponse({"data": summaries, "message": True}, status_code=200)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


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
async def support_message(request: Request):
    reqbody = await request.json()
    
    title=reqbody.get("title"),
    body=reqbody.get("body"),
    isRewrite=reqbody.get("isRewrite")

    if not title or (isRewrite and not body):
        return JSONResponse({"error": "Title, Body (if rewriting) are required."}, status_code=400)
    

    try:
        message = generate_Announcement_Body(title, body, isRewrite)

        return {
            "success": True,
            "data": message
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate support message"
        )

@router.post("/announcement_email")
async def support_message(request: Request):
    reqbody = await request.json()
    
    title=reqbody.get("title"),
    html=reqbody.get("html"),
    isRewrite=reqbody.get("isRewrite")

    if not title or (isRewrite and not html):
        return JSONResponse({"error": "Title, html (if rewriting) are required."}, status_code=400)
    

    try:
        message = generate_Announcement_Email(title, html, isRewrite)

        return {
            "success": True,
            "data": message
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate support message"
        )


