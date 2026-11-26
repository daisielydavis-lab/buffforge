#!/usr/bin/env python3
"""BuffForge static site generator (shell pages only).

Regenerate:  cd <repo root> && python3 scripts/build.py
It reads data/site.json and writes: index.html, ru/index.html,
about/index.html, ru/about/index.html, aion-2/index.html, ru/aion-2/index.html,
gta-6/index.html, ru/gta-6/index.html, 404.html, sitemap.xml, robots.txt,
_headers, _redirects.

Tool pages are hand-written static HTML that share assets/site.css and the
same shell markup (see scripts/shell.py); the AION 2 tracker was re-skinned
from its original by scripts/transform_legacy.py, which preserves its
JavaScript verbatim. The GTA 6 Wanted Level & Evidence Helper is built by
scripts/build_wanted_level.py.

To add a game: add it to data/site.json (games + tools), re-run this script,
then add the tool pages. No HTML copy-paste needed for home / hubs.
"""
import json
import os
import sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import (BASE, EMAIL, GAMES, REVIEWED_EN, REVIEWED_RU, breadcrumb_jsonld,
                   crumbs_html, footer_html, head, header_html, org_website_jsonld, page)
from art import (AION_COVER, AION_FEATURE, DPS_COVER, DPS_FEATURE,
                 GTA_COVER, GTA_FEATURE, POE2_COVER, POE2_FEATURE,
                 ROB_COVER, ROB_FEATURE)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, "data", "site.json"), encoding="utf-8") as f:
    SITE = json.load(f)

GAMES_DATA = {g["id"]: g for g in SITE["games"]}
TOOLS = SITE["tools"]
GUIDES = SITE.get("guides", [])


def tools_for(game_id):
    return [t for t in TOOLS if t["game"] == game_id]


def guides_for(game_id, lang):
    """Live guides for this game in this language only.

    data/site.json "guides" is the hidden list. An entry with "langs"
    is omitted from the other language, so a RU-only guide never
    appears on the EN hub.
    """
    found = []
    for g in GUIDES:
        if g.get("game") != game_id:
            continue
        if g.get("status", "live") != "live":
            continue
        langs = g.get("langs")
        if langs is not None and lang not in langs:
            continue
        if lang not in (g.get("title") or {}):
            continue
        found.append(g)
    return found


def guide_slug(guide, lang):
    slug = guide["slug"]
    if isinstance(slug, dict):
        return slug[lang]
    return slug


def guide_url(lang, guide):
    base = "" if lang == "en" else "/ru"
    return "%s/%s/%s/" % (base, guide["game"], guide_slug(guide, lang))


def featured_for(lang):
    feats = [t for t in TOOLS
             if t["status"] == "live" and t.get("featured", {}).get(lang)]
    feats.sort(key=lambda t: (t.get("featuredOrder", {}).get(lang) is None,
                              t.get("featuredOrder", {}).get(lang) or 99))
    return feats[:4]


def game_order(lang):
    games = list(SITE["games"])
    games.sort(key=lambda g: g.get("homeOrder", {}).get(lang, 99))
    return games


def tool_slug(tool, lang):
    slug = tool["slug"]
    if isinstance(slug, dict):
        return slug[lang]
    return slug


def tool_url(lang, tool):
    base = "" if lang == "en" else "/ru"
    return "%s/%s/%s/" % (base, tool["game"], tool_slug(tool, lang))


def badge(lang, tool):
    if tool["status"] == "pre-launch":
        label = "Unverified" if lang == "en" else "Не проверено"
        return '<span class="badge prelaunch">%s</span>' % label
    label = "Live" if lang == "en" else "Доступно"
    return '<span class="badge live">%s</span>' % label


def game_anchor(lang, game):
    if lang == "en":
        return "%s tools and guides" % game["name"][lang]
    return "инструменты и гайды по %s" % game["name"][lang]


# ---------------------------------------------------------------- home
HOME_COPY = {
    "en": {
        "title": "BuffForge — Game Tools, Trackers & Calculators",
        "desc": "Free game tools, trackers and calculators, organized by game. Every number cites its source and review date. No login, no ads.",
        "h1": "Game Tools, Trackers & Calculators",
        "lede": "BuffForge is a free collection of game tools, trackers and calculators. Every number cites a public source and a review date. There is no login and no advertising. Tools are organized by game: open a game to find its trackers, checkers and (when we have sourced figures) guides. BuffForge is an independent fan project, not affiliated with any publisher. Written guides are added only when we can source the numbers — today the live work is the tools.",
        "kicker": "Sourced, dated, by game",
        "primary": "Browse featured tools",
        "chips": ["Public sources only", "Review dates on every figure", "No login, no ads"],
        "secondary": "How we check our numbers",
        "featured_h": "Featured tools",
        "featured_label": "Featured",
        "featured_sub": "Discover calculators, trackers, and checkers that help you plan ahead, track progress, and make better in-game decisions.",
        "games_h": "Explore games",
        "games_label": "Explore games",
        "games_intro": "Find dedicated game hubs with calculators, trackers, and checkers — all organized by game.",
        "how_h": "How we check every number",
        "how_label": "The method",
        "faq_h": "Frequently asked questions",
        "faq_label": "Questions",
        "faq": [
            ("I play MMOs — which tools are actually useful?", "The ones that track what resets. In AION 2, daily duties reset at 07:00 UTC and weekly duties every Wednesday — miss a reset and that day is gone. The AION 2 tracker on this site lists your duties and counts down to each reset, so you can see what is still open before you log off."),
            ("I play idle games — how do I stop wasting items?", "Check the odds before you commit. In Desktop Pension Squad, nine items go into one fusion and the game never shows the odds. The calculator uses the v1.0.2 Workshop table (build 26611958), checked unchanged on the v1.0.6 wiki page, and compares fusing against selling."),
            ("I play single-player games — what should I check?", "Four things: disk space, unlock time, edition, and console. GTA 6 has been out since 19 Nov 2026. This site has a 212 GB free-space check, the unlock time by store region, Standard vs Ultimate at US prices, and a console check — official figures only."),
            ("What about FPS games?", "The tools FPS players ask for most are a sensitivity converter, a crosshair overlay, and an FPS/ping monitor — they keep your aim consistent and tell you whether a bad round is you or your connection. BuffForge does not list one yet: we only add tools whose numbers can be sourced and checked."),
            ("How do you check numbers?", "Public sources only. Every tool shows its data version, sources, and review date. Corrections are welcome — see About."),
        ],
        "open": "Open the tool",
        "trust": [
            ("Public sources only", "Numbers come from official notes, official or well-sourced wikis, and public APIs. We never invent odds."),
            ("Versioned and dated", "Every tool shows its data version, sources, and review date. Early-access figures can change."),
            ("Tell us when we are wrong", "If we get a number wrong, tell us. We correct it."),
        ],
        "reviewed": "Data reviewed Nov 13, 2026",
    },
    "ru": {
        "title": "BuffForge — игровые инструменты, трекеры и калькуляторы",
        "desc": "Бесплатные игровые инструменты, трекеры и калькуляторы. У каждой цифры — источник и дата проверки. Без регистрации и рекламы.",
        "h1": "Игровые инструменты, трекеры и калькуляторы",
        "lede": "BuffForge — бесплатные игровые инструменты, трекеры и калькуляторы. У каждой цифры есть открытый источник и дата проверки. Регистрации и рекламы нет. Инструменты сгруппированы по играм: откройте игру, чтобы найти трекеры, проверки и — когда появятся проверенные цифры — гайды. BuffForge — независимый фанатский проект, не связанный с издателями. Текстовые гайды выходят только после проверки цифр; сейчас в центре — сами инструменты.",
        "kicker": "С источником и датой, по играм",
        "primary": "К избранным инструментам",
        "chips": ["Только открытые источники", "Дата проверки у каждой цифры", "Без регистрации и рекламы"],
        "secondary": "Как мы проверяем цифры",
        "featured_h": "Избранные инструменты",
        "featured_label": "Избранное",
        "featured_sub": "Калькуляторы, трекеры и проверки, которые помогают планировать заранее, следить за прогрессом и принимать лучшие решения в игре.",
        "games_h": "Обзор игр",
        "games_label": "По играм",
        "games_intro": "Хабы по играм с калькуляторами, трекерами и проверками — всё собрано по играм.",
        "how_h": "Как мы проверяем каждую цифру",
        "how_label": "Метод",
        "faq_h": "Частые вопросы",
        "faq_label": "Вопросы",
        "faq": [
            ("Играю в MMO — какие инструменты правда полезны?", "Те, что следят за сбросами. В AION 2 ежедневные задания сбрасываются в 10:00 по Москве, еженедельные — в среду в 10:00: пропустил сброс — и день потерян. Трекер на этом сайте показывает ваши задания и считает время до каждого сброса, так что перед выходом из игры видно, что ещё не сделано."),
            ("Играю в idle-игры — как не тратить предметы зря?", "Проверяйте шансы до того, как потратить предметы. В Desktop Pension Squad девять предметов уходят в одно слияние, а шансы игра не показывает. Калькулятор использует таблицу Workshop v1.0.2 (сборка 26611958), сверенную как неизменную со страницей вики v1.0.6, и сравнивает слияние с продажей."),
            ("Играю в одиночные игры — что проверить?", "Четыре вещи: место на диске, время открытия, издание и консоль. GTA 6 вышла 19 ноября 2026 года. На сайте есть проверка минимума 212 ГБ, время открытия по региону магазина, Standard и Ultimate по ценам США и проверка консоли — только официальные цифры."),
            ("А что с FPS-играми?", "Чаще всего игроки в FPS просят конвертер чувствительности, прицел-оверлей и монитор FPS и пинга: они держат прицеливание стабильным и показывают, виноваты ли вы или соединение. На BuffForge такого инструмента пока нет: мы добавляем только то, чьи цифры можно подтвердить и проверить."),
            ("Как вы проверяете цифры?", "Только открытые источники. У каждого инструмента видны версия, источники и дата проверки. Исправления приветствуются — см. «О проекте»."),
        ],
        "open": "Открыть",
        "trust": [
            ("Только открытые источники", "Цифры берутся из официальных заметок, проверяемых вики и открытых API. Мы не выдумываем шансы."),
            ("С версией и датой", "У каждого инструмента видны версия данных, источники и дата проверки. Цифры раннего доступа могут измениться."),
            ("Напишите, если мы ошиблись", "Если цифра неверна — напишите. Мы исправим."),
        ],
        "reviewed": "Данные проверены 13 ноября 2026 года",
    },
}


ARROW_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')

GAME_CLS = {"desktop-pension-squad": "dps", "aion-2": "aion", "gta-6": "gta",
            "rob-run": "rob", "path-of-exile-2": "poe"}
FEATURE_ART = {"desktop-pension-squad": DPS_FEATURE, "aion-2": AION_FEATURE,
               "gta-6": GTA_FEATURE, "rob-run": ROB_FEATURE,
               "path-of-exile-2": POE2_FEATURE}
COVER_ART = {"desktop-pension-squad": DPS_COVER, "aion-2": AION_COVER,
             "gta-6": GTA_COVER, "rob-run": ROB_COVER,
             "path-of-exile-2": POE2_COVER}
GSUB = {
    "desktop-pension-squad": {"en": "Steam — Free to play", "ru": "Steam — бесплатно"},
    "aion-2": {"en": "Global servers — 1&nbsp;live tool", "ru": "Глобальные серверы — 1&nbsp;инструмент"},
    "gta-6": {"en": "PS5 and Xbox Series&nbsp;— out since 19&nbsp;Nov&nbsp;2026", "ru": "PS5 и Xbox Series&nbsp;— вышла 19&nbsp;ноября&nbsp;2026"},
    "rob-run": {"en": "Steam Early Access — free", "ru": "Ранний доступ Steam — бесплатно"},
    "path-of-exile-2": {"en": "Steam — 1.0 launches 11&nbsp;Dec&nbsp;2026", "ru": "Steam — 1.0 выйдет 11&nbsp;декабря&nbsp;2026"},
}
PLANNED_HOME = {
    "desktop-pension-squad": {
        "en": "A craft-odds calculator and a drop finder are planned, after their tables are checked. There is no engraving planner here.",
        "ru": "Калькулятор крафта и поиск дропа — в планах, после проверки таблиц. Планировщика рун на сайте нет."},
}
GO_LABELS = {
    "dps-fuse-salvage-calculator": {"en": "Open the calculator", "ru": "Открыть калькулятор"},
    "aion-2-daily-tracker": {"en": "Open the tracker", "ru": "Открыть трекер"},
    "gta-6-storage-check": {"en": "Open the checker", "ru": "Открыть проверку"},
    "gta-6-launch-countdown": {"en": "Open the countdown", "ru": "Открыть отсчёт"},
}
ICONS = {
    "dps-fuse-salvage-calculator": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
    "dps-wiki-search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
    "aion-2-daily-tracker": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "gta-6-launch-countdown": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
    "gta-6-storage-check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12H2M16 6H2M16 18H2"/><rect x="16" y="4" width="6" height="4" rx="1"/><rect x="16" y="16" width="6" height="4" rx="1"/></svg>',
    "gta-6-editions": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3 4 8v8l8 5 8-5V8l-8-5z"/><path d="M12 13V3M4 8l8 5 8-5"/></svg>',
    "gta-6-compatibility": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="6" width="20" height="12" rx="2"/><path d="M6 10h.01M10 10h4"/></svg>',
    "gta-6-wanted-evidence-helper": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "gta-6-ps5-frame-interpolation": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="6" width="11" height="8" rx="1.5"/><rect x="10" y="10" width="11" height="8" rx="1.5"/></svg>',
    "rob-run-federal-raid-countdown": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "rob-run-loot-profit-calculator": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h10"/></svg>',
    "rob-run-squad-loot-splitter": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="8" cy="9" r="2.2"/><circle cx="16" cy="9" r="2.2"/><path d="M4.5 18c.6-2.2 2.2-3.2 3.5-3.2s2.9 1 3.5 3.2M12.5 18c.6-2.2 2.2-3.2 3.5-3.2s2.9 1 3.5 3.2"/></svg>',
    "rob-run-server-status": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="6" rx="1"/><rect x="3" y="14" width="18" height="6" rx="1"/><path d="M7 7h.01M7 17h.01M12 7h6"/></svg>',
    "rob-run-wipe-planner": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4a3 3 0 0 1 6 0M9 11l2 2 4-4"/></svg>',
    "rob-run-kak-ubrat-lagi": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19V5"/><path d="M4 19h16"/><path d="M8 16V11"/><path d="M12 16V7"/><path d="M16 16v-6"/></svg>',
    "poe2-launch-countdown": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
    "poe2-class-selector": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="3.5"/><path d="M5 20c1-3.5 3.5-5 7-5s6 1.5 7 5"/></svg>',
    "poe2-resistance-calculator": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "poe2-campaign-checklist": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4a3 3 0 0 1 6 0M9 11l2 2 4-4"/></svg>',
}
CHIP_ICONS = [
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6 9 17l-5-5"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
]

# Hero preview card (prototype): a light device mock showing the three live
# tools. Static copy — the numbers are the same figures the tools show.
HERO_VISUAL = {
    "en": (
        '<div class="hero-visual" aria-hidden="true"><div class="device">'
        '<div class="device-bar"><i></i><i></i><i></i><span>buffforge.com — fuse calculator</span></div>'
        '<div class="mini"><div class="lab">Desktop Pension Squad <b>LIVE</b></div>'
        '<div class="big">50.12% <small>Legendary, per fuse</small></div>'
        '<p class="note">Nine Epic items, Lv. 10–15. Listed odds from client v1.0.2, same row on the v1.0.6 wiki page.</p>'
        '<div class="odds-row"><div class="odds-pill"><em>Epic</em><strong>49.88%</strong></div>'
        '<div class="odds-pill"><em>Legendary</em><strong>50.12%</strong></div>'
        '<div class="odds-pill"><em>9 items →</em><strong>1 fuse</strong></div></div></div>'
        '<div class="mini"><div class="lab">AION 2 daily reset <b>07:00 UTC</b></div>'
        '<div class="big">Live <small>countdown · local ticks</small></div>'
        '<p class="note">Duties clear themselves at reset. Stored in this browser only.</p></div>'
        '<div class="mini"><div class="lab">GTA 6 storage <b>212 GB</b></div>'
        '<div class="big">Check <small>free space vs PlayStation figure</small></div>'
        '<div class="bar"><span></span></div>'
        '<p class="note">Official minimum free space. Out since 19 Nov 2026.</p></div>'
        '</div></div>'
    ),
    "ru": (
        '<div class="hero-visual" aria-hidden="true"><div class="device">'
        '<div class="device-bar"><i></i><i></i><i></i><span>buffforge.com — калькулятор слияния</span></div>'
        '<div class="mini"><div class="lab">Desktop Pension Squad <b>LIVE</b></div>'
        '<div class="big">50.12% <small>Legendary за одно слияние</small></div>'
        '<p class="note">Девять предметов Epic, ур. 10–15. Шансы клиента v1.0.2, та же строка на странице вики v1.0.6.</p>'
        '<div class="odds-row"><div class="odds-pill"><em>Epic</em><strong>49.88%</strong></div>'
        '<div class="odds-pill"><em>Legendary</em><strong>50.12%</strong></div>'
        '<div class="odds-pill"><em>9 шт. →</em><strong>1 слияние</strong></div></div></div>'
        '<div class="mini"><div class="lab">AION 2, ежедневный сброс <b>07:00 UTC</b></div>'
        '<div class="big">Live <small>таймер · локальные отметки</small></div>'
        '<p class="note">Отметки сбрасываются сами. Хранятся только в этом браузере.</p></div>'
        '<div class="mini"><div class="lab">GTA 6, место на диске <b>212 GB</b></div>'
        '<div class="big">Check <small>свободное место и цифра PlayStation</small></div>'
        '<div class="bar"><span></span></div>'
        '<p class="note">Официальный минимум свободного места. Вышла 19 ноября 2026.</p></div>'
        '</div></div>'
    ),
}


def featured_card(lang, tool, feature=False):
    c = HOME_COPY[lang]
    game = GAMES_DATA[tool["game"]]
    cls = GAME_CLS[tool["game"]]
    title = (tool.get("cardTitle") or {}).get(lang) or tool["title"][lang]
    blurb = (tool.get("cardBlurb") or {}).get(lang) or tool["blurb"][lang]
    go = GO_LABELS.get(tool["id"], {}).get(lang, c["open"])
    if tool["status"] == "live":
        status = "Live" if lang == "en" else "Доступно"
    else:
        status = "Unverified" if lang == "en" else "Не проверено"
    extra = " fcard-feature" if feature else ""
    return (
        '<a class="fcard%s" href="%s">'
        '<div class="fcard-media %s"><div class="art">%s</div></div>'
        '<div class="fcard-body"><div class="tag %s">%s &middot; %s</div>'
        '<h3>%s</h3><p>%s</p>'
        '<span class="go">%s %s</span></div></a>'
        % (extra, tool_url(lang, tool), cls, FEATURE_ART[tool["game"]],
           cls, game["name"][lang], status, title, blurb, go, ARROW_SVG)
    )


def tool_row(lang, t):
    open_l = "Open" if lang == "en" else "Открыть"
    return (
        '<a class="tool-row" href="%s">'
        '<span class="tool-ico" aria-hidden="true">%s</span>'
        '<span><span class="t-name">%s %s</span>'
        '<span class="t-blurb">%s</span></span>'
        '<span class="t-go">%s %s</span></a>'
        % (tool_url(lang, t),
           ICONS.get(t["id"], ICONS["dps-fuse-salvage-calculator"]),
           t["title"][lang], badge(lang, t), t["blurb"][lang], open_l, ARROW_SVG)
    )


def game_block(lang, game):
    c = HOME_COPY[lang]
    tools = tools_for(game["id"])
    rows = "".join(tool_row(lang, t) for t in tools)
    hub = game["hub"] if "hub" in game else {"en": "/%s/" % game["slug"], "ru": "/ru/%s/" % game["slug"]}
    planned = PLANNED_HOME.get(game["id"], {}).get(lang, "")
    planned_html = '<p class="planned">%s</p>' % planned if planned else ""
    short = GAMES[game["id"]].get("short", game["name"][lang])
    return (
        '<article class="game-panel" id="%s">'
        '<div class="game-cover %s"><div class="art">%s</div>'
        '<div class="gname">%s</div><div class="gsub">%s</div></div>'
        '<div class="game-body"><div class="head"><h3>%s</h3>'
        '<a class="view-all" href="%s">%s %s</a></div>'
        '<p class="tagline">%s</p>%s%s</div></article>'
        % (game["slug"], GAME_CLS[game["id"]], COVER_ART[game["id"]],
           short, GSUB[game["id"]][lang], game["name"][lang],
           hub[lang], game_anchor(lang, game), ARROW_SVG,
           game["tagline"][lang], rows, planned_html)
    )


