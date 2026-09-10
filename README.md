# Granite.Fit — Mobile Web Demo

A static, no-build mobile web clone of the Granite.Fit gym app screens (splash → home → profile → access), built for GitHub Pages.

## Files

```
index.html        Entire app (HTML + CSS + JS, single file)
manifest.json      PWA manifest (used for the iOS/Android home-screen icon)
icons/             App icon at every size iOS/Android ask for
```

## Running it

Just open `index.html` in a browser, or serve the folder statically. No build step, no dependencies.

To publish on GitHub Pages:
1. Push this folder to a repo.
2. Repo Settings → Pages → Deploy from branch → `main` / root.
3. Visit `https://<you>.github.io/<repo>/`.

## What's included

- **Splash screen** — matches the dark navy "Loading Router…" screen, shows for 3 seconds on every load, then fades into the app.
- **Home screen** — "Hello, {name}" greeting, Enable Door Access card, empty classes/appointments cards.
- **Profile / Account screen** — avatar, stats pills, membership card (status, price, next payment date, recurring info), Account & Booking lists.
- **Access screen** — Bluetooth permission card, pagination dots, and a real drag-to-unlock slider on the Main Door card.
- **Edit Profile screen** — reachable via the pencil icon on the Profile screen. Lets you change name, club, membership title, status, price, visit/class/appointment counts, and the membership end date.

The "Next payment" date is computed live — it's always the upcoming 1st of the month, based on the device's real clock, not hardcoded.

## The shareable link trick

Since this is a static site with no backend, "saved" data has to live somewhere the browser can read without a server. When you tap **Save changes** on the Edit Profile screen, the app:

1. Serializes your edited values to JSON.
2. Base64-encodes them and appends them to the URL as `?d=...`.
3. Shows you that full URL in a box with a **Copy** button.

Opening that URL — on any device, any browser, with empty storage — will always decode `?d=...` and render the app with exactly those values. That's what makes it safe to **Add to Home Screen**: iOS Safari saves the *exact* URL you add, query string included, so the home-screen icon will always relaunch with your saved name/membership/etc., every time, forever — no server or account needed.

(It also caches the last-used values in `localStorage` as a convenience fallback for plain reloads without the `?d=` param.)

## Icon on iOS home screen

`index.html` links `apple-touch-icon` at 180/167/152/120px, plus a `manifest.json` with 192/512px icons for Android/Chrome install prompts, so "Add to Home Screen" picks up the purple mountain logo automatically.
