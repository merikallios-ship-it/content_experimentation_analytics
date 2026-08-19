from googleapiclient.discovery import build
from config import API_KEY

youtube = build("youtube", "v3", developerKey=API_KEY)

channel_handles = [
    "@CoComelon",
    "@RyansWorld",
    "@Pinkfong",
    "@Blippi",
    "@alanbecker",
    "@TomSka",
    "@Netflix",
    "@WarnerBros",
]

for handle in channel_handles:
    request = youtube.channels().list(
        part="snippet,statistics,contentDetails",
        forHandle=handle
    )
    response = request.execute()
    channel = response["items"][0]

    title = channel["snippet"]["title"]
    subscribers = channel["statistics"]["subscriberCount"]
    uploads_playlist_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]

    print(title, subscribers, uploads_playlist_id)