def home_page(lang):
    import html as _html
    import json as _json

    c = HOME_COPY[lang]
    is_ru = (lang == "ru")
    prefix = "/ru" if is_ru else ""

    # Gather live tools & guides
    live_tools = [t for t in TOOLS if t.get("status") == "live"]
    live_guides = []
    for g in GUIDES:
        if g.get("status") != "live":
            continue
        langs = g.get("langs")
        if langs is not None and lang not in langs:
            continue
        if lang not in (g.get("title") or {}):
            continue
        live_guides.append(g)

    # Sort games with Path of Exile 2 promoted first for 1.0 launch window
    preferred_order = ["path-of-exile-2", "gta-6", "rob-run", "desktop-pension-squad", "aion-2"]
    games_sorted = sorted(
        game_order(lang),
        key=lambda g: preferred_order.index(g["id"]) if g["id"] in preferred_order else 99
    )

    # Bilingual UI strings for v2.2 workbench & sections
    ui = {
        "en": {
            "pulse_poe": "PoE 2 1.0 Launch",
            "pulse_aion": "AION 2 Daily Reset",
            "pulse_gta": "GTA 6 Live",
            "pulse_days_out": "days out",
            "eyebrow": "Independent · Sourced · Zero Ads",
            "h1": 'Game tools built from <em>checked numbers</em>.',
            "lede": "Live timers, calculators, and sourced guides — organized by game. Every figure cites a public source and review date, with zero logins and zero ads.",
            "search_ph": "Search 18 tools & guides (e.g. PoE 2, resistance, wipe, fuse, GTA 6)...",
            "stat_games": "Games",
            "stat_tools": "Live tools",
            "stat_guides": "Guides",
            "stat_ads": "Ads or logins",
            "tab_poe": "PoE 2 1.0",
            "tab_aion": "AION 2 Reset",
            "tab_gta": "GTA 6 Space",
            "wb_live": "Live",
            "poe_kicker": "Dec 11, 2026 (PST) · Free-to-Play Launch",
            "poe_title": "Path of Exile 2 — 1.0 Release Countdown",
            "poe_days": "Days", "poe_hrs": "Hrs", "poe_min": "Min", "poe_sec": "Sec",
            "poe_pills": ["10 Classes (Duelist & Shadow)", "Acts 5–6 Campaign", "Conquerors League"],
            "poe_cta1": "Read 1.0 Full Guide",
            "poe_cta2": "Open Countdown",
            "aion_kicker": "Global Servers · Auto-Resets at 07:00 UTC",
            "aion_title": "AION 2 Daily & Weekly Reset Clock",
            "aion_daily": "Next daily reset (07:00 UTC)",
            "aion_weekly": "Next weekly reset (Wed)",
            "aion_checks": ["Daily quests & contracts cleared", "Daily dungeon entries used", "Weekly raid / boss progress checked"],
            "aion_cta": "Open Full Duty Tracker",
            "gta_kicker": "PS5 & Xbox Series X|S · Official 212 GB Minimum",
            "gta_title": "GTA 6 Quick Free-Space Checker",
            "gta_label": "Your console free space",
            "gta_cta1": "Full Storage Check",
            "gta_cta2": "DPS Fuse Calculator",
            "spot_label": "Spotlight",
            "spot_h": "Hot right now",
            "spot_sub": "Launch-window essentials and our most-used calculators.",
            "flag_badge": "NEW · PILLAR GUIDE · UPDATED NOV 26",
            "flag_title": "Path of Exile 2 1.0 Full Release Guide (Dec 11, 2026)",
            "flag_desc": "Complete Free-to-Play launch breakdown: all 10 classes & 26 ascendancies, Duelist & Shadow weapons, Acts 5–6, Conquerors of Wraeclast endgame, EA wipe rules, and pre-launch checklist.",
            "flag_cta": "Read the complete 1.0 guide",
            "flag_tools": [
                ("Launch Countdown", "/path-of-exile-2/launch-countdown/"),
                ("Class Selector", "/path-of-exile-2/class-selector/"),
                ("Resistance Calc", "/path-of-exile-2/resistance-calculator/"),
                ("Campaign Checklist", "/path-of-exile-2/campaign-checklist/"),
            ],
            "hubs_label": "Directory",
            "hubs_h": "Explore by game or filter everything",
            "hubs_sub": "Jump into a dedicated game hub, or filter all live tools and guides instantly.",
            "hub_open": "Open hub →",
            "all_games": "All games",
            "type_all": "All",
            "type_tools": "Tools",
            "type_guides": "Guides",
            "kind_tool": "Tool",
            "kind_guide": "Guide",
            "reviewed_prefix": "Reviewed",
            "open_short": "Open ↗",
            "read_short": "Read guide ↗",
            "guides_label": "Editorial Guides",
            "guides_h": "Latest sourced guides",
            "guides_sub": "Deep-dive guides written only when every figure can be verified against official announcements or public tests.",
            "trust_label": "The method",
            "trust_h": "How we check every number",
            "no_hits": "No matching tools or guides. Try another keyword.",
            "gta_ok": "Ready to install — comfortable headroom above 230 GB.",
            "gta_warn": "Meets the 212 GB minimum, but tight for patches (230 GB+ recommended).",
            "gta_bad": "Not enough space — free up at least {need} GB to meet the 212 GB minimum.",
        },
        "ru": {
            "pulse_poe": "Релиз PoE 2 1.0",
            "pulse_aion": "Сброс AION 2",
            "pulse_gta": "GTA 6 вышла",
            "pulse_days_out": "дн. с релиза",
            "eyebrow": "Независимо · С источниками · Без рекламы",
            "h1": 'Игровые инструменты на <em>проверенных цифрах</em>.',
            "lede": "Живые таймеры, калькуляторы и гайды по играм. У каждой цифры указан открытый источник и дата проверки — без регистрации и рекламы.",
            "search_ph": "Поиск по 18 инструментам и гайдам (PoE 2, вайп, слияние, GTA 6)...",
            "stat_games": "Игр",
            "stat_tools": "Инструментов",
            "stat_guides": "Гайдов",
            "stat_ads": "Рекламы",
            "tab_poe": "PoE 2 1.0",
            "tab_aion": "Сброс AION 2",
            "tab_gta": "Место GTA 6",
            "wb_live": "Live",
            "poe_kicker": "11 декабря 2026 (PST) · Переход на Free-to-Play",
            "poe_title": "Path of Exile 2 — обратный отсчёт до 1.0",
            "poe_days": "Дн", "poe_hrs": "Час", "poe_min": "Мин", "poe_sec": "Сек",
            "poe_pills": ["10 классов (Дуэлянт и Тень)", "Акты 5–6", "Лига Conquerors"],
            "poe_cta1": "Читать гайд по 1.0",
            "poe_cta2": "Открыть отсчёт",
            "aion_kicker": "Глобальные серверы · Сброс в 10:00 МСК (07:00 UTC)",
            "aion_title": "Таймер сброса AION 2 (ежедневный и недельный)",
            "aion_daily": "До ежедневного сброса",
            "aion_weekly": "До сброса в среду",
            "aion_checks": ["Ежедневные задания выполнены", "Попытки в подземелья использованы", "Недельные боссы проверены"],
            "aion_cta": "Открыть полный трекер",
            "gta_kicker": "PS5 и Xbox Series X|S · Минимум 212 ГБ",
            "gta_title": "Быстрая проверка места под GTA 6",
            "gta_label": "Свободно на консоли",
            "gta_cta1": "Подробная проверка",
            "gta_cta2": "Калькулятор DPS",
            "spot_label": "В фокусе",
            "spot_h": "Актуально сейчас",
            "spot_sub": "Главные материалы к релизу и самые востребованные калькуляторы.",
            "flag_badge": "НОВОЕ · ПОЛНЫЙ ГАЙД · ОБНОВЛЕНО 26 НОЯ",
            "flag_title": "Гайд по релизу Path of Exile 2 1.0 (11 декабря 2026)",
            "flag_desc": "Полный разбор выхода на Free-to-Play: все 10 классов и 26 восхождений, Дуэлянт и Тень, акты 5–6, лига Conquerors of Wraeclast, правила переноса из EA и чек-лист.",
            "flag_cta": "Читать полный гайд по 1.0",
            "flag_tools": [
                ("Отсчёт до 1.0", "/ru/path-of-exile-2/launch-countdown/"),
                ("Подбор класса", "/ru/path-of-exile-2/class-selector/"),
                ("Калькулятор резистов", "/ru/path-of-exile-2/resistance-calculator/"),
                ("Чек-лист кампании", "/ru/path-of-exile-2/campaign-checklist/"),
            ],
            "hubs_label": "Каталог",
            "hubs_h": "Выберите игру или отфильтруйте всё",
            "hubs_sub": "Откройте хаб нужной игры или мгновенно отфильтруйте инструменты и гайды.",
            "hub_open": "Открыть хаб →",
            "all_games": "Все игры",
            "type_all": "Всё",
            "type_tools": "Инструменты",
            "type_guides": "Гайды",
            "kind_tool": "Инструмент",
            "kind_guide": "Гайд",
            "reviewed_prefix": "Проверено",
            "open_short": "Открыть ↗",
            "read_short": "Читать ↗",
            "guides_label": "Редакционные гайды",
            "guides_h": "Свежие проверенные гайды",
            "guides_sub": "Подробные руководства только по тем играм, где каждую цифру можно подтвердить официальными источниками.",
            "trust_label": "Метод",
            "trust_h": "Как мы проверяем каждую цифру",
            "no_hits": "Ничего не найдено. Попробуйте другой запрос.",
            "gta_ok": "Места достаточно — есть комфортный запас свыше 230 ГБ.",
            "gta_warn": "Проходит минимум 212 ГБ, но впритык для патчей (лучше 230+ ГБ).",
            "gta_bad": "Не хватает места — освободите минимум {need} ГБ до порога 212 ГБ.",
        },
    }[lang]

    # Top live pulse bar
    pulse_html = (
        '<div class="bf-pulse" role="region" aria-label="Live game timers"><div class="bf-pulse-inner">'
        '<a class="bf-pulse-item" href="%s/path-of-exile-2/launch-countdown/">'
        '<span class="bf-pulse-dot poe" aria-hidden="true"></span>'
        '<span class="bf-pulse-label">%s</span>'
        '<span class="bf-pulse-val" data-live="poe-short">--d --h --m</span></a>'
        '<span class="bf-pulse-sep" aria-hidden="true"></span>'
        '<a class="bf-pulse-item" href="%s/aion-2/daily-tracker/">'
        '<span class="bf-pulse-dot" aria-hidden="true"></span>'
        '<span class="bf-pulse-label">%s</span>'
        '<span class="bf-pulse-val" data-live="aion-daily">--:--:--</span></a>'
        '<span class="bf-pulse-sep" aria-hidden="true"></span>'
        '<a class="bf-pulse-item" href="%s/gta-6/">'
        '<span class="bf-pulse-label">%s</span>'
        '<span class="bf-pulse-val" data-live="gta-days">-- %s</span></a>'
        '</div></div>'
        % (prefix, ui["pulse_poe"], prefix, ui["pulse_aion"], prefix, ui["pulse_gta"], ui["pulse_days_out"])
    )

    # Interactive 3-tab hero workbench
    poe_pills_html = "".join('<span class="bf-wb-pill">%s</span>' % p for p in ui["poe_pills"])
    aion_checks_html = "".join(
        '<label class="bf-mini-check"><input type="checkbox" data-aion-chk="%d"><span>%s</span></label>'
        % (idx, txt) for idx, txt in enumerate(ui["aion_checks"])
    )
    wb_html = (
        '<div class="bf-wb" id="bf-workbench">'
        '<div class="bf-wb-bar">'
        '<div class="bf-wb-tabs" role="tablist">'
        '<button class="bf-wb-tab" role="tab" type="button" data-tab="poe" aria-selected="true"><span class="dot"></span>%s</button>'
        '<button class="bf-wb-tab" role="tab" type="button" data-tab="aion" aria-selected="false"><span class="dot"></span>%s</button>'
        '<button class="bf-wb-tab" role="tab" type="button" data-tab="gta" aria-selected="false"><span class="dot"></span>%s</button>'
        '</div><span class="bf-wb-live">%s</span></div>'
        # Pane 1: PoE 2
        '<div class="bf-wb-pane active" data-pane="poe" role="tabpanel">'
        '<p class="bf-wb-kicker">%s</p><h2 class="bf-wb-title">%s</h2>'
        '<div class="bf-clock-grid">'
        '<div class="bf-clock-box"><strong data-live="poe-d">--</strong><span>%s</span></div>'
        '<div class="bf-clock-box"><strong data-live="poe-h">--</strong><span>%s</span></div>'
        '<div class="bf-clock-box"><strong data-live="poe-m">--</strong><span>%s</span></div>'
        '<div class="bf-clock-box"><strong data-live="poe-s">--</strong><span>%s</span></div>'
        '</div>'
        '<div class="bf-wb-meta">%s</div>'
        '<div class="bf-wb-actions">'
        '<a class="btn btn-primary" href="%s/path-of-exile-2/1-0-full-release-guide/">%s %s</a>'
        '<a class="btn btn-secondary" href="%s/path-of-exile-2/launch-countdown/">%s</a>'
        '</div></div>'
        # Pane 2: AION 2
        '<div class="bf-wb-pane" data-pane="aion" role="tabpanel">'
        '<p class="bf-wb-kicker">%s</p><h2 class="bf-wb-title">%s</h2>'
        '<div class="bf-reset-row">'
        '<div class="bf-reset-box"><small>%s</small><strong data-live="aion-daily">--:--:--</strong></div>'
        '<div class="bf-reset-box"><small>%s</small><strong data-live="aion-weekly">--d --h</strong></div>'
        '</div>'
        '<div class="bf-mini-checks">%s</div>'
        '<div class="bf-wb-actions">'
        '<a class="btn btn-primary" href="%s/aion-2/daily-tracker/">%s %s</a>'
        '</div></div>'
        # Pane 3: GTA 6 interactive storage slider
        '<div class="bf-wb-pane" data-pane="gta" role="tabpanel">'
        '<p class="bf-wb-kicker">%s</p><h2 class="bf-wb-title">%s</h2>'
        '<div class="bf-slider-box">'
        '<div class="bf-slider-top"><label for="bf-gta-range">%s</label>'
        '<span class="bf-slider-val" id="bf-gta-gb">240 GB</span></div>'
        '<input class="bf-range" id="bf-gta-range" type="range" min="100" max="400" step="5" value="240">'
        '<p class="bf-verdict ok" id="bf-gta-verdict">%s</p></div>'
        '<div class="bf-wb-actions">'
        '<a class="btn btn-primary" href="%s/gta-6/storage-check/">%s %s</a>'
        '<a class="btn btn-secondary" href="%s/desktop-pension-squad/fuse-salvage-calculator/">%s</a>'
        '</div></div>'
        '</div>'
        % (
            ui["tab_poe"], ui["tab_aion"], ui["tab_gta"], ui["wb_live"],
            ui["poe_kicker"], ui["poe_title"],
            ui["poe_days"], ui["poe_hrs"], ui["poe_min"], ui["poe_sec"],
            poe_pills_html, prefix, ui["poe_cta1"], ARROW_SVG, prefix, ui["poe_cta2"],
            ui["aion_kicker"], ui["aion_title"], ui["aion_daily"], ui["aion_weekly"],
            aion_checks_html, prefix, ui["aion_cta"], ARROW_SVG,
            ui["gta_kicker"], ui["gta_title"], ui["gta_label"], ui["gta_ok"],
            prefix, ui["gta_cta1"], ARROW_SVG, prefix, ui["gta_cta2"],
        )
    )

    # Spotlight Bento: Flagship PoE 2 1.0 Guide + Top 3 featured tools
    flag_chips = "".join(
        '<a class="bf-flag-chip" href="%s">%s ↗</a>' % (u, lbl)
        for lbl, u in ui["flag_tools"]
    )
    feats = featured_for(lang)[:3]
    spot_cards = []
    GUIDE_COVERS = {
        "poe2-1-0-full-release-guide": "/assets/games/path-of-exile-2-wide.jpg",
        "gta-6-ps5-frame-interpolation": "/assets/games/gta-6-wide.jpg",
        "rob-run-kak-ubrat-lagi": "/assets/rob-run/lag-hero.webp",
        "rob-run-failed-to-enter-location": "/assets/rob-run/fel-hero.webp",
    }

    for t in feats:
        g = GAMES_DATA[t["game"]]
        cls = GAME_CLS[t["game"]]
        title = (t.get("cardTitle") or {}).get(lang) or t["title"][lang]
        blurb = (t.get("cardBlurb") or {}).get(lang) or t["blurb"][lang]
        rev = t.get("updated") or t.get("dataReviewed") or ""
        thumb = "/assets/games/%s-cover.jpg" % g["slug"]
        spot_cards.append(
            '<a class="bf-spot-card %s" href="%s">'
            '<div class="bf-spot-thumb"><img src="%s" alt="%s" loading="lazy"></div>'
            '<div class="bf-spot-content">'
            '<div><div class="bf-spot-meta"><span>%s</span><span>%s</span></div>'
            '<h3>%s</h3><p>%s</p></div>'
            '<span class="bf-spot-go">%s %s</span></div></a>'
            % (cls, tool_url(lang, t), thumb, _html.escape(g["name"][lang], quote=True),
               g["name"][lang], rev, title, blurb,
               GO_LABELS.get(t["id"], {}).get(lang, ui["open_short"]), ARROW_SVG)
        )

    bento_html = (
        '<div class="bf-bento">'
        '<article class="bf-flagship">'
        '<div class="bf-flag-media"><img src="/assets/games/path-of-exile-2-wide.jpg" alt="Path of Exile 2 1.0 Full Release"></div>'
        '<div class="bf-flag-body">'
        '<div><div class="bf-flag-top"><span class="bf-flag-badge">%s</span>'
        '<span class="bf-flag-cd" data-live="poe-short">--d --h --m</span></div>'
        '<h3>%s</h3><p>%s</p>'
        '<div class="bf-flag-links">%s</div></div>'
        '<a class="bf-flag-cta" href="%s/path-of-exile-2/1-0-full-release-guide/">%s %s</a>'
        '</div></article>'
        '<div class="bf-bento-stack">%s</div>'
        '</div>'
        % (ui["flag_badge"], ui["flag_title"], ui["flag_desc"], flag_chips,
           prefix, ui["flag_cta"], ARROW_SVG, "".join(spot_cards))
    )

    # 5-Game Hub Strip with real wide game covers
    hub_tiles = []
    for g in games_sorted:
        cls = GAME_CLS[g["id"]]
        t_cnt = len(tools_for(g["id"]))
        g_cnt = len(guides_for(g["id"], lang))
        if g_cnt:
            cnt_lbl = "%dT · %dG" % (t_cnt, g_cnt)
        else:
            unit = ("tool" if t_cnt == 1 else "tools") if not is_ru else "инстр."
            cnt_lbl = "%d %s" % (t_cnt, unit)
        hub_href = "/%s/" % g["slug"] if not is_ru else "/ru/%s/" % g["slug"]
        cover_src = "/assets/games/%s-wide.jpg" % g["slug"]
        hub_tiles.append(
            '<a class="bf-hub-tile %s" href="%s">'
            '<div class="bf-hub-cover"><img src="%s" alt="%s" loading="lazy">'
            '<span class="bf-hub-count">%s</span></div>'
            '<div class="bf-hub-body">'
            '<div><h3>%s</h3><p>%s</p></div>'
            '<span class="bf-hub-link">%s</span></div></a>'
            % (cls, hub_href, cover_src, _html.escape(g["name"][lang], quote=True),
               cnt_lbl, g["name"][lang], g["tagline"][lang], ui["hub_open"])
        )

    # Interactive Filterable Directory (all tools + all guides)
    dir_cards = []
    search_index = []
    # Put guides first or interleaved by game order so PoE 2 shines right away
    ordered_items = []
    for g in games_sorted:
        for gd in guides_for(g["id"], lang):
            ordered_items.append(("guide", g, gd))
        for tl in tools_for(g["id"]):
            if tl.get("status") == "live":
                ordered_items.append(("tool", g, tl))

    for kind, g, item in ordered_items:
        cls = GAME_CLS[g["id"]]
        href = guide_url(lang, item) if kind == "guide" else tool_url(lang, item)
        title = item["title"][lang] if kind == "guide" else ((item.get("cardTitle") or {}).get(lang) or item["title"][lang])
        blurb = item["blurb"][lang] if kind == "guide" else ((item.get("cardBlurb") or {}).get(lang) or item["blurb"][lang])
        rev = item.get("updated") or item.get("dataReviewed") or ""
        kind_lbl = ui["kind_guide"] if kind == "guide" else ui["kind_tool"]
        action_lbl = ui["read_short"] if kind == "guide" else ui["open_short"]
        search_txt = ("%s %s %s %s" % (g["name"][lang], title, blurb, kind_lbl)).lower()
        search_index.append({
            "t": title, "g": g["name"][lang], "k": kind_lbl, "u": href, "q": search_txt
        })
        ico_svg = ICONS.get(item.get("id", ""), ICONS["dps-wiki-search"] if kind == "guide" else ICONS["dps-fuse-salvage-calculator"])
        dir_cards.append(
            '<a class="bf-dir-card" href="%s" data-game="%s" data-kind="%s" data-q="%s">'
            '<div><div class="bf-dir-top">'
            '<span class="bf-dir-game %s">%s</span>'
            '<span class="bf-dir-kind %s">%s</span></div>'
            '<div class="bf-dir-head-row"><span class="bf-dir-ico %s" aria-hidden="true">%s</span>'
            '<h3>%s</h3></div><p>%s</p></div>'
            '<div class="bf-dir-foot"><span>%s</span><b>%s</b></div></a>'
            % (href, g["id"], kind, _html.escape(search_txt, quote=True),
               cls, g["name"][lang], kind, kind_lbl,
               cls, ico_svg,
               title, blurb, ("%s %s" % (ui["reviewed_prefix"], rev)) if rev else "", action_lbl)
        )

    filter_pills = ['<button class="bf-pill active" type="button" data-game="all">%s (%d)</button>' % (ui["all_games"], len(ordered_items))]
    for g in games_sorted:
        cnt = len([x for x in ordered_items if x[1]["id"] == g["id"]])
        filter_pills.append(
            '<button class="bf-pill" type="button" data-game="%s"><span class="gdot"></span>%s (%d)</button>'
            % (g["id"], g["name"][lang], cnt)
        )

    # Latest Guides Editorial Shelf
    guides_sorted = sorted(live_guides, key=lambda x: x.get("updated", ""), reverse=True)
    guide_cards = []
    for gd in guides_sorted:
        g = GAMES_DATA[gd["game"]]
        cls = GAME_CLS[gd["game"]]
        gcover = GUIDE_COVERS.get(gd.get("id", ""), "/assets/games/%s-wide.jpg" % g["slug"])
        guide_cards.append(
            '<a class="bf-guide-card %s" href="%s">'
            '<div class="bf-guide-cover"><img src="%s" alt="%s" loading="lazy"></div>'
            '<div class="bf-guide-body">'
            '<div><div class="bf-dir-top">'
            '<span class="bf-dir-game %s">%s</span>'
            '<span class="bf-dir-kind guide">%s</span></div>'
            '<h3>%s</h3><p>%s</p></div>'
            '<div class="bf-dir-foot"><span>%s</span><b>%s</b></div></div></a>'
            % (cls, guide_url(lang, gd), gcover, _html.escape(gd["title"][lang], quote=True),
               cls, g["name"][lang], ui["kind_guide"],
               gd["title"][lang], gd["blurb"][lang], gd.get("updated", ""), ui["read_short"])
        )

    # Trust 3-col cards & FAQ
    trust_cards = "".join(
        '<article class="bf-trust-card"><div class="bf-trust-num">0%d / VERIFIED</div>'
        '<h3>%s</h3><p>%s</p></article>' % (i + 1, t, d)
        for i, (t, d) in enumerate(c["trust"])
    )
    faq_items = "".join(
        '<details%s><summary><h3>%s</h3><span class="plus" aria-hidden="true">'
        '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6">'
        '<path d="M6 1v10M1 6h10"/></svg></span></summary><p>%s</p></details>'
        % (" open" if i == 0 else "", q, a)
        for i, (q, a) in enumerate(c["faq"])
    )

    search_svg = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'

    # Compact interactive JS for timers, tabs, AION checklist, GTA slider, search & directory filters
    js_cfg = _json.dumps({
        "items": search_index,
        "noHits": ui["no_hits"],
        "daysOut": ui["pulse_days_out"],
        "gtaOk": ui["gta_ok"],
        "gtaWarn": ui["gta_warn"],
        "gtaBad": ui["gta_bad"],
    }, ensure_ascii=False)

    script_html = (
        '<script>(function(){'
        'var CFG=%s;'
        'var POE_TARGET=Date.UTC(2026,11,11,8,0,0);'
        'var GTA_LAUNCH=Date.UTC(2026,10,19,0,0,0);'
        'function pad(n){return n<10?"0"+n:""+n;}'
        'function tick(){'
        'var now=Date.now();'
        'var diff=Math.max(0,POE_TARGET-now);'
        'var d=Math.floor(diff/86400000),h=Math.floor((diff%%86400000)/3600000),m=Math.floor((diff%%3600000)/60000),s=Math.floor((diff%%60000)/1000);'
        'document.querySelectorAll("[data-live=poe-d]").forEach(function(e){e.textContent=pad(d);});'
        'document.querySelectorAll("[data-live=poe-h]").forEach(function(e){e.textContent=pad(h);});'
        'document.querySelectorAll("[data-live=poe-m]").forEach(function(e){e.textContent=pad(m);});'
        'document.querySelectorAll("[data-live=poe-s]").forEach(function(e){e.textContent=pad(s);});'
        'var pShort=d+"d "+pad(h)+"h "+pad(m)+"m";'
        'document.querySelectorAll("[data-live=poe-short]").forEach(function(e){e.textContent=pShort;});'
        'var dt=new Date(now);'
        'var nextDaily=Date.UTC(dt.getUTCFullYear(),dt.getUTCMonth(),dt.getUTCDate(),7,0,0);'
        'if(nextDaily<=now)nextDaily+=86400000;'
        'var ad=nextDaily-now;'
        'var ah=Math.floor(ad/3600000),am=Math.floor((ad%%3600000)/60000),as=Math.floor((ad%%60000)/1000);'
        'var aStr=pad(ah)+":"+pad(am)+":"+pad(as);'
        'document.querySelectorAll("[data-live=aion-daily]").forEach(function(e){e.textContent=aStr;});'
        'var dayOfWeek=dt.getUTCDay(),daysToWed=(3-dayOfWeek+7)%%7;'
        'var nextWed=Date.UTC(dt.getUTCFullYear(),dt.getUTCMonth(),dt.getUTCDate()+daysToWed,7,0,0);'
        'if(nextWed<=now)nextWed+=7*86400000;'
        'var aw=nextWed-now,awd=Math.floor(aw/86400000),awh=Math.floor((aw%%86400000)/3600000);'
        'document.querySelectorAll("[data-live=aion-weekly]").forEach(function(e){e.textContent=awd+"d "+pad(awh)+"h";});'
        'var gDays=Math.max(0,Math.floor((now-GTA_LAUNCH)/86400000));'
        'document.querySelectorAll("[data-live=gta-days]").forEach(function(e){e.textContent=gDays+" "+CFG.daysOut;});'
        '}'
        'tick();setInterval(tick,1000);'
        'var wb=document.getElementById("bf-workbench");'
        'if(wb){wb.querySelectorAll(".bf-wb-tab").forEach(function(btn){btn.addEventListener("click",function(){'
        'var t=btn.getAttribute("data-tab");'
        'wb.querySelectorAll(".bf-wb-tab").forEach(function(b){b.setAttribute("aria-selected",b===btn?"true":"false");});'
        'wb.querySelectorAll(".bf-wb-pane").forEach(function(p){p.classList.toggle("active",p.getAttribute("data-pane")===t);});'
        '});});}'
        'var dayKey="bf_aion_"+new Date().toISOString().slice(0,10);'
        'var saved={};try{saved=JSON.parse(localStorage.getItem(dayKey)||"{}");}catch(e){}'
        'document.querySelectorAll("[data-aion-chk]").forEach(function(cb){'
        'var k=cb.getAttribute("data-aion-chk");'
        'if(saved[k]){cb.checked=true;cb.parentElement.classList.add("done");}'
        'cb.addEventListener("change",function(){'
        'saved[k]=cb.checked;cb.parentElement.classList.toggle("done",cb.checked);'
        'try{localStorage.setItem(dayKey,JSON.stringify(saved));}catch(e){}'
        '});});'
        'var rng=document.getElementById("bf-gta-range"),gb=document.getElementById("bf-gta-gb"),vd=document.getElementById("bf-gta-verdict");'
        'if(rng&&gb&&vd){function updGta(){var v=parseInt(rng.value,10);gb.textContent=v+" GB";'
        'if(v>=230){vd.className="bf-verdict ok";vd.textContent=CFG.gtaOk;}'
        'else if(v>=212){vd.className="bf-verdict warn";vd.textContent=CFG.gtaWarn;}'
        'else{vd.className="bf-verdict bad";vd.textContent=CFG.gtaBad.replace("{need}",212-v);}}'
        'rng.addEventListener("input",updGta);updGta();}'
        'var inp=document.getElementById("bf-cmd-input"),res=document.getElementById("bf-cmd-results");'
        'var curGame="all",curKind="all",curQ="";'
        'function applyDir(){'
        'var vis=0;'
        'document.querySelectorAll(".bf-dir-card").forEach(function(card){'
        'var okG=curGame==="all"||card.getAttribute("data-game")===curGame;'
        'var okK=curKind==="all"||card.getAttribute("data-kind")===curKind;'
        'var okQ=!curQ||card.getAttribute("data-q").indexOf(curQ)!==-1;'
        'var show=okG&&okK&&okQ;if(show)vis++;'
        'card.classList.toggle("hidden",!show);'
        '});'
        'var emp=document.getElementById("bf-dir-empty");if(emp)emp.classList.toggle("show",vis===0);'
        '}'
        'var rst=document.getElementById("bf-dir-reset");'
        'if(rst){rst.addEventListener("click",function(){curKind="all";curQ="";if(inp)inp.value="";'
        'document.querySelectorAll(".bf-type-btn").forEach(function(x){x.classList.toggle("active",x.getAttribute("data-kind")==="all");});'
        'applyDir();});}'
        'document.querySelectorAll(".bf-pill").forEach(function(p){p.addEventListener("click",function(){'
        'curGame=p.getAttribute("data-game");'
        'document.querySelectorAll(".bf-pill").forEach(function(x){x.classList.toggle("active",x===p);});'
        'applyDir();});});'
        'document.querySelectorAll(".bf-type-btn").forEach(function(b){b.addEventListener("click",function(){'
        'curKind=b.getAttribute("data-kind");'
        'document.querySelectorAll(".bf-type-btn").forEach(function(x){x.classList.toggle("active",x===b);});'
        'applyDir();});});'
        'if(inp&&res){'
        'function renderDrop(){var q=inp.value.trim().toLowerCase();curQ=q;applyDir();'
        'if(!q){res.classList.remove("open");res.innerHTML="";return;}'
        'var hits=CFG.items.filter(function(it){return it.q.indexOf(q)!==-1;}).slice(0,7);'
        'if(!hits.length){res.innerHTML=\'<div class="bf-cmd-empty">\'+CFG.noHits+\'</div>\';}'
        'else{res.innerHTML=hits.map(function(h){return \'<a class="bf-cmd-hit" href="\'+h.u+\'"><span><strong>\'+h.t+\'</strong><small>\'+h.g+\' · \'+h.k+\'</small></span><span>↗</span></a>\';}).join("");}'
        'res.classList.add("open");}'
        'inp.addEventListener("input",renderDrop);'
        'document.addEventListener("click",function(e){if(!e.target.closest(".bf-cmd-wrap"))res.classList.remove("open");});'
        'document.addEventListener("keydown",function(e){if(e.key==="/"&&document.activeElement.tagName!=="INPUT"&&document.activeElement.tagName!=="TEXTAREA"){e.preventDefault();inp.focus();}});'
        '}'
        '})();</script>'
        % js_cfg
    )

    body = (
        '<main id="main">'
        '%s'
        '<section class="bf-hero"><div class="wrap bf-hero-grid">'
        '<div>'
        '<p class="bf-eyebrow">%s</p>'
        '<h1>%s</h1>'
        '<p class="bf-hero-lede">%s</p>'
        '<div class="bf-cmd-wrap"><div class="bf-cmd">%s'
        '<input id="bf-cmd-input" type="search" placeholder="%s" autocomplete="off" aria-label="%s">'
        '<kbd>/</kbd></div><div class="bf-cmd-results" id="bf-cmd-results"></div></div>'
        '<div class="bf-stats">'
        '<span class="bf-stat"><strong>%d</strong> %s</span>'
        '<span class="bf-stat"><strong>%d</strong> %s</span>'
        '<span class="bf-stat"><strong>%d</strong> %s</span>'
        '<span class="bf-stat"><strong>0</strong> %s</span>'
        '</div></div>'
        '%s'
        '</div></section>'
        '<section class="bf-sec" id="featured"><div class="wrap">'
        '<div class="bf-sec-head"><div><p class="sec-label">%s</p><h2>%s</h2><p class="bf-sec-sub">%s</p></div></div>'
        '%s</div></section>'
        '<section class="bf-sec alt" id="games"><div class="wrap">'
        '<div class="bf-sec-head"><div><p class="sec-label">%s</p><h2>%s</h2><p class="bf-sec-sub">%s</p></div></div>'
        '<div class="bf-hubs-grid">%s</div>'
        '<div class="bf-filter-bar"><div class="bf-pills">%s</div>'
        '<div class="bf-type-seg" role="group">'
        '<button class="bf-type-btn active" type="button" data-kind="all">%s</button>'
        '<button class="bf-type-btn" type="button" data-kind="tool">%s (%d)</button>'
        '<button class="bf-type-btn" type="button" data-kind="guide">%s (%d)</button>'
        '</div></div>'
        '<div class="bf-dir-grid">%s''<div class="bf-dir-empty" id="bf-dir-empty"><p>%s</p><button class="btn btn-secondary" type="button" id="bf-dir-reset">%s</button></div></div>'
        '</div></section>'
        '<section class="bf-sec" id="guides"><div class="wrap">'
        '<div class="bf-sec-head"><div><p class="sec-label">%s</p><h2>%s</h2><p class="bf-sec-sub">%s</p></div></div>'
        '<div class="bf-guides-grid">%s</div>'
        '</div></section>'
        '<section class="bf-sec alt" id="how"><div class="wrap">'
        '<div class="bf-sec-head"><div><p class="sec-label">%s</p><h2>%s</h2></div></div>'
        '<div class="bf-trust-grid">%s</div>'
        '</div></section>'
        '<section class="faq wrap" id="faq">'
        '<p class="sec-label">%s</p><h2>%s</h2>%s</section>'
        '%s'
        '</main>'
        % (
            pulse_html,
            ui["eyebrow"], ui["h1"], ui["lede"],
            search_svg, ui["search_ph"], ui["search_ph"],
            len(games_sorted), ui["stat_games"],
            len(live_tools), ui["stat_tools"],
            len(live_guides), ui["stat_guides"],
            ui["stat_ads"],
            wb_html,
            ui["spot_label"], ui["spot_h"], ui["spot_sub"], bento_html,
            ui["hubs_label"], ui["hubs_h"], ui["hubs_sub"], "".join(hub_tiles),
            "".join(filter_pills), ui["type_all"], ui["type_tools"], len(live_tools),
            ui["type_guides"], len(live_guides), "".join(dir_cards), ui["no_hits"], ("Show all tools & guides" if not is_ru else "Показать все инструменты и гайды"),
            ui["guides_label"], ui["guides_h"], ui["guides_sub"], "".join(guide_cards),
            ui["trust_label"], ui["trust_h"], trust_cards,
            c["faq_label"], c["faq_h"], faq_items,
            script_html,
        )
    )
    canon = "/" if lang == "en" else "/ru/"
    alt = {"en": "/", "ru": "/ru/"}
    return page(lang, c["title"], c["desc"], canon, alt, body,
                jsonld=org_website_jsonld(lang))

