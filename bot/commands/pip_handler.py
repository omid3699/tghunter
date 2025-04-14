import asyncio
import shutil

from bot.config import DOWNLOAD_DIR
from bot.logger import logger

PIP_DIR = DOWNLOAD_DIR / "pip"
PIP_DIR.mkdir(parents=True, exist_ok=True)


async def handle_pip(event):
    args = event.raw_text.strip().split(maxsplit=1)

    if len(args) != 2:
        await event.reply(
            "⚠️ Usage: `/pip <package>`\nExample: `/pip django[redis]==4.2`",
            parse_mode="markdown",
        )
        return

    package = args[1].strip()

    # Normalize folder name
    safe_folder = (
        package.replace("[", "_")
        .replace("]", "")
        .replace("==", "_")
        .replace(">", "_")
        .replace("<", "_")
    )
    pkg_dir = PIP_DIR / safe_folder
    if pkg_dir.exists():
        shutil.rmtree(pkg_dir)
    pkg_dir.mkdir(parents=True)

    await event.reply(f"📦 Downloading `{package}`...", parse_mode="markdown")
    logger.info(f"[pip] Downloading package: {package} into {pkg_dir}")

    try:
        proc = await asyncio.create_subprocess_exec(
            "pip",
            "download",
            package,
            "-d",
            str(pkg_dir),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        out, err = stdout.decode(), stderr.decode()
        if proc.returncode != 0:
            logger.error(f"[pip] pip download failed for `{package}`:\n{err}")
            await event.reply(
                f"❌ pip download failed:\n`{err.strip()}`", parse_mode="markdown"
            )
            return

        files = list(pkg_dir.glob("*"))
        if not files:
            await event.reply(
                "⚠️ No files were downloaded. Check if the package name is correct.",
                parse_mode="markdown",
            )
            return

        await event.reply(
            f"✅ Downloaded `{len(files)}` files for `{package}` in `pip/{safe_folder}`",
            parse_mode="markdown",
        )
        logger.success(f"[pip] Download complete for {package}: {len(files)} files")

    except Exception as e:
        logger.exception(f"[pip] Exception while downloading `{package}`")
        await event.reply(f"❌ Error: `{str(e)}`", parse_mode="markdown")
