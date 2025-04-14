import asyncio
import shutil
import tempfile
import uuid
from pathlib import Path

from bot.config import DOWNLOAD_DIR
from bot.logger import logger

REPO_DIR = DOWNLOAD_DIR / "repos"
REPO_DIR.mkdir(parents=True, exist_ok=True)


async def handle_git(event):
    args = event.raw_text.strip().split()

    if len(args) != 2:
        await event.reply("⚠️ Usage: `/git <repository_url>`", parse_mode="markdown")
        return

    repo_url = args[1]
    session_id = uuid.uuid4().hex[:8]
    temp_dir = Path(tempfile.mkdtemp(prefix="repo_", dir="/tmp"))
    clone_dir = temp_dir / "repo"

    await event.reply(f"🔄 Cloning repository...\n`{repo_url}`", parse_mode="markdown")
    logger.info(f"[{session_id}] Cloning {repo_url} to {clone_dir}")

    try:
        proc = await asyncio.create_subprocess_exec(
            "git",
            "clone",
            "--depth",
            "1",
            repo_url,
            str(clone_dir),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            logger.error(f"[{session_id}] Git clone failed: {stderr.decode().strip()}")
            await event.reply(
                f"❌ Git clone failed:\n`{stderr.decode().strip()}`",
                parse_mode="markdown",
            )
            return

        repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
        zip_path = REPO_DIR / f"{repo_name}.zip"
        shutil.make_archive(str(zip_path.with_suffix("")), "zip", clone_dir)
        logger.success(f"[{session_id}] Repo zipped to {zip_path.name}")

        await event.reply(
            f"✅ Repo cloned and zipped: `{zip_path.name}`", parse_mode="markdown"
        )

    except Exception as e:
        logger.exception(f"[{session_id}] Git handler error")
        await event.reply(f"❌ Error: `{str(e)}`", parse_mode="markdown")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
        logger.info(f"[{session_id}] Cleaned up temp dir {temp_dir}")
