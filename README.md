# WGU Reddit Explorer (Datasette Lite)

This repository hosts a lightweight SQLite database of WGU-related Reddit posts.  
It is a **trial project** to explore using [Datasette Lite](https://github.com/simonw/datasette-lite) for quick, browser-based data exploration.

## About the data
- Posts are collected from **51 WGU-related subreddits**  
- This database contains the **10,000 most recent posts** (unfiltered)  
- Updated **daily**  

## Live viewer — 10k most recent posts

👉 [Open the WGU Reddit Explorer landing page](https://wguDataNinja.github.io/datasette_lite_reddit_explorer/)

This page lets you:
- Run keyword searches across titles and post bodies  
- Jump into canned queries (recent posts, last 7 days, example searches)  
- Explore the full Datasette Lite interface if you prefer  

## Files in this repo
- `data/wgu_reddit_10k.db` – SQLite database with ~10k recent posts  
- `metadata.json` – Datasette Lite configuration (canned queries, defaults)  
- `index.html` – Custom landing page with search + links  
- `README.md` – You are here  
- `LICENSE` – Project license