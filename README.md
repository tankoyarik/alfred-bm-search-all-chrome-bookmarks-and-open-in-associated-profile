# Chrome Bookmarks Search — Alfred Workflow

![Alfred](https://img.shields.io/badge/Alfred-Workflow-blueviolet)

## The Problem

Alfred's built-in bookmark search (`bm`) only looks within a single Chrome profile. Worse, when you select a bookmark, it opens in whichever Chrome window happens to be in front — not the profile the bookmark belongs to. So if you're searching for a work bookmark but your personal Chrome window is active, it opens there instead. There's no profile awareness at all.

If you use multiple Chrome profiles (work, personal, client projects, etc.), this makes the default bookmark search nearly useless.

## The Solution

This workflow fixes both issues:

1. **Searches across all Chrome profiles** — every bookmark from every profile appears in one unified list, labeled with its profile name and icon
2. **Opens in the correct profile** — selecting a bookmark launches it in the Chrome profile it belongs to, every time
3. **Learns your habits** — frequently opened bookmarks float to the top using exponential decay, so your most-used results are always first

## Installation

1. Download the latest `Chrome.Bookmarks.alfredworkflow` from [Releases](../../releases)
2. Double-click the file — Alfred imports it automatically

## Usage

| Action | Description |
|--------|-------------|
| `bm <query>` | Search bookmarks by name |
| `Enter` | Open bookmark in its Chrome profile |
| `⌘` (hold) | Preview the full URL |

Results are sorted by usage frequency — the more you open a bookmark, the higher it ranks. Stale entries fade out automatically over time.

## How It Works

The workflow reads `~/Library/Application Support/Google/Chrome/Local State` to discover profiles, then scans each profile's `Bookmarks` JSON file. Results are returned as Alfred JSON with profile-specific icons. The selected bookmark is opened via:

```bash
open -na "Google Chrome" --args --profile-directory="<profile>" "<url>"
```

Usage tracking is stored in `~/Library/Application Support/Alfred/Workflow Data/com.custom.chrome-bookmarks-search/usage.json`. Counts use exponential decay (factor 0.95) so they stay bounded and stale entries self-prune.

## Requirements

- macOS
- Google Chrome with one or more profiles
- Alfred 5 with Powerpack
- Python 3 (ships with macOS)

## Files

| File | Purpose |
|------|---------|
| `bookmarks.py` | Script Filter — reads bookmarks and usage data, outputs Alfred JSON |
| `open_bookmark.py` | Run Script — tracks usage and opens URL in the correct profile |
| `info.plist` | Alfred workflow definition |

## License

MIT
