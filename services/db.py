from pymongo import MongoClient, ASCENDING
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["recordify"]
cache = db["jobs_cache"]

# TTL Index (auto delete after 1 day)
cache.create_index(
    [("created_at", ASCENDING)],
    expireAfterSeconds=86400
)
