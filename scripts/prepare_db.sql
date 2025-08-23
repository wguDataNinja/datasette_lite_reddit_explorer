PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;

-- lean indexes
CREATE INDEX IF NOT EXISTS idx_posts_course ON filtered_posts(course_code);

-- external-content FTS5: tiny and rebuildable
DROP TABLE IF EXISTS filtered_posts_fts;
CREATE VIRTUAL TABLE filtered_posts_fts USING fts5(
  title,
  selftext,
  content='filtered_posts',
  content_rowid='rowid',
  detail=none
);

-- build from content table
INSERT INTO filtered_posts_fts(filtered_posts_fts) VALUES('rebuild');

-- sync triggers
DROP TRIGGER IF EXISTS filtered_posts_ai;
DROP TRIGGER IF EXISTS filtered_posts_ad;
DROP TRIGGER IF EXISTS filtered_posts_au;

CREATE TRIGGER filtered_posts_ai AFTER INSERT ON filtered_posts BEGIN
  INSERT INTO filtered_posts_fts(rowid, title, selftext)
  VALUES (new.rowid, COALESCE(new.title,''), COALESCE(new.selftext,''));
END;

CREATE TRIGGER filtered_posts_ad AFTER DELETE ON filtered_posts BEGIN
  INSERT INTO filtered_posts_fts(filtered_posts_fts, rowid) VALUES ('delete', old.rowid);
END;

CREATE TRIGGER filtered_posts_au AFTER UPDATE ON filtered_posts BEGIN
  INSERT INTO filtered_posts_fts(filtered_posts_fts, rowid) VALUES ('delete', old.rowid);
  INSERT INTO filtered_posts_fts(rowid, title, selftext)
  VALUES (new.rowid, COALESCE(new.title,''), COALESCE(new.selftext,''));
END;

-- compact browse view (keep small)
DROP VIEW IF EXISTS filtered_posts_view;
CREATE VIEW filtered_posts_view AS
SELECT
  post_id,
  course_code,
  sentiment,
  datetime(created_utc,'unixepoch') AS created_at,
  title,
  selftext,
  -- full URL
  CASE
    WHEN permalink LIKE 'http%' THEN permalink
    ELSE 'https://www.reddit.com' || permalink
  END AS permalink_url,
  -- clickable HTML (will render via plugin below)
  '<a href="' ||
  CASE
    WHEN permalink LIKE 'http%' THEN permalink
    ELSE 'https://www.reddit.com' || permalink
  END ||
  '" target="_blank" rel="noopener">open</a>' AS permalink_html
FROM filtered_posts;

PRAGMA optimize;