#!/usr/bin/env python3
"""Build data/rob-run-items.json from the public robrunwiki items catalogue.

Source: https://robrunwiki.com/data/items.csv (schema.org Dataset, free to use;
the site asks for a source link, which the calculator page carries).
Snapshot verified 17 Nov 2026: 569 rows, 373 priced (min > 0), only two
max/min ratios in the priced rows: 362 x1.5 and 11 x1.25.

The script reads the verified snapshot /tmp/items.csv when it exists, and
falls back to the durable repo copy data/rob-run-items-source.csv (same file,
checked in so rebuilds keep working after /tmp is cleared).

After a game patch: re-download items.csv, re-check the row count and the
ratio distribution (this script fails loudly on any change), then rebuild.
The JSON is served as a static file at /data/rob-run-items.json; it is not
a page and must not enter sitemap.xml.

Run:  cd <repo root> && python3 scripts/build_rob_data.py
Then rebuild the calculator page:  python3 scripts/build_rob.py
"""
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP_CSV = "/tmp/items.csv"
REPO_CSV = os.path.join(ROOT, "data", "rob-run-items-source.csv")
OUT = os.path.join(ROOT, "data", "rob-run-items.json")

EXPECTED_COLS = ["id", "name_ru", "name_en", "category_ru", "rarity",
                 "fence_price_min_usd", "fence_price_max_usd", "url"]
EXPECTED_TOTAL = 569
EXPECTED_PRICED = 373
# (ratio, count) seen on 17 Nov 2026. Any other ratio fails the build.
EXPECTED_RATIOS = {1.5: 362, 1.25: 11}
VERSION = "0.7.0"
SOURCE = "https://robrunwiki.com/data/items.csv"


def main():
    src = TMP_CSV if os.path.exists(TMP_CSV) else REPO_CSV
    print("source:", src)
    with open(src, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != EXPECTED_COLS:
            sys.exit("ABORT: unexpected CSV columns: %s" % (reader.fieldnames,))
        rows = list(reader)
    if len(rows) != EXPECTED_TOTAL:
        sys.exit("ABORT: total rows %d, expected %d (catalogue changed?)"
                 % (len(rows), EXPECTED_TOTAL))
    items = []
    ratios = {}
    for r in rows:
        lo = float(r["fence_price_min_usd"] or 0)
        hi = float(r["fence_price_max_usd"] or 0)
        if lo <= 0:
            continue
        ratio = round(hi / lo, 4)
        ratios[ratio] = ratios.get(ratio, 0) + 1
        items.append({
            "id": r["id"],
            "name_en": r["name_en"],
            "name_ru": r["name_ru"],
            "category_ru": r["category_ru"],
            "rarity": r["rarity"],
            "min": int(lo),
            "max": int(hi),
            "url": r["url"],
        })
    if len(items) != EXPECTED_PRICED:
        sys.exit("ABORT: priced rows %d, expected %d"
                 % (len(items), EXPECTED_PRICED))
    for ratio, count in sorted(ratios.items()):
        if EXPECTED_RATIOS.get(ratio) != count:
            sys.exit("ABORT: ratio %s appears %d times, expected %s "
                     "(ladder logic may need review)"
                     % (ratio, count, EXPECTED_RATIOS.get(ratio)))
    data = {
        "meta": {
            "version": VERSION,
            "source": SOURCE,
            "fetched": "2026-11-17",
            "total": len(rows),
            "priced": len(items),
        },
        "items": items,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    print("wrote data/rob-run-items.json: total=%d priced=%d ratios=%s"
          % (len(rows), len(items), ratios))


if __name__ == "__main__":
    main()
