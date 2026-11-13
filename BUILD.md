# BuffForge — how to rebuild

Pure static site. No backend, no build step at deploy time: Cloudflare Pages
serves the files in this repo as-is.

## Regenerate the generated pages

```bash
python3 scripts/build.py            # home, about, hubs, 404, sitemap, robots, _headers, _redirects
python3 scripts/build_tools.py      # 4 GTA 6 official-facts tools, EN + RU
python3 scripts/transform_legacy.py # AION 2 tracker + GTA 6 Wanted Evidence Helper, EN + RU
```

## Sources of truth

- `data/site.json` — games, tools, featured picks per language, guides.
  Home and hub pages are rendered from this file. To add a game: add the
  game + its tools here, re-run the scripts, then add the tool pages.
- Homepage Title / H1 and hub copy follow BuffForge SEO plan v2 §5
  (`workspace/user/files/buffforge-seo-plan-v2.md`): home = brand + broad
  category, never a game name; hubs = game name + tools and guides.
  The implementation spec's §8 homepage copy is superseded by v2.
- `assets/site.css` — the one shared visual shell (light theme, system fonts).
- `scripts/shell.py` — shared header / footer / head tags / JSON-LD.

## Rules that must survive any rebuild

- Temporary `noindex` on every page (user decision 2026-11-13) until the
  content set is complete; `robots.txt` stays `Allow: /`.
- Canonical URLs without `www`; `www.buffforge.com` 301s to `buffforge.com`
  (see `_redirects`; also confirm in the Cloudflare dashboard).
- `buffforge.pages.dev` gets `X-Robots-Tag: noindex` via `_headers`
  (and a 301 to the canonical domain via `_redirects`).
- Pre-launch tools (Wanted Evidence Helper) never enter `featured` and
  never enter `sitemap.xml`.
- Never publish a TODO number as fact (Shugo key caps, conquest counts,
  Ludra time limit, wanted star values, Xbox preload Moscow time).
  When in doubt, write "confirm in-game" / "check the store".
- Only push to the `preview` branch for review; `main` is production.
