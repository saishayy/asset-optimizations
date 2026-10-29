---
name: assets-optimizations
description: Compresses image and audio assets before they ship in an app or repo — converts PNG/JPG/JPEG to WebP and MP3 to AAC/M4A (or Opus) with no visible/audible quality loss. Use when the user asks to optimize, compress, or shrink app assets, reduce bundle size, convert images to WebP, or convert audio to M4A/AAC — in any project (Flutter, web, etc.), not tied to one specific app.
---

# Asset Optimization

Shrinks binary assets (images, audio) before they get committed or bundled into an app, using lossy-but-imperceptible conversions:

- **Images**: PNG/JPG/JPEG → WebP (typically 25–50% smaller, no visible quality loss)
- **Audio**: MP3 → AAC/M4A or Opus (typically 30–40% smaller than the source MP3)

Both scripts are generic — they take any directory as an argument and work in any project (Flutter, web, or otherwise). They are not tied to a specific app's folder layout.

## Prerequisites

- **Images**: `pip install Pillow`
- **Audio**: `ffmpeg` on PATH
  - macOS: `brew install ffmpeg`
  - Windows: https://ffmpeg.org/download.html

Check for these before running the scripts; if missing, tell the user how to install them (the scripts also fail with a clear message if a dependency is missing).

## Instructions

The scripts referenced below live in `scripts/` next to this file — resolve the path relative to this SKILL.md's own location (it may be installed under `~/.claude/skills/`, a project's `.claude/skills/`, or a Claude Code plugin directory).

### Step 1: Identify the target directory

Ask or infer which directory holds the assets to convert (e.g. `assets/images`, `assets/audio`, or a project-specific path). Both scripts default to `assets/images` and `assets/audio` **relative to the current working directory** if no directory is given — this only works if you run them from the project root, so pass an explicit path otherwise.

### Step 2: Dry-run first

Always do a `--dry-run` first to show the user what will be converted before writing/deleting anything:

```bash
python3 scripts/convert_images.py assets/images --dry-run
python3 scripts/compress_audio.py assets/audio --dry-run
```

### Step 3: Run the real conversion

**Images** (`scripts/convert_images.py`):

```bash
python3 scripts/convert_images.py                      # ./assets/images, quality 85, deletes originals
python3 scripts/convert_images.py path/to/dir          # custom directory
python3 scripts/convert_images.py --quality 90         # set WebP quality 1–100 (default 85)
python3 scripts/convert_images.py --keep               # keep original PNG/JPEGs after conversion
```

Matches `*.png`, `*.jpg`, and `*.jpeg` recursively under the target directory. Writes `.webp` files alongside the originals. **Deletes originals by default** — pass `--keep` to retain them.

**Audio** (`scripts/compress_audio.py`):

```bash
python3 scripts/compress_audio.py                      # ./assets/audio, AAC 96kbps, deletes originals
python3 scripts/compress_audio.py path/to/dir          # custom directory
python3 scripts/compress_audio.py --bitrate 128        # set bitrate in kbps (default 96 for AAC, 64 for Opus)
python3 scripts/compress_audio.py --format opus        # use Opus (.opus) instead of AAC (.m4a)
python3 scripts/compress_audio.py --keep               # keep original MP3s after conversion
```

Matches `*.mp3` recursively under the target directory. Writes `.m4a` (or `.opus`) files alongside the originals. **Deletes originals by default** — pass `--keep` to retain them. AAC/M4A plays natively on both iOS and Android (e.g. via Flutter's `audioplayers` package) with no extra configuration.

### Step 4: Report savings

Both scripts print a per-file and total before/after size summary — surface that summary to the user so they can see the space saved.

## Notes

- Both scripts always overwrite an existing output file of the same name (`ffmpeg -y` for audio; `Image.save` for images), so re-running is safe/idempotent.
- Originals are deleted by default after a successful conversion; use `--keep` whenever the user wants to review output before removing sources, or wants to keep both formats.
- `--dry-run` never writes or deletes anything — safe to run anytime to preview scope.
