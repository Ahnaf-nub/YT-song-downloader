from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch

def download_song(song_name, author):
    # Search for the song on YouTube
    query = f"{song_name} {author}"
    videos_search = VideosSearch(query, limit=1)
    result = videos_search.result()

    if not result['result']:
        print("No results found.")
        return

    video_url = result['result'][0]['link']

    # Download the audio
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    print(f"Downloaded: {result['result'][0]['title']}")

# Example usage
song_name = "Ghum"
author = "Odd Signature"
download_song(song_name, author)