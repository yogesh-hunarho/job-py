from datetime import datetime, timedelta
from services.db import cache, internship_cache

def cleanup_old_records():
    """Force delete old records beyond their TTL window."""

    # Jobs older than 3 days
    jobs_threshold = datetime.utcnow() - timedelta(days=3)
    cache.delete_many({"created_at": {"$lt": jobs_threshold}})

    # Internships older than 1 day
    internships_threshold = datetime.utcnow() - timedelta(days=1)
    internship_cache.delete_many({"created_at": {"$lt": internships_threshold}})

    print("🧹 Cleanup completed!")
