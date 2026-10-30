import os
import warnings
warnings.filterwarnings("ignore")
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from .config import DEFAULT_GEMINI_MODEL, FALLBACK_GEMINI_MODELS, BACKEND_DIR, PROJECT_DIR

GROUNDED_SYSTEM_PROMPT = """You are an expert research analyst and intelligent data assistant.
Your goal is to provide an accurate, thoroughly grounded, human-readable, and beautifully structured answer based strictly on the provided Context.

GUIDELINES FOR PRESENTATION & FORMATTING:
1. Organization & Structure: Organize your answer logically using clean Markdown headings (e.g., `### Overview`, `### Key Findings`, `### Detailed Breakdown`, `### Summary`).
2. Tables: When presenting metrics, comparisons, values, parameters, or structured data, ALWAYS format them as clean Markdown tables with distinct headers (e.g., | Metric | Description / Formula | Value | Interpretation |).
3. Formulas & Math: Write formulas and calculations in clean, readable plain-text notation (e.g., `Accuracy = (TP + TN) / Total` or `TP = 23`). Do NOT use raw LaTeX markup like \\text or \\frac.
4. Bullet Points: Use organized bullet lists for enumerating multiple items, properties, or takeaways.
5. Emphasize Key Insights: Use **bold text** to highlight critical numbers, terms, and conclusions so the answer is immediately scannable.
6. Tone: Maintain a professional, articulate, and direct tone.

STRICT GROUNDING RULES:
1. Every fact, statistic, and conclusion must come strictly from the provided Context.
2. If the core topic or subject asked by the user is completely missing or unmentioned in the Context, respond strictly with: "The information is not provided."
3. Do not introduce outside facts, dates, or concepts that are unrelated to what is discussed in the Context.

Context:
{context}

Question: {query}
Answer:"""

def generate_answer(query: str, combined_context: str) -> str:
    """
    Generates a strictly grounded response using Google Gemini models.
    Supports graceful fallback across active Gemini models.
    """
    # Reload environment to pick up any runtime .env changes
    load_dotenv(PROJECT_DIR / ".env", override=True)
    load_dotenv(BACKEND_DIR / ".env", override=True)
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    if not api_key:
        return (
            "Missing Gemini API Key. Please get a free API key at https://aistudio.google.com/app/apikey "
            "and add it to your .env file: GEMINI_API_KEY=AIzaSy... then retry."
        )

    # Configure Gemini with HTTPS REST transport for Windows stability
    genai.configure(api_key=api_key, transport="rest")

    prompt = GROUNDED_SYSTEM_PROMPT.format(context=combined_context, query=query)

    candidate_models = [DEFAULT_GEMINI_MODEL] + FALLBACK_GEMINI_MODELS
    last_error = None

    for model_name in candidate_models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            err_msg = str(e)
            last_error = e
            # If model deprecated/not found, try next candidate
            if "not found" in err_msg.lower() or "404" in err_msg or "no longer available" in err_msg.lower():
                continue
            else:
                return f"Gemini API Error: {err_msg}"

    return f"Error: All configured Gemini models failed. Last error: {str(last_error)}"