# ---------------------------------------------------------------- about
ABOUT_COPY = {
    "en": {
        "title": "About BuffForge — How We Check Our Numbers",
        "desc": "BuffForge is an independent fan project. We build small game tools from public sources only, show every data version and review date, and correct mistakes when readers report them.",
        "h1": "About BuffForge",
        "lede": "An independent fan project. Small tools, checked numbers, no noise.",
        "sections": [
            ("What BuffForge is",
             "BuffForge is a game-by-game tool site. For each game we build small tools — trackers, checkers, calculators — and short guides that answer one specific question. We start with one tool per game and expand only when real players use it."),
            ("What we do",
             "We use public sources only: official patch notes and announcements, official wikis, and public APIs. Every tool shows its data version, its sources, and the date it was last reviewed, so you can check our work."),
            ("What we do not do",
             "We do not datamine game files or reverse-engineer clients. We do not scrape or copy databases or images from Wowhead, Maxroll, Game8, or other sites. We do not publish numbers we have not verified — where sources disagree, we say so and tell you to confirm in-game. We do not write guides for buying games through other regions or bypassing regional restrictions."),
            ("How we check our numbers",
             "Official announcements first. Community trackers are cited as community sources, never presented as official statements. The Wanted helper was checked against the shipped game on 23 Nov 2026 and is labelled Live. If a number turns out to be wrong, we fix the page and update the review date."),
            ("Report a mistake",
             "Found a wrong number? Email <a href=\"mailto:%s\">%s</a> with the page URL and what is wrong. We correct verified mistakes and update the review date on the page." % (EMAIL, EMAIL)),
        ],
    },
    "ru": {
        "title": "О проекте BuffForge — как мы проверяем цифры",
        "desc": "BuffForge — независимый фанатский проект. Небольшие игровые инструменты только из открытых источников: у каждой цифры — версия данных и дата проверки, а ошибки мы исправляем по письмам читателей.",
        "h1": "О проекте BuffForge",
        "lede": "Независимый фанатский проект. Небольшие инструменты, проверенные цифры, без шума.",
        "sections": [
            ("Что такое BuffForge",
             "BuffForge — сайт инструментов, организованный по играм. Для каждой игры мы делаем небольшие инструменты — трекеры, проверки, калькуляторы — и короткие гайды, отвечающие на один конкретный вопрос. Начинаем с одного инструмента на игру и расширяемся, только когда им реально пользуются."),
            ("Что мы делаем",
             "Мы используем только открытые источники: официальные патчноуты и объявления, официальные вики и публичные API. У каждого инструмента указаны версия данных, источники и дата последней проверки — чтобы вы могли перепроверить нашу работу."),
            ("Чего мы не делаем",
             "Мы не разбираем файлы игры и не реверсим клиент. Мы не копируем базы данных и картинки с Wowhead, Maxroll, Game8 и других сайтов. Мы не публикуем непроверенные цифры: если источники расходятся, мы так и пишем и просим свериться в игре. Мы не пишем гайды о покупке игр через другие регионы и обходе региональных ограничений."),
            ("Как мы проверяем цифры",
             "Сначала — официальные объявления. Данные трекеров сообщества указываются как источники сообщества, а не как официальные заявления. Помощник по уликам сверен с вышедшей игрой 23 ноября 2026 и помечен «Доступно». Если цифра оказалась неверной, мы исправляем страницу и обновляем дату проверки."),
            ("Сообщить об ошибке",
             "Нашли неверную цифру? Напишите на <a href=\"mailto:%s\">%s</a>: укажите ссылку на страницу и что именно неверно. Подтверждённые ошибки мы исправляем и обновляем дату проверки на странице." % (EMAIL, EMAIL)),
            ("Почему есть русская версия",
             "Официальный глобальный сайт AION 2 по русскому адресу перенаправляет на английскую версию, поэтому наши русские страницы написаны под вопросы русскоязычных игроков — а не как перевод английских."),
        ],
    },
}


