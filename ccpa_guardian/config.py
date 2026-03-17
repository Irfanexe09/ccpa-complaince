import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if it exists
load_dotenv()

# --- PROJECT PATHS ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
STATIC_DIR = BASE_DIR / "static"

# Create directories if they don't exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR.mkdir(parents=True, exist_ok=True)

# --- FILE PATHS ---
DEFAULT_STATUTE_PDF = RAW_DATA_DIR / "ccpa_statute.pdf"
FAISS_INDEX_PATH = PROCESSED_DATA_DIR / "faiss_index"

# --- MODEL CONFIGURATION ---
# Use an environment variable for the model ID, fallback to Qwen-2.5-1.5B
MODEL_ID = os.getenv("MODEL_ID", "Qwen/Qwen2.5-1.5B-Instruct")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# --- API & APP SETTINGS ---
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

# --- HF TOKEN ---
HF_TOKEN = os.getenv("HF_TOKEN")
