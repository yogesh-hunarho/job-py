import json
from config import GEMINI_MODEL, GENERATION_CONFIG

def generate_profile_summary(skills: list[str],summary=None, isRewrite=False):
    """Generate profile summaries using Gemini."""

    if isRewrite:
        prompt = f"""
        Rewrite a 300-character professional profile summary for a student.
        Skills: {", ".join(skills)}.
        Summary:{summary}

        Return professionally rewritten summaries (under 300 characters) in JSON format:
        ["summary"]
        """
    else:
        prompt = f"""
        You are a career counselor AI helping students write profile summaries.

        Generate 2 professional profile summaries (each under 300 characters)
        for a student based on the following details:

        Skills: {", ".join(skills)}.

        Return them in JSON format:
        ["summary1", "summary2"]
        """

    response = GEMINI_MODEL.generate_content(
        prompt, generation_config=GENERATION_CONFIG
    )

    return json.loads(response.text.strip())

def generate_Internship_summary(designation, company, summary=None, isRewrite=False):
    """Generate or polish internship summaries using Gemini."""

    if isRewrite:
        prompt = f"""
        You are an expert career writing assistant.

        The user has written an internship summary that may contain grammatical errors or weak phrasing.
        Your task is to polish and professionally rewrite it while keeping the meaning the same.

        Company: {company}
        Designation: {designation}
        User Summary: {summary}

        Return professionally rewritten summaries (under 300 characters) in JSON format:
        ["summary"]
        """
    else:
        prompt = f"""
        You are a career counselor AI helping students write internship summaries.

        Generate 2 professional internship summaries (each under 300 characters)
        for a student based on the following details:

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
    """Generate or polish professional experience summaries using Gemini."""

    if isRewrite:
        prompt = f"""
        You are a professional career writing assistant.

        The user has written an experience summary that may contain grammatical or stylistic issues.
        Please polish and rewrite it in a professional tone while keeping the same meaning.

        - Use present tense if the person is currently working.
        - Use past tense if the experience has ended.

        Details:
        Company: {company}
        Designation: {designation}
        Currently Working: {currently_working}
        User Summary: {summary}

        Return improved summaries (under 300 characters) in JSON format:
        ["summary"]
        """
    else:
        tense_instruction = (
            "Use present tense (e.g., 'developing', 'leading', 'managing') since the person is currently working."
            if currently_working
            else "Use past tense (e.g., 'developed', 'led', 'managed') since the experience has ended."
        )

        prompt = f"""
        You are a career coach AI helping professionals write concise experience summaries.

        Generate 2 professional and achievement-oriented summaries (each under 250 characters)
        for the following role:

        Designation: {designation}
        Company: {company}

        {tense_instruction}

        Return 2 improved summaries (each under 300 characters) in JSON format::
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
