# Calendrop Site

The landing page, the user documentation and the legal pages for [Calendrop](https://github.com/calendrop-app/Calendrop), published at [calendrop-app.github.io](https://calendrop-app.github.io).

## Tech stack

- [Astro](https://astro.build) with [Starlight](https://starlight.astro.build) for the documentation: sidebar, full-text search (Pagefind), light and dark themes and the table of contents come with it.
- The landing page (`src/pages/index.astro`) is a plain Astro page with its own styles, outside Starlight. Its illustration of the cut-in is drawn in CSS.
- Fonts are Fraunces for the name and headings and Hanken Grotesk for the text, self-hosted through Fontsource. Colours are the brand's: the hardware ink, the midnight cloth and the Join blue.
- Deployed to GitHub Pages by `.github/workflows/deploy.yml` on every push to `main`.

## Development

With Nix, `nix develop` gives Node.js, just and Python. Without it, Node.js 24 and Python 3 are enough.

```sh
just install   # npm install
just dev       # dev server with hot reload
just check     # unit tests, type check, build, link check
just preview   # serve dist/
```

## Layout

```
src/
├── pages/
│   ├── index.astro            # landing page
│   └── docs/releases.astro    # release history, built from src/data/releases.json
├── components/
│   └── LatestDownload.astro   # the download of the newest release, for the install page
├── content/docs/
│   ├── docs/                  # the documentation, served under /docs/
│   ├── privacy.md             # /privacy/
│   └── terms.md               # /terms/
├── lib/
│   ├── history.ts             # loads src/data/releases.json
│   └── releases.ts            # renders the release notes
└── styles/                    # fonts, Starlight theme, landing page
public/
└── logo/                      # brand logos, from calendrop-brand
scripts/
├── fetch_releases.py          # reads every release of Calendrop and its notes (runs before dev and build)
└── check-links.py             # checks every internal link and #fragment in dist/
```

## Keeping up with Calendrop

The documentation describes Calendrop's behaviour in the words of a user; its source of truth is `docs/spec/` in the Calendrop repository. Describe only what the specs promise, and when the behaviour changes there, change the page that describes it here.

## The release history and the download

`scripts/fetch_releases.py` reads every published release of Calendrop from the GitHub API into `src/data/releases.json`. `/docs/releases/` lists them with their notes as written on GitHub; a patch release is folded into its X.Y.0 release, and the notes are rendered at build time with raw HTML dropped. The landing page and `/docs/install/` link the app's zip (`Calendrop-<version>-macos-arm64.zip`) on the newest release that is not a prerelease and has it attached.

The file is generated and not committed. A repository the API does not show — private, or not created yet — counts as one without releases, and the pages then say no release is out yet. Without the network, the history read before is used. Set `GITHUB_TOKEN` to raise the API's rate limit or to read a private repository; the deploy workflow passes its own.

Calendrop's release can run the deploy workflow (`workflow_dispatch`) once its zip is attached, so the site links the new download right away.

## The legal pages

`/privacy/` and `/terms/` are the URLs registered on Google Cloud's OAuth consent screen, so they must not move. When the Privacy Policy or the Terms change, update the "Last updated" date at the top of the page. The Privacy Policy must keep naming the exact Google scopes Calendrop requests and the Limited Use statement; change it in the same breath as any change to what Calendrop reads or stores.

## Writing the documentation

- Write in English, in plain words: short sentences, the names of buttons and settings as the app shows them, in bold.
- Link between pages with absolute paths (`/docs/cut-in/`). `just check` fails on a link to a page or a heading that does not exist.
