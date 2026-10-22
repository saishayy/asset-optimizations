# asset-optimization

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)

Shrinks image and audio assets before they ship in an app — no visible/audible quality loss, no manual copy-pasting between projects.

- **Images**: PNG / JPG / JPEG → WebP (typically 25–50% smaller)
- **Audio**: MP3 → AAC/M4A or Opus (typically 30–40% smaller)

Works in any project — Flutter, web, or otherwise. Ships as a [Claude Code](https://claude.com/claude-code) skill/plugin, comes with instruction files for Cursor, Gemini CLI, GitHub Copilot, and Windsurf, and the scripts also run standalone with plain Python for any other agent or workflow.

## Contents

- [Install as a Claude Code plugin](#install-as-a-claude-code-plugin-recommended)
- [Install as a personal skill (manual)](#install-as-a-personal-skill-manual)
- [Other coding agents](#other-coding-agents)
- [Requirements](#requirements)
- [Usage](#use-the-scripts-directly-no-claude-code-required)
- [Options reference](#options-reference)
- [Example output](#example-output)
- [Repo structure](#repo-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Install as a Claude Code plugin (recommended)

```
/plugin marketplace add saishayy/asset-optimizationa
/plugin install asset-optimization@asset-optimization
```

Then just ask Claude to "optimize the images/audio in this project" — it will pick up the skill automatically.

## Install as a personal skill (manual)

Clone this repo and copy (or symlink) the skill folder into your Claude Code skills directory:

```bash
git clone https://github.com/saishayy/asset-optimizationa.git
cp -r asset-optimizationa/skills/asset-optimization ~/.claude/skills/
```

Note: the `SKILL.md` format above is a Claude Code-specific convention — other agents don't auto-discover it. See below.

## Other coding agents

`SKILL.md` and the plugin manifest are Claude Code-specific, but the two scripts are plain Python CLI tools with no framework coupling — any agent that can run shell commands can invoke them directly. This repo also includes ready-made instruction files so several agents auto-discover the scripts the way Claude Code does:

| Agent            | File                                  |
| ----------------- | -------------------------------------- |
| Claude Code        | `skills/asset-optimization/SKILL.md`   |
| Cursor              | `.cursor/rules/asset-optimization.mdc` |
| Gemini CLI          | `GEMINI.md`                            |
| GitHub Copilot      | `.github/copilot-instructions.md`      |
| Windsurf            | `.windsurfrules`                       |
| Codex CLI / others  | `AGENTS.md`                            |

`AGENTS.md` follows the emerging [agents.md](https://agents.md) cross-tool convention and is also picked up as a fallback by several other agents beyond Codex.

These files only get auto-discovered by an agent working **in this repo** (or wherever you copy them). If you want a different agent to auto-discover the scripts inside *another* project, copy the matching instruction file — and the `skills/asset-optimization/scripts/` folder — into that project's root. Otherwise, just tell your agent to run the scripts directly (see [Usage](#use-the-scripts-directly-no-claude-code-required) below); every agent with shell access can do that regardless of which convention it reads.

## Requirements

| Task              | Requirement       | Install                                                        |
| ------------------ | ------------------ | ---------------------------------------------------------------- |
| Image conversion   | Python 3.9+, Pillow | `pip install Pillow`                                            |
| Audio conversion   | Python 3.9+, ffmpeg | macOS: `brew install ffmpeg` · Windows: [ffmpeg.org/download](https://ffmpeg.org/download.html) |

Both scripts check for their dependency on startup and exit with a clear message if it's missing — no silent failures.

## Use the scripts directly (no Claude Code required)

**Images:**

```bash
python3 skills/asset-optimization/scripts/convert_images.py                # ./assets/images, quality 85
python3 skills/asset-optimization/scripts/convert_images.py path/to/dir    # custom directory
python3 skills/asset-optimization/scripts/convert_images.py --quality 90   # 1–100, default 85
python3 skills/asset-optimization/scripts/convert_images.py --keep         # keep original PNG/JPEGs
python3 skills/asset-optimization/scripts/convert_images.py --dry-run      # preview only
```

**Audio:**

```bash
python3 skills/asset-optimization/scripts/compress_audio.py                # ./assets/audio, AAC 96kbps
python3 skills/asset-optimization/scripts/compress_audio.py path/to/dir    # custom directory
python3 skills/asset-optimization/scripts/compress_audio.py --bitrate 128  # kbps
python3 skills/asset-optimization/scripts/compress_audio.py --format opus  # Opus (.opus) instead of AAC (.m4a)
python3 skills/asset-optimization/scripts/compress_audio.py --keep         # keep original MP3s
python3 skills/asset-optimization/scripts/compress_audio.py --dry-run      # preview only
```

Both scripts default to `assets/images` / `assets/audio` relative to wherever you run them from, recurse into subdirectories, delete originals after a successful conversion by default, and print a before/after size summary.

## Options reference

### `convert_images.py`

| Flag         | Default         | Description                                            |
| ------------ | ---------------- | -------------------------------------------------------- |
| `directory`  | `assets/images` | Positional. Directory to scan (recursive), relative to CWD. |
| `--quality N` | `85`             | WebP quality, 1–100.                                     |
| `--keep`     | off (originals deleted) | Keep original PNG/JPEG/JPG files after conversion.       |
| `--dry-run`  | off              | List what would be converted; writes nothing.            |

### `compress_audio.py`

| Flag           | Default        | Description                                                  |
| -------------- | --------------- | ---------------------------------------------------------------- |
| `directory`    | `assets/audio` | Positional. Directory to scan (recursive), relative to CWD.     |
| `--bitrate N`  | `96` (AAC) / `64` (Opus) | Output bitrate in kbps, 8–320.                        |
| `--format`     | `aac`          | `aac` (→ `.m4a`) or `opus` (→ `.opus`).                          |
| `--keep`       | off (originals deleted) | Keep original MP3 files after conversion.                |
| `--dry-run`    | off             | List what would be converted; writes nothing.                    |

Both output formats overwrite an existing file of the same name, so re-running either script is safe and idempotent.

## Example output

```text
$ python3 skills/asset-optimization/scripts/convert_images.py assets/images

Converting 2 image file(s) in assets/images
Quality: 85  |  Delete originals: True  |  Dry-run: False

  logo.png → logo.webp (245.3 KB → 128.7 KB, -48%)
  hero.jpg → hero.webp (1.2 MB → 640.1 KB, -46%)
    deleted logo.png
    deleted hero.jpg

✓ Done. Total: 1.4 MB → 768.8 KB (-45% saved)
```

```text
$ python3 skills/asset-optimization/scripts/compress_audio.py assets/audio --bitrate 128

Converting 1 MP3 file(s) in assets/audio
Format: AAC/M4A  |  Bitrate: 128 kbps  |  Delete originals: True  |  Dry-run: False

  theme.mp3 → theme.m4a (3.8 MB → 2.1 MB, -45%)
    deleted theme.mp3

✓ 1/1 file(s) converted. Total: 3.8 MB → 2.1 MB (-45% saved)
```

## Repo structure

```text
asset-optimizationa/
├── .claude-plugin/
│   ├── plugin.json                   # Claude Code plugin manifest
│   └── marketplace.json              # makes this repo installable via /plugin marketplace add
├── .cursor/
│   └── rules/
│       └── asset-optimization.mdc    # Cursor rule
├── .github/
│   └── copilot-instructions.md       # GitHub Copilot instructions
├── skills/
│   └── asset-optimization/
│       ├── SKILL.md                  # skill instructions Claude reads to use the scripts
│       └── scripts/
│           ├── convert_images.py
│           └── compress_audio.py
├── AGENTS.md                         # Codex CLI + generic agents.md convention
├── GEMINI.md                         # Gemini CLI
├── .windsurfrules                    # Windsurf
├── README.md
└── LICENSE
```

## Troubleshooting

- **`Missing dependency: pip install Pillow`** — install Pillow in the same Python environment you're invoking the script with (`pip install Pillow` or `pip3 install Pillow`).
- **`ffmpeg not found on PATH`** — install it (`brew install ffmpeg` on macOS) and open a new shell so `PATH` picks it up.
- **`Directory not found: ...`** — the positional directory argument is resolved relative to your current working directory, not the script's location. Pass an absolute path if you're unsure, or `cd` into the project root first.
- **Nothing gets converted** — the scripts only match `*.png`/`*.jpg`/`*.jpeg` (images) or `*.mp3` (audio); other extensions are ignored by design.
- **Want to keep both the original and the optimized file?** — pass `--keep`; originals are deleted by default.

## License

MIT — see [LICENSE](LICENSE).
