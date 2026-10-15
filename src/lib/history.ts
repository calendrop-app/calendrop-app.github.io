import type { Releases } from "./releases";

// Globbed rather than imported so that a missing file fails with a hint
// instead of an unresolved import.
const found = Object.values(
  import.meta.glob<Releases>("../data/releases.json", { eager: true, import: "default" }),
)[0];
if (!found) {
  throw new Error("src/data/releases.json is missing; run `npm run fetch`");
}

/** src/data/releases.json, as scripts/fetch_releases.py wrote it before the build. */
export const history: Releases = found;
