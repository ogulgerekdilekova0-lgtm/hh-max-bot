import hashlib
import json
from pathlib import Path

from yandex_ai_studio_sdk import AIStudio
from yandex_ai_studio_sdk.search_indexes import StaticIndexChunkingStrategy, TextSearchIndexType

from app.config import (
    HH_DOCS_CACHE_DIR,
    INDEX_STATE_PATH,
    YANDEX_API_KEY,
    YANDEX_FOLDER_ID,
    YANDEX_INDEX_LABEL,
)

_sdk: AIStudio | None = None


def _get_sdk() -> AIStudio:
    global _sdk
    if _sdk is None:
        _sdk = AIStudio(folder_id=YANDEX_FOLDER_ID, auth=YANDEX_API_KEY)
    return _sdk


def _file_hashes(docs_path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(docs_path.glob("*.md")):
        digest = hashlib.md5(path.read_bytes()).hexdigest()
        result[path.name] = digest
    return result


def _load_state() -> dict:
    state_path = Path(INDEX_STATE_PATH)
    if not state_path.exists():
        return {}
    return json.loads(state_path.read_text(encoding="utf-8"))


def _save_state(state: dict) -> None:
    state_path = Path(INDEX_STATE_PATH)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _find_index(sdk: AIStudio):
    for index in sdk.search_indexes.list():
        labels = index.labels or {}
        if labels.get("project") == YANDEX_INDEX_LABEL:
            return index
    return None


def _delete_index(index) -> None:
    try:
        index.delete()
    except Exception:
        pass


def sync_search_index(docs_dir: str) -> str:
    docs_path = Path(docs_dir)
    if not docs_path.exists() or not any(docs_path.glob("*.md")):
        return "empty"

    if not YANDEX_FOLDER_ID or not YANDEX_API_KEY:
        return "no yandex creds"

    current_hashes = _file_hashes(docs_path)
    state = _load_state()
    if state.get("file_hashes") == current_hashes and state.get("search_index_id"):
        return "ok"

    sdk = _get_sdk()
    old_index = _find_index(sdk)
    if old_index:
        _delete_index(old_index)

    uploaded = []
    for path in sorted(docs_path.glob("*.md")):
        uploaded.append(
            sdk.files.upload(
                path,
                ttl_days=30,
                expiration_policy="static",
            )
        )

    operation = sdk.search_indexes.create_deferred(
        uploaded,
        name=YANDEX_INDEX_LABEL,
        labels={"project": YANDEX_INDEX_LABEL},
        index_type=TextSearchIndexType(
            chunking_strategy=StaticIndexChunkingStrategy(
                max_chunk_size_tokens=700,
                chunk_overlap_tokens=200,
            )
        ),
    )
    search_index = operation.wait(timeout=600)

    _save_state(
        {
            "search_index_id": search_index.id,
            "file_hashes": current_hashes,
        }
    )
    return "updated"