# About UI strings for the demo-style About layout (hero, statement,
# three pillars, method, principles, contact). ABOUT_COPY (Title / H1 /
# lede / description / section texts) is unchanged; the new layout reuses
# those section texts (see the mapping in about_page) and adds only
# chrome strings here. No new facts: the statement and method paragraphs
# are the user-supplied demo copy, translated for RU.
ABOUT_UI = {
    "en": {
        "eyebrow": "About BuffForge",
        "art_title": "Everything in one game hub",
        "art_cards": [
            ("▦", "Interactive tools", "Plan, compare, calculate"),
            ("◇", "Practical guides", "Clear answers, when sources allow"),
            ("▤", "Game knowledge", "Structured references, in progress"),
        ],
        "cta_hubs": "Explore game hubs ↗",
        "cta_how": "How it works ↓",
        "statement_kicker": "Why we are building it",
        "statement_h": "A home for the useful side of gaming.",
        "statement_p": ("Game information is often scattered across spreadsheets, forum replies, "
                        "wikis, videos, and disconnected tools. BuffForge is designed around a simpler "
                        "idea: start with a game, then bring its most useful resources together in a "
                        "consistent, easy-to-navigate home."),
        "offer_kicker": "Built around real player needs",
        "offer_h": "Three ways to find your answer",
        "offer_sub": "Each game hub can combine the right mix of interactive tools and reference content.",
        "offers": [
            {"icon": "▦", "title": "Tools & calculators",
             "body": ("Small, focused utilities that help you work something out instead of reading "
                      "through a long explanation. Every tool shows its data version, its sources, and "
                      "the date it was last reviewed, so you can check our work."),
             "items": "CALCULATORS · TRACKERS · COMPARISONS",
             "status": "Live", "cls": "live", "note": None},
            {"icon": "▤", "title": "Game wiki",
             "body": ("Organized reference pages for characters, weapons, skills, locations, systems "
                      "and other game-specific details — built only from verified sources."),
             "items": "CHARACTERS · BUILDS · DATABASES",
             "status": "In progress", "cls": "wip",
             "note": "No wiki pages published yet — the first ones appear when their facts are verified."},
            {"icon": "◇", "title": "Guides & explainers",
             "body": ("Clear, searchable articles for common questions, game mechanics, setup, "
                      "and troubleshooting."),
             "items": "HOW-TOS · WALKTHROUGHS · FAQS",
             "status": "In progress", "cls": "wip",
             "note": "No guides published yet. Guides appear only when we can source the numbers."},
        ],
        "method_kicker": "How BuffForge works",
        "method_h": "One game. One connected hub.",
        "method_p": ("Instead of treating every article and calculator as an isolated page, "
                     "BuffForge groups resources by game. That makes it easier to move between a "
                     "quick answer and a practical tool without starting your search over."),
        "method_label": "GAME-FIRST STRUCTURE",
        "method_steps": [
            ("Choose a game", "Start at a dedicated hub for the title you play."),
            ("Find the right resource", "Explore the tools and reference content."),
            ("Use it and keep exploring", "Move naturally between related answers, calculators and references."),
        ],
        "principles_kicker": "Our approach",
        "principles_h": "Useful by design",
        "principles_sub": "The principles we want every BuffForge game hub to follow.",
        "principles": [
            ("01 / CLARITY", "Answers before noise",
             "Readable layouts, focused tools and sensible navigation, without burying the information people came to find."),
            ("02 / ACCURACY", "Separate facts from estimates",
             "Official announcements first. Community trackers are cited as community sources, never presented as official statements. If a number turns out to be wrong, we fix the page and update the review date."),
            ("03 / RELEVANCE", "Built for each game",
             "Different games need different utilities. The hub structure stays familiar, while the content reflects real gameplay needs. We start with one tool per game and expand only when real players use it."),
        ],
        "affil": ("BuffForge is an independent fan project and is not affiliated with NCSOFT, "
                  "Rockstar Games, Take-Two Interactive, detailgames, storytaco, or Kefir."),
        "cta_kicker": "Help us make it better",
        "cta_h": "Have a useful tool idea?",
        "cta_p": ("We're interested in problems that could be solved with a small calculator, "
                  "a clearer reference page, or a better game guide."),
        "cta_report": "Report a mistake ↗",
        "cta_suggest": "Suggest a tool ↗",
        "report_subject": "Wrong number on BuffForge",
        "suggest_subject": "Suggest a tool for BuffForge",
    },
    "ru": {
        "eyebrow": "О проекте BuffForge",
        "art_title": "Всё в одном хабе игры",
        "art_cards": [
            ("▦", "Интерактивные инструменты", "Планируйте, сравнивайте, считайте"),
            ("◇", "Практичные гайды", "Понятные ответы, когда есть источники"),
            ("▤", "Знания об игре", "Структурированные справки — в работе"),
        ],
        "cta_hubs": "Смотреть хабы игр ↗",
        "cta_how": "Как это работает ↓",
        "statement_kicker": "Зачем мы это строим",
        "statement_h": "Дом для полезной стороны игр.",
        "statement_p": ("Информация об играх часто разбросана по таблицам, ответам на форумах, вики, "
                        "видео и разрозненным инструментам. В основе BuffForge — простая идея: начать "
                        "с игры и собрать её самые полезные ресурсы в одном удобном месте."),
        "offer_kicker": "С учётом реальных нужд игроков",
        "offer_h": "Три способа найти ответ",
        "offer_sub": "Каждый хаб игры сочетает интерактивные инструменты и справочные материалы.",
        "offers": [
            {"icon": "▦", "title": "Инструменты и калькуляторы",
             "body": ("Небольшие точные утилиты, которые помогают посчитать и проверить, а не читать "
                      "длинное объяснение. У каждого инструмента указаны версия данных, источники и "
                      "дата последней проверки — чтобы вы могли перепроверить нашу работу."),
             "items": "КАЛЬКУЛЯТОРЫ · ТРЕКЕРЫ · СРАВНЕНИЯ",
             "status": "Доступно", "cls": "live", "note": None},
            {"icon": "▤", "title": "Вики по игре",
             "body": ("Упорядоченные справки по персонажам, оружию, навыкам, локациям, системам "
                      "и другим деталям игры — только по проверенным источникам."),
             "items": "ПЕРСОНАЖИ · СБОРКИ · БАЗЫ ДАННЫХ",
             "status": "В работе", "cls": "wip",
             "note": "Пока ни одной страницы вики не опубликовано — первые появятся, когда их факты будут проверены."},
            {"icon": "◇", "title": "Гайды и объяснения",
             "body": ("Понятные статьи с ответами на частые вопросы, по механикам игры, настройке "
                      "и решению проблем."),
             "items": "КАК СДЕЛАТЬ · ПРОХОЖДЕНИЯ · ВОПРОСЫ",
             "status": "В работе", "cls": "wip",
             "note": "Пока гайдов нет. Гайды появляются, только когда мы можем проверить цифры."},
        ],
        "method_kicker": "Как работает BuffForge",
        "method_h": "Одна игра. Один связанный хаб.",
        "method_p": ("Вместо того чтобы держать каждую статью и калькулятор отдельной страницей, "
                     "BuffForge группирует ресурсы по играм. Так проще переходить от быстрого ответа "
                     "к практичному инструменту, не начиная поиск заново."),
        "method_label": "СТРУКТУРА «СНАЧАЛА ИГРА»",
        "method_steps": [
            ("Выберите игру", "Начните с хаба игры, в которую играете."),
            ("Найдите нужный ресурс", "Изучите инструменты и справочные материалы."),
            ("Пользуйтесь и изучайте дальше", "Свободно переходите между ответами, калькуляторами и справками."),
        ],
        "principles_kicker": "Наш подход",
        "principles_h": "Польза по замыслу",
        "principles_sub": "Принципы, которым следует каждый хаб BuffForge.",
        "principles": [
            ("01 / ЯСНОСТЬ", "Сначала ответы, потом шум",
             "Понятная вёрстка, точные инструменты и удобная навигация — информация, за которой пришли, не теряется в шуме."),
            ("02 / ТОЧНОСТЬ", "Факты отдельно, оценки отдельно",
             "Сначала — официальные объявления. Данные трекеров сообщества указываются как источники сообщества, а не как официальные заявления. Если цифра оказалась неверной, мы исправляем страницу и обновляем дату проверки."),
            ("03 / АКТУАЛЬНОСТЬ", "Под каждую игру",
             "Разным играм нужны разные инструменты. Структура хаба привычна, а содержимое отражает реальные нужды игроков. Начинаем с одного инструмента на игру и расширяемся, только когда им реально пользуются."),
        ],
        "affil": ("BuffForge — независимый фанатский проект, не связанный с NCSOFT, "
                  "Rockstar Games, Take-Two Interactive, detailgames, storytaco и Kefir."),
        "cta_kicker": "Помогите сделать лучше",
        "cta_h": "Есть идея полезного инструмента?",
        "cta_p": ("Нам интересны задачи, которые можно решить небольшим калькулятором, "
                  "более понятной справкой или хорошим гайдом."),
        "cta_report": "Сообщить об ошибке ↗",
        "cta_suggest": "Предложить инструмент ↗",
        "report_subject": "Неверная цифра на BuffForge",
        "suggest_subject": "Предложение инструмента для BuffForge",
    },
}


def about_page(lang):
    c = ABOUT_COPY[lang]
    ui = ABOUT_UI[lang]
    # Existing ABOUT_COPY section texts, reused (indices match the list):
    # [0] What BuffForge is -> hero paragraph; [2] What we do not do ->
    # its own section; [4] Report a mistake -> contact note;
    # [5] RU-only "Почему есть русская версия" -> RU page only.
    # "What we do" and "How we check our numbers" are distilled into the
    # Tools offer card and the Accuracy principle (see ABOUT_UI).
    what = c["sections"][0][1]
    notdo_h, notdo_p = c["sections"][2]
    report_p = c["sections"][4][1]
    ru_only = c["sections"][5] if lang == "ru" and len(c["sections"]) > 5 else None
    n_live = len([t for t in TOOLS if t["status"] == "live"])
    n_games = len(SITE["games"])
    home_url = "/" if lang == "en" else "/ru/"

    art_cards = "".join(
        '<div class="about-art-card %s"><div class="about-art-symbol">%s</div>'
        '<h3>%s</h3><p>%s</p></div>' % (cls, sym, t, s)
        for cls, (sym, t, s) in zip(("one", "two", "three"), ui["art_cards"]))
    hero = (
        '<section class="about-hero"><div class="about-intro">'
        '<p class="about-eyebrow">%s</p><h1>%s</h1>'
        '<p class="about-lede">%s</p><p class="about-para">%s</p>'
        '<div class="about-cta-row"><a class="btn btn-primary" href="%s">%s</a>'
        '<a class="btn btn-secondary" href="#how-it-works">%s</a></div></div>'
        '<div class="about-art" aria-hidden="true"><div class="about-art-glow"></div>'
        '<div class="about-art-title">%s</div>%s</div></section>'
        % (ui["eyebrow"], c["h1"], c["lede"], what, home_url,
           ui["cta_hubs"], ui["cta_how"], ui["art_title"], art_cards)
    )
    statement = (
        '<section class="about-statement"><div><p class="about-eyebrow">%s</p>'
        '<h2>%s</h2></div><p>%s</p></section>'
        % (ui["statement_kicker"], ui["statement_h"], ui["statement_p"])
    )

    def offer_card(o):
        if o["note"] is None:
            note = ("%d live tools · %d games" % (n_live, n_games) if lang == "en"
                    else "%d инструментов · %d игры" % (n_live, n_games))
        else:
            note = o["note"]
        return (
            '<article class="about-offer-card"><span class="about-status %s">%s</span>'
            '<div class="about-offer-icon">%s</div><h3>%s</h3><p>%s</p>'
            '<p class="about-status-note">%s</p>'
            '<div class="about-item-list">%s</div></article>'
            % (o["cls"], o["status"], o["icon"], o["title"], o["body"], note, o["items"]))
    offers = "".join(offer_card(o) for o in ui["offers"])
    offer_sec = (
        '<section class="about-section" id="what-we-build"><div class="about-sec-top"><div>'
        '<p class="about-eyebrow">%s</p><h2>%s</h2><p class="about-sub">%s</p></div></div>'
        '<div class="about-offer-grid">%s</div></section>'
        % (ui["offer_kicker"], ui["offer_h"], ui["offer_sub"], offers)
    )

    steps = "".join(
        '<div class="about-method-step"><span class="about-stepnum">%02d</span>'
        '<div><h3>%s</h3><p>%s</p></div></div>' % (i + 1, t, p)
        for i, (t, p) in enumerate(ui["method_steps"]))
    method = (
        '<section class="about-section" id="how-it-works"><div class="about-method">'
        '<div class="about-method-left"><p class="about-eyebrow">%s</p><h2>%s</h2><p>%s</p>'
        '<span class="about-label">%s</span></div>'
        '<div class="about-method-list">%s</div></div></section>'
        % (ui["method_kicker"], ui["method_h"], ui["method_p"], ui["method_label"], steps)
    )

    prins = "".join(
        '<div class="about-principle"><span>%s</span><h3>%s</h3><p>%s</p></div>' % (k, t, p)
        for k, t, p in ui["principles"])
    principles = (
        '<section class="about-section" id="principles"><div class="about-sec-top"><div>'
        '<p class="about-eyebrow">%s</p><h2>%s</h2><p class="about-sub">%s</p></div></div>'
        '<div class="about-principles">%s</div></section>'
        % (ui["principles_kicker"], ui["principles_h"], ui["principles_sub"], prins)
    )

    notdo_sec = (
        '<section class="about-section"><div class="prose"><h2 class="about-h2">%s</h2>'
        '<p>%s</p></div></section>' % (notdo_h, notdo_p)
    )
    ru_sec = ""
    if ru_only:
        ru_sec = (
            '<section class="about-section"><div class="prose"><h2 class="about-h2">%s</h2>'
            '<p>%s</p></div></section>' % ru_only)

    report_mailto = "mailto:%s?subject=%s" % (EMAIL, quote(ui["report_subject"]))
    suggest_mailto = "mailto:%s?subject=%s" % (EMAIL, quote(ui["suggest_subject"]))
    cta = (
        '<section class="about-cta" id="contact"><div>'
        '<p class="about-eyebrow">%s</p><h2>%s</h2><p>%s</p>'
        '<p class="about-contact-note">%s</p></div>'
        '<div class="about-cta-btns"><a class="btn btn-primary" href="%s">%s</a>'
        '<a class="btn btn-secondary" href="%s">%s</a></div></section>'
        % (ui["cta_kicker"], ui["cta_h"], ui["cta_p"], report_p,
           suggest_mailto, ui["cta_suggest"], report_mailto, ui["cta_report"])
    )

    body = (
        '<main id="main" class="wrap">%s%s%s%s%s%s%s%s<p class="about-affil">%s</p>%s</main>'
        % (crumbs_html(lang, [(c["h1"], None)]),
           hero, statement, offer_sec, method, principles, notdo_sec, ru_sec,
           ui["affil"], cta)
    )
    canon = "/about/" if lang == "en" else "/ru/about/"
    alt = {"en": "/about/", "ru": "/ru/about/"}
    jl = breadcrumb_jsonld(lang, [(("Home" if lang == "en" else "Главная"),
                                   "/" if lang == "en" else "/ru/"), (c["h1"], canon)])
    return page(lang, c["title"], c["desc"], canon, alt, body, jsonld=jl)


# ---------------------------------------------------------------- hubs
HUB_COPY = {
    "desktop-pension-squad": {
        "en": {
            "title": "Desktop Pension Squad tools and guides — BuffForge",
            "desc": "Desktop Pension Squad tools: fuse or salvage calculator and a fan wiki search. Official client is v1.0.6. Fusion odds are the v1.0.2 table, checked unchanged on 22 Nov 2026.",
            "h1": "Desktop Pension Squad tools and guides",
            "lede": "Desktop Pension Squad is a free Steam Early Access idle RPG. Nine items go into one fusion, and the game does not show the odds. The official client is v1.0.6. The calculator still uses the Workshop table transcribed from client v1.0.2, Steam build 26611958. On 22 Nov 2026 that same table was still on DPSquad Wiki, which now cites build 26804378 and says the Workshop is unchanged. This is a cross-check, not a new extract. Blank Soul prices stay unknown.",
            "tools_h": "Tools", "guides_h": "Guides",
        },
        "ru": {
            "title": "Desktop Pension Squad: инструменты и гайды — BuffForge",
            "desc": "Инструменты Desktop Pension Squad: калькулятор слияния и поиск по фанатской вики. Официальный клиент — v1.0.6. Шансы слияния — таблица v1.0.2, 22 ноября 2026 сверена как неизменная.",
            "h1": "Инструменты и гайды по Desktop Pension Squad",
            "lede": "Desktop Pension Squad — бесплатная idle-RPG в раннем доступе Steam. Девять предметов уходят в одно слияние, и игра шансы не показывает. Официальный клиент — v1.0.6. Калькулятор по-прежнему использует таблицу Workshop, переписанную из клиента v1.0.2, сборка Steam 26611958. 22 ноября 2026 года та же таблица была на DPSquad Wiki: вики ссылается на сборку 26804378 и пишет, что Workshop не менялся. Это сверка, а не новая выгрузка. Пустая цена Soul остаётся неизвестной.",
            "tools_h": "Инструменты", "guides_h": "Гайды",
        },
    },
    "aion-2": {
        "en": {
            "title": "AION 2 tools and guides — BuffForge",
            "desc": "AION 2 tools and guides: daily and weekly tracker, reset times (07:00 UTC), and sourced checklists for global servers. No login, no ads.",
            "h1": "AION 2 tools and guides",
            "lede": "AION 2 runs on daily and weekly resets — miss one and a day of duties is gone. The tracker on this hub lists the global servers' duties and counts down to the 07:00 UTC daily reset and the Wednesday weekly reset, so you can see at a glance what is still open and how long you have left. Tick duties off as you finish them; your checkmarks stay in your browser. Reset times cite public sources and a review date.",
            "tools_h": "Tools", "guides_h": "Guides",
        },
        "ru": {
            "title": "AION 2: трекер и гайды, сброс 10:00 МСК — BuffForge",
            "desc": "Инструменты и гайды по AION 2: трекер ежедневных заданий, время сброса 10:00 МСК, чек-листы для глобальных серверов. Без регистрации и рекламы.",
            "h1": "Инструменты и гайды по AION 2",
            "lede": "В AION 2 всё завязано на ежедневные и еженедельные сбросы: пропустил — и день заданий потерян. Трекер на этой странице показывает задания глобальных серверов и считает время до сброса — ежедневно в 10:00 по Москве, еженедельно — в среду в 10:00, — чтобы сразу было видно, что ещё не сделано и сколько времени осталось. Отмечайте задания по мере выполнения: отметки хранятся в вашем браузере. Время сбросов указано с открытыми источниками и датой проверки.",
            "tools_h": "Инструменты", "guides_h": "Гайды",
        },
    },
    "gta-6": {
        "en": {
            "title": "GTA 6 tools and guides — BuffForge",
            "desc": "GTA 6 tools and guides: 212 GB free-space check, launch time by store region, Standard vs Ultimate, and console compatibility. Official public figures only. Out since 19 Nov 2026.",
            "h1": "GTA 6 tools and guides",
            "lede": "GTA 6 has been out since 19 Nov 2026 on PS5 and Xbox Series X|S. The questions now are practical: does your free space meet PlayStation’s 212 GB minimum, what time did your store region unlock, what does Ultimate include, and does your console run it? This hub answers those from official pages: a storage check, the unlock time by store region, Standard vs Ultimate, and a compatibility check. Standard $79.99 and Ultimate $99.99 are the US store prices, confirmed after launch. Xbox One has no native version; cloud play is live since 19 Nov 2026 — a separate $79.99 purchase, not in Game Pass, streams to Xbox consoles only. There is no announced PC version.",
            "tools_h": "Tools — official facts", "guides_h": "Guides",
        },
        "ru": {
            "title": "GTA 6: инструменты и гайды — BuffForge",
            "desc": "Инструменты и гайды по GTA 6: минимум 212 ГБ, время выхода по региону, издания и совместимость. Только официальные цифры. Игра вышла 19 ноября 2026 года.",
            "h1": "Инструменты и гайды по GTA 6",
            "lede": "GTA 6 вышла 19 ноября 2026 года на PS5 и Xbox Series X|S. Теперь вопросы практические: хватает ли свободного места до минимума PlayStation в 212 ГБ, во сколько открылся ваш регион магазина, что входит в Ultimate и запустится ли игра на вашей консоли. Здесь ответы по официальным страницам: проверка места, время открытия по региону, Standard и Ultimate и совместимость. Standard $79.99 и Ultimate $99.99 — цены магазина США, подтверждены после выхода. У Xbox One нет нативной версии; облачная игра работает с 19 ноября 2026 года — отдельная покупка $79.99, не входит в Game Pass, трансляция только на консоли Xbox. Версия для ПК не анонсирована.",
            "tools_h": "Инструменты — официальные данные", "guides_h": "Гайды",
        },
    },
    "rob-run": {
        "en": {
            "title": "ROB RUN tools and guides — BuffForge",
            "desc": "ROB RUN tools: Federal Raid countdown, loot and squad calculators, and official Steam server announcements. Not a live EU or East US probe. Free Early Access on Steam since 4 Nov 2026.",
            "h1": "ROB RUN tools and guides",
            "lede": "ROB RUN is Kefir’s free Early Access game on Steam, out since 4 Nov 2026. Seven days after a server opens, the Federal Raid wipes plots, bases, weapons and cash. Time that raid, total a haul, or split it with your squad. The 20 Nov 2026 Steam patch shows online friends in the server list. The server page requests those announcements. It does not measure EU or East US.",
            "tools_h": "Tools", "guides_h": "Guides",
        },
        "ru": {
            "title": "ROB RUN: инструменты и гайды — BuffForge",
            "desc": "Инструменты ROB RUN: отсчёт до Федеральной облавы, добыча, дележ и официальные объявления Steam. Это не проверка серверов EU и East US. Ранний доступ Steam с 4 ноября 2026 года.",
            "h1": "Инструменты и гайды по ROB RUN",
            "lede": "ROB RUN — бесплатная игра Kefir в раннем доступе Steam с 4 ноября 2026 года. Через семь дней после открытия сервера Федеральная облава обнуляет земли, базы, оружие и деньги. Здесь — отсчёт до облавы, расчёт добычи и дележ в отряде. Патч Steam от 20 ноября 2026 года показывает друзей онлайн в списке серверов. Страница про вход запрашивает эти объявления и не измеряет EU или East US.",
            "tools_h": "Инструменты", "guides_h": "Гайды",
        },
    },
    "path-of-exile-2": {
        "en": {
            "title": "Path of Exile 2 tools and guides — BuffForge",
            "desc": "Path of Exile 2 tools and guides: 1.0 launch countdown, class selector, resistance calculator, and campaign reward checklist. Early Access 0.5.5 data reviewed 25 Nov 2026. No login, no ads.",
            "h1": "Path of Exile 2 tools and guides",
            "lede": "Path of Exile 2 leaves Early Access on 11 Dec 2026 (PST) and goes free to play, with a six-act campaign, two new classes — Shadow and Duelist — and a new challenge league. Until then, everything here is Early Access 0.5.5 data, reviewed 25 Nov 2026: count down to launch, find a class that fits how you play, check your resistances against the campaign penalty, and tick off every permanent campaign reward.",
            "tools_h": "Tools", "guides_h": "Guides",
        },
        "ru": {
            "title": "Path of Exile 2: инструменты и гайды — BuffForge",
            "desc": "Инструменты и гайды по Path of Exile 2: отсчёт до 1.0, выбор класса, калькулятор сопротивлений и чек-лист наград кампании. Данные раннего доступа 0.5.5, сверка 25 ноября 2026. Без регистрации и рекламы.",
            "h1": "Инструменты и гайды по Path of Exile 2",
            "lede": "Path of Exile 2 выходит из раннего доступа 11 декабря 2026 года (тихоокеанское время) и становится бесплатной: шесть актов кампании, два новых класса — Тень и Дуэлянт — и новая лига испытаний. До этого момента здесь данные раннего доступа 0.5.5, сверенные 25 ноября 2026 года: отсчёт до выхода, подбор класса под ваш стиль игры, проверка сопротивлений с учётом штрафа кампании и чек-лист всех постоянных наград кампании.",
            "tools_h": "Инструменты", "guides_h": "Гайды",
        },
    },
}


