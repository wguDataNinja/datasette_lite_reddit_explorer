# /Users/buddy/Desktop/projects/datasette_lite_reddit_explorer/scripts/combine_scripts_to_doc.py
from pathlib import Path

# Project root
ROOT_DIR = Path("/Users/buddy/Desktop/projects/datasette_lite_reddit_explorer")

# Files to combine (relative to ROOT_DIR)
FILES = [
    "scripts/verify_db.py",
    "scripts/prepare_db.sql",
    "scripts/prepare_db.py",
    "scripts/build_db.py",
]

OUTPUT_FILE = ROOT_DIR / "outputs" / "combined_pipeline_code.txt"

def write_section(header: str, file_list: list[str], out_f):
    out_f.write(f"# --- {header} ---\n\n")
    for relative_path in file_list:
        full_path = ROOT_DIR / relative_path
        out_f.write(f"# {relative_path}\n\n")
        if not full_path.exists():
            out_f.write(f"# [missing: {full_path}]\n\n")
            continue
        with open(full_path, "r", encoding="utf-8") as in_f:
            out_f.write(in_f.read())
        out_f.write("\n\n")

def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
        write_section("DATASATTE LITE REDDIT EXPLORER", FILES, out_f)
    print(f"Wrote {OUTPUT_FILE}")

if __name__ == "__main__":
    main()