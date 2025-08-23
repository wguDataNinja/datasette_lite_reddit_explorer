Here’s the revised dev log entry.

—

Dev Log — Datasette Lite Explorer Setup
Date: 2025-08-22
Project: datasette_lite_reddit_explorer

Steps completed
	1.	Created empty GitHub repository: datasette_lite_reddit_explorer.
	2.	Initialized PyCharm project in ~/Desktop/projects/.
	3.	Initialized Git and set remote:
	•	git init
	•	git remote add origin https://github.com/wguDataNinja/datasette_lite_reddit_explorer.git
	•	git branch -M main
	4.	Added .gitignore (.venv, pycache, *.sqlite, *.db, .DS_Store).
	5.	Added data/filtered_posts.jsonl (local only; not for commit).
	6.	Wrote scripts/build_db.py and built data/wgu_reddit_filtered.db (table: filtered_posts).
	7.	Wrote scripts/prepare_db.sql and scripts/prepare_db.py; prepared DB:
	•	Indexes on course_code, created_utc, sentiment
	•	FTS5 index on title, selftext
	•	View filtered_posts_view
	•	Row count after prepare: 831
	8.	Added scripts/verify_db.py; confirmed schema and sample rows.
	9.	Ran local Datasette: http://127.0.0.1:8001 and verified browsing.

Issue noted
	•	Sentiment scores are inaccurate for posts containing code; VADER misreads code tokens and outputs overly negative values.

Decision
	•	Pause publishing and UI polish until sentiment handling is corrected.

Next actions
	•	Adjust sentiment pipeline before rebuild:
	•	Strip code blocks and inline code from text prior to VADER.
	•	Remove URLs and common code artifacts before scoring.
	•	Clamp near-neutral scores to a tighter band or set to null if text is code-heavy.
	•	Rebuild DB and re-prepare after sentiment fix.
	•	Then push DB and metadata for Datasette Lite demo.