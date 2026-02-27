# v1 prompt for Resume Generation (1st Pass)
GENERATOR_PROMPT_V1 = """
You are an expert resume writer. Please rewrite the following original resume content 
so that it better aligns with the provided Job Description (JD).

JD Keywords to include: {keywords}

Original Resume:
{original_resume}

Output only the upgraded resume text, keeping a professional tone and emphasizing achievements.
"""
