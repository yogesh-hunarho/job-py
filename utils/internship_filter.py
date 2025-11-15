INTERNSHIP_KEYWORDS = [
    "intern",
    "internship",
    "trainee",
    "apprentice",
    "student",
    "fresher",
]


def is_internship(job):
    text = (job.get("title","") + " " + job.get("description","")).lower()
    return any(kw in text for kw in INTERNSHIP_KEYWORDS)


def filter_internships(job):
    title = job.get("title", "").lower()
    if "intern" in title or "internship" in title:
        return True

    return False