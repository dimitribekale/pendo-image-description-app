import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
APP_NAME = "Pendo"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "huggingface")
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "Salesforce/blip-image-captioning-large") 