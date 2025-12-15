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

def generate_JobShort_Description(company, title, short_description=None, isRewrite=False):
    """Generate or polish job short descriptions in first-person."""

    if isRewrite:
        prompt = f"""
        You are an expert career writing assistant.

        The user has written a job short description that may contain grammatical errors or weak phrasing.
        Rewrite the short description in a professional tone using FIRST PERSON
        (use "I", not third-person language like "the candidate").

        Keep the meaning the same and limit to 300 characters.

        Company: {company}
        Role: {title}
        User Short Description: {short_description or ''}

        Return professionally rewritten summaries (under 300 characters) in JSON format:
        ["description"]
        """
    else:
        prompt = f"""
        You are a career counselor AI helping students write job short descriptions.

        Generate 2 professional job short descriptions using FIRST PERSON (use "I", not third-person language).
        Each summary must be under 300 characters.

        Role: {title}
        Company: {company}

        Return them in JSON format:
        ["description1", "description2"]
        """

    response = GEMINI_MODEL.generate_content(prompt, generation_config=GENERATION_CONFIG)
    return json.loads(response.text.strip())

def generate_Job_Description(company,title,skills=None,education=None,industry=None,work_type=None,location=None,description=None,isRewrite=False):
    """Generate or polish a structured HTML job description."""

    skills = skills or []
    education = education or []
    work_type = work_type or []
    location = location or []

    skills_text = ", ".join(skills) if skills else "N/A"
    education_text = ", ".join(education) if education else "N/A"
    work_type_text = ", ".join(work_type) if work_type else "N/A"
    location_text = ", ".join(location) if location else "N/A"
    industry_text = industry or "N/A"

    if isRewrite:
        prompt = f"""
        You are an expert HR content writer.

        The user has provided a job description that may be verbose or inconsistently formatted.
        Rewrite it into a clean, professional posting suitable for employers and candidates.
        Preserve the original meaning and role expectations.

        Output strictly HTML (no scripts/styles). Use the following structure:
        <h3>Overview</h3>
        <p>...</p>
        <h3>Responsibilities</h3>
        <ul><li>...</li></ul>
        <h3>Requirements</h3>
        <ul><li>...</li></ul>
        <h3>Preferred Qualifications</h3>
        <ul><li>...</li></ul>
        <h3>Benefits</h3>
        <ul><li>...</li></ul>
        <h3>Location & Work Type</h3>
        <p>...</p>

        Keep between 450–900 words. Do not use first-person.
        Incorporate these contextual details where relevant:

        Company: {company}
        Role: {title}
        Skills: {skills_text}
        Education: {education_text}
        Industry: {industry_text}
        Work Type: {work_type_text}
        Location: {location_text}

        Original Description:
        {description or ''}

        Return JSON array with one item:
        ["html"]
        """
    else:
        prompt = f"""
        You are a career/HR content generator.

        Create a professional employer-style job description in clean HTML.
        Do not use first-person; write as a job posting for candidates.

        Output strictly HTML (no scripts/styles). Use this structure:
        <h3>Overview</h3>
        <p>...</p>
        <h3>Responsibilities</h3>
        <ul><li>...</li></ul>
        <h3>Requirements</h3>
        <ul><li>...</li></ul>
        <h3>Preferred Qualifications</h3>
        <ul><li>...</li></ul>
        <h3>Benefits</h3>
        <ul><li>...</li></ul>
        <h3>Location & Work Type</h3>
        <p>...</p>

        Keep between 450–900 words.
        Use realistic, concise bullets and avoid fluff.
        Reflect the inputs below, integrating them naturally:

        Company: {company}
        Role: {title}
        Skills: {skills_text}
        Education: {education_text}
        Industry: {industry_text}
        Work Type: {work_type_text}
        Location: {location_text}

        Return JSON array with one item:
        ["html"]
        """

    response = GEMINI_MODEL.generate_content(prompt, generation_config=GENERATION_CONFIG)
    return json.loads(response.text.strip())


def generate_Support_Message(subject, message=None, isRewrite=False):
    """Generate or rewrite a concise first‑person support message."""

    if isRewrite:
        prompt = f"""
        You are an empathetic support assistant.

        Rewrite the user's support message to be clear, polite, and actionable.
        Use FIRST PERSON ("I") and a professional tone.
        Keep the meaning the same and limit to 300 characters.

        Subject: {subject}
        User Message: {message or ''}

        Return JSON:
        ["message"]
        """
    else:
        prompt = f"""
        You are an empathetic support assistant.

        Generate 2 concise first-person support messages about the issue below.
        Use a professional tone, include key context, and politely request next steps.
        Each must be under 300 characters.

        Subject: {subject}

        Return JSON:
        ["message1", "message2"]
        """

    response = GEMINI_MODEL.generate_content(prompt, generation_config=GENERATION_CONFIG)
    return json.loads(response.text.strip())

def generate_Announcement_Body(title, body=None, isRewrite=False):
    """Generate or rewrite a clear announcement body in HTML."""

    import json

    if isRewrite:
        prompt = f"""
        You are a communications editor.

        Rewrite the announcement body to be clear, concise, and engaging.
        Keep the original meaning, polish grammar and flow, and maintain a formal but friendly tone.
        Output clean HTML (no styles/scripts), 150–400 words.

        Title: {title}
        Original Body:
        {body or ''}

        Return JSON:
        ["html"]
        """
    else:
        prompt = f"""
        You are a communications writer.

        Create a clear, engaging announcement body in clean HTML (no styles/scripts), 150–400 words.
        Include a short intro, 2–4 key points in <ul>, and a closing call‑to‑action if relevant.

        Title: {title}

        Return JSON:
        ["html"]
        """

    response = GEMINI_MODEL.generate_content(prompt, generation_config=GENERATION_CONFIG)
    return json.loads(response.text.strip())


def generate_Announcement_Email(title, html=None, isRewrite=False):
    """Generate or rewrite an announcement email HTML with a clear structure."""

    import json

    if isRewrite:
        prompt = f"""
        You are an email communications editor.

        Rewrite the announcement email HTML to be clear, concise, and engaging.
        Improve structure, headings, and calls-to-action while preserving intent.
        Keep it mobile-friendly and avoid inline styles or scripts.

        Title: {title}
        Original HTML:
        {html or ''}

        Return JSON:
        ["html"]
        """
    else:
        prompt = f"""
        You are an email communications writer.

        Create clean HTML for an announcement email with:
        - A concise header
        - A friendly intro
        - 2–4 bullet points
        - A clear call‑to‑action
        - A short footer/sign-off

        No inline styles or scripts. Keep it mobile-friendly.

        Title: {title}

        Return JSON:
        ["html"]
        """

    response = GEMINI_MODEL.generate_content(prompt, generation_config=GENERATION_CONFIG)
    return json.loads(response.text.strip())