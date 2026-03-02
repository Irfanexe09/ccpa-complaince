import os

# --- MODEL CONFIGURATION ---
# Qwen-2.5-1.5B is our high-performance production model.
MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"

# --- SYSTEM PATHS ---
# We use dynamic paths so the code works on Mac, Linux, and Docker!
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATUTE_PDF = os.path.join(BASE_DIR, "ccpa_statute.pdf")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# --- API SETTINGS ---
PORT = 8000
HOST = "0.0.0.0"
