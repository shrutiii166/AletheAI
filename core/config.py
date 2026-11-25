import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from the project's .env file
load_dotenv()

# Application settings
APP_NAME = "AletheAI"

# Groq configuration
try:
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
except Exception:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = "openai/gpt-oss-20b"

# Session settings
SESSION_TIMEOUT_MINUTES = 60

# Document processing settings
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K_RESULTS = 4