"""Registre des audits de publication — archive avec SHA-256 et horodatage."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REGISTRY = Path("audit_registry.jsonl")


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def append_record(text: str, report_json: str) -> None:
    """
    Ajoute une entrée au registre (format JSON Lines).
    Chaque ligne contient : horodatage, hash du texte, hash du rapport, contenu complet.
    """
    try:
        report = json.loads(report_json)
    except (json.JSONDecodeError, TypeError):
        report = {"raw": str(report_json)}

    record = {
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "text_sha256": _hash(text),
        "report_sha256": _hash(report_json),
        "text_preview": text[:120],
        "report": report,
    }

    with REGISTRY.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_all() -> list:
    """Retourne toutes les entrées du registre."""
    if not REGISTRY.exists():
        return []
    with REGISTRY.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


if __name__ == "__main__":
    records = read_all()
    print(f"Registre : {REGISTRY}")
    print(f"Entrées  : {len(records)}")
    for i, r in enumerate(records, 1):
        print(f"  {i}. {r['audited_at']} | {r['text_preview']}")
