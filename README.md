# YT-DLP EasyMode

A tiny helper project whose only purpose is to make using `yt-dlp` easier.

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

- The bundled `yt-dlp.exe` must stay in the same folder as `dl-link.py`.
- Downloads are saved into the `output/` directory.
- The script always converts the downloaded video to MP4, instead of leaving it in the format yt-dlp would normally choose, making it easier to use in video editing software.

## Purpose

This project exists only to avoid manually constructing a `yt-dlp` command. It wraps the executable in a simple prompt-driven Python script so you can download a single YouTube video with minimal effort.
