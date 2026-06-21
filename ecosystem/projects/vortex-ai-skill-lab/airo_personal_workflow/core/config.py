import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / ".airo_personal_data"
DEFAULT_DB_PATH = DATA_DIR / "airo_personal_workflow.sqlite3"
DB_PATH = Path(os.environ.get("AIRO_DB_PATH", str(DEFAULT_DB_PATH)))
