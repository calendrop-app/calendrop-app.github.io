---
title: Settings
description: Every setting Calendrop has, and where it keeps them.
---

Open **Settings…** from the Calendrop menu. Every change applies at once; there
is no Save button. Settings are shared with your other Macs through
[sync](#sync).

## General

### Show before a meeting

How many minutes before the start the cut-in covers every screen, from 0 to
120. The default is 2. Zero shows the cut-in when the meeting starts.

### Meetings without a video link

Off by default. Turn it on to have meetings with nothing to join, such as
in-person ones, cut in too. Their cut-in closes with **OK**.

### Meetings not yet accepted

On by default. Meetings you answered "maybe" to, or have not answered, cut in
and are marked as such. Turn it off to have only meetings you accepted cut in.

## Appearance

### Style

Pick one of the preset styles — **Midnight** (the default), **Daylight**,
**Sunset**, **Ocean** and **Monochrome** — or **Custom**. The style applies to
every cut-in on every Mac that shares your settings.

**Customize…** copies the selected preset into the custom style, where you set
the background's top and bottom colours, the text colour, the Join button's
colour, and the font: standard, rounded, serif or monospaced. The custom style
is kept while a preset is selected.

### Preview

Shows the selected style live with sample meetings. **Try Full Screen** shows
it on every screen; see [Try it](/docs/cut-in/#try-it).

### Motion

**Drop in from the top** is on by default. When off, the cut-in appears at
once. With Reduce Motion on in System Settings, it fades in either way.

## Accounts

Add, open and remove your Google accounts, and set each one's label, colour and
calendars. See [Getting started](/docs/getting-started/). **Refresh Now** reads
every account again at once; calendars also refresh on their own.

## Sync

Calendrop keeps your accounts and settings in one file:

- `Calendrop/config.json` on iCloud Drive, so every Mac signed in to the same
  iCloud account reads the same file; or
- `~/Library/Application Support/Calendrop/config.json` when iCloud Drive is
  off.

Edits made on one Mac reach the others on their next refresh. **Show in Finder**
reveals the file.

The file never holds a sign-in token. Tokens stay in the Keychain of the Mac
that signed in, so each Mac signs in to each account once. A listed account
that has not been signed in on this Mac is shown as **Sign-in required on this
Mac**.