# Hub body copy. NOTE (2026-11-13, user rule): the "planned" and
# "other" lists below are data only — they are NOT rendered.
# A section appears on a hub only when it has real content;
# planned tools and other-game links are already covered by
# the tool grid and the site header/footer.
HUB_BODY = {
    "desktop-pension-squad": {
        "en": {
            "guides_h": "Guides",
            "guides_note": "No guides published yet. Guides appear here only when we can source the numbers — nothing is listed until then.",
            "planned_h": "Planned tools and guides",
            "planned": [
                "A craft odds calculator — once the craft table is verified from the game client.",
                "An engraving Soul planner and a drop finder — after their tables are verified.",
                "An offline rewards calculator — after its formula is verified.",
                "No codes page, and no guides for bypassing regional restrictions.",
            ],
            "faq_h": "Frequently asked questions",
            "faq": [
                ("How does fusion work in Desktop Pension Squad?", "Fusion combines nine items of the same rarity, category and level bracket into one item of a higher rarity. The result rarity is random; the odds are listed in the calculator. Unequip the items first — equipped items cannot be fused."),
                ("Where do the fusion odds come from?", "The odds were transcribed from DPSquad Wiki’s reading of client v1.0.2, Steam build 26611958, reviewed 12 Nov 2026. On 22 Nov 2026 the same Epic rows were still on the wiki’s Workshop page, which now cites build 26804378 (v1.0.6) and says the Workshop is unchanged. The numbers were not re-extracted from that build."),
                ("Is Desktop Pension Squad free?", "Yes. It is free to play on Steam (Early Access since Nov 11, 2026). There is no official Russian server; the game has a Russian interface."),
            ],
            "other_h": "Other games on BuffForge",
            "other": [("AION 2 tools and guides", "/aion-2/"),
                      ("GTA 6 tools and guides", "/gta-6/")],
        },
        "ru": {
            "guides_h": "Гайды",
            "guides_note": "Гайдов пока нет. Гайды появятся здесь, только когда мы сможем проверить цифры, — до тех пор ничего не публикуется.",
            "planned_h": "Запланированные инструменты и гайды",
            "planned": [
                "Калькулятор шансов крафта — после проверки таблицы крафта по клиенту игры.",
                "Планировщик рун (Soul) и поиск дропа — после проверки их таблиц.",
                "Калькулятор наград за офлайн — после проверки формулы.",
                "Страницы кодов не будет, как и гайдов по обходу региональных ограничений.",
            ],
            "faq_h": "Частые вопросы",
            "faq": [
                ("Как работает слияние в Desktop Pension Squad?", "Слияние объединяет девять предметов одной редкости, категории и диапазона уровней в один предмет более высокой редкости. Итоговая редкость случайна, шансы указаны в калькуляторе. Сначала снимите предметы — экипированные предметы слить нельзя."),
                ("Откуда берутся шансы слияния?", "Шансы переписаны из чтения DPSquad Wiki клиента v1.0.2, сборка Steam 26611958, сверка 12 ноября 2026 года. 22 ноября 2026 года те же строки Epic всё ещё были на странице Workshop: вики теперь ссылается на сборку 26804378 (v1.0.6) и пишет, что Workshop не менялся. Из этой сборки числа заново не снимали."),
                ("Desktop Pension Squad бесплатна?", "Да. Игра бесплатна в Steam (ранний доступ с 11 ноября 2026 года). Официального русского сервера нет; русский интерфейс в игре есть."),
            ],
            "other_h": "Другие игры на BuffForge",
            "other": [("инструменты и гайды по AION 2", "/ru/aion-2/"),
                      ("инструменты и гайды по GTA 6", "/ru/gta-6/")],
        },
    },
    "aion-2": {
        "en": {
            "reset_h": "Reset times for global servers",
            "reset": [
                ("Daily reset — 07:00 UTC", "The daily checklist clears at 07:00 UTC every day."),
                ("Weekly reset — Wednesday 07:00 UTC", "The weekly checklist clears every Wednesday at 07:00 UTC."),
            ],
            "guides_h": "Guides",
            "guides_note": "No guides published yet. Guides appear here only when we can source the numbers — nothing is listed until then.",
            "planned_h": "Planned tools and guides",
            "planned": [
                "Short explainers for the daily and weekly duties behind the tracker.",
                "Later, if sources allow: an Odyle Energy calculator and class starter guides.",
                "No tier-list ranking site, and no guides for bypassing regional restrictions.",
            ],
            "faq_h": "Frequently asked questions",
            "faq": [
                ("What time is the AION 2 daily reset?", "07:00 UTC, every day."),
                ("When is the weekly reset?", "Wednesday at 07:00 UTC."),
                ("Is there an official NC tracker?", "No. NCSoft does not publish an official daily and weekly tracker — this one is built from public sources and community trackers, with a review date on the page."),
                ("Do I need an account?", "No. The tracker runs in your browser and saves your checkmarks locally."),
            ],
            "other_h": "Other games on BuffForge",
            "other": [("Desktop Pension Squad tools and guides", "/desktop-pension-squad/"),
                      ("GTA 6 tools and guides", "/gta-6/"),
                      ("BuffForge game tools and trackers", "/")],
        },
        "ru": {
            "reset_h": "Время сброса для глобальных серверов",
            "reset": [
                ("Ежедневный сброс — 10:00 МСК", "Список ежедневных заданий сбрасывается каждый день в 10:00 по Москве (07:00 UTC)."),
                ("Еженедельный сброс — среда, 10:00 МСК", "Список еженедельных заданий сбрасывается каждую среду в 10:00 по Москве (07:00 UTC)."),
            ],
            "guides_h": "Гайды",
            "guides_note": "Гайдов пока нет. Гайды появятся здесь, только когда мы сможем проверить цифры, — до тех пор ничего не публикуется.",
            "planned_h": "Запланированные инструменты и гайды",
            "planned": [
                "Короткие объяснения ежедневных и еженедельных заданий из трекера.",
                "Позже, если появятся источники: калькулятор эфирной энергии (Odyle Energy) и стартовые гайды по классам.",
                "Никаких рейтинговых tier list без источников и гайдов по обходу региональных ограничений.",
            ],
            "faq_h": "Частые вопросы",
            "faq": [
                ("Во сколько ежедневный сброс в AION 2?", "В 10:00 по Москве (07:00 UTC), каждый день."),
                ("Когда еженедельный сброс?", "В среду в 10:00 по Москве (07:00 UTC)."),
                ("AION 2 официально доступна в России?", "Нет. По данным на ноябрь 2026 года, официальная глобальная версия не распространяется в России и Беларуси: NC включает их в список стран с ограничениями. Русскоязычный интерфейс в глобальной версии есть, отдельного русского сервера нет. При этом ряд других стран СНГ входит в список обслуживаемых регионов. Никаких инструкций по обходу ограничений здесь нет."),
                ("Нужна ли регистрация?", "Нет. Трекер работает в браузере, а отметки сохраняются локально."),
            ],
            "other_h": "Другие игры на BuffForge",
            "other": [("инструменты и гайды по Desktop Pension Squad", "/ru/desktop-pension-squad/"),
                      ("инструменты и гайды по GTA 6", "/ru/gta-6/"),
                      ("игровые инструменты и трекеры BuffForge", "/ru/")],
        },
    },
    "gta-6": {
        "en": {
            "prelaunch_h": "Unverified tool",
            "prelaunch_note": "The Wanted Evidence Helper is still based on pre-release previews. It has not been checked against the shipped game.",
            "guides_h": "Guides",
            "guides_note": "No guides published yet. Guides appear here only when we can source the numbers — nothing is listed until then.",
            "planned_h": "Planned tools and guides",
            "planned": [
                "Storage, launch time, editions and compatibility stay tied to official pages.",
                "Gameplay guides only when we can cite official or verifiable sources.",
                "No PC spec table until Rockstar officially announces a PC version. No buying guides.",
            ],
            "faq_h": "Frequently asked questions",
            "faq": [
                ("How big is GTA 6?", "PlayStation lists a minimum of 212 GB free. Measured downloads are about 209.75 GB on PS5 and 209.86 GB on Xbox, installed at about 212 GB. Leave about 230 GB free. Use the storage check."),
                ("When did GTA 6 come out?", "19 Nov 2026, at local midnight in your store region. It is out. The launch-time page shows that midnight and the time since."),
                ("Standard or Ultimate — what is the difference?", "Standard $79.99 and Ultimate $99.99 are the US store prices, confirmed after launch. Other regions differ. The pre-order window closed at the end of 19 Nov 2026. See the editions page for the PlayStation Ultimate list."),
                ("Can I play GTA 6 on PC?", "There is no officially announced PC version, and no official PC system requirements. Do not trust spec tables you see online — they are not from Rockstar."),
                ("Can I play on PS4 or Xbox One?", "PS4: no. Xbox One: no native version. Cloud play is live since 19 Nov 2026: a separate $79.99 purchase, not in Game Pass, streams to Xbox consoles only."),
            ],
            "other_h": "Other games on BuffForge",
            "other": [("Desktop Pension Squad tools and guides", "/desktop-pension-squad/"),
                      ("AION 2 tools and guides", "/aion-2/"),
                      ("BuffForge game tools and trackers", "/")],
        },
        "ru": {
            "prelaunch_h": "Непроверенный инструмент",
            "prelaunch_note": "Помощник по уликам по-прежнему основан на предрелизных превью и не сверен с вышедшей игрой.",
            "guides_h": "Гайды",
            "guides_note": "Гайдов пока нет. Гайды появятся здесь, только когда мы сможем проверить цифры, — до тех пор ничего не публикуется.",
            "planned_h": "Запланированные инструменты и гайды",
            "planned": [
                "Место, время выхода, издания и совместимость остаются привязаны к официальным страницам.",
                "Гайды по игре — только когда можно сослаться на официальные или проверяемые источники.",
                "Таблицы системных требований для ПК — только после официального анонса ПК-версии. Гайдов по покупке не будет.",
            ],
            "faq_h": "Частые вопросы",
            "faq": [
                ("Сколько весит GTA 6?", "PlayStation указывает минимум 212 ГБ свободного места. Замеры загрузки: около 209,75 ГБ на PS5 и 209,86 ГБ на Xbox, после установки — около 212 ГБ. Оставьте около 230 ГБ свободными. Проверка — на странице места."),
                ("Когда вышла GTA 6?", "19 ноября 2026 года, в местную полночь региона магазина. Игра уже вышла. Страница времени выхода показывает эту полночь и сколько прошло."),
                ("Какие системные требования на ПК?", "Версия для ПК официально не анонсирована, официальных системных требований нет. Таблицы из интернета — не данные Rockstar, мы их не публикуем."),
                ("Можно ли играть на PS4 или Xbox One?", "PS4: нет. У Xbox One нет нативной версии. Облачная игра работает с 19 ноября 2026 года: отдельная покупка $79.99, не входит в Game Pass, трансляция только на консоли Xbox."),
                ("Можно ли купить GTA 6 в официальном магазине в России?", "По состоянию на ноябрь 2026 года купить игру в российском PlayStation Store или через Microsoft Store в России по официальным каналам нельзя."),
                ("Standard или Ultimate — в чём разница?", "Standard $79.99 и Ultimate $99.99 — цены магазина США, подтверждены после выхода. В других регионах цены другие. Окно предзаказа закрылось в конце 19 ноября 2026 года. Список Ultimate — на странице сравнения."),
            ],
            "other_h": "Другие игры на BuffForge",
            "other": [("инструменты и гайды по Desktop Pension Squad", "/ru/desktop-pension-squad/"),
                      ("инструменты и гайды по AION 2", "/ru/aion-2/"),
                      ("игровые инструменты и трекеры BuffForge", "/ru/")],
        },
    },
    "rob-run": {
        "en": {
            "guides_h": "Guides",
            "guides_note": "No guides published yet. Guides appear here only when we can source the numbers — nothing is listed until then.",
            "faq_h": "Frequently asked questions",
            "faq": [
                ("When is the Federal Raid?", "Seven days after that server opened. Servers launched on 4 Nov 2026 were raided on 11 Nov 2026 at 20:00 MSK (17:00 UTC). A server opened later keeps its own clock. Check your server on the <a href=\"/rob-run/federal-raid-countdown/\">Federal Raid countdown</a>."),
                ("What is wiped, and what stays?", "Plots, bases, weapons and cash are wiped and turned into <a href=\"/rob-run/jail-time-authority-calculator/\">jail time and authority</a>. Cosmetics, your name, tutorial progress, settings and accumulated jail time stay. The <a href=\"/rob-run/wipe-planner/\">Wipe Planner</a> lists each item. Source: Kefir’s Federal Raid FAQ."),
                ("Do the calculators know in-game prices?", "No. You type the cash amounts. This site is not connected to the game."),
                ("Is the ROB RUN EU server down right now?", "This site cannot say. The server-news page requests official Steam announcements and still does not measure EU or East US."),
            ],
        },
        "ru": {
            "guides_h": "Гайды",
            "guides_note": "Гайдов пока нет. Гайды появятся здесь, только когда мы сможем проверить цифры, — до тех пор ничего не публикуется.",
            "faq_h": "Частые вопросы",
            "faq": [
                ("Когда Федеральная облава?", "Через семь дней после открытия этого сервера. Серверы, запущенные 4 ноября 2026 года, прошли облаву 11 ноября в 20:00 МСК (17:00 UTC). У сервера, открытого позже, свой отсчёт. Проверьте свой сервер на странице <a href=\"/ru/rob-run/federal-raid-countdown/\">отсчёта до Федеральной облавы</a>."),
                ("Что обнуляется, а что остаётся?", "Земли, базы, оружие и деньги обнуляются и превращаются в <a href=\"/ru/rob-run/jail-time-authority-calculator/\">тюремный срок и авторитет</a>. Косметика, ник, прогресс обучения, настройки и накопленный срок остаются. Каждый предмет — в <a href=\"/ru/rob-run/wipe-planner/\">планировщике вайпа</a>. Источник — справка Kefir о Федеральной облаве."),
                ("Калькулятор знает игровые цены?", "Нет. Суммы вводите вы. Сайт к игре не подключён."),
                ("ROB RUN не работает — это сервер EU?", "Сайт так не отвечает. Страница про вход запрашивает официальные объявления Steam и не измеряет EU или East US."),
            ],
        },
    },
    "path-of-exile-2": {
        "en": {
            "guides_h": "Guides",
            "guides_note": "No guides published yet. Guides appear here only when we can source the numbers — nothing is listed until then.",
            "faq_h": "Frequently asked questions",
            "faq": [
                ("When does Path of Exile 2 1.0 come out?", "11 Dec 2026 (PST). The exact launch hour has not been announced. The game becomes free to play at launch."),
                ("Are these tools updated for 1.0?", "Not yet. The class list, resistance penalties and campaign rewards reflect Early Access 0.5.5, reviewed 25 Nov 2026. Acts 5–6 and the new classes' final numbers are not presented as confirmed until they are verified after launch."),
                ("Which class should I start with?", "Start with the combat pattern you enjoy, not a damage ranking. The Class Selector matches the eight Early Access classes by playstyle. Shadow and Duelist arrive with 1.0 and are not scored until their final mechanics are verified."),
                ("Do I need an account?", "No. The tools run in your browser; the campaign checklist saves locally."),
            ],
            "other_h": "Other games on BuffForge",
            "other": [("Desktop Pension Squad tools and guides", "/desktop-pension-squad/"),
                      ("AION 2 tools and guides", "/aion-2/"),
                      ("GTA 6 tools and guides", "/gta-6/"),
                      ("ROB RUN tools and guides", "/rob-run/")],
        },
        "ru": {
            "guides_h": "Гайды",
            "guides_note": "Гайдов пока нет. Гайды появятся здесь, только когда мы сможем проверить цифры, — до тех пор ничего не публикуется.",
            "faq_h": "Частые вопросы",
            "faq": [
                ("Когда выходит Path of Exile 2 1.0?", "11 декабря 2026 года (тихоокеанское время). Точный час запуска пока не объявлен. При выходе игра становится бесплатной."),
                ("Инструменты обновлены под 1.0?", "Пока нет. Список классов, штрафы сопротивлений и награды кампании — по раннему доступу 0.5.5, сверка 25 ноября 2026 года. Акты 5–6 и финальные цифры новых классов не выдаются за подтверждённые, пока не будут сверены после выхода."),
                ("С какого класса начать?", "С того стиля боя, который нравится, а не с рейтинга урона. Подборщик классов сопоставляет восемь классов раннего доступа по стилю игры. Тень и Дуэлянт появятся в 1.0 и не оцениваются, пока их финальная механика не проверена."),
                ("Нужна ли регистрация?", "Нет. Инструменты работают в браузере, а чек-лист кампании сохраняется локально."),
            ],
            "other_h": "Другие игры на BuffForge",
            "other": [("инструменты и гайды по Desktop Pension Squad", "/ru/desktop-pension-squad/"),
                      ("инструменты и гайды по AION 2", "/ru/aion-2/"),
                      ("инструменты и гайды по GTA 6", "/ru/gta-6/"),
                      ("инструменты и гайды по ROB RUN", "/ru/rob-run/")],
        },
    },
}


# ---------------------------------------------------------------- hub chrome
# Hub UI strings for the demo-style hub layout (hero, jump nav, section
# headings, explore, suggest). HUB_COPY (Title / H1 / lede / description)
# is SEO v2 copy and is NOT touched here.
HUB_UI = {
    "en": {
        "eyebrow": "BuffForge / Game hub",
        "cta_tools": "Explore tools",
        "cta_faq": "Quick answers",
        "jump_label": "On this page",
        "jump": [("Tools", "#tools"), ("Preview", "#preview"),
                 ("Search", "#explore"), ("FAQ", "#faq")],
        "tools_kicker": "Start here",
        "tools_h": "Popular tools",
        "tools_sub": "Quick, useful utilities — no account required.",
        "tools_more": "Browse everything",
        "open_tool": "Open tool \u2197",
        "preview_kicker": "Try it now",
        "preview_h": "Interactive tool preview",
        "explore_kicker": "Find what you need",
        "explore_h": "Explore the %s hub",
        "explore_sub": "Search across this hub's tools and questions.",
        "explore_label": "What are you looking for?",
        "explore_placeholder": "Search tools and questions...",
        "explore_search": "Search \u2197",
        "chip_all": "All",
        "chip_tools": "Tools",
        "chip_faq": "FAQ",
        "no_results": "No matching content. Try another keyword.",
        "suggest_kicker": "Community input",
        "suggest_h": "Missing a useful tool?",
        "suggest_p": "Have a calculator, checker or tracker idea? Tell us what you would like to see next.",
        "suggest_btn": "Suggest a tool \u2197",
        "suggest_subject": "Suggest a tool for ",
        "faq_kicker": "Quick answers",
        "side_kicker": "At a glance",
        "langs_meta": "Languages",
        "type_tool": "Tool",
        "type_faq": "FAQ",
        # Rendered only when this language has a guide in data/site.json.
        "guides_kicker": "Read next",
        "open_guide": "Open guide \u2197",
        "chip_guides": "Guides",
        "type_guide": "Guide",
    },
    "ru": {
        "eyebrow": "BuffForge / Игровой хаб",
        "cta_tools": "Смотреть инструменты",
        "cta_faq": "Быстрые ответы",
        "jump_label": "На этой странице",
        "jump": [("Инструменты", "#tools"), ("Превью", "#preview"),
                 ("Поиск", "#explore"), ("Вопросы", "#faq")],
        "tools_kicker": "Начните здесь",
        "tools_h": "Популярные инструменты",
        "tools_sub": "Полезные утилиты — без регистрации.",
        "tools_more": "Смотреть всё",
        "open_tool": "Открыть инструмент \u2197",
        "preview_kicker": "Попробуйте сейчас",
        "preview_h": "Интерактивный предпросмотр",
        "explore_kicker": "Найдите нужное",
        "explore_h": "Поиск по хабу %s",
        "explore_sub": "Поиск по инструментам и вопросам хаба.",
        "explore_label": "Что вы ищете?",
        "explore_placeholder": "Поиск по инструментам и вопросам...",
        "explore_search": "Найти \u2197",
        "chip_all": "Все",
        "chip_tools": "Инструменты",
        "chip_faq": "Вопросы",
        "no_results": "Ничего не найдено. Попробуйте другой запрос.",
        "suggest_kicker": "Мнение сообщества",
        "suggest_h": "Не хватает нужного инструмента?",
        "suggest_p": "Есть идея калькулятора, проверки или трекера? Расскажите, что хотели бы увидеть дальше.",
        "suggest_btn": "Предложить инструмент \u2197",
        "suggest_subject": "Suggest a tool for ",
        "faq_kicker": "Быстрые ответы",
        "side_kicker": "Кратко",
        "langs_meta": "Языка",
        "type_tool": "Инструмент",
        "type_faq": "Вопрос",
        "guides_kicker": "Коротко",
        "open_guide": "Открыть гайд \u2197",
        "chip_guides": "Гайды",
        "type_guide": "Гайд",
    },
}


