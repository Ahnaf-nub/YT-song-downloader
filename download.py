import os
import subprocess

def download_ffmpeg():
    # Create a bin directory if it doesn't exist
    os.makedirs("bin", exist_ok=True)

    # URL for FFmpeg static build
    ffmpeg_url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"

    # Download the FFmpeg binary
    subprocess.run(["curl", "-L", ffmpeg_url, "-o", "ffmpeg.tar.xz"], check=True)
    subprocess.run(["tar", "-xJf", "ffmpeg.tar.xz", "--strip-components=1", "-C", "bin"], check=True)
    os.remove("ffmpeg.tar.xz")

if __name__ == "__main__":
    download_ffmpeg()
