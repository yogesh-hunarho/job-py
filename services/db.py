from pymongo import MongoClient, ASCENDING
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["recordify"]
cache = db["jobs_cache"]

# TTL Index (auto delete after 2 day)
cache.create_index(
    [("created_at", ASCENDING)],
    expireAfterSeconds=2 * 86400
)
cache.create_index(
    [("search_term", ASCENDING), ("location", ASCENDING), ("country_indeed", ASCENDING)]
)

internship_cache = db["internships_cache"]
# TTL Index (auto delete after 3 day)
internship_cache.create_index(
    [("created_at", ASCENDING)],
    expireAfterSeconds=3 * 86400
)
internship_cache.create_index(
    [("title", ASCENDING), ("location", ASCENDING)]
)
