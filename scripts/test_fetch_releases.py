import json
import unittest
import urllib.error
from unittest import mock

import fetch_releases
from fetch_releases import english_date, group_releases, latest_download, parse_releases


def release(tag, published_at, **fields):
    return {
        "tag_name": tag,
        "html_url": f"https://github.com/calendrop-app/Calendrop/releases/tag/{tag}",
        "draft": False,
        "prerelease": False,
        "published_at": published_at,
        "body": f"notes of {tag}",
        "assets": [],
        **fields,
    }


def asset(name):
    return {
        "name": name,
        "browser_download_url": f"https://github.com/calendrop-app/Calendrop/releases/download/v0.1.0/{name}",
    }


def entry(tag, published_at, prerelease=False, assets=()):
    return {"version": tag, "published_at": published_at, "prerelease": prerelease, "assets": list(assets)}


class EnglishDate(unittest.TestCase):
    def test_writes_the_day_in_utc_with_the_month_spelled_out(self):
        self.assertEqual(english_date("2026-10-08T08:50:21Z"), "October 8, 2026")
        self.assertEqual(english_date("2026-10-10T23:59:59Z"), "October 10, 2026")


class ParseReleases(unittest.TestCase):
    def test_reads_each_release_from_every_page(self):
        pages = [
            json.dumps(
                [release("v0.2.0", "2026-10-08T08:50:21Z", assets=[asset("Calendrop-0.2.0-macos-arm64.zip")])]
            ).encode(),
            json.dumps([release("v0.1.0", "2026-10-07T04:06:36Z", prerelease=True)]).encode(),
        ]
        self.assertEqual(
            parse_releases(pages),
            [
                {
                    "version": "v0.2.0",
                    "url": "https://github.com/calendrop-app/Calendrop/releases/tag/v0.2.0",
                    "published_at": "2026-10-08T08:50:21Z",
                    "date": "October 8, 2026",
                    "prerelease": False,
                    "body": "notes of v0.2.0",
                    "assets": [
                        {
                            "name": "Calendrop-0.2.0-macos-arm64.zip",
                            "url": "https://github.com/calendrop-app/Calendrop/releases/download/v0.1.0/Calendrop-0.2.0-macos-arm64.zip",
                        }
                    ],
                },
                {
                    "version": "v0.1.0",
                    "url": "https://github.com/calendrop-app/Calendrop/releases/tag/v0.1.0",
                    "published_at": "2026-10-07T04:06:36Z",
                    "date": "October 7, 2026",
                    "prerelease": True,
                    "body": "notes of v0.1.0",
                    "assets": [],
                },
            ],
        )

    def test_leaves_out_drafts(self):
        page = json.dumps(
            [release("v0.3.0", None, draft=True), release("v0.2.0", "2026-10-08T08:50:21Z")]
        ).encode()
        self.assertEqual([r["version"] for r in parse_releases([page])], ["v0.2.0"])

    def test_takes_a_missing_body_or_asset_list_as_empty(self):
        page = json.dumps([release("v0.1.0", "2026-10-05T18:00:15Z", body=None, assets=None)]).encode()
        parsed = parse_releases([page])[0]
        self.assertEqual((parsed["body"], parsed["assets"]), ("", []))


