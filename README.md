# TGHunter - Telegram Bot self hosted telegram bot for file downloading

TGHunter is an advanced self-hosted Telegram bot designed for downloading various types of files. It supports multiple download methods including media files, YouTube videos, website cloning, Git repository cloning, and Python package downloads.
Features

    Download Media: Supports downloading media forwarded to the bot (images, videos, etc.).

    YouTube Downloader: Download YouTube videos, audio, and playlists with format and quality selection.

    Website Cloning: Clone entire websites with httrack and save as a zip file.

    Git Repo Cloning: Clone public/private Git repositories and send them as zip files.

    Pip Package Download: Download Python packages (with support for versions and extras).

Requirements

    Python 3.9+

    Pip packages: telethon, yt-dlp, httrack, etc.

    Running on a Linux server (recommended).

    Podman (for containerization).

## Clone the repository

```
git clone https://github.com/omid3699/tghunter.git
```

cd tghunter

## Set up virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
```

## Install dependencies

```sh
pip install -r requirements.txt
```

## Create a .env file with your bot's token and authorized user ID

```
BOT_TOKEN=your_bot_token
AUTHORIZED_USER_ID=your_user_id
DOWNLOAD_DIR=./download
```

## Run the bot

```sh
python bot/main.py
```

Optional: Run the bot using Podman (for containerized setup):

```sh
podman-compose up
```

## Commands

    /clone <url>: Clone a website using httrack.

    /git <repo_url>: Clone a Git repository and zip it.

    /pip <package_name>: Download Python packages (supports versions and extras).

    /yt <video_url>: Download YouTube videos or audio.
