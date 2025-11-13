
# from fastapi import FastAPI, BackgroundTasks
# from datetime import datetime, date
# from jobspy import scrape_jobs
# from pymongo import MongoClient, ASCENDING
# import math
# import numpy as np
# import os

# MONGO_URI = os.getenv(
#     "MONGO_URI",
#     "mongodb+srv://yogesh:3CXDTlZp96XYawfw@cluster0.edvquc4.mongodb.net/recordify?retryWrites=true&w=majority&appName=Cluster0"
# )
# client = MongoClient(MONGO_URI)
# db = client["recordify"]
# collection = db["jobs_cache"]

# collection.create_index(
#     [("created_at", ASCENDING)],
#     expireAfterSeconds=7 * 24 * 60 * 60
# )

# app = FastAPI()

# def fix_types(obj):
#     """Convert unsupported data types (datetime, date, NaN, numpy) to JSON-safe values."""
#     if isinstance(obj, list):
#         return [fix_types(x) for x in obj]
#     elif isinstance(obj, dict):
#         return {k: fix_types(v) for k, v in obj.items()}
#     elif isinstance(obj, datetime):
#         return obj.isoformat()
#     elif isinstance(obj, date):
#         return datetime(obj.year, obj.month, obj.day).isoformat()
#     elif isinstance(obj, float):
#         if math.isnan(obj) or math.isinf(obj):
#             return None
#         return obj
#     elif isinstance(obj, np.generic):  # e.g. numpy.float64, numpy.bool_
#         return obj.item()
#     else:
#         return obj


# @app.get("/")
# def read_root():
#     return {
#         "AI": "This API fetches jobs from multiple job boards using JobSpy.",
#         "endpoints": ["/api/jobs", "/refresh"],
#     }


# @app.get("/api/jobs")
# def get_jobs(
#     search_term: str,
#     location: str,
#     country_indeed: str = "India",
#     background_tasks: BackgroundTasks = None
# ):
#     """
#     Fetch jobs. If data is in Mongo cache (<7 days old), return cached.
#     Otherwise scrape new data and store in DB.
#     """
#     try:
#         # Check cache
#         cached = collection.find_one({
#             "search_term": search_term,
#             "location": location,
#             "country_indeed": country_indeed
#         })

#         if cached:
#             print(f"📦 Returning cached data for '{search_term}' in {location}")
#             cached["_id"] = str(cached["_id"])
#             # Background refresh (don’t block request)
#             background_tasks.add_task(refresh_cache, search_term, location, country_indeed)
#             return {
#                 "source": "cache",
#                 "count": len(cached.get("results", [])),
#                 "data": cached["results"],
#                 "last_updated": cached.get("created_at")
#             }

#         # No cache found → fetch live data
#         print(f"🔍 Fetching fresh jobs for '{search_term}' in {location}...")
#         jobs_df = scrape_jobs(
#             site_name=["linkedin", "indeed", "glassdoor","google"],
#             search_term=search_term,
#             location=location,
#             country_indeed=country_indeed,
#             results_wanted=10,
#         )

#         job_data = jobs_df.to_dict(orient="records")
#         safe_data = fix_types(job_data)

#         # Store in Mongo
#         collection.insert_one({
#             "search_term": search_term,
#             "location": location,
#             "country_indeed": country_indeed,
#             "results": safe_data,
#             "created_at": datetime.utcnow()
#         })

#         return {
#             "source": "live",
#             "count": len(safe_data),
#             "data": safe_data,
#         }

#     except Exception as e:
#         print(f"❌ Error fetching jobs: {e}")
#         return {"error": str(e), "message": "Failed to fetch job data. Please try again later."}


# # === Background Refresh Function ===
# def refresh_cache(search_term: str, location: str, country_indeed: str):
#     """Fetch fresh data in background and update Mongo cache."""
#     try:
#         print(f"🔄 Refreshing cache for '{search_term}' in {location}...")
#         jobs_df = scrape_jobs(
#             site_name=["linkedin", "indeed", "glassdoor","google"],
#             search_term=search_term,
#             location=location,
#             country_indeed=country_indeed,
#             results_wanted=10,
#         )

#         job_data = jobs_df.to_dict(orient="records")
#         safe_data = fix_types(job_data)

#         collection.update_one(
#             {"search_term": search_term, "location": location, "country_indeed": country_indeed},
#             {"$set": {
#                 "results": safe_data,
#                 "created_at": datetime.utcnow()
#             }},
#             upsert=True
#         )

#         print(f"✅ Cache updated successfully for '{search_term}' - {location}")

#     except Exception as e:
#         print(f"❌ Background refresh failed: {e}")


# # === Status Endpoint (Optional) ===
# @app.get("/status")
# def status():
#     count = collection.count_documents({})
#     return {"status": "ok", "cached_records": count}




from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, date
from jobspy import scrape_jobs
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING
import math
import numpy as np
import os
import traceback
import httpx
import google.generativeai as genai

load_dotenv()

