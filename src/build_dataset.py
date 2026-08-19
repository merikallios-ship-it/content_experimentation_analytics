import json
import pandas as pd
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_RAW_DIR = SCRIPT_DIR.parent / "data" / "raw"
DATA_PROCESSED_DIR = SCRIPT_DIR.parent / "data" / "processed"

channel_names = [
    "Cocomelon - Nursery Rhymes",
    "Ryan's World",
    "Baby Shark - Pinkfong Kids' Songs & Stories",
    "Blippi - Educational Videos for Kids",
    "Alan Becker",
    "TomSka",
    "Netflix",
    "Warner Bros.",
]

all_rows = []

for channel_name in channel_names:
    safe_name = channel_name.lower().replace(" ", "_").replace("'", "").replace("-", "").replace("&", "and")
    filepath = DATA_RAW_DIR / f"{safe_name}.json"

    with open(filepath) as f:
        video_details = json.load(f)

    for video in video_details:
        all_rows.append({
            "channel_name": channel_name,
            "video_id": video["id"],
            "title": video["snippet"]["title"],
            "published_at": video["snippet"]["publishedAt"],
            "view_count": video["statistics"].get("viewCount"),
            "like_count": video["statistics"].get("likeCount"),
            "comment_count": video["statistics"].get("commentCount"),
        })

df = pd.DataFrame(all_rows)
print(df.shape)
print(df["channel_name"].value_counts())

df["view_count"] = pd.to_numeric(df["view_count"])
df["like_count"] = pd.to_numeric(df["like_count"])
df["comment_count"] = pd.to_numeric(df["comment_count"])

df.to_csv(DATA_PROCESSED_DIR / "video_data.csv", index=False)
print("Saved to data/processed/video_data.csv")
print(df.shape)

import sqlite3

conn = sqlite3.connect(DATA_PROCESSED_DIR / "analytics.db")

df.to_sql("videos", conn, index=False, if_exists="replace")

check = pd.read_sql("SELECT COUNT(*) AS total_rows FROM videos", conn)
print(check)

top_videos = pd.read_sql("""
    select 
        channel_name,
        title,
        view_count,
        RANK() over (partition by channel_name order by view_count desc) as view_rank 
        from videos
""", conn)

print(top_videos[top_videos["view_rank"] == 1])

top_warner = pd.read_sql("""
    select 
        title,
        view_count
    from videos
    where channel_name = 'Warner Bros.' 
    order by view_count desc """, conn)

print(top_warner)


conn.close()