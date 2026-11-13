# BuffForge — Design System ("Daylight Forge")

Reusable design record for the BuffForge site. **Source of truth is
`assets/site.css` `:root`** — this document mirrors it. If the two ever
drift, `:root` wins; update this file when a token changes.

This doc records visual tokens only (colors, type, fonts, layout). It does
not cover SEO, indexing, sitemap, or content rules — the temporary noindex,
for example, is not a design token and is deliberately not listed here.

## Colors

Page surfaces:

| Token | Hex | Used for |
|---|---|---|
| `--bg` | `#F3F5F8` | Page background (cool off-white, not pure white) |
| `--bg-elev` | `#EEF1F5` | Elevated background areas |
| `--paper` | `#FFFFFF` | Cards, panels, page paper |
| `--paper-2` | `#F7F8FA` | Secondary paper surface |
| `--line` | `#E2E6ED` | Hairline borders, dividers |
| `--line-strong` | `#CDD3DC` | Stronger borders (inputs, active states) |

Text:

| Token | Hex | Used for | Contrast |
|---|---|---|---|
| `--ink` | `#14181F` | Headings, near-black | 16.29:1 on `#F3F5F8` |
| `--body` | `#3A4250` | Primary running text | 9.27:1 on `#F3F5F8` |
| `--muted` | `#3A4250` | Secondary / description text (ledes, card blurbs, FAQ answers, meta lines, footer) | 9.27:1 on `#F3F5F8` — same as `--body` |
| `--faint` | `#3A4250` | Same value as `--muted`; currently unused in the CSS. Do not lighten it for running text. | — |

All description and secondary running text goes through `--muted` or
`--body`. No lighter gray is used for reading text on the light background.

Brand:

| Token | Hex | Used for |
|---|---|---|
| `--teal` | `#0C706C` | Primary brand (buttons, links, active states) |
| `--teal-deep` | `#0B5F5C` | Darker teal (hover, deep accents) |
| `--teal-mid` | `#0D7A76` | Mid teal |
| `--teal-dim` | `#E6F3F2` | Teal tint wash (selected chips, active nav) |
| `--teal-ink` | `#FFFFFF` | White text on teal |
| `--warm` | `#9A5610` | Copper accent (pre-launch / planned badges, warnings) |
| `--warm-dim` | `#F8EBD9` | Copper tint wash |
| `--warm-ink` | `#6B3B08` | Dark copper text on the wash |
| `--ok` | `#0F6B43` | Success green |
| `--ok-dim` | `#E3F5EC` | Success tint wash |
| `--danger` | `#C1392B` | Error red |
| `--danger-dim` | `#FDECEA` | Error tint wash |

Game accents (hub identity colors):

| Game | Base | Wash | Deep |
|---|---|---|---|
| AION 2 (`--aion`) | `#8A6710` | `#F4EBD2` | `#5C4A18` |
| GTA 6 (`--gta`) | `#0E7A72` | `#DCEFED` | `#0B4F4A` |
| Desktop Pension Squad (`--dps`) | `#0C706C` | `#DCEEEC` | `#0A4543` |

Rarity dots (DPS fusion calculator; visual only, not official colors):

| Token | Hex |
|---|---|
| `--r-common` | `#5C6778` |
| `--r-uncommon` | `#1E8A4C` |
| `--r-rare` | `#1D5FB8` |
| `--r-unique` | `#6B46C1` |
| `--r-epic` | `#8B3DA8` |
| `--r-legendary` | `#9A5610` |
| `--r-immortal` | `#C14A32` |
| `--r-ascendant` | `#0C706C` |
| `--r-primordial` | `#A13E8A` |
| `--r-mythic` | `#8A6710` |

## Type scale

Every `font-size` in the CSS uses a `--fs-*` token. Floors: no sentence or
paragraph text below 13px; 12px only for short uppercase labels; 11px only
for pills/badges. 10px is deleted everywhere.

| Token | Size | Line-height | Used for |
|---|---|---|---|
| `--fs-h1` | `clamp(32px, 4vw, 44px)` | 1.12 | Page heroes (`.page-h1`, `.tool-hero h1`) |
| `--fs-h2` | 28px (24px at ≤600px) | 1.25 | Section headings (`h2`, `h2.sec`) |
| `--fs-h3` | 20px (18px at ≤600px) | 1.35 | Card / panel titles (`h3`, `.fcard-body h3`) |
| `--fs-h4` | 17px | 1.4 | Small titles |
| `--fs-lede` | 17px | 1.7 | Hero / page ledes (`.lede`) |
| `--fs-body` | 16px | 1.7 | Prose, answers, results (`body`) |
| `--fs-card` | 14px | 1.65 | Card blurbs, section subs, descriptions (`.fcard-body p`, `.t-blurb`, `.tagline`, `.intro-note`) |
| `--fs-small` | 13px | 1.6 | Notes, captions, footer, form hints (`.data-line`, `.field-help`, `.mini .note`) |
| `--fs-meta` | 12px | inherits | UPPERCASE kickers / labels ONLY |
| `--fs-badge` | 11px | inherits | Pills / badges ONLY |

Kept as-is (not reading text): the 404 giant number, hub stat watermarks
(VI / 2 / DPS), countdown / tracker display figures, icon glyphs, and
`.checker` inputs (16px — iOS Safari zooms on focus below 16px).

## Fonts

Self-hosted IBM Plex, no Google Fonts (hard dependency forbidden).

- **Sans:** IBM Plex Sans, weights 400 / 500 / 600 / 700 plus 400–600
  italics; includes Cyrillic and Cyrillic Extended. Stack:
  `"IBM Plex Sans", system-ui, -apple-system, "Segoe UI", "Helvetica Neue", "Noto Sans", "Noto Sans CJK SC", Arial, sans-serif`.
- **Mono:** IBM Plex Mono, weights 400 / 500. Stack:
  `"IBM Plex Mono", ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace`.
- Font files live in `assets/fonts/` and are declared in
  `assets/fonts.css` (36 `@font-face` rules: 28 Sans + 8 Mono).

## Layout

| Token | Value | Notes |
|---|---|---|
| `--wrap` | 1180px | Content width (`.wrap` is `min(1180px, 100% - 48px)`; 28px gutters at ≤600px) |
| `--header-h` | 68px | Translucent white header |
| `--r-sm` | 6px | Small radius |
| `--r` | 10px | Buttons, inputs |
| `--r-lg` | 14px | Cards |
| `--r-xl` | 18px | Large cards / panels |
| `--space-1` … `--space-9` | 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96px | Spacing scale |
| `--shadow-sm` | `0 1px 2px rgba(20,24,31,.05)` | — |
| `--shadow` | `0 1px 2px rgba(20,24,31,.04), 0 10px 28px rgba(20,24,31,.07)` | Cards |
| `--shadow-hover` | `0 1px 2px rgba(20,24,31,.05), 0 16px 36px rgba(20,24,31,.10)` | Cards on hover |
| `--ease` | 160ms ease | Hover transitions |

Card radii stay restrained (14–18px); buttons are 10px, not pill-shaped.

## Standing rules

- New text always uses a `--fs-*` token; never add a raw `font-size` in px.
- New secondary text uses `--muted` (or `--body`); never introduce a
  lighter gray for reading text.
- New colors go in `:root` as tokens; never hard-code a hex in a rule
  except white text on a dark surface or a decorative glyph.
- When a token changes, update this file in the same commit.
