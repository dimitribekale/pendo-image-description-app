import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

APP_NAME = "Pendo"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "huggingface")
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "Salesforce/blip-image-captioning-large")
HUGGINGFACE_DEVICE = os.getenv('HUGGINGFACE_DEVICE', 'auto')
MODELS_CACHE_DIR = BASE_DIR / 'models_cache'
MODELS_CACHE_DIR.mkdir(exist_ok=True)

MAX_IMAGE_SIZE = 10 * 1024 * 1024 # 10MB
SUPPORTED_FORMATS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]
THUMBNAIL_SIZE = (400, 400)

ASSETS_DIR = BASE_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
CACHE_DIR = BASE_DIR / "cache"
TEMP_DIR = BASE_DIR / "temp"

for directory in [CACHE_DIR, TEMP_DIR]:
    directory.mkdir(exist_ok=True)

DARK_MODE = True
PRIMARY_COLOR = "#2563eb"
SECONDARY_COLOR = "#64748b"
BACKGROUND_COLOR = "#0f172a"
TEXT_COLOR = "#f1f5f9"