# Hero stat card per game. Paragraphs are drawn only from the existing
# hub ledes (HUB_COPY) — no new facts.
HUB_HERO = {
    "gta-6": {
        "en": {
            "pill": "GAME HUB · LIVE",
            "h2": "Your GTA 6 workspace, all in one place.",
            "para": "Five tools built on official facts only: a storage check, a launch countdown, an editions comparison, a console compatibility check, and a wanted level helper. No PC version has been officially announced.",
            "wm": "wm-vi",
        },
        "ru": {
            "pill": "ИГРОВОЙ ХАБ · АКТИВЕН",
            "h2": "Ваш хаб GTA 6 — всё в одном месте.",
            "para": "Пять инструментов только по официальным цифрам: проверка места, обратный отсчёт, сравнение изданий, проверка совместимости и помощник по розыску. Версия для ПК официально не анонсирована.",
            "wm": "wm-vi",
        },
    },
    "aion-2": {
        "en": {
            "pill": "GAME HUB · LIVE",
            "h2": "Your AION 2 reset workspace, all in one place.",
            "para": "A daily and weekly tracker for the global servers: tick duties off and watch the countdown to the daily reset and the Wednesday weekly reset. Reset times cite public sources and a review date.",
            "wm": "wm-2",
        },
        "ru": {
            "pill": "ИГРОВОЙ ХАБ · АКТИВЕН",
            "h2": "Ваш хаб сбросов AION 2 — всё в одном месте.",
            "para": "Трекер ежедневных и еженедельных заданий для глобальных серверов: отмечайте задания и следите за отсчётом до сброса. Время сброса — с указанием открытых источников и даты проверки.",
            "wm": "wm-2",
        },
    },
    "desktop-pension-squad": {
        "en": {
            "pill": "GAME HUB · EARLY ACCESS",
            "h2": "Your DPS fusion workspace, all in one place.",
            "para": "A fuse or salvage calculator: nine-item fusion odds for every level bracket, plus a Soul comparison when you enter sell prices. Odds were transcribed from client v1.0.2, build 26611958, and matched the fan wiki’s v1.0.6 Workshop page on 22 Nov 2026.",
            "wm": "wm-dps",
        },
        "ru": {
            "pill": "ИГРОВОЙ ХАБ · РАННИЙ ДОСТУП",
            "h2": "Ваш хаб слияний DPS — всё в одном месте.",
            "para": "Калькулятор слияния и разбора: шансы девяти предметов для каждого диапазона уровней и сравнение Soul по введённым ценам. Шансы переписаны из клиента v1.0.2, сборка 26611958, и 22 ноября 2026 совпали со страницей Workshop вики v1.0.6.",
            "wm": "wm-dps",
        },
    },
    "rob-run": {
        "en": {
            "pill": "GAME HUB · EARLY ACCESS",
            "h2": "Your ROB RUN workspace, all in one place.",
            "para": "A Federal Raid countdown, a haul calculator, and a squad split. Cash figures are the ones you type. Server news is a separate page of Steam announcements, not a measurement of EU or East US.",
            "wm": "wm-rob",
        },
        "ru": {
            "pill": "ИГРОВОЙ ХАБ · РАННИЙ ДОСТУП",
            "h2": "Хаб ROB RUN — всё в одном месте.",
            "para": "Отсчёт до Федеральной облавы, калькулятор добычи и дележ в отряде. Суммы в деньгах вводите вы. Новости серверов — отдельная страница с объявлениями Steam, без замера EU или East US.",
            "wm": "wm-rob",
        },
    },
    "path-of-exile-2": {
        "en": {
            "pill": "GAME HUB · EARLY ACCESS",
            "h2": "Your Path of Exile 2 launch workspace, all in one place.",
            "para": "A 1.0 launch countdown, a class selector for the eight Early Access classes, a resistance calculator with the campaign penalty table, and a checklist of the campaign's permanent rewards. All Early Access 0.5.5 data, reviewed 25 Nov 2026.",
            "wm": "wm-poe",
        },
        "ru": {
            "pill": "ИГРОВОЙ ХАБ · РАННИЙ ДОСТУП",
            "h2": "Ваш хаб запуска Path of Exile 2 — всё в одном месте.",
            "para": "Отсчёт до выхода 1.0, подборщик классов из восьми классов раннего доступа, калькулятор сопротивлений с таблицей штрафов кампании и чек-лист постоянных наград кампании. Все данные — ранний доступ 0.5.5, сверка 25 ноября 2026 года.",
            "wm": "wm-poe",
        },
    },
}


# Preview-section copy per game: right-column bullets (existing facts
# only) plus the mini-widget strings. "cta_tool" is the real tool page
# the widget's button opens.
HUB_PREVIEW = {
    "gta-6": {
        "en": {
            "side_h": "One game. Multiple useful checks.",
            "bullets": [
                ("Official facts only",
                 "Storage, launch time, editions and compatibility all cite official sources."),
                ("Out since 19 Nov 2026",
                 "PlayStation 5 and Xbox Series X|S. No announced PC version."),
                ("Wanted helper reviewed 23 Nov 2026",
                 "Built on post-launch guides; it is in the sitemap."),
            ],
            "widget_title": "Storage Space Calculator",
            "widget_small": "Enter your own figures · no assumed GTA 6 install size",
            "label_avail": "Available device storage (GB)",
            "label_req": "Required game storage (GB)",
            "result_remain": "Storage remaining after install",
            "result_need": "Additional storage needed",
            "note_ok": "Based on your custom inputs",
            "note_short": "Your entered requirement exceeds available space",
            "ps_note": "PlayStation lists at least 212 GB of free space for GTA 6 — enter 212 as the required size to check your console.",
            "cta": "Open the storage check",
            "cta_tool": "gta-6-storage-check",
            "hint": "Try \u201cstorage\u201d, \u201ccountdown\u201d, \u201ceditions\u201d or \u201ccompatibility\u201d.",
        },
        "ru": {
            "side_h": "Одна игра. Несколько полезных проверок.",
            "bullets": [
                ("Только официальные цифры",
                 "Место, время выхода, издания и совместимость — всё с указанием официальных источников."),
                ("Вышла 19 ноября 2026",
                 "PlayStation 5 и Xbox Series X|S. Версия для ПК не анонсирована."),
                ("Помощник по уликам сверен 23 ноября 2026",
                 "Построен на гайдах после выхода игры; он есть в карте сайта."),
            ],
            "widget_title": "Калькулятор места на диске",
            "widget_small": "Введите свои цифры · размер установки не подставляется",
            "label_avail": "Свободное место на устройстве (ГБ)",
            "label_req": "Нужно игре (ГБ)",
            "result_remain": "Останется после установки",
            "result_need": "Нужно освободить ещё",
            "note_ok": "По вашим цифрам",
            "note_short": "Требуемый размер больше свободного места",
            "ps_note": "PlayStation указывает: для GTA 6 нужно не менее 212 ГБ — введите 212 в поле «Нужно игре», чтобы проверить свою консоль.",
            "cta": "Открыть проверку места",
            "cta_tool": "gta-6-storage-check",
            "hint": "Попробуйте «место», «отсчёт», «издания» или «совместимость».",
        },
    },
    "aion-2": {
        "en": {
            "side_h": "One tracker. Every reset covered.",
            "bullets": [
                ("Daily reset 07:00 UTC",
                 "Every day — 10:00 Moscow time."),
                ("Weekly reset Wednesday 07:00 UTC",
                 "Every Wednesday — 10:00 Moscow time."),
                ("No account, saved locally",
                 "The tracker runs in your browser and saves your checkmarks locally."),
            ],
            "widget_title": "Daily Reset Countdown",
            "widget_small": "Live · next reset 07:00 UTC",
            "meta_prefix": "Resets 07:00 UTC daily · your time: ",
            "meta_pending": "Resets 07:00 UTC daily · your time: —",
            "weekly_line": "Weekly reset: Wednesday 07:00 UTC.",
            "cta": "Open the tracker",
            "cta_tool": "aion-2-daily-tracker",
            "hint": "Try \u201ctracker\u201d, \u201creset\u201d or \u201cweekly\u201d.",
        },
        "ru": {
            "side_h": "Один трекер. Все сбросы учтены.",
            "bullets": [
                ("Ежедневный сброс — 10:00 МСК",
                 "Каждый день, 07:00 UTC."),
                ("Еженедельный сброс — среда, 10:00 МСК",
                 "Каждую среду, 07:00 UTC."),
                ("Без регистрации, отметки локально",
                 "Трекер работает в браузере, а отметки сохраняются локально."),
            ],
            "widget_title": "Отсчёт до ежедневного сброса",
            "widget_small": "Вживую · следующий сброс в 10:00 МСК",
            "meta_prefix": "Сброс в 10:00 МСК (07:00 UTC) каждый день · ваше время: ",
            "meta_pending": "Сброс в 10:00 МСК (07:00 UTC) каждый день · ваше время: —",
            "weekly_line": "Еженедельный сброс: среда, 10:00 МСК (07:00 UTC).",
            "cta": "Открыть трекер",
            "cta_tool": "aion-2-daily-tracker",
            "hint": "Попробуйте «трекер», «сброс» или «еженедельный».",
        },
    },
    "desktop-pension-squad": {
        "en": {
            "side_h": "One calculator. Every fusion answered.",
            "bullets": [
                ("Odds from client v1.0.2",
                 "Cross-checked 22 Nov 2026 against the fan wiki’s v1.0.6 Workshop page. The table was unchanged. Not a new extract."),
                ("Early Access — numbers can change",
                 "The calculator shows its data version and is updated when the game changes."),
                ("No account needed",
                 "Free to use, no login."),
            ],
            "widget_title": "Fusion Preview",
            "widget_small": "Example: Epic, Lv. 10–15",
            "label_items": "How many Epic items do you have?",
            "stat_fusions": "Complete fusions",
            "leftover_init": "0 leftover items",
            "leftover_one": "1 leftover item",
            "leftover_many": "{n} leftover items",
            "stat_per": "Legendary+ per fuse",
            "stat_per_sub": "Listed odds, Epic Lv. 10–15",
            "stat_atleast": "At least one Legendary+",
            "stat_atleast_sub": "across your fusions",
            "stat_expected": "Expected Legendary+ hits",
            "stat_expected_sub": "average, not a guarantee",
            "source_note": "Odds transcribed from client v1.0.2, build 26611958. Same Epic row on the fan wiki’s v1.0.6 page (build 26804378), checked 22 Nov 2026. Not a new extract.",
            "cta": "Open the calculator",
            "cta_tool": "dps-fuse-salvage-calculator",
            "hint": "Try \u201cfuse\u201d, \u201csalvage\u201d or \u201codds\u201d.",
        },
        "ru": {
            "side_h": "Один калькулятор. Все слияния посчитаны.",
            "bullets": [
                ("Шансы — из клиента игры",
                 "Таблица v1.0.2. 22 ноября 2026 сверена со страницей Workshop вики v1.0.6: числа те же. Это не новая выгрузка."),
                ("Ранний доступ — цифры могут меняться",
                 "У калькулятора указана версия данных; при изменении игры данные обновляются."),
                ("Без регистрации",
                 "Бесплатно, без входа."),
            ],
            "widget_title": "Предпросмотр слияния",
            "widget_small": "Пример: Epic, ур. 10–15",
            "label_items": "Сколько у вас предметов Epic?",
            "stat_fusions": "Полных слияний",
            "leftover_init": "Остаток: 0 шт.",
            "leftover_one": "Остаток: 1 шт.",
            "leftover_many": "Остаток: {n} шт.",
            "stat_per": "Legendary+ за одно слияние",
            "stat_per_sub": "Указанные шансы, Epic, ур. 10–15",
            "stat_atleast": "Хотя бы один Legendary+",
            "stat_atleast_sub": "по вашим слияниям",
            "stat_expected": "Ожидаемо Legendary+",
            "stat_expected_sub": "в среднем, без гарантии",
            "source_note": "Шансы переписаны из клиента v1.0.2, сборка 26611958. Та же строка Epic на странице вики v1.0.6 (сборка 26804378), сверка 22 ноября 2026. Это не новая выгрузка.",
            "cta": "Открыть калькулятор",
            "cta_tool": "dps-fuse-salvage-calculator",
            "hint": "Попробуйте «слияние», «разбор» или «шансы».",
        },
    },
    "rob-run": {
        "en": {
            "side_h": "Calculators use your numbers.",
            "bullets": [
                ("Free Early Access since 4 Nov 2026",
                 "Steam app 4262460. Developed and published by Kefir."),
                ("Federal Raid every 7 days",
                 "Counted from that server’s own opening, not one global clock."),
                ("You type the cash",
                 "No symbol and no price list — Kefir’s FAQ calls it cash."),
            ],
            "widget_title": "Haul minus costs",
            "widget_small": "Example only · you enter both numbers",
            "label_haul": "Haul (cash)",
            "label_cost": "Gear and costs (cash)",
            "result_net": "Net",
            "note": "Not a live price. The full calculator is on the next page.",
            "cta": "Open the calculator",
            "cta_tool": "rob-run-loot-profit-calculator",
            "hint": "Try “raid”, “loot”, “split” or “server”.",
        },
        "ru": {
            "side_h": "Калькуляторы считают ваши цифры.",
            "bullets": [
                ("Бесплатный ранний доступ с 4 ноября 2026",
                 "Steam, приложение 4262460. Разработчик и издатель — Kefir."),
                ("Федеральная облава каждые 7 дней",
                 "Отсчёт идёт от открытия вашего сервера, а не от одной даты на всех."),
                ("Деньги вводите вы",
                 "Символа валюты и прайса нет — в справке Kefir это просто деньги."),
            ],
            "widget_title": "Добыча минус расходы",
            "widget_small": "Только пример · обе цифры ваши",
            "label_haul": "Добыча (деньги)",
            "label_cost": "Снаряжение и расходы (деньги)",
            "result_net": "Итог",
            "note": "Это не живая цена. Полный калькулятор — на следующей странице.",
            "cta": "Открыть калькулятор",
            "cta_tool": "rob-run-loot-profit-calculator",
            "hint": "Попробуйте «облава», «добыча», «делёж» или «сервер».",
        },
    },
    "path-of-exile-2": {
        "en": {
            "side_h": "One game. Launch day covered.",
            "bullets": [
                ("1.0 launches 11 Dec 2026 (PST)",
                 "Free to play. Exact launch hour not announced yet."),
                ("10 classes at 1.0",
                 "Eight Early Access classes plus Shadow and Duelist."),
                ("Early Access data, reviewed 25 Nov 2026",
                 "Campaign rewards and resistance penalties are 0.5.5; Acts 5–6 are not presented as confirmed."),
            ],
            "widget_title": "1.0 Launch Countdown",
            "widget_small": "Dec 11, 2026 (PST) · free to play",
            "days_one": "day",
            "days_few": "days",
            "days_many": "days",
            "until_suffix": "until release date",
            "released": "Release date is here — check the official announcement for live availability.",
            "cta": "Open the countdown",
            "cta_tool": "poe2-launch-countdown",
            "hint": "Try “countdown”, “class”, “resistance” or “checklist”.",
        },
        "ru": {
            "side_h": "Одна игра. День выхода учтён.",
            "bullets": [
                ("1.0 выйдет 11 декабря 2026 (Тихоокеанское время)",
                 "Игра станет бесплатной. Точный час запуска пока не объявлен."),
                ("10 классов в 1.0",
                 "Восемь классов раннего доступа плюс Тень и Дуэлянт."),
                ("Данные раннего доступа, сверка 25 ноября 2026",
                 "Награды кампании и штрафы сопротивлений — 0.5.5; акты 5–6 не выдаются за подтверждённые."),
            ],
            "widget_title": "Отсчёт до выхода 1.0",
            "widget_small": "11 декабря 2026 (Тихоокеанское время) · бесплатно",
            "days_one": "день",
            "days_few": "дня",
            "days_many": "дней",
            "until_suffix": "до даты выхода",
            "released": "День выхода настал — смотрите официальное объявление о доступности.",
            "cta": "Открыть отсчёт",
            "cta_tool": "poe2-launch-countdown",
            "hint": "Попробуйте «отсчёт», «класс», «сопротивления» или «чек-лист».",
        },
    },
}


def tool_by_id(tool_id):
    for t in TOOLS:
        if t["id"] == tool_id:
            return t
    raise KeyError(tool_id)


HUB_GUIDE_COVERS = {
    "poe2-1-0-full-release-guide": "/assets/games/path-of-exile-2-wide.jpg",
    "gta-6-ps5-frame-interpolation": "/assets/games/gta-6-wide.jpg",
    "rob-run-kak-ubrat-lagi": "/assets/rob-run/lag-hero.webp",
    "rob-run-failed-to-enter-location": "/assets/rob-run/fel-hero.webp",
}


def hub_card(lang, game, t):
    import html as _html
    ui = HUB_UI[lang]
    cls = GAME_CLS.get(game["id"], "dps")
    rev = t.get("updated") or t.get("dataReviewed") or ""
    rev_html = '<span class="hub-tool-rev">%s</span>' % rev if rev else ""
    q = _html.escape((t["title"][lang] + " " + t["blurb"][lang]).lower(), quote=True)
    return (
        '<a class="hub-tool %s" href="%s" data-hub-q="%s">'
        '<div class="hub-tool-top"><span class="hub-tool-ico" aria-hidden="true">%s</span>%s</div>'
        '<h3>%s</h3><p>%s</p>'
        '<span class="hub-tool-bottom">%s<span>%s</span></span></a>'
        % (cls, tool_url(lang, t), q,
           ICONS.get(t["id"], ICONS["dps-fuse-salvage-calculator"]), rev_html,
           t["title"][lang], t["blurb"][lang], badge(lang, t), ui["open_tool"])
    )


def guide_card(lang, g):
    import html as _html
    ui = HUB_UI[lang]
    cover = HUB_GUIDE_COVERS.get(g.get("id", ""), "/assets/games/%s-wide.jpg" % g["game"])
    upd = g.get("updated") or ""
    upd_html = '<span class="hub-tool-rev">%s</span>' % upd if upd else ""
    return (
        '<a class="hub-guide-card" href="%s">'
        '<div class="hub-guide-cover"><img src="%s" alt="%s" loading="lazy"></div>'
        '<div class="hub-guide-body">'
        '<div><div class="hub-tool-top">%s%s</div>'
        '<h3>%s</h3><p>%s</p></div>'
        '<span class="hub-tool-bottom"><span>%s</span><span>%s</span></span></div></a>'
        % (guide_url(lang, g), cover, _html.escape(g["title"][lang], quote=True),
           badge(lang, g), upd_html,
           g["title"][lang], g["blurb"][lang],
           "Guide" if lang == "en" else "Гайд", ui["open_guide"])
    )


def preview_widget_gta(lang, ui, pv):
    t = tool_by_id(pv["cta_tool"])
    return (
        '<div class="hub-calc"><div class="hub-calc-head">'
        '<div class="hub-calc-icon" aria-hidden="true">%s</div>'
        '<div><h3>%s</h3><small>%s</small></div></div>'
        '<div class="hub-form-row">'
        '<div class="hub-field"><label for="hub-avail">%s</label>'
        '<input id="hub-avail" type="number" min="0" value="250"></div>'
        '<div class="hub-field"><label for="hub-req">%s</label>'
        '<input id="hub-req" type="number" min="0" value="200"></div></div>'
        '<div class="hub-result" id="hub-result"><div>'
        '<span id="hub-result-label">%s</span>'
        '<div class="hub-note" id="hub-result-note">%s</div></div>'
        '<strong id="hub-result-value">50 GB</strong></div>'
        '<p class="hub-note">%s</p>'
        '<p style="margin-top:16px"><a class="btn btn-primary" href="%s">%s %s</a></p></div>'
        % (ICONS["gta-6-storage-check"], pv["widget_title"], pv["widget_small"],
           pv["label_avail"], pv["label_req"], pv["result_remain"], pv["note_ok"],
           pv["ps_note"], tool_url(lang, t), pv["cta"], ARROW_SVG)
    )


