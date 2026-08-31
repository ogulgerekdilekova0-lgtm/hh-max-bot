import os

from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/hh_max_bot",
)
MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN", "")
YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID", "")
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY", "")
HH_DOCS_REPO_URL = os.getenv("HH_DOCS_REPO_URL", "https://github.com/hhru/api")
HH_DOCS_BRANCH = os.getenv("HH_DOCS_BRANCH", "master")
HH_DOCS_PATH = os.getenv("HH_DOCS_PATH", "docs")
HH_DOCS_CACHE_DIR = os.getenv("HH_DOCS_CACHE_DIR", "data/knowledge")
