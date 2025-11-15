from fastapi import APIRouter, BackgroundTasks
from services.job_service import fetch_and_cache, get_cached_jobs
from datetime import datetime
from services.db import internship_cache
# from services.internship_service import  get_cached_internships,fetch_internships_api,update_cached_internships
from services.internship_service import fetch_and_cache_internships, get_cached_internships

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
def get_internships(
    title: str,
    location: str,
    background_tasks: BackgroundTasks = None
):
    cached = get_cached_internships(title, location)

    if cached and cached.get("results"):
        # async refresh in background
        background_tasks.add_task(fetch_and_cache_internships, title, location)

        return {
            "source": "cache",
            "count": len(cached["results"]),
            "data": cached["results"],
            "last_updated": cached["created_at"]
        }

    # Fetch fresh
    fresh = fetch_and_cache_internships(title, location)
    return {
        "source": "live",
        "count": len(fresh),
        "data": fresh
    }


# LIMIT = 30

# @router.get("/internships")
# async def get_internships(
#     title: str = "",
#     location: str = "",
#     offset: int = 0,
#     background_tasks: BackgroundTasks = None
# ):
#     limit = 10

#     cache = get_cached_internships(title, location)

#     if cache:
#         results = cache["results"]

#         if len(results) >= offset + limit:
#             sliced = results[offset: offset + limit]

#             background_tasks.add_task(
#                 fetch_and_append_in_background, title, location, offset
#             )

#             return {
#                 "source": "cache",
#                 "count": len(sliced),
#                 "data": sliced,
#                 "total_cached": len(results),
#             }

#         # Fetch fresh page
#         api_data = await fetch_internships_api(title, location, offset)
#         new_results = api_data if isinstance(api_data, list) else api_data.get("results", [])

#         update_cached_internships(title, location, new_results)

#         return {
#             "source": "live",
#             "count": len(new_results),
#             "data": new_results,
#         }

#     # No cache — first time
#     api_data = await fetch_internships_api(title, location, offset)
#     results = api_data if isinstance(api_data, list) else api_data.get("results", [])

#     update_cached_internships(title, location, results)

#     return {
#         "source": "live",
#         "count": len(results),
#         "data": results,
#     }

# async def fetch_and_append_in_background(title, location, offset):
#     api_data = await fetch_internships_api(title, location, offset)
#     new_results = api_data if isinstance(api_data, list) else api_data.get("results", [])

#     if new_results:
#         update_cached_internships(title, location, new_results)

