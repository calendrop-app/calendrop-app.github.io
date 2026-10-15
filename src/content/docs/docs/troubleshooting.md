---
title: Troubleshooting
description: What to do when macOS, Google or an account does not behave as expected.
---

## Keychain asks again after each update

After you install a new version, macOS asks whether Calendrop may use its
Keychain item, even if you chose **Always Allow** before.

Calendrop is signed with its own certificate rather than one issued by Apple.
Without an Apple team ID in the signature, macOS ties "Always Allow" to the
exact build, not to the app, so each new build is asked once. Enter your login
password and choose **Always Allow** again. Nothing is wrong with your
sign-in.

## macOS will not open Calendrop

Calendrop is not notarized, so macOS blocks its first launch. Allow it in
**System Settings › Privacy & Security**; see
[Allow the first launch](/docs/install/#allow-the-first-launch).

## Sign-in is stuck in the browser

If you closed the browser tab, or Google showed an error page instead of
returning to Calendrop, the accounts page keeps waiting for the sign-in to
finish. Press **Cancel Sign-In**, then **Add Account…** to start again.
Starting a new sign-in, from the menu or the accounts page, also replaces the
one still waiting.

## Google says the API "has not been used" or is disabled

An account shows an error such as *Google Calendar API has not been used in
project … before or it is disabled*. This is a problem with the Google Cloud
project behind the build you are running, not with your account.

- With a download from this site or Homebrew, please
  [report it](https://github.com/calendrop-app/Calendrop/issues).
- With a build you made yourself, enable the **Google Calendar API** in that
  project in Google Cloud Console, wait a few minutes, and press **Refresh
  Now** on the accounts page.

## An account shows "Sign-in required"

Calendrop cannot use the account's sign-in on this Mac. Its meetings disappear
from the menu and do not cut in until you sign in again. This happens when:

- the account was added on another Mac and has not been signed in on this one;
- you removed Calendrop's access in your Google Account;
- Google expired the sign-in.

Open the account in **Settings › Accounts** and press **Sign In…**, or use
**Sign In to …** in the menu. The browser opens with the account already
chosen.

When only the network is down, the account does not need signing in: the
meetings last fetched stay until Calendrop can reach Google again.

## The sign-in was turned back

Calendrop needs to see both your calendar list and your events. If you unticked
either on Google's consent screen, it turns the sign-in back with an
explanation. Sign in again and leave both ticked.

## A meeting did not cut in

Check that:

- it is on a calendar Calendrop reads for that account — by default only the
  main calendar; see [Choose calendars](/docs/getting-started/#choose-calendars);
- it has a video link, or **Meetings without a video link** is on;
- you accepted it, or **Meetings not yet accepted** is on;
- you did not decline it, it is not an all-day event, and it was not cancelled;
- you had not already joined or dismissed it.

## Still stuck

Search or open an issue on the
[issue tracker](https://github.com/calendrop-app/Calendrop/issues).
