import re
from pathlib import Path

from app.config import HH_DOCS_CACHE_DIR

CHUNK_SIZE = 900


def _split_text(text: str, source: str) -> list[dict[str, str]]:
    parts = re.split(r"\n{2,}", text.strip())
    chunks: list[dict[str, str]] = []
    buf = ""

    for part in parts:
        piece = part.strip()
        if not piece:
            continue
        if len(buf) + len(piece) + 2 <= CHUNK_SIZE:
            buf = f"{buf}\n\n{piece}".strip()
            continue
        if buf:
            chunks.append({"source": source, "text": buf})
        buf = piece

    if buf:
        chunks.append({"source": source, "text": buf})

    return chunks


def load_chunks(docs_dir: str | None = None) -> list[dict[str, str]]:
    root = Path(docs_dir or HH_DOCS_CACHE_DIR)
    if not root.exists():
        return []

    chunks: list[dict[str, str]] = []
    for path in sorted(root.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        chunks.extend(_split_text(text, path.name))
    return chunks


def _score_chunk(question: str, chunk: dict[str, str]) -> int:
    q_words = {w for w in re.findall(r"[a-zA-Zа-яА-Я0-9_]+", question.lower()) if len(w) > 2}
    if not q_words:
        return 0

    text = chunk["text"].lower()
    source = chunk["source"].lower()
    score = sum(2 for w in q_words if w in text)
    score += sum(3 for w in q_words if w in source)
    return score


def find_relevant_chunks(question: str, docs_dir: str | None = None, limit: int = 4) -> list[dict[str, str]]:
    chunks = load_chunks(docs_dir)
    ranked = sorted(chunks, key=lambda c: _score_chunk(question, c), reverse=True)
    return [c for c in ranked if _score_chunk(question, c) > 0][:limit]


def build_context(question: str, docs_dir: str | None = None) -> str:
    parts = find_relevant_chunks(question, docs_dir=docs_dir)
    if not parts:
        chunks = load_chunks(docs_dir)
        parts = chunks[:3]

    blocks = [f"[{item['source']}]\n{item['text']}" for item in parts]
    return "\n\n---\n\n".join(blocks)
