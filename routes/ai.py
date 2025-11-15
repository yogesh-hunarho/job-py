from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from services.ai_service import generate_profile_summary, generate_Internship_summary, generate_Experience_summary, generate_Accomplishment_summary

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
