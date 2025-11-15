
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["indeed", "linkedin", "zip_recruiter"],
    search_term="web developer internship OR web developer intern",
    google_search_term="web developer internship in Mumbai posted past 3 days",
    location="Mumbai",
    hours_old=72,
    country_indeed="India",
    results_wanted=50
)
print(f"Found {len(jobs)} jobs")
print(jobs)
