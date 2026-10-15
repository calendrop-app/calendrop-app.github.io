"""Read every published release of Calendrop from the GitHub API into
src/data/releases.json, for the release history page and the download links.

Each release keeps its notes as written on GitHub, in Markdown; the site
renders them. A patch release (X.Y.Z, Z > 0) and a prerelease are folded into
the section of the X.Y.0 release they belong to. The download is the app's zip
attached to the newest release that is not a prerelease.

A repository the API does not show (private, or not created yet) counts as one
without releases, so the site still builds and says no release is out yet.

GITHUB_TOKEN, when set, is sent to raise the API's rate limit and to see a
private repository. Without the network, the history read before is kept.
"""
import calendar
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPOSITORY = "calendrop-app/Calendrop"
API = f"https://api.github.com/repos/{REPOSITORY}/releases"
PER_PAGE = 100
VERSION = re.compile(r"^v?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?P<suffix>.*)$")
APP_ZIP = re.compile(r"^Calendrop-.+-macos-arm64\.zip$")
MANIFEST = Path(__file__).resolve().parents[1] / "src" / "data" / "releases.json"


def english_date(published_at):
    day = datetime.fromisoformat(published_at.replace("Z", "+00:00")).astimezone(timezone.utc)
    return f"{calendar.month_name[day.month]} {day.day}, {day.year}"


def parse_releases(pages):
    return [
        {
            "version": r["tag_name"],
            "url": r["html_url"],
            "published_at": r["published_at"],
            "date": english_date(r["published_at"]),
            "prerelease": bool(r.get("prerelease")),
            "body": r.get("body") or "",
            "assets": [{"name": a["name"], "url": a["browser_download_url"]} for a in r.get("assets") or []],
        }
        for page in pages
        for r in json.loads(page)
        if not r.get("draft") and r.get("published_at")
    ]


def group_releases(releases):
    """One section per X.Y, headed by X.Y.0 and holding the rest newest first;
    without an X.Y.0, the earliest release of X.Y heads it. A tag that is not
    a version is a section of its own. Sections are newest first by their head,
    so a late fix to an older X.Y does not move its section up."""
    sections = {}
    for r in releases:
        found = VERSION.match(r["version"])
        key = (int(found["major"]), int(found["minor"])) if found else r["version"]
        sections.setdefault(key, []).append(r)
    groups = []
    for members in sections.values():
        members = sorted(members, key=lambda r: r["published_at"])
        head = next((r for r in members if is_minor_release(r["version"])), members[0])
        patches = sorted((r for r in members if r is not head), key=lambda r: r["published_at"], reverse=True)
        groups.append({**head, "patches": patches})
    return sorted(groups, key=lambda g: g["published_at"], reverse=True)


def is_minor_release(version):
    found = VERSION.match(version)
    return bool(found) and found["patch"] == "0" and not found["suffix"]


def latest_download(releases):
    for r in sorted(releases, key=lambda r: r["published_at"], reverse=True):
        if r["prerelease"]:
            continue
        for a in r["assets"]:
            if APP_ZIP.match(a["name"]):
                return {"version": r["version"], "name": a["name"], "url": a["url"]}
    return None


def request(url):
    headers = {
        "User-Agent": "calendrop-site",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as response:
        return response.read()


def fetch_pages():
    pages = []
    while True:
        page = request(f"{API}?per_page={PER_PAGE}&page={len(pages) + 1}")
        pages.append(page)
        if len(json.loads(page)) < PER_PAGE:
            return pages


def write_manifest(manifest):
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")


def main():
    try:
        releases = parse_releases(fetch_pages())
    except urllib.error.HTTPError as error:
        if error.code != 404:
            return keep_or_fail(error)
        print(f"fetch-releases: {REPOSITORY} is not visible; taking it as without releases", file=sys.stderr)
        releases = []
    except OSError as error:
        return keep_or_fail(error)
    except (ValueError, KeyError) as error:
        print(f"fetch-releases: {error!r}", file=sys.stderr)
        return 1
    groups = group_releases(releases)
    write_manifest(
        {
            "releases": f"https://github.com/{REPOSITORY}/releases",
            "download": latest_download(releases),
            "groups": groups,
        }
    )
    print(f"fetch-releases: {len(releases)} releases in {len(groups)} sections")
    return 0


def keep_or_fail(error):
    if MANIFEST.exists():
        print(f"fetch-releases: {error}; keeping the history read before", file=sys.stderr)
        return 0
    print(f"fetch-releases: {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
