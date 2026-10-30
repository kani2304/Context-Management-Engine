import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BACKEND_DIR.parent

# Load environment variables (.env in project root or current folder)
load_dotenv(PROJECT_DIR / ".env")
load_dotenv(BACKEND_DIR / ".env")

# Gemini Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
DEFAULT_GEMINI_MODEL = "models/gemini-3.5-flash"
FALLBACK_GEMINI_MODELS = [
    "models/gemini-3.5-flash-lite",
    "models/gemini-3.8-flash",
    "models/gemini-flash-latest",
]

# RAG & Chunking Settings
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Conversational stop words stripped from lexical BM25 matching
CONVERSATIONAL_STOPWORDS = {
    "explain", "tell", "what", "is", "are", "me", "in", "a", "an", "the",
    "very", "basic", "layman", "language", "with", "real", "life", "example",
    "examples", "simple", "terms", "give", "how", "does", "work", "about",
    "can", "you", "please", "could", "would", "describe"
}

# CORS settings
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
ALLOWED_ORIGIN_REGEX = r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$"