# === MongoDB Setup ===
MONGO_URI = os.getenv("MONGO_URI")
RAPIDAPI_KEY= os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST= os.getenv("RAPIDAPI_HOST")
BASE_URL = os.getenv("BASE_URL")

client = MongoClient(MONGO_URI)
db = client["recordify"]
collection = db["jobs_cache"]

# TTL Index: auto-delete docs after 1 days (ensure created_at is a datetime field)
collection.create_index(
    [("created_at", ASCENDING)],
    expireAfterSeconds=1 * 24 * 60 * 60
)

# === FastAPI App ===
app = FastAPI(
    title="AI Job API",
    description="Fetches jobs using JobSpy scraper and Also use this for regenerate then text with gemini",
    version="1.0.0",
    contact={
        "name": "Yogesh Singh",
        "url": "https://abtyogesh.vercel.app"
    }
)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash"
)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json"
}

# Allow all CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Utility: Clean unsupported data types ===
def fix_types(obj):
    """Convert unsupported data types (datetime, date, NaN, numpy) to JSON-safe values."""
    if isinstance(obj, list):
        return [fix_types(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: fix_types(v) for k, v in obj.items()}
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, date):
        return datetime(obj.year, obj.month, obj.day).isoformat()
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    elif isinstance(obj, np.generic):  # e.g. numpy.float64, numpy.bool_
        return obj.item()
    else:
        return obj

def refresh_cache(search_term: str, location: str, country_indeed: str):
    """
    Fetch fresh data and update MongoDB cache.
    Returns the fetched data (for immediate use if cache was missing).
    """
    try:
        print(f"🔄 Refreshing cache for '{search_term}' in {location}...")
        jobs_df = scrape_jobs(
            site_name=["linkedin", "indeed", "glassdoor","google"],
            search_term=search_term,
            location=location,
            country_indeed=country_indeed,
            results_wanted=30,
        )

        job_data = jobs_df.to_dict(orient="records")
        safe_data = fix_types(job_data)

        collection.update_one(
            {"search_term": search_term, "location": location, "country_indeed": country_indeed},
            {"$set": {
                "results": safe_data,
                "created_at": datetime.utcnow()
            }},
            upsert=True
        )

        print(f"✅ Cache updated successfully for '{search_term}' - {location}")
        return safe_data

    except Exception as e:
        print(f"❌ Background refresh failed: {e}")
        traceback.print_exc()
        return []

@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)

@app.get("/")
def read_root():
    return {
        "AI": "This API fetches jobs from multiple job boards using JobSpy.",
        "endpoints": ["/api/jobs", "/status"],
    }

@app.get("/api/jobs")
def get_jobs(
    search_term: str,
    location: str,
    country_indeed: str = "India",
    background_tasks: BackgroundTasks = None
):
    """
    Fetch jobs. If cached data exists, return immediately and refresh in background.
    If no cache exists, fetch fresh data now and store in DB.
    """
    try:
        cached = collection.find_one({
            "search_term": search_term,
            "location": location,
            "country_indeed": country_indeed
        })

        if cached and cached.get("results"):
            print(f"📦 Returning cached data for '{search_term}' in {location}")
            cached["_id"] = str(cached["_id"])
            background_tasks.add_task(refresh_cache, search_term, location, country_indeed)
            return {
                "source": "cache",
                "count": len(cached.get("results", [])),
                "data": cached["results"],
                "last_updated": cached.get("created_at")
            }

        print(f"🔍 Fetching fresh jobs for '{search_term}' in {location}...")
        fresh_data = refresh_cache(search_term, location, country_indeed)
        return {
            "source": "live",
            "count": len(fresh_data),
            "data": fresh_data,
        }

    except Exception as e:
        print("❌ Error fetching jobs:", traceback.format_exc())
        return {"error": str(e), "message": "Failed to fetch job data. Please try again later."}

@app.get("/api/internships")
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

@app.post("/api/resume-summary")
async def resume_summary(request: Request):
    body = await request.json()
    skills = body.get("skills")

    # Validate input
    if not skills or not isinstance(skills, list):
        return JSONResponse(
            {"error": "No valid skills provided"}, 
            status_code=400
        )

    # Build prompt
    SummaryPrompt = f"""
    Generate a 250-character professional resume summary for a student highlighting their 
    technical and soft skills. The student's skills are: {", ".join(skills)}.
    The tone should be confident and beginner-friendly, suitable for a resume headline.
    Return 2 or more summary variations in JSON array format:
    ["summary1", "summary2"]
    """

    try:
        response = model.generate_content(
            SummaryPrompt,
            generation_config=generation_config
        )

        # Parse JSON output
        ai_result = response.text
        ai_result = ai_result.strip()

        # Ensure JSON output is valid
        import json
        summaries = json.loads(ai_result)

        return JSONResponse({"data": summaries, "message": True}, status_code=200)

    except Exception as e:
        print("❌ Gemini Error:", e)
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/status")
def status():
    count = collection.count_documents({})
    return {
        "status": "ok",
        "cached_records": count,
        "ttl_days": 7
    }
