#!/usr/bin/env python3
"""Combine existing Anki packages under ordered series/deck hierarchies.

Requires Anki's Python package (tested with Anki 23.12.1).
Run from repo root: python tools/merge_series_decks.py
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

from anki.collection import (
    Collection,
    ExportAnkiPackageOptions,
    ImportAnkiPackageOptions,
    ImportAnkiPackageRequest,
)
from anki.generic_pb2 import Empty
from anki.import_export_pb2 import ExportLimit


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def merge(output: str, items: list[tuple[str, str, str]]) -> None:
    """items are (source path relative to repo, source root, destination root)."""
    temp = tempfile.TemporaryDirectory(prefix="anki-series-")
    col = Collection(os.path.join(temp.name, "series.anki2"))
    before = 0
    try:
        for rel_path, source_root, destination_root in items:
            package = ROOT / rel_path
            if not package.is_file():
                raise FileNotFoundError(package)
            col.import_anki_package(
                ImportAnkiPackageRequest(
                    package_path=str(package),
                    options=ImportAnkiPackageOptions(
                        with_scheduling=True, with_deck_configs=True
                    ),
                )
            )
            did = col.decks.id(source_root, create=False)
            if not did:
                roots = [
                    d.name
                    for d in col.decks.all_names_and_ids()
                    if "::" not in d.name and d.name != "Default"
                ]
                raise RuntimeError(
                    f"Không tìm thấy deck gốc {source_root!r} sau khi nhập {package.name}; "
                    f"deck gốc hiện có: {roots}"
                )
            col.decks.rename(did, destination_root)
            now = col.note_count()
            added = now - before
            print(f"  {package.name}: +{added} notes -> {destination_root}")
            before = now

        out = DIST / output
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            out.unlink()
        col.export_anki_package(
            out_path=str(out),
            options=ExportAnkiPackageOptions(
                with_scheduling=True, with_deck_configs=True,
                with_media=True, legacy=False,
            ),
            limit=ExportLimit(whole_collection=Empty()),
        )
        print(f"BUILT {out} | {col.note_count()} notes | {col.card_count()} cards")
    finally:
        col.close()
        temp.cleanup()


def main() -> None:
    merge(
        "Grammar in Use.apkg",
        [
            ("dist/individual/Essential Grammar In Use (Elementary).apkg",
             "Essential Grammar In Use (Elementary)",
             "Grammar in Use::01 Essential Grammar In Use (Elementary)"),
            ("dist/individual/English Grammar In Use (Intermediate).apkg",
             "English Grammar In Use (Intermediate)",
             "Grammar in Use::02 English Grammar In Use (Intermediate)::01 Main Book"),
            ("dist/individual/English Grammar In Use Supplementary Exercises.apkg",
             "English Grammar In Use Supplementary Exercises",
             "Grammar in Use::02 English Grammar In Use (Intermediate)::02 Supplementary Exercises"),
            ("dist/individual/Advanced Grammar In Use.apkg",
             "Advanced Grammar In Use",
             "Grammar in Use::03 Advanced Grammar In Use"),
        ],
    )
    merge(
        "English Vocabulary In Use.apkg",
        [
            ("dist/individual/English Vocabulary In Use (Elementary).apkg",
             "English Vocabulary In Use (Elementary)",
             "English Vocabulary In Use::01 Elementary (A2)"),
            ("dist/individual/English Vocabulary In Use (Pre-Intermediate and Intermediate).apkg",
             "English Vocabulary In Use (Pre-Intermediate and Intermediate)",
             "English Vocabulary In Use::02 Pre-Intermediate and Intermediate (B1)"),
            ("dist/individual/English Vocabulary In Use (Upper-Intermediate).apkg",
             "English Vocabulary In Use (Upper-Intermediate)",
             "English Vocabulary In Use::03 Upper-Intermediate (B2)"),
            ("dist/individual/English Vocabulary In Use (Advanced).apkg",
             "English Vocabulary In Use (Advanced)",
             "English Vocabulary In Use::04 Advanced (C1-C2)"),
            ("English Vocabulary In Use (Academic).apkg",
             "English Vocabulary In Use (Academic)",
             "English Vocabulary In Use::05 Academic Vocabulary in Use (B2-C1, source deck)"),
        ],
    )


if __name__ == "__main__":
    main()
