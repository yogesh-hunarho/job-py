# from datetime import datetime
# from config import RAPIDAPI_KEY, RAPIDAPI_HOST, BASE_URL
# from services.db import internship_cache
# import httpx
# import traceback

# async def fetch_internships_api(title: str, location: str, offset: int):
#     """Call RapidAPI Internship API."""
#     params = {
#         "offset": offset
#     }
#     if title:
#         params["title_filter"] = title
#     if location:
#         params["location_filter"] = location

#     headers = {
#         "x-rapidapi-key": RAPIDAPI_KEY,
#         "x-rapidapi-host": RAPIDAPI_HOST,
#     }

#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.get(BASE_URL, params=params, headers=headers)
#             return response.json()
#     except Exception:
#         traceback.print_exc()
#         return {"results": []}


# def get_cached_internships(title: str, location: str):
#     return internship_cache.find_one({"title": title, "location": location})


# def update_cached_internships(title: str, location: str, new_results: list):
#     internship_cache.update_one(
#         {"title": title, "location": location},
#         {
#             "$set": {"created_at": datetime.utcnow()},
#             "$push": {"results": {"$each": new_results}}
#         },
#         upsert=True
#     )




from datetime import datetime
from jobspy import scrape_jobs
from services.db import internship_cache
from utils.serializer import fix_types
import traceback

def generate_google_search_term(title: str, location: str):
    """
    Google Jobs requires the EXACT TEXT that appears in their search box.
    """
    return f"{title} internship in {location} posted past 3 days"


def fetch_and_cache_internships(title: str, location: str):
    try:
        search_str = f"{title} internship OR {title} intern"
        # keyword_filter = " OR ".join([f'"{k}"' for k in keywords])
        # search_str = f'{title} ({keyword_filter})'
        # print("search_str",search_str)

        google_term = generate_google_search_term(title, location)

        jobs_df = scrape_jobs(
            site_name=["indeed", "linkedin", "zip_recruiter", "google"],
            search_term=search_str,
            google_search_term=google_term,
            location=location,
            hours_old=24*10,            # last 3 days
            country_indeed="India",
            results_wanted=100
        )

        safe_results = fix_types(jobs_df.to_dict(orient="records"))

        internship_cache.update_one(
            {"title": title.lower(), "location": location.lower()},
            {"$set": {"results": safe_results, "created_at": datetime.utcnow()}},
            upsert=True
        )

        return safe_results

    except Exception:
        traceback.print_exc()
        return []


def get_cached_internships(title: str, location: str):
    return internship_cache.find_one({
        "title": title.lower(),
        "location": location.lower()
    })
