# scripts/verify_db.py
import sqlite3
from pathlib import Path

DB_PATH = Path("../data/wgu_reddit_filtered.db")

def main():
    if not DB_PATH.exists():
        print(f"Database not found: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    print("\nTables:")
    c.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view') ORDER BY 1;")
    print([r[0] for r in c.fetchall()])

    print("\nSchema for filtered_posts:")
    for col in c.execute("PRAGMA table_info(filtered_posts)"):
        print(f"- {col[1]} ({col[2]})")

    print("\nIntegrity check:")
    print(c.execute("PRAGMA integrity_check").fetchone()[0])

    print("\nRow counts:")
    posts = c.execute("SELECT COUNT(*) FROM filtered_posts").fetchone()[0]
    fts   = c.execute("SELECT COUNT(*) FROM filtered_posts_fts").fetchone()[0]
    print({"filtered_posts": posts, "filtered_posts_fts": fts})

    print("\nSample rows:")
    for r in c.execute("SELECT post_id, course_code, datetime(created_utc,'unixepoch') AS created_at, substr(title,1,60) FROM filtered_posts LIMIT 5;"):
        print(r)

    print("\nSample FTS search:")
    q = "wgu"
    sql = """
      SELECT fp.post_id, fp.course_code, substr(fp.title,1,60)
      FROM filtered_posts_fts f
      JOIN filtered_posts fp ON fp.rowid = f.rowid
      WHERE filtered_posts_fts MATCH ?
      LIMIT 5
    """
    for r in c.execute(sql, (q,)):
        print(r)

    conn.close()

if __name__ == "__main__":
    main()