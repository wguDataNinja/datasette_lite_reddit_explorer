# scripts/build_db.py
import json, sqlite3, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
INPUT_FILE = DATA / "filtered_posts.jsonl"
OUTPUT_DB  = DATA / "wgu_reddit_filtered.db"

STRICT = True  # skip rows with missing/empty course_code

def _norm_str(x):
    return x.strip() if isinstance(x, str) else x

def _first_nonempty(iterable):
    if not iterable:
        return None
    for v in iterable:
        s = _norm_str(v)
        if isinstance(s, str) and s:
            return s
    return None

def _extract_course_code(p):
    # Try multiple fields; accept string or list
    candidates = []
    # singular
    if isinstance(p.get("course_code"), str):
        candidates.append(p.get("course_code"))
    # plural common variants
    for key in ("matched_course_codes", "course_codes", "courses"):
        val = p.get(key)
        if isinstance(val, list):
            candidates.extend(val)
        elif isinstance(val, str):
            candidates.append(val)
    return _first_nonempty(candidates)

def build():
    if not INPUT_FILE.exists():
        print(f"Input not found: {INPUT_FILE}", file=sys.stderr)
        sys.exit(1)

    OUTPUT_DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(OUTPUT_DB)
    cur = con.cursor()

    cur.executescript("""
        PRAGMA foreign_keys=ON;
        PRAGMA journal_mode=WAL;
        PRAGMA synchronous=NORMAL;

        DROP TABLE IF EXISTS filtered_posts;
        CREATE TABLE filtered_posts (
          -- implicit rowid is used by FTS
          post_id     TEXT UNIQUE NOT NULL,
          subreddit   TEXT NOT NULL,
          course_code TEXT {nullness},
          sentiment   REAL,
          created_utc INTEGER NOT NULL,
          title       TEXT,
          selftext    TEXT,
          text_clean  TEXT,
          text_length INTEGER,
          score       INTEGER,
          permalink   TEXT
        );
    """.format(nullness="NOT NULL" if STRICT else ""))

    rows = []
    total = 0
    skipped_no_course = 0
    sample_skips = []

    with INPUT_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            total += 1
            p = json.loads(line)

            course_code = _extract_course_code(p)
            if STRICT and not course_code:
                skipped_no_course += 1
                if len(sample_skips) < 5:
                    sample_skips.append({
                        "post_id": p.get("post_id"),
                        "keys_present": [k for k in ("course_code","matched_course_codes","course_codes","courses") if k in p],
                        "values": {k: p.get(k) for k in ("course_code","matched_course_codes","course_codes","courses")}
                    })
                continue

            rows.append((
                p["post_id"],
                _norm_str(p.get("subreddit") or "") or "unknown",
                course_code,
                p.get("vader_compound"),
                int(p["created_utc"]),
                p.get("title"),
                p.get("selftext"),
                p.get("text_clean"),
                p.get("text_length"),
                p.get("score"),
                p.get("permalink"),
            ))

    if rows:
        cur.executemany("""
          INSERT INTO filtered_posts
          (post_id, subreddit, course_code, sentiment, created_utc,
           title, selftext, text_clean, text_length, score, permalink)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, rows)

    cur.executescript("""
      CREATE INDEX IF NOT EXISTS idx_posts_course ON filtered_posts(course_code);
      -- CREATE INDEX IF NOT EXISTS idx_posts_created ON filtered_posts(created_utc DESC);
    """)

    con.commit()
    n = cur.execute("SELECT COUNT(*) FROM filtered_posts").fetchone()[0]
    print(f"Built {OUTPUT_DB.name} with {n} rows")
    print(f"Input rows: {total}")
    print(f"Skipped (missing/empty course_code): {skipped_no_course}")
    if sample_skips:
        print("Sample skipped rows (first 5):")
        for s in sample_skips:
            print(s)

    con.close()

if __name__ == "__main__":
    build()