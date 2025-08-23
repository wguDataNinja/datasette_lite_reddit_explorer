# WGU Reddit Explorer (Datasette Lite)

This repository hosts a lightweight SQLite database of WGU-related Reddit posts. It is a **trial project** to explore using [Datasette Lite](https://github.com/simonw/datasette-lite) for quick, browser-based data exploration.

## About the data
- Posts are collected from **51 WGU-related subreddits**  
- Filtered for course codes based on the **2025_06 WGU course catalog**  
- The database is **updated daily**

## Live viewer
Open the database in Datasette Lite:  
[Explore the data](https://lite.datasette.io/?url=https://wguDataNinja.github.io/datasette_lite_reddit_explorer/data/wgu_reddit_filtered.db&metadata=https://wguDataNinja.github.io/datasette_lite_reddit_explorer/metadata.json&install=datasette-render-html#/wgu_reddit_filtered/filtered_posts_view)

- Use the `permalink_html` column to jump directly to Reddit posts  
- Supports text search across titles and post bodies

## Files in this repo
- `data/wgu_reddit_filtered.db` – SQLite database with posts  
- `metadata.json` – Datasette Lite configuration for rendering links  
- `README.md` – You are here 
- `LICENSE` – Project license