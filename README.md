# YT-DLP EasyMode

A tiny helper project whose only purpose is to make using `yt-dlp` easier.  I made this because when I want to use a YouTube video in one of my own video projects,
such as a free Green Screen video, I'm too lazy to manually put together the full yt-dlp command.  Lol.

## What this does

- You run `python dl-link.py`
- You paste a single YouTube video URL when prompted
- The script downloads the video automatically into the `output/` folder

That is the entire workflow. No need to write a full `yt-dlp` command yourself.

## How to use

1. Open a terminal in this folder.
2. Run:
   ```powershell
   py dl-link.py
   ```
3. When prompted, paste the YouTube video link.
4. Wait for the download to finish.

## Notes

- Download the latest `yt-dlp` binary from the official releases page:
  https://github.com/yt-dlp/yt-dlp/releases
- On Windows, place `yt-dlp.exe` in the same folder as `dl-link.py`.
- On Linux/macOS, place the corresponding `yt-dlp` binary for your OS in the same folder or install `yt-dlp` system-wide.
- Downloads are saved into the `output/` directory.
- The script converts the downloaded video to MP4 format.
