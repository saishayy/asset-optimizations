"""
Image Optimizer — PNG/JPG to WebP Converter
=============================================
Converts PNG and JPEG images to WebP for smaller file sizes with no visible
quality loss. Originals are kept untouched by default. WebP files are written
alongside the source images.

Requirements:
    pip install Pillow

Usage:
    python3 convert_images.py                    # convert ./assets/images/ (relative to CWD)
    python3 convert_images.py path/to/dir        # custom directory
    python3 convert_images.py --quality 90       # set WebP quality (default 85)
    python3 convert_images.py --keep             # keep original files after conversion
    python3 convert_images.py --dry-run          # preview without writing files
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Missing dependency: pip install Pillow")


DEFAULT_QUALITY = 85
DEFAULT_DIR = "assets/images"
SOURCE_EXTENSIONS = ("*.png", "*.jpg", "*.jpeg")


def convert(image_path: Path, quality: int, replace: bool, dry_run: bool) -> tuple[int, int]:
    """Convert a single PNG/JPEG to WebP. Returns (original_bytes, webp_bytes)."""
    webp_path = image_path.with_suffix(".webp")
    original_bytes = image_path.stat().st_size

    if dry_run:
        print(f"  [dry-run] {image_path.name} → {webp_path.name}")
        return original_bytes, 0

    with Image.open(image_path) as img:
        img.save(webp_path, format="WEBP", quality=quality, method=6)

    webp_bytes = webp_path.stat().st_size
    saving_pct = (1 - webp_bytes / original_bytes) * 100 if original_bytes else 0

    print(
        f"  {image_path.name} → {webp_path.name} "
        f"({_fmt(original_bytes)} → {_fmt(webp_bytes)}, -{saving_pct:.0f}%)"
    )

    if replace:
        image_path.unlink()
        print(f"    deleted {image_path.name}")

    return original_bytes, webp_bytes


def _fmt(n: int) -> str:
    """Format byte count as KB."""
    return f"{n / 1024:.1f} KB"


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert PNG/JPEG images to WebP.")
    parser.add_argument(
        "directory",
        nargs="?",
        default=DEFAULT_DIR,
        help=f"Directory to scan, relative to the current working directory (default: {DEFAULT_DIR})",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=DEFAULT_QUALITY,
        metavar="N",
        help=f"WebP quality 1–100 (default: {DEFAULT_QUALITY})",
    )
    parser.add_argument(
        "--keep",
        action="store_true",
        help="Keep original PNG/JPEG files after conversion (deleted by default)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List files that would be converted without writing anything",
    )
    args = parser.parse_args()

    if not 1 <= args.quality <= 100:
        parser.error("--quality must be between 1 and 100")

    target_dir = Path(args.directory)
    if not target_dir.exists():
        sys.exit(f"Directory not found: {target_dir}")

    images = sorted(
        {p for pattern in SOURCE_EXTENSIONS for p in target_dir.rglob(pattern)}
    )
    if not images:
        print(f"No PNG/JPEG files found in {target_dir}")
        return

    replace = not args.keep

    print(f"\nConverting {len(images)} image file(s) in {target_dir}")
    print(f"Quality: {args.quality}  |  Delete originals: {replace}  |  Dry-run: {args.dry_run}\n")

    total_original = 0
    total_webp = 0

    for image in images:
        orig, webp = convert(image, args.quality, replace, args.dry_run)
        total_original += orig
        total_webp += webp

    if not args.dry_run and total_original:
        total_saving_pct = (1 - total_webp / total_original) * 100
        print(
            f"\n✓ Done. Total: {_fmt(total_original)} → {_fmt(total_webp)} "
            f"(-{total_saving_pct:.0f}% saved)"
        )
    elif args.dry_run:
        print(f"\n[dry-run] {len(images)} file(s) would be converted. Run without --dry-run to apply.")


if __name__ == "__main__":
    main()