class GroupReleases(unittest.TestCase):
    def test_folds_the_patches_into_their_minor_release_newest_first(self):
        groups = group_releases(
            [
                entry("v0.4.1", "2026-10-08T08:50:21Z"),
                entry("v0.4.0", "2026-10-08T04:06:36Z"),
                entry("v0.3.0", "2026-10-06T18:21:14Z"),
                entry("v0.1.3", "2026-10-06T05:56:38Z"),
                entry("v0.1.0", "2026-10-05T18:00:15Z"),
                entry("v0.1.1", "2026-10-05T18:25:06Z"),
            ]
        )
        self.assertEqual(
            [(g["version"], [p["version"] for p in g["patches"]]) for g in groups],
            [("v0.4.0", ["v0.4.1"]), ("v0.3.0", []), ("v0.1.0", ["v0.1.3", "v0.1.1"])],
        )

    def test_heads_a_minor_release_without_its_x_y_0_by_its_earliest_release(self):
        groups = group_releases(
            [
                entry("v0.2.2", "2026-10-07T00:00:00Z"),
                entry("v0.2.1", "2026-10-06T00:00:00Z"),
                entry("v0.1.0", "2026-10-05T00:00:00Z"),
            ]
        )
        self.assertEqual(
            [(g["version"], [p["version"] for p in g["patches"]]) for g in groups],
            [("v0.2.1", ["v0.2.2"]), ("v0.1.0", [])],
        )

    def test_folds_a_prerelease_of_x_y_0_into_the_x_y_0_release(self):
        groups = group_releases(
            [
                entry("v0.5.0", "2026-10-12T00:00:00Z"),
                entry("v0.5.0-rc.1", "2026-10-11T00:00:00Z"),
            ]
        )
        self.assertEqual(
            [(g["version"], [p["version"] for p in g["patches"]]) for g in groups],
            [("v0.5.0", ["v0.5.0-rc.1"])],
        )

    def test_gives_a_tag_that_is_not_a_version_a_section_of_its_own(self):
        groups = group_releases(
            [
                entry("nightly", "2026-10-09T00:00:00Z"),
                entry("v0.4.0", "2026-10-08T00:00:00Z"),
            ]
        )
        self.assertEqual(
            [(g["version"], g["patches"]) for g in groups],
            [("nightly", []), ("v0.4.0", [])],
        )

    def test_orders_the_sections_by_the_date_of_their_head(self):
        # A fix to an older minor release, published after a newer one, stays
        # in the older section and does not move it up.
        groups = group_releases(
            [
                entry("v0.4.2", "2026-10-12T00:00:00Z"),
                entry("v0.5.0", "2026-10-11T00:00:00Z"),
                entry("v0.4.0", "2026-10-08T00:00:00Z"),
            ]
        )
        self.assertEqual([g["version"] for g in groups], ["v0.5.0", "v0.4.0"])


class LatestDownload(unittest.TestCase):
    ZIP = {"name": "Calendrop-0.2.0-macos-arm64.zip", "url": "https://example.com/Calendrop-0.2.0-macos-arm64.zip"}

    def test_picks_the_app_zip_of_the_newest_release(self):
        releases = [
            entry("v0.1.0", "2026-10-05T00:00:00Z", assets=[{"name": "Calendrop-0.1.0-macos-arm64.zip", "url": "u"}]),
            entry("v0.2.0", "2026-10-08T00:00:00Z", assets=[{"name": "notes.txt", "url": "n"}, self.ZIP]),
        ]
        self.assertEqual(latest_download(releases), {"version": "v0.2.0", **self.ZIP})

    def test_skips_prereleases(self):
        releases = [
            entry("v0.1.0", "2026-10-05T00:00:00Z", assets=[{"name": "Calendrop-0.1.0-macos-arm64.zip", "url": "u"}]),
            entry("v0.2.0-rc.1", "2026-10-08T00:00:00Z", prerelease=True, assets=[self.ZIP]),
        ]
        self.assertEqual(latest_download(releases)["version"], "v0.1.0")

    def test_skips_a_release_whose_zip_is_not_attached_yet(self):
        # The release workflow attaches the zip a few minutes after publishing.
        releases = [
            entry("v0.1.0", "2026-10-05T00:00:00Z", assets=[{"name": "Calendrop-0.1.0-macos-arm64.zip", "url": "u"}]),
            entry("v0.2.0", "2026-10-08T00:00:00Z"),
        ]
        self.assertEqual(latest_download(releases)["version"], "v0.1.0")

    def test_is_none_without_any_release(self):
        self.assertIsNone(latest_download([]))


class Main(unittest.TestCase):
    def test_takes_a_repository_it_cannot_see_as_one_without_releases(self):
        # A private repository answers 404 rather than 403 to whoever may not see it.
        missing = urllib.error.HTTPError(fetch_releases.API, 404, "Not Found", {}, None)
        written = {}
        with (
            mock.patch.object(fetch_releases, "fetch_pages", side_effect=missing),
            mock.patch.object(fetch_releases, "write_manifest", side_effect=written.update),
        ):
            self.assertEqual(fetch_releases.main(), 0)
        self.assertEqual(written["groups"], [])
        self.assertIsNone(written["download"])


if __name__ == "__main__":
    unittest.main()
