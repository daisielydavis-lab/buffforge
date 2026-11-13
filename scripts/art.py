"""Game cover art for the home page (Games panels + Featured tools).

Real official game art, local files under assets/games/ — no hotlinking.
User decision 2026-11-13 overrides the design spec's "no official art" rule.

- Desktop Pension Squad / AION 2: Steam CDN capsule art (capsule_616x353)
  for the wide Featured media; portrait covers are center-crops (PIL)
  of official Steam art because neither game ships a library_600x900
  portrait on the CDN (404 on shared.akamai / cdn.akamai / cdn.cloudflare).
  DPS cover is cropped from an official Steam store screenshot (item UI +
  archer character); AION 2 cover is cropped from the official page
  background key art (shattered planet Atreia). Each image was visually
  verified to be the right game before use.
- GTA 6: no Steam page. Wide art is the og:image from
  https://www.rockstargames.com/VI (official GTA VI key-art collage);
  the portrait cover is a PIL center-crop of the same image.
"""

DPS_FEATURE = '<img src="/assets/games/desktop-pension-squad-wide.jpg" alt="" loading="lazy">'
DPS_COVER = '<img src="/assets/games/desktop-pension-squad-cover.jpg" alt="" loading="lazy">'
AION_FEATURE = '<img src="/assets/games/aion-2-wide.jpg" alt="" loading="lazy">'
AION_COVER = '<img src="/assets/games/aion-2-cover.jpg" alt="" loading="lazy">'
GTA_FEATURE = '<img src="/assets/games/gta-6-wide.jpg" alt="" loading="lazy">'
GTA_COVER = '<img src="/assets/games/gta-6-cover.jpg" alt="" loading="lazy">'
# ROB RUN: official Steam capsule (wide) and a portrait crop of the
# official store page background. No library_600x900 on the CDN.
ROB_FEATURE = '<img src="/assets/games/rob-run-wide.jpg" alt="ROB RUN" loading="lazy">'
ROB_COVER = '<img src="/assets/games/rob-run-cover.jpg" alt="ROB RUN" loading="lazy">'
