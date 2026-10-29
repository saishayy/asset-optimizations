"""
Audio Optimizer — MP3 to AAC/M4A Compressor
==============================================
Converts MP3 audio to AAC (.m4a) using ffmpeg.
AAC at 96 kbps is perceptually transparent for voice + ambient music content
and produces files ~30–40% smaller than MP3 at 128 kbps.

Both iOS and Android support AAC natively; Flutter's audioplayers package
plays .m4a files on all platforms without extra configuration.

Requirements:
    ffmpeg (must be on PATH)
        macOS:   brew install ffmpeg
        Windows: https://ffmpeg.org/download.html

Usage:
    python3 compress_audio.py                     # convert ./assets/audio/ (relative to CWD)
    python3 compress_audio.py path/to/dir         # custom directory
    python3 compress_audio.py --bitrate 128       # set bitrate kbps (default 96)
    python3 compress_audio.py --format opus       # use Opus instead of AAC
    python3 compress_audio.py --keep              # keep original MP3s after conversion
    python3 compress_audio.py --dry-run           # preview without writing files
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_DIR = "assets/audio"

FORMAT_CONFIG = {
    "aac": {
        "extension": ".m4a",
        "codec": "aac",
        "default_bitrate": 96,
        "container": "ipod",  # ffmpeg muxer for .m4a
        "label": "AAC/M4A",
    },
    "opus": {
        "extension": ".opus",
        "codec": "libopus",
        "default_bitrate": 64,
        "container": "ogg",
        "label": "Opus/OGG",
    },
}


def check_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        sys.exit(
            "ffmpeg not found on PATH.\n"
            "  macOS:   brew install ffmpeg\n"
            "  Windows: https://ffmpeg.org/download.html"
        )


def convert(
    mp3_path: Path,
    fmt: dict,
    bitrate: int,
    replace: bool,
    dry_run: bool,
) -> tuple[int, int]:
    """Convert one MP3 to the target format. Returns (original_bytes, output_bytes)."""
    out_path = mp3_path.with_suffix(fmt["extension"])
    original_bytes = mp3_path.stat().st_size

    if dry_run:
        print(f"  [dry-run] {mp3_path.name} → {out_path.name}")
        return original_bytes, 0

    cmd = [
        "ffmpeg",
        "-y",                        # overwrite without prompt
        "-i", str(mp3_path),
        "-c:a", fmt["codec"],
        "-b:a", f"{bitrate}k",
        "-f", fmt["container"],
        "-vn",                       # strip any embedded artwork
        str(out_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR converting {mp3_path.name}:\n{result.stderr.strip()}", file=sys.stderr)
        return original_bytes, 0

    out_bytes = out_path.stat().st_size
    saving_pct = (1 - out_bytes / original_bytes) * 100 if original_bytes else 0

    print(
        f"  {mp3_path.name} → {out_path.name} "
        f"({_fmt(original_bytes)} → {_fmt(out_bytes)}, -{saving_pct:.0f}%)"
    )

    if replace:
        mp3_path.unlink()
        print(f"    deleted {mp3_path.name}")

    return original_bytes, out_bytes


def _fmt(n: int) -> str:
    if n >= 1_048_576:
        return f"{n / 1_048_576:.1f} MB"
    return f"{n / 1024:.1f} KB"


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert MP3 audio to AAC/M4A or Opus.")
    parser.add_argument(
        "directory",
        nargs="?",
        default=DEFAULT_DIR,
        help=f"Directory to scan, relative to the current working directory (default: {DEFAULT_DIR})",
    )
    parser.add_argument(
        "--bitrate",
        type=int,
        metavar="N",
        help="Output bitrate in kbps (default: 96 for AAC, 64 for Opus)",
    )
    parser.add_argument(
        "--format",
        choices=["aac", "opus"],
        default="aac",
        help="Output format: aac (.m4a) or opus (.opus) — default: aac",
    )
    parser.add_argument(
        "--keep",
        action="store_true",
        help="Keep original MP3 files after conversion (deleted by default)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List files that would be converted without writing anything",
    )
    args = parser.parse_args()

    check_ffmpeg()

    fmt = FORMAT_CONFIG[args.format]
    bitrate = args.bitrate if args.bitrate is not None else fmt["default_bitrate"]
    replace = not args.keep

    if not 8 <= bitrate <= 320:
        parser.error("--bitrate must be between 8 and 320")

    target_dir = Path(args.directory)
    if not target_dir.exists():
        sys.exit(f"Directory not found: {target_dir}")

    mp3s = sorted(target_dir.rglob("*.mp3"))
    if not mp3s:
        print(f"No MP3 files found in {target_dir}")
        return

    print(f"\nConverting {len(mp3s)} MP3 file(s) in {target_dir}")
    print(
        f"Format: {fmt['label']}  |  Bitrate: {bitrate} kbps  |  "
        f"Delete originals: {replace}  |  Dry-run: {args.dry_run}\n"
    )

    total_original = 0
    total_out = 0
    errors = 0

    for mp3 in mp3s:
        orig, out = convert(mp3, fmt, bitrate, replace, args.dry_run)
        total_original += orig
        if out:
            total_out += out
        elif not args.dry_run:
            errors += 1

    if args.dry_run:
        print(f"\n[dry-run] {len(mp3s)} file(s) would be converted. Run without --dry-run to apply.")
        return

    converted = len(mp3s) - errors
    if total_original and total_out:
        saving_pct = (1 - total_out / total_original) * 100
        print(
            f"\n✓ {converted}/{len(mp3s)} file(s) converted. "
            f"Total: {_fmt(total_original)} → {_fmt(total_out)} (-{saving_pct:.0f}% saved)"
        )
    if errors:
        print(f"  {errors} file(s) failed — check stderr above.")


if __name__ == "__main__":
    main()
