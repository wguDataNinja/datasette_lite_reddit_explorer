Here’s a concise blurb you can share:

⸻

This stage of the pipeline pulls posts from the SQLite DB, enriches them with subreddit names, 
cleans and normalizes text, calculates a VADER sentiment score, and applies filters — 
including the course code filter — to keep only relevant posts. 
The output is a clean JSONL file with consistent fields for downstream processing, 
including post_id, subreddit, title, selftext, permalink, created_utc, score, text_length,
vader_compound, and course_code.
