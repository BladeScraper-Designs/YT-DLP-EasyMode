import os
import platform
import shutil
import subprocess
import sys
from urllib.parse import urlparse


def find_yt_dlp_executable():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    system = platform.system()
    if system == "Windows":
        local_names = ["yt-dlp.exe", "yt-dlp"]
        path_name = "yt-dlp.exe"
    else:
        local_names = ["yt-dlp", "yt-dlp-linux", "yt-dlp-macos"]
        path_name = "yt-dlp"

    for name in local_names:
        candidate = os.path.join(script_dir, name)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate

    path_candidate = shutil.which(path_name)
    if path_candidate:
        return path_candidate

    return None


def prompt_for_link():
    print("Enter the YouTube video link:")
    link = input("> ").strip()
    while not link:
        print("No link was provided. Please enter a YouTube video link:")
        link = input("> ").strip()
    return link


def is_supported_youtube_url(url):
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if host in {"www.youtube.com", "youtube.com", "m.youtube.com", "youtu.be"}:
        return True
    return False


def download_video(link, yt_dlp_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    command = [
        yt_dlp_path,
        "--no-playlist",
        "--recode-video",
        "mp4",
        "--merge-output-format",
        "mp4",
        "--output",
        os.path.join(output_dir, "%(title)s.%(ext)s"),
        link,
    ]

    print(f"Starting download into: {output_dir}")
    print("Please wait...")
    completed = subprocess.run(command, cwd=script_dir, check=False)

    if completed.returncode == 0:
        print("Download completed successfully.")
    else:
        print(f"Download failed with exit code {completed.returncode}.")
        sys.exit(completed.returncode)


def main():
    yt_dlp_path = find_yt_dlp_executable()
    if not yt_dlp_path:
        print("yt-dlp was not found in the same folder as this script.")
        sys.exit(1)

    link = prompt_for_link()
    if not is_supported_youtube_url(link):
        print("Please enter a valid YouTube video link.")
        sys.exit(1)

    download_video(link, yt_dlp_path)


if __name__ == "__main__":
    main()
