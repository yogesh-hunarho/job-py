import json
from config import GEMINI_MODEL, GENERATION_CONFIG

def generate_profile_summary(skills: list[str],summary=None, isRewrite=False):
    """Generate profile summaries using Gemini in first-person."""

    if isRewrite:
        prompt = f"""
        Rewrite a 300-character professional profile summary in a professional tone
        using FIRST PERSON (use "I", not "the student").
        Skills: {", ".join(skills)}.
        Summary:{summary}

        Return professionally rewritten summaries (under 300 characters) in JSON format:
        ["summary"]
        """
    else:
        prompt = f"""
        You are a career counselor AI helping students write profile summaries.

        Generate 2 professional profile summaries (each under 300 characters)
        in a professional tone using FIRST PERSON (use "I", not "the student"). based on the following details:

        Skills: {", ".join(skills)}.

        Return them in JSON format:
        ["summary1", "summary2"]
        """

    response = GEMINI_MODEL.generate_content(
        prompt, generation_config=GENERATION_CONFIG
    )

    return json.loads(response.text.strip())

def generate_Internship_summary(designation, company, summary=None, isRewrite=False):
    """Generate or polish internship summaries using Gemini in first-person."""

    if isRewrite:
        prompt = f"""
        You are an expert career writing assistant.

        The user has written an internship summary that may contain grammatical errors or weak phrasing.
        Rewrite the internship summary in a professional tone using FIRST PERSON
        (use "I", not third-person language like "the intern").
        
        Keep the meaning the same and limit to 300 characters.

        Company: {company}
        Designation: {designation}
        User Summary: {summary}

        Return professionally rewritten summaries (under 300 characters) in JSON format:
        ["summary"]
        """
    else:
        prompt = f"""
        You are a career counselor AI helping students write internship summaries.

        Generate 2 professional internship summaries using FIRST PERSON (use "I", not third-person language).
        Each summary must be under 300 characters.

        Designation: {designation}
        Company: {company}

        Return them in JSON format:
        ["summary1", "summary2"]
        """

    response = GEMINI_MODEL.generate_content(
        prompt, generation_config=GENERATION_CONFIG
    )
    return json.loads(response.text.strip())

def generate_Experience_summary(designation, company, summary=None, isRewrite=False, currently_working=False):
    """Generate or polish professional experience summaries using Gemini in first-person."""

    tense_rule = (
        "Use present tense (e.g., 'developing', 'leading', 'managing') because this is a current role."
        if currently_working
        else "Use past tense (e.g., 'developed', 'led', 'managed') because this role has ended."
    )
    
    if isRewrite:
        prompt = f"""
        You are a professional career writing assistant.

        The user has written an experience summary that may contain grammatical or stylistic issues.
        Rewrite the experience summary in a clear, professional tone using FIRST PERSON (use "I", not third-person language).

        Keep the original meaning unchanged.
        Limit to 300 characters.

        {tense_rule}

        Details:
        Company: {company}
        Designation: {designation}
        Currently Working: {currently_working}
        User Summary: {summary}

        Return improved summaries (under 300 characters) in JSON format:
        ["summary"]
        """
    else:

        prompt = f"""
        You are a career coach AI helping professionals write concise experience summaries.
        Generate 2 concise, achievement-focused summaries using FIRST PERSON
        (use "I", not third-person language).

        Keep the original meaning unchanged.
        Each summary must be under 300 characters.

        Designation: {designation}
        Company: {company}

        {tense_rule}

        Return 2 summaries in JSON format::
        ["summary1", "summary2"]
        """

    response = GEMINI_MODEL.generate_content(
        prompt, generation_config=GENERATION_CONFIG
    )
    return json.loads(response.text.strip())


def generate_Accomplishment_summary(title, description=None, isRewrite=False):
    """Generate or polish accomplishment summaries using Gemini."""

    if isRewrite:
        prompt = f"""
        You are a professional resume writing assistant.

        The user has written an accomplishment description that may need improvement.
        Polish and professionally rewrite it while keeping the same meaning and tone.
        Focus on making it concise and impactful.

        Title: {title}
        User Description: {description}

        Return improved versions (under 200 characters) in JSON format:
        ["summary"]
        """
    else:
        prompt = f"""
        You are a resume optimization assistant.

        Generate 2 short and professional accomplishment summaries (each under 200 characters)
        based on the following achievement title. 
        Use a confident and result-oriented tone suitable for a resume.

        Title: {title}

        Return them in JSON format:
        ["summary1", "summary2"]
        """

    response = GEMINI_MODEL.generate_content(
        prompt, generation_config=GENERATION_CONFIG
    )
    return json.loads(response.text.strip())
