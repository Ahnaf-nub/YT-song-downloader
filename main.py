from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch

from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def download_song(song_name, author, codec='mp3'):
    query = f"{song_name} {author}"
    videos_search = VideosSearch(query, limit=1)
    result = videos_search.result()

    if not result['result']:
        raise HTTPException(status_code=404, detail="Not found")

    video_url = result['result'][0]['link']

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': codec,
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        title = info_dict.get('title', None)
        file_path = f"{title}.{codec}"
    
    return file_path

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/download/", response_class=HTMLResponse)
async def download(request: Request):
    form = await request.form()
    song_name = form.get("song_name")
    author = form.get("author")
    codec = form.get("codec", "mp3")
    try:
        file_path = download_song(song_name, author, codec)
        return templates.TemplateResponse("result.html", {"request": request, "file_path": file_path})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1")


