#!/usr/bin/env python3
"""Import and render-check the merged series packages in dist/."""
from __future__ import annotations

import collections
import os
import re
import tempfile
from pathlib import Path

from anki.collection import Collection, ImportAnkiPackageOptions, ImportAnkiPackageRequest

ROOT = Path(__file__).resolve().parents[1]


def verify(filename: str) -> None:
    path = ROOT / "dist" / filename
    temp = tempfile.TemporaryDirectory(prefix="anki-verify-series-")
    col = Collection(os.path.join(temp.name, "verify.anki2"))
    bad = 0
    guids = collections.Counter()
    missing_media: set[str] = set()
    try:
        col.import_anki_package(
            ImportAnkiPackageRequest(
                package_path=str(path),
                options=ImportAnkiPackageOptions(
                    with_scheduling=True, with_deck_configs=True
                ),
            )
        )
        for nid in col.find_notes(""):
            guids[col.get_note(nid).guid] += 1
        for cid in col.find_cards(""):
            card = col.get_card(cid)
            try:
                rendered = card.question() + card.answer()
                if "{{" in rendered or "Unknown field" in rendered or not re.sub(
                    r"<[^>]+>", " ", rendered
                ).strip():
                    bad += 1
            except Exception:
                bad += 1
        for nid in col.find_notes(""):
            note = col.get_note(nid)
            for value in note.fields:
                for name in col.media.files_in_str(note.mid, value):
                    if not col.media.have(name):
                        missing_media.add(name)
        duplicates = sum(n - 1 for n in guids.values() if n > 1)
        roots = sorted(
            {
                col.decks.name(col.get_card(cid).did).split("::")[0]
                for cid in col.find_cards("")
            }
        )
        print(
            f"{filename}: notes={col.note_count()} cards={col.card_count()} "
            f"bad_renders={bad} duplicate_GUIDs={duplicates} "
            f"missing_media={len(missing_media)} roots={roots}"
        )
        if bad or duplicates or missing_media:
            raise SystemExit(1)
    finally:
        col.close()
        temp.cleanup()


if __name__ == "__main__":
    verify("Grammar in Use.apkg")
    verify("English Vocabulary In Use.apkg")
    verify("Business Vocabulary In Use.apkg")
