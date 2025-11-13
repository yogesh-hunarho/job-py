from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from services.ai_service import generate_resume_summary

router = APIRouter()

@router.post("/summary")
async def resume_summary(request: Request):
    body = await request.json()
    skills = body.get("skills")

    if not skills or not isinstance(skills, list):
        return JSONResponse({"error": "Skills must be a list"}, status_code=400)

    try:
        summaries = generate_resume_summary(skills)
        return JSONResponse({"data": summaries, "message": True})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