def preview_widget_aion(lang, ui, pv):
    t = tool_by_id(pv["cta_tool"])
    return (
        '<div class="hub-calc"><div class="hub-calc-head">'
        '<div class="hub-calc-icon" aria-hidden="true">%s</div>'
        '<div><h3>%s</h3><small>%s</small></div></div>'
        '<div class="countdown-big" id="hub-daily-count">--:--:--</div>'
        '<p class="hub-note" id="hub-daily-meta">%s</p>'
        '<p class="hub-note">%s</p>'
        '<p style="margin-top:16px"><a class="btn btn-primary" href="%s">%s %s</a></p></div>'
        % (ICONS["aion-2-daily-tracker"], pv["widget_title"], pv["widget_small"],
           pv["meta_pending"], pv["weekly_line"], tool_url(lang, t), pv["cta"], ARROW_SVG)
    )


def preview_widget_dps(lang, ui, pv):
    t = tool_by_id(pv["cta_tool"])
    # Listed odds for Epic input, Lv. 10-15 (bracket index 2):
    # Epic 49.88 / Legendary 50.12. Lv. 20-30 is 49.88 / 49.88 / 0.25.
    # Transcribed from client v1.0.2; same row on the v1.0.6 wiki page.
    # Listed odds sum to 100.00, so no normalization is needed here.
    rows = (
        '<div class="outcome-row"><div class="outcome-meta">'
        '<span class="rarity-label"><span class="rarity-dot" style="--swatch: var(--r-epic)"></span>Epic</span>'
        '<strong>49.88%</strong></div>'
        '<div class="meter"><div class="meter-inner" style="--pct: 49.88%; --swatch: var(--r-epic)"></div></div></div>'
        '<div class="outcome-row"><div class="outcome-meta">'
        '<span class="rarity-label"><span class="rarity-dot" style="--swatch: var(--r-legendary)"></span>Legendary</span>'
        '<strong>50.12%</strong></div>'
        '<div class="meter"><div class="meter-inner" style="--pct: 50.12%; --swatch: var(--r-legendary)"></div></div></div>'
    )
    return (
        '<div class="hub-calc"><div class="hub-calc-head">'
        '<div class="hub-calc-icon" aria-hidden="true">%s</div>'
        '<div><h3>%s</h3><small>%s</small></div></div>'
        '<div class="hub-field"><label for="hub-items">%s</label>'
        '<input id="hub-items" type="number" min="0" value="90"></div>'
        '<div class="stats" style="margin-top:16px">'
        '<div class="stat"><em>%s</em><strong id="hub-fusions">10</strong>'
        '<span id="hub-leftover">%s</span></div>'
        '<div class="stat"><em>%s</em><strong>50.12%%</strong><span>%s</span></div>'
        '<div class="stat"><em>%s</em><strong id="hub-atleast">99.90%%</strong><span>%s</span></div>'
        '<div class="stat"><em>%s</em><strong id="hub-expected">5.01</strong><span>%s</span></div>'
        '</div>'
        '<div class="outcomes" style="margin-top:16px">%s</div>'
        '<p class="hub-note">%s</p>'
        '<p style="margin-top:16px"><a class="btn btn-primary" href="%s">%s %s</a></p></div>'
        % (ICONS["dps-fuse-salvage-calculator"], pv["widget_title"], pv["widget_small"],
           pv["label_items"],
           pv["stat_fusions"], pv["leftover_init"],
           pv["stat_per"], pv["stat_per_sub"],
           pv["stat_atleast"], pv["stat_atleast_sub"],
           pv["stat_expected"], pv["stat_expected_sub"],
           rows, pv["source_note"], tool_url(lang, t), pv["cta"], ARROW_SVG)
    )


def preview_widget_rob(lang, ui, pv):
    t = tool_by_id(pv["cta_tool"])
    return (
        '<div class="hub-calc"><div class="hub-calc-head">'
        '<div class="hub-calc-icon" aria-hidden="true">%s</div>'
        '<div><h3>%s</h3><small>%s</small></div></div>'
        '<div class="hub-form-row">'
        '<div class="hub-field"><label for="hub-haul">%s</label>'
        '<input id="hub-haul" type="number" value="120000" inputmode="decimal"></div>'
        '<div class="hub-field"><label for="hub-cost">%s</label>'
        '<input id="hub-cost" type="number" value="23000" inputmode="decimal"></div></div>'
        '<div class="hub-result" id="hub-result"><span id="hub-net-label">%s</span>'
        '<strong id="hub-net">97000</strong></div>'
        '<p class="hub-note">%s</p>'
        '<p style="margin-top:16px"><a class="btn btn-primary" href="%s">%s %s</a></p></div>'
        % (ICONS["rob-run-loot-profit-calculator"], pv["widget_title"], pv["widget_small"],
           pv["label_haul"], pv["label_cost"], pv["result_net"], pv["note"],
           tool_url(lang, t), pv["cta"], ARROW_SVG)
    )


def preview_widget_poe2(lang, ui, pv):
    t = tool_by_id(pv["cta_tool"])
    return (
        '<div class="hub-calc"><div class="hub-calc-head">'
        '<div class="hub-calc-icon" aria-hidden="true">%s</div>'
        '<div><h3>%s</h3><small>%s</small></div></div>'
        '<div class="countdown-big" id="hub-poe2-count">--</div>'
        '<p class="hub-note" id="hub-poe2-meta">%s</p>'
        '<p style="margin-top:16px"><a class="btn btn-primary" href="%s">%s %s</a></p></div>'
        % (ICONS["poe2-launch-countdown"], pv["widget_title"], pv["widget_small"],
           pv["until_suffix"], tool_url(lang, t), pv["cta"], ARROW_SVG)
    )


def preview_side(lang, ui, pv):
    items = "".join(
        '<div class="hub-side-item"><div class="hub-bullet-icon" aria-hidden="true">%s</div>'
        '<div><strong>%s</strong><span>%s</span></div></div>'
        % (CHIP_ICONS[i], title, sub)
        for i, (title, sub) in enumerate(pv["bullets"]))
    return (
        '<div class="hub-side"><p class="sec-label">%s</p>'
        '<h3 class="hub-side-h">%s</h3><div class="hub-side-list">%s</div></div>'
        % (ui["side_kicker"], pv["side_h"], items)
    )


# ---------------------------------------------------------------- hub JS
# Search is shared by all hubs; each widget script is per game. Tokens
# __ENTRIES__ / __SEARCH_STR__ / __WIDGET_STR__ are replaced with JSON
# in hub_js() — the JS itself is never %-formatted.
HUB_SEARCH_JS = """
(function () {
  var ENTRIES = __ENTRIES__;
  var STR = __SEARCH_STR__;
  var box = document.getElementById('hub-search');
  var results = document.getElementById('hub-results');
  var chips = document.querySelectorAll('.hub-chip');
  var filter = 'all';
  function render() {
    var q = box.value.trim().toLowerCase();
    var hits = ENTRIES.filter(function (e) {
      if (filter !== 'all' && e.type !== filter) return false;
      if (!q) return filter !== 'all';
      return (e.name + ' ' + e.key).toLowerCase().indexOf(q) !== -1;
    });
    if (!q && filter === 'all') {
      results.classList.remove('visible');
      results.innerHTML = '';
      return;
    }
    results.innerHTML = hits.length
      ? hits.map(function (e) {
          return '<a class="hub-result-item" href="' + e.href + '"><b>' +
            e.name + '</b><span>' +
            (e.type === 'tool' ? STR.tool : STR.faq) + ' \\u2192</span></a>';
        }).join('')
      : '<div class="hub-result-item">' + STR.noResults + '</div>';
    results.classList.add('visible');
  }
  box.addEventListener('input', render);
  document.getElementById('hub-search-btn').addEventListener('click', render);
  chips.forEach(function (btn) {
    btn.addEventListener('click', function () {
      chips.forEach(function (x) { x.classList.remove('selected'); });
      btn.classList.add('selected');
      filter = btn.getAttribute('data-filter');
      render();
      box.focus();
    });
  });
  document.querySelectorAll('.hub-jump a').forEach(function (a) {
    a.addEventListener('click', function () {
      document.querySelectorAll('.hub-jump a').forEach(function (x) { x.classList.remove('active'); });
      a.classList.add('active');
    });
  });
})();
"""

# Storage widget: two editable inputs, available minus required.
# Same result logic as the storage-check tool (remaining / additional
# needed); no install size is assumed — both figures come from the visitor.
HUB_WIDGET_GTA = """
(function () {
  var STR = __WIDGET_STR__;
  var avail = document.getElementById('hub-avail');
  var req = document.getElementById('hub-req');
  var box = document.getElementById('hub-result');
  var label = document.getElementById('hub-result-label');
  var note = document.getElementById('hub-result-note');
  var value = document.getElementById('hub-result-value');
  function fmt(n) {
    return n.toLocaleString(STR.locale, {maximumFractionDigits: 2});
  }
  function recalc() {
    var a = Math.max(0, Number(avail.value) || 0);
    var b = Math.max(0, Number(req.value) || 0);
    var diff = a - b;
    if (diff >= 0) {
      label.textContent = STR.remain;
      note.textContent = STR.noteOk;
      value.textContent = fmt(diff) + ' GB';
      value.style.color = '';
      box.classList.remove('short');
    } else {
      label.textContent = STR.need;
      note.textContent = STR.noteShort;
      value.textContent = fmt(-diff) + ' GB';
      value.style.color = 'var(--warm)';
      box.classList.add('short');
    }
  }
  avail.addEventListener('input', recalc);
  req.addEventListener('input', recalc);
  recalc();
})();
"""

# AION 2 widget: live countdown to the next daily reset. Same computation
# as the tracker (nextDailyReset, 07:00 UTC) — copied verbatim, not
# re-derived.
HUB_WIDGET_AION = """
(function () {
  var STR = __WIDGET_STR__;
  function nextDailyReset(now) {
    var d = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), 7, 0, 0, 0));
    if (d.getTime() <= now.getTime()) d.setUTCDate(d.getUTCDate() + 1);
    return d;
  }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function fmt(ms) {
    if (ms < 0) ms = 0;
    var s = Math.floor(ms / 1000);
    var h = Math.floor(s / 3600);
    var m = Math.floor((s % 3600) / 60);
    var sec = s % 60;
    return pad(h) + '<span class="unit">h</span>' + pad(m) + '<span class="unit">m</span>' + pad(sec) + '<span class="unit">s</span>';
  }
  var countEl = document.getElementById('hub-daily-count');
  var metaEl = document.getElementById('hub-daily-meta');
  var lastTarget = 0;
  function tick() {
    var now = new Date();
    var nd = nextDailyReset(now);
    countEl.innerHTML = fmt(nd.getTime() - now.getTime());
    if (nd.getTime() !== lastTarget) {
      lastTarget = nd.getTime();
      try {
        metaEl.textContent = STR.metaPrefix + nd.toLocaleString(undefined, {hour: 'numeric', minute: '2-digit', timeZoneName: 'short'});
      } catch (e) {
        metaEl.textContent = STR.metaPrefix + nd.toLocaleString();
      }
    }
  }
  tick();
  setInterval(tick, 1000);
})();
"""

# DPS widget: fixed Epic, Lv. 10-15 (bracket index 2). P = 0.5012 Legendary
# per fuse (listed 49.88 Epic / 50.12 Legendary). Lv. 20-30 is a different
# row (49.88 / 49.88 / 0.25) and is not shown here.
# fusions = floor(items / 9);
# at-least-one = 1 - (1 - p)^n; expected = n * p. Same math as the
# calculator (independent rolls, no pity).
HUB_WIDGET_DPS = """
(function () {
  var STR = __WIDGET_STR__;
  var P = 0.5012;
  var itemsEl = document.getElementById('hub-items');
  var fusionsEl = document.getElementById('hub-fusions');
  var leftoverEl = document.getElementById('hub-leftover');
  var atleastEl = document.getElementById('hub-atleast');
  var expectedEl = document.getElementById('hub-expected');
  function pct(x) { return x >= 99.995 ? '100%' : x.toFixed(2) + '%'; }
  function recalc() {
    var n = Math.max(0, Math.floor(Number(itemsEl.value) || 0));
    var fusions = Math.floor(n / 9);
    var left = n - fusions * 9;
    var atLeast = fusions > 0 ? (1 - Math.pow(1 - P, fusions)) * 100 : 0;
    var expected = fusions * P;
    fusionsEl.textContent = fusions;
    leftoverEl.textContent = left === 1 ? STR.leftoverOne : STR.leftoverMany.replace('{n}', left);
    atleastEl.textContent = pct(atLeast);
    expectedEl.textContent = expected.toFixed(2);
  }
  itemsEl.addEventListener('input', recalc);
  recalc();
})();
"""

# ROB RUN hub preview: haul minus costs. Both numbers are the visitor's.
# Empty fields count as zero. No currency symbol.
HUB_WIDGET_ROB = """
(function () {
  var STR = __WIDGET_STR__;
  var haul = document.getElementById('hub-haul');
  var cost = document.getElementById('hub-cost');
  var value = document.getElementById('hub-net');
  var box = document.getElementById('hub-result');
  function num(el) {
    var n = parseFloat(el.value);
    return isFinite(n) ? n : 0;
  }
  function fmt(n) {
    return n.toLocaleString(STR.locale, {maximumFractionDigits: 2});
  }
  function recalc() {
    var net = num(haul) - num(cost);
    value.textContent = fmt(net);
    if (net < 0) box.classList.add('short');
    else box.classList.remove('short');
  }
  haul.addEventListener('input', recalc);
  cost.addEventListener('input', recalc);
  recalc();
})();
"""


HUB_WIDGET_POE2 = """
(function () {
  var STR = __WIDGET_STR__;
  var start = new Date('2026-12-11T00:00:00-08:00');
  var countEl = document.getElementById('hub-poe2-count');
  var metaEl = document.getElementById('hub-poe2-meta');
  function plural(n, forms) {
    var m = Math.abs(n) % 100, d = m % 10;
    if (m > 10 && m < 20) return forms[2];
    if (d > 1 && d < 5) return forms[1];
    if (d === 1) return forms[0];
    return forms[2];
  }
  function tick() {
    var now = new Date();
    if (now < start) {
      var d = Math.max(0, Math.ceil((start - now) / 86400000));
      countEl.textContent = d;
      metaEl.textContent = d + ' ' + plural(d, [STR.daysOne, STR.daysFew, STR.daysMany]) + ' ' + STR.untilSuffix;
    } else {
      countEl.textContent = '0';
      metaEl.textContent = STR.released;
    }
  }
  tick();
  setInterval(tick, 60000);
})();
"""


def hub_js(game_id, lang):
    ui = HUB_UI[lang]
    pv = HUB_PREVIEW[game_id][lang]
    b = HUB_BODY[game_id][lang]
    entries = []
    for t in tools_for(game_id):
        entries.append({"name": t["title"][lang], "key": t["blurb"][lang],
                        "href": tool_url(lang, t), "type": "tool"})
    page_guides = guides_for(game_id, lang)
    for g in page_guides:
        entries.append({"name": g["title"][lang], "key": g["blurb"][lang],
                        "href": guide_url(lang, g), "type": "guide"})
    for q, a in b["faq"]:
        entries.append({"name": q, "key": a, "href": "#faq", "type": "faq"})
    payload = {"noResults": ui["no_results"],
               "tool": ui["type_tool"],
               "faq": ui["type_faq"]}
    template = HUB_SEARCH_JS
    # Label "Гайд" only on hubs that actually list a guide. Other hubs
    # keep the original script byte-for-byte.
    if page_guides:
        payload["guide"] = ui["type_guide"]
        template = template.replace(
            "(e.type === 'tool' ? STR.tool : STR.faq)",
            "(e.type === 'tool' ? STR.tool : (e.type === 'guide' ? STR.guide : STR.faq))")
    search_str = json.dumps(payload, ensure_ascii=False)
    js = template.replace("__ENTRIES__", json.dumps(entries, ensure_ascii=False))
    js = js.replace("__SEARCH_STR__", search_str)
    if game_id == "gta-6":
        wstr = json.dumps({"remain": pv["result_remain"], "need": pv["result_need"],
                           "noteOk": pv["note_ok"], "noteShort": pv["note_short"],
                           "locale": "en-US" if lang == "en" else "ru-RU"},
                          ensure_ascii=False)
        js += HUB_WIDGET_GTA.replace("__WIDGET_STR__", wstr)
    elif game_id == "aion-2":
        wstr = json.dumps({"metaPrefix": pv["meta_prefix"]}, ensure_ascii=False)
        js += HUB_WIDGET_AION.replace("__WIDGET_STR__", wstr)
    elif game_id == "rob-run":
        wstr = json.dumps({"locale": "en-US" if lang == "en" else "ru-RU"},
                          ensure_ascii=False)
        js += HUB_WIDGET_ROB.replace("__WIDGET_STR__", wstr)
    elif game_id == "path-of-exile-2":
        wstr = json.dumps({"daysOne": pv["days_one"], "daysFew": pv["days_few"],
                           "daysMany": pv["days_many"],
                           "untilSuffix": pv["until_suffix"],
                           "released": pv["released"]},
                          ensure_ascii=False)
        js += HUB_WIDGET_POE2.replace("__WIDGET_STR__", wstr)
    else:
        wstr = json.dumps({"leftoverOne": pv["leftover_one"],
                           "leftoverMany": pv["leftover_many"]}, ensure_ascii=False)
        js += HUB_WIDGET_DPS.replace("__WIDGET_STR__", wstr)
    js += """
(function(){
  var qf = document.getElementById('hub-tool-filter');
  if (qf) {
    qf.addEventListener('input', function(){
      var v = qf.value.trim().toLowerCase();
      document.querySelectorAll('#tools .hub-tool').forEach(function(c){
        var hay = c.getAttribute('data-hub-q') || c.textContent.toLowerCase();
        c.classList.toggle('hub-hidden', !!v && hay.indexOf(v) === -1);
      });
    });
  }
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.hub-jump a[href^="#"]'));
  if (navLinks.length && 'IntersectionObserver' in window) {
    var obs = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting) {
          var id = '#' + e.target.id;
          navLinks.forEach(function(a){ a.classList.toggle('active', a.getAttribute('href') === id); });
        }
      });
    }, { rootMargin: '-20% 0px -65% 0px' });
    navLinks.forEach(function(a){
      var sec = document.querySelector(a.getAttribute('href'));
      if (sec) obs.observe(sec);
    });
  }
})();
"""
    return "<script>\n" + js + "\n</script>"


def tools_meta_label(lang, n):
    # Stat-card label must agree with the count: "1 Tool" / "5 Tools";
    # Russian: 1 инструмент, 2–4 инструмента, 5+ инструментов.
    if lang == "en":
        return "Tool" if n == 1 else "Tools"
    if n == 1:
        return "Инструмент"
    if n in (2, 3, 4):
        return "Инструмента"
    return "Инструментов"


