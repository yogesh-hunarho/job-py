# # MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://yogesh:3CXDTlZp96XYawfw@cluster0.edvquc4.mongodb.net/recordify?retryWrites=true&w=majority&appName=Cluster0")

from fastapi import FastAPI
from datetime import date, datetime
from jobspy import scrape_jobs
import math
import numpy as np

app = FastAPI()

print("🚀 JobScraper API running without MongoDB cache...")

# --- Fix data types before returning (safety for JSON responses) ---
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


@app.get("/")
def read_root():
    return {
        "AI": "This API fetches jobs from multiple job boards using JobSpy.",
        "endpoints": ["/api/jobs"],
    }


@app.get("/api/jobs")
def get_jobs(
    search_term: str,
    location: str,
    country_indeed: str = "India",
):
    """
    Fetch fresh job data directly from JobSpy (no cache, no database).
    Example:
    /api/jobs?search_term=react%20developer&location=Mumbai
    """
    try:
        print(f"🔍 Fetching jobs for '{search_term}' in {location}...")
        jobs_df = scrape_jobs(
            site_name=["linkedin","indeed",'glassdoor'],
            search_term=search_term,
            location=location,
            country_indeed=country_indeed,
            results_wanted=10,
        )

        job_data = jobs_df.to_dict(orient="records")
        safe_data = fix_types(job_data)

        return {
            "source": "live",
            "count": len(safe_data),
            "data": safe_data,
        }

    except Exception as e:
        print(f"❌ Error fetching jobs: {e}")
        return {
            "error": str(e),
            "message": "Failed to fetch job data. Please try again later.",
        }
