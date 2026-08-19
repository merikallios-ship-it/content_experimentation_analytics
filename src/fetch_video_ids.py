import json
from googleapiclient.discovery import build
from config import API_KEY
from pathlib import Path
SCRIPT_DIR = Path(__file__).parent
DATA_RAW_DIR = SCRIPT_DIR.parent / "data" / "raw"

youtube = build("youtube", "v3", developerKey=API_KEY)

channels = {
    "Cocomelon - Nursery Rhymes": "UUbCmjCuTUZos6Inko4u57UQ",
    "Ryan's World": "UUhGJGhZ9SOOHvBB0Y4DOO_w",
    "Baby Shark - Pinkfong Kids' Songs & Stories": "UUcdwLMPsaU2ezNSJU1nFoBQ",
    "Blippi - Educational Videos for Kids": "UU5PYHgAzJ1wLEidB58SK6Xw",
    "Alan Becker": "UUbKWv2x9t6u8yZoB3KcPtnw",
    "TomSka": "UUOYWgypDktXdb-HfZnSMK6A",
    "Netflix": "UUWOA1ZGywLbqmigxE4Qlvuw",
    "Warner Bros.": "UUjmJDM5pRKbUlVIzDYYWb6g",
}

TARGET_VIDEO_COUNT = 250

for channel_name, playlist_id in channels.items():
    video_ids = []
    next_page_token = None

    while len(video_ids) < TARGET_VIDEO_COUNT:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break
    batch_size = 50
    video_details = []
    start = 0

    while start < len(video_ids):
        batch = video_ids[start:start + batch_size]

        videos_request = youtube.videos().list(
            part="snippet,statistics",
            id=",".join(batch)
        )
        videos_response = videos_request.execute()

        for video in videos_response["items"]:
            video_details.append(video)

        start += batch_size

    safe_name = channel_name.lower().replace(" ", "_").replace("'", "").replace("-", "").replace("&", "and")
    filepath = DATA_RAW_DIR / f"{safe_name}.json"


    with open(filepath, "w") as f:
        json.dump(video_details, f, indent=2)

    print(f"Saved {len(video_details)} videos for {channel_name}")