def hub_page(game_id, lang):
    c = HUB_COPY[game_id][lang]
    b = HUB_BODY[game_id][lang]
    ui = HUB_UI[lang]
    hero = HUB_HERO[game_id][lang]
    pv = HUB_PREVIEW[game_id][lang]
    game = GAMES_DATA[game_id]
    tools = tools_for(game_id)
    guides = guides_for(game_id, lang)
    hub_path = "/%s/" % game_id if lang == "en" else "/ru/%s/" % game_id
    alt = {"en": "/%s/" % game_id, "ru": "/ru/%s/" % game_id}
    home_label = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    short = GAMES[game_id]["short"]

    # Hero: eyebrow + H1 + lede (SEO v2 copy, unchanged) + CTAs, and the
    # stat card (status pill, per-game line, honest paragraph, real stats).
    # A Guides jump is added only when this language has a guide.
    jump_items = list(ui["jump"])
    if guides:
        jump_items.insert(1, (b["guides_h"], "#guides"))
    jump = "".join(
        '<a href="%s">%s</a>' % (href, label) for label, href in jump_items)
    gcls = GAME_CLS.get(game_id, "dps")
    cover_img = "/assets/games/%s-wide.jpg" % game["slug"]
    guides_cta = ""
    if guides:
        g_btn = ("Read %s" % ("1.0 Guide" if game_id == "path-of-exile-2" else b["guides_h"])) if lang == "en" else ("Гайды" if game_id != "path-of-exile-2" else "Гайд по 1.0")
        guides_cta = '<a class="btn btn-secondary" href="%s">%s ↗</a>' % (guide_url(lang, guides[0]), g_btn)
    else:
        guides_cta = '<a class="btn btn-secondary" href="#faq">%s</a>' % ui["cta_faq"]

    guides_meta = ""
    if guides:
        g_lbl = ("Guide" if len(guides) == 1 else "Guides") if lang == "en" else ("Гайд" if len(guides) == 1 else "Гайда")
        guides_meta = '<div><strong>%d</strong><span>%s</span></div>' % (len(guides), g_lbl)

    sw_order = [("path-of-exile-2", "PoE 2"), ("gta-6", "GTA 6"), ("rob-run", "ROB RUN"), ("desktop-pension-squad", "DPS"), ("aion-2", "AION 2")]
    sw_links = "".join(
        '<a class="hub-sw-pill%s" href="%s/%s/">%s</a>'
        % (" current" if gid == game_id else "", "" if lang == "en" else "/ru", gid, lbl)
        for gid, lbl in sw_order
    )

    hero_html = (
        '<section class="hub-hero"><div class="hub-hero-main %s">'
        '<p class="hub-eyebrow">%s</p><h1>%s</h1>'
        '<p class="hub-lede">%s</p>'
        '<div class="cta"><a class="btn btn-primary" href="#tools">%s %s</a>'
        '%s</div></div>'
        '<aside class="hub-stat %s">'
        '<div class="hub-stat-media"><img src="%s" alt="%s">'
        '<span class="hub-pill"><span class="dot"></span>%s</span></div>'
        '<div class="hub-stat-body"><div><h2>%s</h2><p>%s</p></div>'
        '<div class="hub-meta"><div><strong>%d</strong><span>%s</span></div>'
        '%s<div><strong>2</strong><span>%s</span></div></div></div></aside></section>'
        '<div class="hub-jump-bar"><nav class="hub-jump" aria-label="%s">%s</nav>'
        '<div class="hub-switcher" aria-label="Switch game">%s</div></div>'
        % (gcls, ui["eyebrow"], c["h1"], c["lede"], ui["cta_tools"], ARROW_SVG,
           guides_cta,
           hero["wm"], cover_img, game["name"][lang], hero["pill"],
           hero["h2"], hero["para"],
           len(tools), tools_meta_label(lang, len(tools)), guides_meta, ui["langs_meta"],
           ui["jump_label"], jump, sw_links)
    )

    # Tools: one card per real tool page (live + pre-launch in one grid).
    # The GTA 6 pre-launch note still appears exactly once, under the grid.
    cards = "".join(hub_card(lang, game, t) for t in tools)
    note = ""
    if any(t["status"] == "pre-launch" for t in tools) and b.get("prelaunch_note"):
        note = '<p class="intro-note">%s</p>' % b["prelaunch_note"]
    qfilter_html = ""
    if len(tools) >= 4:
        qf_ph = ("Filter %s tools..." % short) if lang == "en" else ("Фильтр инструментов %s..." % short)
        qfilter_html = (
            '<div class="hub-quick-filter">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'
            '<input id="hub-tool-filter" type="search" placeholder="%s" aria-label="%s"></div>'
            % (qf_ph, qf_ph)
        )
    tools_html = (
        '<section class="hub-section" id="tools">'
        '<div class="hub-sec-head"><div><p class="sec-label">%s</p>'
        '<h2>%s</h2><p class="hub-sub">%s</p></div>'
        '<a class="hub-more" href="#explore">%s %s</a></div>'
        '%s<div class="hub-tools">%s</div>%s</section>'
        % (ui["tools_kicker"], ui["tools_h"], ui["tools_sub"],
           ui["tools_more"], ARROW_SVG, qfilter_html, cards, note)
    )

    # Preview: one real working mini-widget + honest bullets. The AION 2
    # reset facts live here now (no standalone Reset section).
    if game_id == "gta-6":
        widget = preview_widget_gta(lang, ui, pv)
    elif game_id == "aion-2":
        widget = preview_widget_aion(lang, ui, pv)
    elif game_id == "rob-run":
        widget = preview_widget_rob(lang, ui, pv)
    elif game_id == "path-of-exile-2":
        widget = preview_widget_poe2(lang, ui, pv)
    else:
        widget = preview_widget_dps(lang, ui, pv)
    if widget.startswith('<div class="hub-calc">'):
        chrome_lbl = "Interactive Workbench" if lang == "en" else "Интерактивный инструмент"
        widget = (
            '<div class="hub-calc"><div class="hub-calc-chrome"><span>%s · %s</span>'
            '<span class="live-pill"><i></i>LIVE</span></div><div class="hub-calc-inner">'
            % (short, chrome_lbl)
        ) + widget[len('<div class="hub-calc">'):-len('</div>')] + '</div></div>'
    preview_html = (
        '<section class="hub-section" id="preview">'
        '<div class="hub-sec-head"><div><p class="sec-label">%s</p>'
        '<h2>%s</h2></div></div>'
        '<div class="hub-workspace">%s%s</div></section>'
        % (ui["preview_kicker"], ui["preview_h"], widget, preview_side(lang, ui, pv))
    )

    # Guides section only exists once THIS language has a live guide
    # (data/site.json top-level "guides", matched on game id and langs).
    # Until then the hub shows no Guides block at all — the placeholder
    # note in HUB_BODY stays unused. A RU-only guide does not open the
    # section on the EN hub.
    # No wiki section: no wiki data exists yet. When wiki data lands in
    # data/site.json, render it here, gated the same way as guides.
    guides_html = ""
    if guides:
        cards = "".join(guide_card(lang, g) for g in guides)
        guides_html = (
            '<section class="hub-section" id="guides">'
            '<div class="hub-sec-head"><div><p class="sec-label">%s</p>'
            '<h2>%s</h2></div></div>'
            '<div class="hub-guides-grid">%s</div></section>'
            % (ui["guides_kicker"], b["guides_h"], cards)
        )

    # Explore: client-side search over this hub's real tools + FAQ, and a
    # suggest box with a real mailto link (no demo prompt/toast).
    mailto = "mailto:%s?subject=%s" % (
        EMAIL, (ui["suggest_subject"] + game["name"]["en"]).replace(" ", "%20"))
    chips = (
        '<button class="hub-chip selected" type="button" data-filter="all">%s</button>'
        '<button class="hub-chip" type="button" data-filter="tool">%s</button>'
        % (ui["chip_all"], ui["chip_tools"]))
    if guides:
        chips += ('<button class="hub-chip" type="button" data-filter="guide">%s</button>'
                  % ui["chip_guides"])
    chips += ('<button class="hub-chip" type="button" data-filter="faq">%s</button>'
              % ui["chip_faq"])
    explore_html = (
        '<section class="hub-section" id="explore">'
        '<div class="hub-sec-head"><div><p class="sec-label">%s</p>'
        '<h2>%s</h2><p class="hub-sub">%s</p></div></div>'
        '<div class="hub-explore"><div class="hub-browse">'
        '<h3>%s</h3><p class="hub-sub">%s</p>'
        '<div class="hub-searchbox">'
        '<input id="hub-search" type="search" placeholder="%s" aria-label="%s">'
        '<button id="hub-search-btn" type="button">%s</button></div>'
        '<div class="hub-chips">%s</div>'
        '<div class="hub-results" id="hub-results" aria-live="polite"></div>'
        '</div>'
        '<aside class="hub-suggest"><div><p class="sec-label">%s</p>'
        '<h3>%s</h3><p>%s</p></div>'
        '<a class="btn btn-primary" href="%s">%s</a></aside></div></section>'
        % (ui["explore_kicker"], ui["explore_h"] % short, ui["explore_sub"],
           ui["explore_label"], pv["hint"], ui["explore_placeholder"],
           ui["explore_label"], ui["explore_search"],
           chips,
           ui["suggest_kicker"], ui["suggest_h"], ui["suggest_p"],
           mailto, ui["suggest_btn"])
    )

    # FAQ: same Q&As as before (text unchanged), first item open.
    faq_items = "".join(
        '<details%s><summary><h3>%s</h3><span class="plus" aria-hidden="true">'
        '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6">'
        '<path d="M6 1v10M1 6h10"/></svg></span></summary><p>%s</p></details>'
        % (" open" if i == 0 else "", q, a)
        for i, (q, a) in enumerate(b["faq"]))
    faq_html = (
        '<section class="hub-section faq hub-faq" id="faq">'
        '<p class="sec-label">%s</p><h2>%s</h2>%s</section>'
        % (ui["faq_kicker"], b["faq_h"], faq_items)
    )

    body = (
        '<main id="main" class="wrap">%s%s%s%s%s%s%s</main>'
        % (crumbs_html(lang, [(game["name"][lang], None)]),
           hero_html, tools_html, preview_html, guides_html, explore_html,
           faq_html)
    )
    jl = breadcrumb_jsonld(lang, [(home_label, home_path), (game["name"][lang], hub_path)])
    return page(lang, c["title"], c["desc"], hub_path, alt, body,
                jsonld=jl, games=(game_id,), tail=hub_js(game_id, lang))


# ---------------------------------------------------------------- 404
# Search index for the 404 page: live pages only (home, about, hubs,
# live tools and live guides).
NF_HUB_CARDS = {
    "desktop-pension-squad": ("▦", "fuse or salvage calculator", "калькулятор слияния и разбора"),
    "aion-2": ("✦", "daily & weekly tracker", "трекер ежедневных и еженедельных заданий"),
    "gta-6": ("Ⅵ", "storage check, launch countdown, editions, compatibility, wanted level helper", "проверка места, обратный отсчёт, издания, совместимость, помощник по розыску"),
    "rob-run": ("⬢", "federal raid countdown, loot calculator, server news, jail time calculator", "обратный отсчёт облавы, калькулятор добычи, новости серверов, калькулятор тюремного срока"),
}

NF_SEARCH_JS = """
(function () {
  var DATA = __ENTRIES__;
  var input = document.getElementById('nf-query');
  var results = document.getElementById('nf-results');
  var form = document.getElementById('nf-search-form');
  function render() {
    var q = input.value.trim().toLowerCase();
    if (!q) {
      results.classList.remove('show');
      results.innerHTML = '';
      return;
    }
    var hits = DATA.filter(function (item) {
      return (item.name + ' ' + item.key).toLowerCase().indexOf(q) !== -1;
    });
    results.innerHTML = hits.length
      ? hits.map(function (i) {
          return '<a href="' + i.href + '"><span>' + i.name + '</span><small>' + i.type + ' \\u2197</small></a>';
        }).join('')
      : '<p>__NO_MATCHES__</p>';
    results.classList.add('show');
  }
  input.addEventListener('input', render);
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    render();
    var first = results.querySelector('a');
    if (first) location.href = first.href;
  });
})();
"""


NF_COPY = {
    "en": {
        "home_name": "BuffForge — home", "home_type": "Page",
        "home_key": "home buffforge game tools trackers calculators",
        "about_name": "About BuffForge", "about_type": "Info",
        "about_key": "about mission numbers sources contact feedback",
        "hub_type": "Game hub", "tool_type": "Tool", "guide_type": "Guide",
        "no_matches": "No matches. Try “GTA”, “tracker”, or “calculator”.",
        "eyebrow": "Lost in the game world?",
        "h1": "Looks like a wrong turn.",
        "lead": ("This page might have moved, or the link may be broken. "
                 "Your next useful tool is only a click away."),
        "back": "↖ Back to home", "about_btn": "About BuffForge ↗",
        "other_lang": 'Russian version: <a href="/ru/">BuffForge на русском</a>.',
        "search_ph": "Search tools, hubs, and pages...",
        "search_label": "Search BuffForge", "search_btn": "Search →",
        "sec_eyebrow": "Find your way", "sec_h2": "Where would you like to go?",
        "sec_sub": "Pick up where you left off, or discover something useful.",
        "open_hub": "Open the hub ↗",
        "banner_h": "Something not working?",
        "banner_p": "Broken links and outdated pages happen.",
        "banner_btn": "Get in touch ↗",
        "title": "Page Not Found — BuffForge",
        "desc": "This page does not exist on BuffForge.",
    },
    "ru": {
        "home_name": "BuffForge — главная", "home_type": "Страница",
        "home_key": "главная buffforge игровые инструменты трекеры калькуляторы",
        "about_name": "О проекте BuffForge", "about_type": "Инфо",
        "about_key": "о проекте миссия цифры источники контакты обратная связь",
        "hub_type": "Хаб игры", "tool_type": "Инструмент", "guide_type": "Гайд",
        "no_matches": "Ничего не найдено. Попробуйте «GTA», «трекер» или «калькулятор».",
        "eyebrow": "Заблудились в игровом мире?",
        "h1": "Похоже, вы свернули не туда.",
        "lead": ("Возможно, страница переехала или ссылка сломана. "
                 "Нужный инструмент — в одном клике."),
        "back": "↖ На главную", "about_btn": "О проекте ↗",
        "other_lang": 'English version: <a href="/">BuffForge in English</a>.',
        "search_ph": "Искать инструменты, хабы и страницы...",
        "search_label": "Поиск по BuffForge", "search_btn": "Найти →",
        "sec_eyebrow": "Найдите дорогу", "sec_h2": "Куда вы хотите попасть?",
        "sec_sub": "Продолжите с того места, где остановились, или найдите что-то полезное.",
        "open_hub": "Открыть хаб ↗",
        "banner_h": "Что-то не работает?",
        "banner_p": "Сломанные ссылки и устаревшие страницы случаются.",
        "banner_btn": "Напишите нам ↗",
        "title": "Страница не найдена — BuffForge",
        "desc": "Такой страницы на BuffForge нет.",
    },
}


def not_found_entries(lang):
    c = NF_COPY[lang]
    prefix = "" if lang == "en" else "ru/"
    entries = [
        {"name": c["home_name"], "type": c["home_type"], "href": "/" + prefix,
         "key": c["home_key"]},
        {"name": c["about_name"], "type": c["about_type"], "href": "/%sabout/" % prefix,
         "key": c["about_key"]},
    ]
    for gid in ("desktop-pension-squad", "aion-2", "gta-6", "rob-run", "path-of-exile-2"):
        live = [t for t in tools_for(gid) if t["status"] == "live"]
        entries.append({
            "name": HUB_COPY[gid][lang]["h1"], "type": c["hub_type"],
            "href": "/%s%s/" % (prefix, gid),
            "key": (GAMES_DATA[gid]["name"][lang] + " hub tools guides "
                    + " ".join(t["title"][lang] for t in live)).lower(),
        })
        for t in live:
            entries.append({
                "name": t["title"][lang], "type": c["tool_type"],
                "href": "/%s%s/%s/" % (prefix, gid, tool_slug(t, lang)),
                "key": (t["title"][lang] + " " + t["blurb"][lang]).lower(),
            })
    for g in GUIDES:
        if g.get("status", "live") != "live":
            continue
        langs = g.get("langs")
        if langs is not None and lang not in langs:
            continue
        title = (g.get("title") or {}).get(lang)
        blurb = (g.get("blurb") or {}).get(lang)
        if not title or not blurb:
            continue
        entries.append({
            "name": title, "type": c["guide_type"],
            "href": guide_url(lang, g),
            "key": (title + " " + blurb).lower(),
        })
    return entries


def not_found_page(lang="en"):
    c = NF_COPY[lang]
    prefix = "" if lang == "en" else "ru/"
    cards = ""
    for gid in ("desktop-pension-squad", "aion-2", "gta-6", "rob-run"):
        live = [t for t in tools_for(gid) if t["status"] == "live"]
        n = len(live)
        icon, labels_en, labels_ru = NF_HUB_CARDS[gid]
        labels = labels_en if lang == "en" else labels_ru
        if lang == "en":
            line = "%s — %d live tool%s" % (labels, n, "" if n == 1 else "s")
        else:
            word = ("инструмент" if n == 1 else
                    "инструмента" if n in (2, 3, 4) else "инструментов")
            line = "%s — %d %s" % (labels, n, word)
        cards += (
            '<a class="nf-card" href="/%s%s/"><div class="nf-icon">%s</div>'
            '<h3>%s</h3><p>%s.</p><span>%s</span></a>'
            % (prefix, gid, icon, GAMES_DATA[gid]["name"][lang], line, c["open_hub"]))
    script = ("<script>\n" + NF_SEARCH_JS.replace(
        "__ENTRIES__", json.dumps(not_found_entries(lang), ensure_ascii=False)).replace(
        "__NO_MATCHES__", c["no_matches"]) + "\n</script>")
    body = (
        '<main id="main" class="wrap">%s'
        '<section class="nf-hero"><p class="nf-eyebrow">%s</p>'
        '<div class="nf-num" aria-hidden="true">404</div>'
        '<h1>%s</h1>'
        '<p class="nf-lead">%s</p>'
        '<div class="nf-actions"><a class="btn btn-primary" href="/%s">%s</a>'
        '<a class="btn btn-secondary" href="/%sabout/">%s</a></div>'
        '<p class="nf-ru">%s</p>'
        '<form class="nf-search" id="nf-search-form" role="search">'
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#829993" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m16 16 5 5"/></svg>'
        '<input type="search" id="nf-query" placeholder="%s" aria-label="%s" autocomplete="off">'
        '<button class="btn btn-primary" type="submit">%s</button></form>'
        '<div class="nf-results" id="nf-results" aria-live="polite"></div></section>'
        '<section class="nf-section"><div class="about-sec-top"><div>'
        '<p class="about-eyebrow">%s</p><h2>%s</h2>'
        '<p class="about-sub">%s</p></div></div>'
        '<div class="nf-cards">%s</div></section>'
        '<aside class="nf-banner"><div><h3>%s</h3>'
        '<p>%s</p></div>'
        '<a class="btn btn-secondary" href="/%sabout/#contact">%s</a></aside></main>'
        % (crumbs_html(lang, [("404", None)]), c["eyebrow"], c["h1"], c["lead"],
           prefix, c["back"], prefix, c["about_btn"], c["other_lang"],
           c["search_ph"], c["search_label"], c["search_btn"],
           c["sec_eyebrow"], c["sec_h2"], c["sec_sub"], cards,
           c["banner_h"], c["banner_p"], prefix, c["banner_btn"])
    )
    # 404 page: no hreflang pair, noindex, no canonical.
    switch = "/ru/" if lang == "en" else "/"
    html = ('<!DOCTYPE html>\n<html lang="%s">\n<head>\n%s\n</head>\n<body>\n%s\n%s\n%s\n%s\n</body>\n</html>\n'
            % (lang, head(lang, c["title"], c["desc"], None, None, None, noindex=True),
               header_html(lang, "/%s404.html" % prefix, switch),
               body, footer_html(lang, ("desktop-pension-squad", "aion-2", "gta-6")), script))
    return html


# ---------------------------------------------------------------- sitemap / robots / headers
def sitemap_xml():
    urls = []

    def add(path, freq, prio, lastmod="2026-11-13"):
        urls.append('  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n'
                    '    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>'
                    % (BASE, path, lastmod, freq, prio))

    add("/", "weekly", "1.0", "2026-11-22")
    add("/ru/", "weekly", "1.0", "2026-11-22")
    add("/about/", "monthly", "0.6")
    add("/ru/about/", "monthly", "0.6")
    for g in SITE["games"]:
        hub_mod = {"gta-6": "2026-11-22", "desktop-pension-squad": "2026-11-22",
                   "rob-run": "2026-11-22",
                   "path-of-exile-2": "2026-11-25"}.get(g["slug"], "2026-11-13")
        add("/%s/" % g["slug"], "weekly", "0.8", hub_mod)
        add("/ru/%s/" % g["slug"], "weekly", "0.8", hub_mod)
    for t in TOOLS:
        if t["status"] != "live":
            continue  # pre-launch tools never enter the submitted sitemap
        lastmod = t.get("updated") or "2026-11-13"
        add("/%s/%s/" % (t["game"], tool_slug(t, "en")), "weekly", "0.9", lastmod)
        add("/ru/%s/%s/" % (t["game"], tool_slug(t, "ru")), "weekly", "0.9", lastmod)
    for g in GUIDES:
        if g.get("status", "live") != "live":
            continue
        langs = g.get("langs") or ["en", "ru"]
        lastmod = g.get("updated") or "2026-11-13"
        for lang in langs:
            if lang not in (g.get("title") or {}):
                continue
            prefix = "" if lang == "en" else "/ru"
            add("%s/%s/%s/" % (prefix, g["game"], guide_slug(g, lang)), "weekly", "0.7", lastmod)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", rel)


def main():
    write("index.html", home_page("en"))
    write("ru/index.html", home_page("ru"))
    write("about/index.html", about_page("en"))
    write("ru/about/index.html", about_page("ru"))
    for gid in ("desktop-pension-squad", "aion-2", "gta-6", "rob-run", "path-of-exile-2"):
        write("%s/index.html" % gid, hub_page(gid, "en"))
        write("ru/%s/index.html" % gid, hub_page(gid, "ru"))
    write("404.html", not_found_page("en"))
    write("ru/404.html", not_found_page("ru"))
    write("sitemap.xml", sitemap_xml())
    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: https://buffforge.com/sitemap.xml\n")
    write("_headers",
          "https://buffforge.pages.dev/*\n  X-Robots-Tag: noindex\n\n"
          "https://*.buffforge.pages.dev/*\n  X-Robots-Tag: noindex\n")
    write("_redirects",
          "# Canonical host: www -> bare domain (verify in Cloudflare dashboard too).\n"
          "https://www.buffforge.com/* https://buffforge.com/:splat 301\n"
          "# Default Pages domain -> canonical domain.\n"
          "https://buffforge.pages.dev/* https://buffforge.com/:splat 301\n")
    print("build done")


if __name__ == "__main__":
    main()
