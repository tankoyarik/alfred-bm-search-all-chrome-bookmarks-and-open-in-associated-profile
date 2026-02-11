#!/usr/bin/env python3
"""Alfred Script Filter: Search Chrome bookmarks across all profiles."""
import json
import os
import sys

CHROME_DIR = os.path.expanduser("~/Library/Application Support/Google/Chrome")
CHROME_ICON = "/Applications/Google Chrome.app/Contents/Resources/app.icns"


def get_profiles():
    """Return dict of {profile_dir: display_name}."""
    try:
        with open(os.path.join(CHROME_DIR, "Local State"), "r") as f:
            state = json.load(f)
        cache = state.get("profile", {}).get("info_cache", {})
        return {d: info.get("name", d) for d, info in cache.items()}
    except Exception:
        return {}


def get_bookmarks(profile_dir):
    """Recursively extract all bookmarks from a profile."""
    path = os.path.join(CHROME_DIR, profile_dir, "Bookmarks")
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except Exception:
        return []

    results = []

    def traverse(node, folder=""):
        t = node.get("type", "")
        if t == "url":
            results.append({
                "name": node.get("name", ""),
                "url": node.get("url", ""),
                "folder": folder,
            })
        children = node.get("children", [])
        new_folder = node.get("name", folder) if t == "folder" else folder
        for child in children:
            traverse(child, new_folder)

    for root in data.get("roots", {}).values():
        if isinstance(root, dict):
            traverse(root)
    return results


def profile_icon(profile_dir):
    """Return best available icon path for a Chrome profile."""
    pic = os.path.join(CHROME_DIR, profile_dir, "Google Profile Picture.png")
    if os.path.exists(pic):
        return pic
    return CHROME_ICON


def main():
    query = sys.argv[1].strip().lower() if len(sys.argv) > 1 else ""
    profiles = get_profiles()
    items = []

    for pdir, pname in sorted(profiles.items()):
        icon = profile_icon(pdir)
        for bm in get_bookmarks(pdir):
            if query and query not in bm["name"].lower():
                continue
            items.append({
                "title": bm["name"],
                "subtitle": f"[{pname}]  {bm['folder']}",
                "arg": f"{pdir}|||{bm['url']}",
                "autocomplete": bm["name"],
                "valid": True,
                "icon": {"path": icon},
                "mods": {
                    "cmd": {
                        "subtitle": bm["url"],
                        "valid": True,
                    }
                },
            })

    if not items:
        items.append({
            "title": "No bookmarks found",
            "subtitle": f"No match for '{query}'" if query else "No Chrome bookmarks",
            "valid": False,
        })

    print(json.dumps({"items": items}))


if __name__ == "__main__":
    main()
