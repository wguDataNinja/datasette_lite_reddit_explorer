# scripts/prepare_db.py
import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DB   = BASE / "data" / "wgu_reddit_filtered.db"
SQL  = BASE / "scripts" / "prepare_db.sql"

def _table_sql(con, name):
    row = con.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (name,)).fetchone()
    return row[0] if row else ""

def _columns(con, name):
    return [r[1] for r in con.execute(f"PRAGMA table_info({name})")]

def _needs_migration(con) -> bool:
    sql = _table_sql(con, "filtered_posts").upper()
    cols = set(_columns(con, "filtered_posts"))
    if not sql:
        return False
    # migrate if WITHOUT ROWID, or missing post_id, or has legacy id PK
    return ("WITHOUT ROWID" in sql) or ("POST_ID" not in cols) or ("ID" in cols)

def _auto_migrate(con):
    if not _needs_migration(con):
        return
    con.execute("PRAGMA foreign_keys=OFF")
    con.execute("BEGIN")
    try:
        con.execute("""
          CREATE TABLE filtered_posts_new (
            post_id   TEXT UNIQUE NOT NULL,
            subreddit TEXT NOT NULL,
            course_code TEXT NOT NULL,
            sentiment REAL,
            created_utc INTEGER NOT NULL,
            title TEXT,
            selftext TEXT,
            text_clean TEXT,
            text_length INTEGER,
            score INTEGER,
            permalink TEXT
          ); -- WITH rowid
        """)
        src_cols = set(_columns(con, "filtered_posts"))
        # map old column names if present
        id_expr = "post_id" if "post_id" in src_cols else ("id" if "id" in src_cols else "NULL")
        course_expr = "course_code" if "course_code" in src_cols else "NULL"
        select_sql = f"""
          SELECT
            {id_expr} AS post_id,
            subreddit,
            {course_expr} AS course_code,
            sentiment,
            created_utc,
            title,
            selftext,
            text_clean,
            text_length,
            score,
            permalink
          FROM filtered_posts
        """
        con.execute(f"""
          INSERT INTO filtered_posts_new
          (post_id, subreddit, course_code, sentiment, created_utc, title, selftext, text_clean, text_length, score, permalink)
          {select_sql}
        """)
        con.execute("DROP TABLE filtered_posts;")
        con.execute("ALTER TABLE filtered_posts_new RENAME TO filtered_posts;")
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK")
        raise
    finally:
        con.execute("PRAGMA foreign_keys=ON")

def main():
    if not DB.exists():
        raise FileNotFoundError(DB)
    if not SQL.exists():
        raise FileNotFoundError(SQL)

    with sqlite3.connect(DB) as con:
        _auto_migrate(con)

        with open(SQL, "r", encoding="utf-8") as f:
            con.executescript(f.read())

        con.execute("PRAGMA wal_checkpoint(FULL)")
        con.execute("VACUUM")

        posts = con.execute("SELECT COUNT(*) FROM filtered_posts").fetchone()[0]
        fts   = con.execute("SELECT COUNT(*) FROM filtered_posts_fts").fetchone()[0]
        fk    = con.execute("PRAGMA foreign_keys").fetchone()[0]
        wal   = con.execute("PRAGMA journal_mode").fetchone()[0]
        sync  = con.execute("PRAGMA synchronous").fetchone()[0]
        print(f"{DB.name}: prepared")
        print(f"  rows: filtered_posts={posts}, filtered_posts_fts={fts}")
        print(f"  pragmas: foreign_keys={fk}, journal_mode={wal}, synchronous={sync}")

if __name__ == "__main__":
    main()