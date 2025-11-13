import json
from config import GEMINI_MODEL, GENERATION_CONFIG

def generate_resume_summary(skills: list[str]):
    """Generate resume summaries using Gemini."""
    prompt = f"""
    Generate a 250-character professional resume summary for a student.
    Skills: {", ".join(skills)}.
    Return 2 JSON strings: ["summary1", "summary2"]
    """

    response = GEMINI_MODEL.generate_content(
        prompt, generation_config=GENERATION_CONFIG
    )

    return json.loads(response.text.strip())
