import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"


with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    LAB_LINKS = json.load(f)
