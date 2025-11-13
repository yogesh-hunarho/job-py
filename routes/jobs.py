from fastapi import APIRouter, BackgroundTasks
from services.job_service import fetch_and_cache, get_cached_jobs
from fastapi.responses import JSONResponse
from config import RAPIDAPI_KEY, RAPIDAPI_HOST, BASE_URL
import httpx

router = APIRouter()

@router.get("/jobs")
def get_jobs(
    search_term: str,
    location: str,
    country_indeed: str = "India",
    background_tasks: BackgroundTasks = None
):
    cached = get_cached_jobs(search_term, location, country_indeed)

    if cached and cached.get("results"):
        background_tasks.add_task(fetch_and_cache, search_term, location, country_indeed)

        return {
            "source": "cache",
            "count": len(cached["results"]),
            "data": cached["results"],
            "last_updated": cached["created_at"]
        }

    fresh_data = fetch_and_cache(search_term, location, country_indeed)
    return {"source": "live", "count": len(fresh_data), "data": fresh_data}

@router.get("/internships")
async def get_internships(title: str = "", location: str = "", offset: int = 0):
    params = {}
    if title:
        params["title_filter"] = title
    if location:
        params["location_filter"] = location
    params["offset"] = offset

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, params=params, headers=headers)

        data = response.json()
        return JSONResponse(content=data)

    except Exception as e:
        print("❌ Error:", e)
        return JSONResponse(content={"error": "Internal Server Error"}, status_code=500)
