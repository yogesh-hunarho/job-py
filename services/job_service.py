from datetime import datetime
from jobspy import scrape_jobs
from services.db import cache
from utils.serializer import fix_types
import traceback

def fetch_and_cache(search_term: str, location: str, country: str):
    """Fetch fresh job data using JobSpy and update Mongo cache."""
    try:
        jobs_df = scrape_jobs(
            site_name=["indeed", "linkedin", "zip_recruiter", "google"],
            search_term=search_term,
            location=location,
            country_indeed=country,
            hours_old=72,
            results_wanted=20
        )

        safe_results = fix_types(jobs_df.to_dict(orient="records"))

        cache.update_one(
            {"search_term": search_term, "location": location, "country_indeed": country},
            {"$set": {"results": safe_results, "created_at": datetime.utcnow()}},
            upsert=True
        )

        return safe_results

    except Exception:
        traceback.print_exc()
        return []

def get_cached_jobs(search_term: str, location: str, country: str):
    """Retrieve cached job data if available."""
    return cache.find_one({
        "search_term": search_term,
        "location": location,
        "country_indeed": country
    })
