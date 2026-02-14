#!/usr/bin/env python3
"""Increment usage count for chosen bookmark, then open it in the right Chrome profile."""
import json
import os
import subprocess
import sys

DATA_DIR = os.path.expanduser(
    "~/Library/Application Support/Alfred/Workflow Data/"
    "com.custom.chrome-bookmarks-search"
)
USAGE_FILE = os.path.join(DATA_DIR, "usage.json")


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if "|||" not in arg:
        return
    profile_dir, url = arg.split("|||", 1)

    # Open in the correct Chrome profile immediately
    subprocess.Popen([
        "open", "-na", "Google Chrome",
        "--args", f"--profile-directory={profile_dir}", url,
    ])

    # Update usage tracking after firing the open command
    DECAY = 0.95
    MIN_SCORE = 0.01

    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(USAGE_FILE, "r") as f:
            usage = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        usage = {}

    usage = {k: v * DECAY for k, v in usage.items() if v * DECAY >= MIN_SCORE}
    usage[url] = usage.get(url, 0) + 1

    with open(USAGE_FILE, "w") as f:
        json.dump(usage, f)


if __name__ == "__main__":
    main()
