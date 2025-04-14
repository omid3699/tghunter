import asyncio

from bot.config import DOWNLOAD_DIR


async def download_with_aria2(url: str) -> bool:
    """Use Aria2 to download the file from the URL asynchronously."""
    download_dir = DOWNLOAD_DIR / "downloads"
    download_dir.mkdir(parents=True, exist_ok=True)

    command = [
        "aria2c",
        "--dir=" + str(download_dir),
        "--max-connection-per-server=16",
        "--split=16",
        "--continue=true",
        "--max-download-limit=0",
        url,
    ]

    try:
        process = await asyncio.create_subprocess_exec(
            *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            print(f"[Aria2] Download complete for: {url}")
            return True
        else:
            print(f"[Aria2] Download failed for {url}:\n{stderr.decode()}")
            return False

    except Exception as e:
        print(f"[Aria2] Exception occurred during download: {e}")
        return False
