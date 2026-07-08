import os
import platform
import shutil
import subprocess
import sys
from urllib.parse import parse_qs, urlparse

MAX_RETRIES = 2


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
    print("Enter the YouTube video or playlist link:")
    link = input("> ").strip()
    while not link:
        print("No link was provided. Please enter a YouTube video or playlist link:")
        link = input("> ").strip()
    return link


def is_supported_youtube_url(url):
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    return host in {"www.youtube.com", "youtube.com", "m.youtube.com", "youtu.be"}


def is_playlist_url(url):
    parsed = urlparse(url)
    if "/playlist" in parsed.path.lower():
        return True
    query = parse_qs(parsed.query)
    return "list" in query


def ensure_output_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def run_command(command, cwd):
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True)


def download_single_video(link, yt_dlp_path, output_dir):
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

    print(f"Downloading: {link}")
    result = run_command(command, cwd=os.path.dirname(os.path.abspath(__file__)))

    if result.returncode == 0:
        print("Download completed successfully.")
        return True

    print(f"Download failed with exit code {result.returncode}.")
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return False


def extract_playlist_video_ids(link, yt_dlp_path):
    command = [
        yt_dlp_path,
        "--flat-playlist",
        "--yes-playlist",
        "--get-id",
        link,
    ]
    result = run_command(command, cwd=os.path.dirname(os.path.abspath(__file__)))

    if result.returncode != 0:
        print("Failed to extract playlist entries.")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return []

    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def download_playlist(link, yt_dlp_path, output_dir):
    video_ids = extract_playlist_video_ids(link, yt_dlp_path)
    if not video_ids:
        print("No playlist entries were found.")
        return False

    print(f"Detected playlist with {len(video_ids)} videos.")
    failed_urls = []

    for video_id in video_ids:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        if not download_single_video(video_url, yt_dlp_path, output_dir):
            failed_urls.append(video_url)

    if failed_urls:
        print("Retrying failed playlist videos...")
        still_failed = []
        for video_url in failed_urls:
            success = False
            for attempt in range(1, MAX_RETRIES + 1):
                print(f"Retry {attempt}/{MAX_RETRIES} for: {video_url}")
                if download_single_video(video_url, yt_dlp_path, output_dir):
                    success = True
                    break
            if not success:
                still_failed.append(video_url)

        if still_failed:
            print("The following videos still failed after retries:")
            for url in still_failed:
                print(" -", url)
            return False

    return True


def main():
    yt_dlp_path = find_yt_dlp_executable()
    if not yt_dlp_path:
        print("yt-dlp was not found in the same folder as this script or on PATH.")
        sys.exit(1)

    link = prompt_for_link()
    if not is_supported_youtube_url(link):
        print("Please enter a valid YouTube video or playlist link.")
        sys.exit(1)

    output_dir = ensure_output_dir()
    if is_playlist_url(link):
        success = download_playlist(link, yt_dlp_path, output_dir)
    else:
        success = download_single_video(link, yt_dlp_path, output_dir)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
