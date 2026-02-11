# Chrome Bookmarks Search — Alfred Workflow

Search all Chrome bookmarks across every profile and open them in the correct profile.

![Alfred](https://img.shields.io/badge/Alfred-Workflow-blueviolet)

## Features

- **Multi-profile support** — discovers all Chrome profiles automatically
- **Profile icons** — shows the Google profile picture for each bookmark (falls back to Chrome icon)
- **Profile-aware open** — bookmarks launch in the Chrome profile they belong to
- **Fast filtering** — searches bookmark names as you type

## Installation

1. Download the latest `Chrome.Bookmarks.alfredworkflow` from [Releases](../../releases)
2. Double-click the file — Alfred imports it automatically

## Usage

| Action | Description |
|--------|-------------|
| `bm <query>` | Search bookmarks by name |
| `Enter` | Open bookmark in its Chrome profile |
| `⌘` (hold) | Preview the full URL |

## How It Works

The workflow reads `~/Library/Application Support/Google/Chrome/Local State` to discover profiles, then scans each profile's `Bookmarks` JSON file. Results are returned as Alfred JSON with profile-specific icons. The selected bookmark is opened via:

```bash
open -na "Google Chrome" --args --profile-directory="<profile>" "<url>"
```

## Requirements

- macOS
- Google Chrome with one or more profiles
- Alfred 5 with Powerpack
- Python 3 (ships with macOS)

## Files

| File | Purpose |
|------|---------|
| `bookmarks.py` | Script Filter — reads bookmarks, outputs Alfred JSON |
| `info.plist` | Alfred workflow definition |

## License

MIT
