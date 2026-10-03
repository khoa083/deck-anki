"""Xuất lại bộ mẫu English Grammar In Use (Intermediate) đã bỏ chữ "Anki Support Vietnam"
(yêu cầu: bỏ chữ này khỏi TẤT CẢ các deck). Nội dung, GUID, lịch học giữ nguyên.
Dùng: python3 tools/clean_sample.py  ->  out/English Grammar In Use (Intermediate).apkg"""
import os, sys, tempfile
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KIT, "tools"))
BASE = os.path.join(KIT, "base", "English Grammar In Use (Intermediate).apkg")


def main():
    from anki.collection import Collection, ImportAnkiPackageRequest, ImportAnkiPackageOptions, ExportAnkiPackageOptions
    from anki.import_export_pb2 import ExportLimit
    from anki.generic_pb2 import Empty
    from nobrand import strip_brand, brand_left
    d = tempfile.mkdtemp(); col = Collection(os.path.join(d, "c.anki2"))
    col.import_anki_package(ImportAnkiPackageRequest(package_path=BASE,
                            options=ImportAnkiPackageOptions(with_scheduling=True, with_deck_configs=True)))
    col.decks.remove([nd.id for nd in col.decks.all_names_and_ids() if nd.name == "Default" and nd.id != 1])
    print("Bỏ chữ Anki Support Vietnam:", strip_brand(col), "| còn:", brand_left(col))
    out = os.path.join(KIT, "out", os.path.basename(BASE))
    if os.path.exists(out): os.remove(out)
    col.export_anki_package(out_path=out, limit=ExportLimit(whole_collection=Empty()),
                            options=ExportAnkiPackageOptions(with_scheduling=True, with_deck_configs=True, with_media=True, legacy=False))
    print("notes:", col.note_count(), "->", out)
    col.close()


if __name__ == "__main__":
    main()
