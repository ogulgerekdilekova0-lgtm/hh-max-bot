from pathlib import Path

import httpx

from app.config import HH_DOCS_BRANCH, HH_DOCS_CACHE_DIR, HH_DOCS_PATH, HH_DOCS_REPO_URL


def _github_api_docs_url() -> str:
    repo = HH_DOCS_REPO_URL.rstrip("/").replace("https://github.com/", "")
    return f"https://api.github.com/repos/{repo}/contents/{HH_DOCS_PATH}?ref={HH_DOCS_BRANCH}"


def list_doc_files() -> list[str]:
    response = httpx.get(_github_api_docs_url(), timeout=30.0)
    response.raise_for_status()
    items = response.json()
    return sorted(item["name"] for item in items if item["name"].endswith(".md"))


def download_docs(cache_dir: str | None = None) -> Path:
    target = Path(cache_dir or HH_DOCS_CACHE_DIR)
    target.mkdir(parents=True, exist_ok=True)

    repo = HH_DOCS_REPO_URL.rstrip("/").replace("https://github.com/", "")
    for file_name in list_doc_files():
        raw_url = (
            f"https://raw.githubusercontent.com/{repo}/{HH_DOCS_BRANCH}/"
            f"{HH_DOCS_PATH}/{file_name}"
        )
        content = httpx.get(raw_url, timeout=30.0).text
        (target / file_name).write_text(content, encoding="utf-8")

    return target
