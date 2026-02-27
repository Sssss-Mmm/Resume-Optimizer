import json
from openai import AsyncOpenAI
from app.core.config import settings
from app.core.prompts.analyzer import JD_ANALYZER_PROMPT_V1
from app.core.prompts.generator import GENERATOR_PROMPT_V1
from typing import List

# Instantiate async OpenAI client if api_key is provided
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

async def extract_keywords_from_jd(jd_text: str) -> List[str]:
    """
    Extracts essential keywords from a Job Description using OpenAI.
    """
    if not client:
        return ["python", "fastapi", "database"] # fallback for missing API key during local test

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": JD_ANALYZER_PROMPT_V1},
                {"role": "user", "content": jd_text}
            ],
            response_format={"type": "json_object"} # Ensure JSON output if modeled well, or instruct to output raw json list.
        )
        # Usually we might want to parse standard json {"keywords": ["...", "..."]}
        content = response.choices[0].message.content
        data = json.loads(content)
        return data.get("keywords", [])
    except Exception as e:
        print(f"Error in LLM keyword extraction: {e}")
        return []

async def generate_initial_resume(original_resume: str, keywords: List[str]) -> str:
    """
    Rewrites the original resume based on extracted JD keywords.
    """
    if not client:
        return original_resume + "\n\n(Added generated boilerplate for missing API Key)"
        
    keyword_str = ", ".join(keywords)
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user", 
                    "content": GENERATOR_PROMPT_V1.format(keywords=keyword_str, original_resume=original_resume)
                }
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in LLM generation: {e}")
        return original_resume
