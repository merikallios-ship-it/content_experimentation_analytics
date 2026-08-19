from googleapiclient.discovery import build
from config import API_KEY

youtube = build("youtube", "v3", developerKey=API_KEY)

request = youtube.channels().list(
    part="snippet,statistics",
    forHandle="@mkbhd"
)
response = request.execute()

channel = response["items"][0]
print(channel["snippet"]["title"])
print(channel["statistics"]["subscriberCount"])