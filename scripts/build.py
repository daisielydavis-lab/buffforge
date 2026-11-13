#!/usr/bin/env python3
"""BuffForge static site generator (shell pages only).

Regenerate:  cd <repo root> && python3 scripts/build.py
It reads data/site.json and writes: index.html, ru/index.html,
about/index.html, ru/about/index.html, aion-2/index.html, ru/aion-2/index.html,
gta-6/index.html, ru/gta-6/index.html, 404.html, sitemap.xml, robots.txt,
_headers, _redirects.

Tool pages are hand-written static HTML that share assets/site.css and the
same shell markup (see scripts/shell.py); the AION 2 tracker and the GTA 6
Wanted Evidence Helper were re-skinned from their originals by
scripts/transform_legacy.py, which preserves their JavaScript verbatim.

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
                 GTA_COVER, GTA_FEATURE)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, "data", "site.json"), encoding="utf-8") as f:
    SITE = json.load(f)

GAMES_DATA = {g["id"]: g for g in SITE["games"]}
TOOLS = SITE["tools"]
GUIDES = SITE.get("guides", [])


def tools_for(game_id):
    return [t for t in TOOLS if t["game"] == game_id]


def featured_for(lang):
    feats = [t for t in TOOLS
             if t["status"] == "live" and t.get("featured", {}).get(lang)]
    feats.sort(key=lambda t: (t.get("featuredOrder", {}).get(lang) is None,
                              t.get("featuredOrder", {}).get(lang) or 99))
    return feats[:3]


def game_order(lang):
    games = list(SITE["games"])
    games.sort(key=lambda g: g.get("homeOrder", {}).get(lang, 99))
    return games


def tool_url(lang, tool):
    base = "" if lang == "en" else "/ru"
    return "%s/%s/%s/" % (base, tool["game"], tool["slug"])


def badge(lang, tool):
    if tool["status"] == "pre-launch":
        label = "Pre-launch" if lang == "en" else "До выхода"
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
        "title": "BuffForge — game tools, trackers and calculators",
        "desc": "Free game tools, trackers and calculators, organized by game. Every number cites its source and review date. No login, no ads.",
        "h1": "Game tools, trackers and calculators",
        "lede": "BuffForge is a free collection of game tools, trackers and calculators. Every number cites a public source and a review date. There is no login and no advertising. Tools are organized by game: open a game to find its trackers, checkers and (when we have sourced figures) guides. BuffForge is an independent fan project, not affiliated with any publisher. Written guides are added only when we can source the numbers — today the live work is the tools.",
        "kicker": "Sourced, dated, by game",
        "primary": "Browse featured tools",
        "chips": ["Public sources only", "Review dates on every figure", "No login, no ads"],
        "secondary": "How we check our numbers",
        "featured_h": "Featured tools",
        "featured_label": "Featured",
        "games_h": "Games",
        "games_label": "The roster",
        "games_intro": 'Games on BuffForge today: <a href="/desktop-pension-squad/">Desktop Pension Squad</a>, <a href="/aion-2/">AION 2</a> and <a href="/gta-6/">GTA 6</a>.',
        "how_h": "How we check every number",
        "how_label": "The method",
        "faq_h": "Frequently asked questions",
        "faq_label": "Questions",
        "faq": [
            ("What is BuffForge?", "A free site of game tools, trackers and calculators. Every number has a source and a review date."),
            ("Do I need an account?", "No. Everything works without an account or a login — your tracker checkmarks are stored in your own browser only."),
            ("Is BuffForge official?", "BuffForge is an independent fan project. It is not affiliated with, endorsed by, or sponsored by NCSOFT, Rockstar Games, Take-Two Interactive, detailgames, or storytaco."),
            ("Which games are covered?", "See the Games section. We add a game only when we can source the numbers. AION 2 and GTA 6 were the first; Desktop Pension Squad is the newest addition."),
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
        "games_h": "Игры",
        "games_label": "Состав",
        "games_intro": 'Сейчас на BuffForge: <a href="/ru/desktop-pension-squad/">Desktop Pension Squad</a>, <a href="/ru/aion-2/">AION 2</a> и <a href="/ru/gta-6/">GTA 6</a>.',
        "how_h": "Как мы проверяем каждую цифру",
        "how_label": "Метод",
        "faq_h": "Частые вопросы",
        "faq_label": "Вопросы",
        "faq": [
            ("Что такое BuffForge?", "Бесплатный сайт игровых инструментов, трекеров и калькуляторов. У каждой цифры — источник и дата проверки."),
            ("Нужна ли регистрация?", "Нет. Всё работает без регистрации — отметки трекера хранятся только в вашем браузере."),
            ("Это официальный сайт?", "BuffForge — независимый фанатский проект. Сайт не связан с NCSOFT, Rockstar Games, Take-Two Interactive, detailgames и storytaco и не одобрен ими."),
            ("По каким играм есть инструменты?", "Смотрите раздел «Игры». Игру добавляем только когда можем подтвердить цифры. Первыми были AION 2 и GTA 6; Desktop Pension Squad — последняя добавленная."),
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

GAME_CLS = {"desktop-pension-squad": "dps", "aion-2": "aion", "gta-6": "gta"}
FEATURE_ART = {"desktop-pension-squad": DPS_FEATURE, "aion-2": AION_FEATURE,
               "gta-6": GTA_FEATURE}
COVER_ART = {"desktop-pension-squad": DPS_COVER, "aion-2": AION_COVER,
             "gta-6": GTA_COVER}
GSUB = {
    "desktop-pension-squad": {"en": "Steam — Free to play", "ru": "Steam — бесплатно"},
    "aion-2": {"en": "Global servers — 1&nbsp;live tool", "ru": "Глобальные серверы — 1&nbsp;инструмент"},
    "gta-6": {"en": "PS5 and Xbox Series&nbsp;— Nov&nbsp;19,&nbsp;2026", "ru": "PS5 и Xbox Series&nbsp;— 19&nbsp;ноября&nbsp;2026"},
}
PLANNED_HOME = {
    "desktop-pension-squad": {
        "en": "More tools for this game — craft odds, an engraving Soul planner, and a drop finder — are planned.",
        "ru": "Планируются и другие инструменты: шансы крафта, планировщик рун (Soul) и поиск дропа."},
}
GO_LABELS = {
    "dps-fuse-salvage-calculator": {"en": "Open the calculator", "ru": "Открыть калькулятор"},
    "aion-2-daily-tracker": {"en": "Open the tracker", "ru": "Открыть трекер"},
    "gta-6-storage-check": {"en": "Open the checker", "ru": "Открыть проверку"},
    "gta-6-launch-countdown": {"en": "Open the countdown", "ru": "Открыть отсчёт"},
}
ICONS = {
    "dps-fuse-salvage-calculator": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
    "aion-2-daily-tracker": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "gta-6-launch-countdown": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
    "gta-6-storage-check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12H2M16 6H2M16 18H2"/><rect x="16" y="4" width="6" height="4" rx="1"/><rect x="16" y="16" width="6" height="4" rx="1"/></svg>',
    "gta-6-editions": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3 4 8v8l8 5 8-5V8l-8-5z"/><path d="M12 13V3M4 8l8 5 8-5"/></svg>',
    "gta-6-compatibility": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="6" width="20" height="12" rx="2"/><path d="M6 10h.01M10 10h4"/></svg>',
    "gta-6-wanted-evidence-helper": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
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
        '<p class="note">Nine Epic items, Lv. 10–15. Listed odds from DPSquad Wiki, game client v1.0.2.</p>'
        '<div class="odds-row"><div class="odds-pill"><em>Epic</em><strong>49.88%</strong></div>'
        '<div class="odds-pill"><em>Legendary</em><strong>50.12%</strong></div>'
        '<div class="odds-pill"><em>9 items →</em><strong>1 fuse</strong></div></div></div>'
        '<div class="mini"><div class="lab">AION 2 daily reset <b>07:00 UTC</b></div>'
        '<div class="big">Live <small>countdown · local ticks</small></div>'
        '<p class="note">Duties clear themselves at reset. Stored in this browser only.</p></div>'
        '<div class="mini"><div class="lab">GTA 6 storage <b>212 GB</b></div>'
        '<div class="big">Check <small>free space vs PlayStation figure</small></div>'
        '<div class="bar"><span></span></div>'
        '<p class="note">Official figure, dated. Launches 19 Nov 2026.</p></div>'
        '</div></div>'
    ),
    "ru": (
        '<div class="hero-visual" aria-hidden="true"><div class="device">'
        '<div class="device-bar"><i></i><i></i><i></i><span>buffforge.com — калькулятор слияния</span></div>'
        '<div class="mini"><div class="lab">Desktop Pension Squad <b>LIVE</b></div>'
        '<div class="big">50.12% <small>Legendary за одно слияние</small></div>'
        '<p class="note">Девять предметов Epic, ур. 10–15. Указанные шансы: DPSquad Wiki, клиент v1.0.2.</p>'
        '<div class="odds-row"><div class="odds-pill"><em>Epic</em><strong>49.88%</strong></div>'
        '<div class="odds-pill"><em>Legendary</em><strong>50.12%</strong></div>'
        '<div class="odds-pill"><em>9 шт. →</em><strong>1 слияние</strong></div></div></div>'
        '<div class="mini"><div class="lab">AION 2, ежедневный сброс <b>07:00 UTC</b></div>'
        '<div class="big">Live <small>таймер · локальные отметки</small></div>'
        '<p class="note">Отметки сбрасываются сами. Хранятся только в этом браузере.</p></div>'
        '<div class="mini"><div class="lab">GTA 6, место на диске <b>212 GB</b></div>'
        '<div class="big">Check <small>свободное место и цифра PlayStation</small></div>'
        '<div class="bar"><span></span></div>'
        '<p class="note">Официальная цифра, с датой. Выход — 19 ноября 2026.</p></div>'
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
    status = "Live" if tool["status"] == "live" else "Pre-launch"
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
    c = HOME_COPY[lang]
    feats = featured_for(lang)
    first = feats[0] if feats else None
    rest = feats[1:] if len(feats) > 1 else []
    feature_html = featured_card(lang, first, feature=True) if first else ""
    secondary_html = "".join(featured_card(lang, t) for t in rest)
    about_url = "/about/" if lang == "en" else "/ru/about/"
    blocks = "".join(game_block(lang, g) for g in game_order(lang))
    trust_items = "".join("<li><b>%s</b>%s</li>" % (t, d) for t, d in c["trust"])
    faq_items = "".join(
        '<details%s><summary><h3>%s</h3><span class="plus" aria-hidden="true">'
        '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6">'
        '<path d="M6 1v10M1 6h10"/></svg></span></summary><p>%s</p></details>'
        % (" open" if i == 0 else "", q, a)
        for i, (q, a) in enumerate(c["faq"]))
    chips = "".join('<span class="chip">%s%s</span>'
                    % (CHIP_ICONS[i], label) for i, label in enumerate(c["chips"]))
    # Lede: first two sentences are the lead, the rest follows.
    parts = c["lede"].split(". ", 2)
    lead = parts[0] + ". " + parts[1] + "."
    rest_text = parts[2] if len(parts) > 2 else ""
    body = (
        '<main id="main">'
        '<section class="hero"><div class="wrap hero-grid"><div>'
        '<p class="kicker">%s</p><h1>%s</h1>'
        '<p class="lede"><span class="lead">%s</span> %s</p>'
        '<div class="cta"><a class="btn btn-primary" href="#featured">%s %s</a>'
        '<a class="btn btn-secondary" href="#how">%s</a></div>'
        '<div class="chips" aria-label="%s">%s</div>'
        '</div>%s</div></section>'
        '<section class="block" id="featured"><div class="wrap">'
        '<p class="sec-label">%s</p><div class="sec-head"><h2>%s</h2></div>'
        '<div class="featured-layout">%s<div class="featured-secondary">%s</div></div>'
        '</div></section>'
        '<section class="block" id="games"><div class="wrap">'
        '<p class="sec-label">%s</p><h2>%s</h2><p class="intro">%s</p>%s</div></section>'
        '<section class="trust" id="how"><div class="wrap">'
        '<p class="sec-label">%s</p><h2><a href="#how">%s</a></h2><ol>%s</ol></div></section>'
        '<section class="faq wrap" id="faq">'
        '<p class="sec-label">%s</p><h2>%s</h2>%s</section>'
        '</main>'
        % (c["kicker"], c["h1"], lead, rest_text, c["primary"], ARROW_SVG,
           c["secondary"], "At a glance" if lang == "en" else "Кратко", chips,
           HERO_VISUAL[lang], c["featured_label"], c["featured_h"],
           feature_html, secondary_html,
           c["games_label"], c["games_h"], c["games_intro"], blocks,
           c["how_label"], c["how_h"], trust_items,
           c["faq_label"], c["faq_h"], faq_items)
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
             "Official announcements first. Community trackers are cited as community sources, never presented as official statements. Pre-launch tools are labelled Pre-launch and are re-checked against the live game after release. If a number turns out to be wrong, we fix the page and update the review date."),
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
             "Сначала — официальные объявления. Данные трекеров сообщества указываются как источники сообщества, а не как официальные заявления. Инструменты до выхода игры помечаются «До выхода» и перепроверяются по живой игре после релиза. Если цифра оказалась неверной, мы исправляем страницу и обновляем дату проверки."),
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
                  "Rockstar Games, Take-Two Interactive, detailgames, or storytaco."),
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
                  "Rockstar Games, Take-Two Interactive, detailgames и storytaco."),
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
            "desc": "Desktop Pension Squad tools and guides: fuse or salvage calculator with sourced odds from the game client (v1.0.2, build 26611958). Free to play on Steam.",
            "h1": "Desktop Pension Squad tools and guides",
            "lede": "Desktop Pension Squad is an idle RPG where nine items go into one fusion, and one wrong call can waste a whole batch. The game never shows you the odds — they sit in the client data — so most players guess. The calculator on this hub uses the real odds from the client (v1.0.2, Steam build 26611958): enter your items and Soul sell prices, and it shows whether fusing or salvaging pays off, and what you are likely to get. The game is free to play on Steam Early Access.",
            "tools_h": "Tools", "guides_h": "Guides",
        },
        "ru": {
            "title": "Desktop Pension Squad: инструменты и гайды — BuffForge",
            "desc": "Инструменты и гайды по Desktop Pension Squad: калькулятор слияния и разбора с шансами из клиента игры (v1.0.2, сборка 26611958). Игра бесплатна в Steam.",
            "h1": "Инструменты и гайды по Desktop Pension Squad",
            "lede": "Desktop Pension Squad — idle-RPG, в которой девять предметов уходят в одно слияние, и один неверный шаг может стоить целой партии. Сама игра шансы не показывает — они лежат в данных клиента, поэтому большинство игроков действуют наугад. Калькулятор на этой странице использует настоящие шансы из клиента (v1.0.2, сборка Steam 26611958): введите предметы и цены продажи Soul, и он покажет, что выгоднее — слияние или продажа, — и что вы, скорее всего, получите. Игра бесплатна в раннем доступе Steam.",
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
            "desc": "GTA 6 tools and guides: storage check (at least 212 GB), Nov 19 unlock time, Standard vs Ultimate, and console compatibility. Official public figures only.",
            "h1": "GTA 6 tools and guides",
            "lede": "GTA 6 launches November 19, 2026, and launch week is all questions: will 212 GB fit on your drive, when exactly does it unlock in your region, is Ultimate worth $20 more than Standard, and does your console run it at all? This hub answers all four from official facts only: a storage check, a countdown by store region, a Standard vs Ultimate comparison ($79.99 vs $99.99, US MSRP from Take-Two), and a console compatibility check — including the Xbox One cloud-gaming route. There is no officially announced PC version.",
            "tools_h": "Tools — official facts", "guides_h": "Guides",
        },
        "ru": {
            "title": "GTA 6 инструменты и гайды: 212 ГБ, 19 ноября — BuffForge",
            "desc": "Инструменты и гайды по GTA 6: сколько весит (не менее 212 ГБ), во сколько выйдет 19 ноября, издания и совместимость. Только официальные цифры.",
            "h1": "Инструменты и гайды по GTA 6",
            "lede": "GTA 6 выходит 19 ноября 2026 года, и перед запуском у всех одни и те же вопросы: влезут ли 212 ГБ на диск, во сколько игра откроется именно в вашем регионе, стоит ли Ultimate своих $20 сверху и запустится ли игра на вашей консоли? На этой странице — ответы на все четыре вопроса и только по официальным фактам: проверка места на диске, обратный отсчёт по региону магазина, сравнение Standard и Ultimate ($79.99 и $99.99, цены Take-Two в США) и проверка совместимости консолей, включая облачный вариант для Xbox One. Версия для ПК официально не анонсирована.",
            "tools_h": "Инструменты — официальные данные", "guides_h": "Гайды",
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
                ("Where do the fusion odds come from?", "The odds are transcribed from DPSquad Wiki, which reads them from the game client (version 1.0.2, Steam build 26611958). We reviewed the table against the wiki on Nov 12, 2026, Pacific Time. The game is in Early Access, so the numbers can change with patches — the calculator shows its data version."),
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
                ("Откуда берутся шансы слияния?", "Шансы переписаны из DPSquad Wiki, которая читает их из клиента игры (версия 1.0.2, сборка Steam 26611958). Мы сверили таблицу с вики 12 ноября 2026 года, тихоокеанское время. Игра в раннем доступе, поэтому цифры могут меняться с патчами — у калькулятора указана версия данных."),
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
            "prelaunch_h": "Pre-launch tool",
            "prelaunch_note": "Based on pre-release previews. Mechanics will be verified in-game after launch on Nov 19, 2026.",
            "guides_h": "Guides",
            "guides_note": "No guides published yet. Guides appear here only when we can source the numbers — nothing is listed until then.",
            "planned_h": "Planned tools and guides",
            "planned": [
                "After launch, the same four tools are updated from official patches — storage, countdown, editions, and compatibility.",
                "Gameplay guides only when we can cite official or verifiable sources.",
                "No PC spec table until Rockstar officially announces a PC version. No buying guides.",
            ],
            "faq_h": "Frequently asked questions",
            "faq": [
                ("How big is GTA 6?", "At least 212 GB of free space, according to PlayStation. Check your console with the storage check."),
                ("When does GTA 6 come out?", "Nov 19, 2026, at local midnight in your store region — see the launch countdown for your time zone."),
                ("Standard or Ultimate — what is the difference?", "Standard is $79.99 and Ultimate is $99.99 (US MSRP from Take-Two). See the editions comparison for what each one includes."),
                ("Can I play GTA 6 on PC?", "There is no officially announced PC version, and no official PC system requirements. Do not trust spec tables you see online — they are not from Rockstar."),
                ("Can I play on PS4 or Xbox One?", "PS4: no. Xbox One: no native version, but playable through Xbox Cloud Gaming from Nov 19 (Xbox Wire, Nov 10, 2026)."),
            ],
            "other_h": "Other games on BuffForge",
            "other": [("Desktop Pension Squad tools and guides", "/desktop-pension-squad/"),
                      ("AION 2 tools and guides", "/aion-2/"),
                      ("BuffForge game tools and trackers", "/")],
        },
        "ru": {
            "prelaunch_h": "Инструмент до выхода",
            "prelaunch_note": "По материалам превью до выхода. После 19 ноября 2026 года сверим механику с игрой.",
            "guides_h": "Гайды",
            "guides_note": "Гайдов пока нет. Гайды появятся здесь, только когда мы сможем проверить цифры, — до тех пор ничего не публикуется.",
            "planned_h": "Запланированные инструменты и гайды",
            "planned": [
                "После выхода те же четыре инструмента обновляются по официальным патчам: место, отсчёт, издания и совместимость.",
                "Гайды по игре — только когда можно сослаться на официальные или проверяемые источники.",
                "Таблицы системных требований для ПК — только после официального анонса ПК-версии. Гайдов по покупке не будет.",
            ],
            "faq_h": "Частые вопросы",
            "faq": [
                ("Сколько весит GTA 6?", "Не менее 212 ГБ свободного места по данным PlayStation. Проверьте свою консоль на странице проверки места."),
                ("Во сколько выйдет GTA 6 19 ноября по Москве?", "Выход — в местную полночь 19 ноября по региону магазина. Точное время для вашего региона — на странице обратного отсчёта."),
                ("Какие системные требования на ПК?", "Версия для ПК официально не анонсирована, официальных системных требований нет. Таблицы из интернета — не данные Rockstar, мы их не публикуем."),
                ("Можно ли играть на PS4 или Xbox One?", "PS4: нет. Xbox One: нативной версии нет, но можно играть через Xbox Cloud Gaming с 19 ноября (Xbox Wire, 10 ноября 2026 года)."),
                ("Можно ли купить GTA 6 в официальном магазине в России?", "По состоянию на ноябрь 2026 года купить игру в российском PlayStation Store или через Microsoft Store в России по официальным каналам нельзя."),
                ("Standard или Ultimate — что выбрать?", "Standard — $79.99, Ultimate — $99.99 (рекомендованные цены Take-Two в США). Что входит в каждое издание — на странице сравнения."),
            ],
            "other_h": "Другие игры на BuffForge",
            "other": [("инструменты и гайды по Desktop Pension Squad", "/ru/desktop-pension-squad/"),
                      ("инструменты и гайды по AION 2", "/ru/aion-2/"),
                      ("игровые инструменты и трекеры BuffForge", "/ru/")],
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
    },
}


# Hero stat card per game. Paragraphs are drawn only from the existing
# hub ledes (HUB_COPY) — no new facts.
HUB_HERO = {
    "gta-6": {
        "en": {
            "pill": "GAME HUB · PRE-LAUNCH",
            "h2": "Your GTA 6 workspace, all in one place.",
            "para": "Four tools built on official facts only: a storage check, a launch countdown, an editions comparison, and a console compatibility check. No PC version has been officially announced.",
            "wm": "wm-vi",
        },
        "ru": {
            "pill": "ИГРОВОЙ ХАБ · ДО ВЫХОДА",
            "h2": "Ваш хаб GTA 6 — всё в одном месте.",
            "para": "Четыре инструмента только по официальным цифрам: проверка места, обратный отсчёт, сравнение изданий и проверка совместимости. Версия для ПК официально не анонсирована.",
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
            "para": "A fuse or salvage calculator: nine-item fusion odds for every level bracket, plus a Soul comparison when you enter sell prices. Odds are transcribed from DPSquad Wiki, which reads them from the game client (v1.0.2, build 26611958).",
            "wm": "wm-dps",
        },
        "ru": {
            "pill": "ИГРОВОЙ ХАБ · РАННИЙ ДОСТУП",
            "h2": "Ваш хаб слияний DPS — всё в одном месте.",
            "para": "Калькулятор слияния и разбора: шансы слияния девяти предметов для каждого диапазона уровней и сравнение Soul при введённых ценах. Шансы переписаны из DPSquad Wiki — из клиента игры (v1.0.2, сборка 26611958).",
            "wm": "wm-dps",
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
                ("Pre-launch until Nov 19, 2026",
                 "The Wanted Evidence Helper is based on pre-release previews and will be verified in-game after launch."),
                ("Updated after launch",
                 "The same tools are updated from official patches once the game is out."),
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
                ("До выхода — 19 ноября 2026",
                 "Помощник по уликам основан на превью до выхода; после релиза сверим механику с игрой."),
                ("Обновим после выхода",
                 "Те же инструменты обновятся по официальным патчам, когда игра выйдет."),
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
                ("Odds from the game client",
                 "DPSquad Wiki reads them from client v1.0.2, build 26611958."),
                ("Early Access — numbers can change",
                 "The calculator shows its data version and is updated when the game changes."),
                ("No account needed",
                 "Free to use, no login."),
            ],
            "widget_title": "Fusion Preview",
            "widget_small": "Example: Epic, Lv. 20–30",
            "label_items": "How many Epic items do you have?",
            "stat_fusions": "Complete fusions",
            "leftover_init": "0 leftover items",
            "leftover_one": "1 leftover item",
            "leftover_many": "{n} leftover items",
            "stat_per": "Legendary+ per fuse",
            "stat_per_sub": "Listed odds, Epic Lv. 20–30",
            "stat_atleast": "At least one Legendary+",
            "stat_atleast_sub": "across your fusions",
            "stat_expected": "Expected Legendary+ hits",
            "stat_expected_sub": "average, not a guarantee",
            "source_note": "Odds from DPSquad Wiki (game client v1.0.2, build 26611958). Independent rolls, no pity.",
            "cta": "Open the calculator",
            "cta_tool": "dps-fuse-salvage-calculator",
            "hint": "Try \u201cfuse\u201d, \u201csalvage\u201d or \u201codds\u201d.",
        },
        "ru": {
            "side_h": "Один калькулятор. Все слияния посчитаны.",
            "bullets": [
                ("Шансы — из клиента игры",
                 "DPSquad Wiki читает их из клиента v1.0.2, сборка 26611958."),
                ("Ранний доступ — цифры могут меняться",
                 "У калькулятора указана версия данных; при изменении игры данные обновляются."),
                ("Без регистрации",
                 "Бесплатно, без входа."),
            ],
            "widget_title": "Предпросмотр слияния",
            "widget_small": "Пример: Epic, ур. 20–30",
            "label_items": "Сколько у вас предметов Epic?",
            "stat_fusions": "Полных слияний",
            "leftover_init": "Остаток: 0 шт.",
            "leftover_one": "Остаток: 1 шт.",
            "leftover_many": "Остаток: {n} шт.",
            "stat_per": "Legendary+ за одно слияние",
            "stat_per_sub": "Указанные шансы, Epic, ур. 20–30",
            "stat_atleast": "Хотя бы один Legendary+",
            "stat_atleast_sub": "по вашим слияниям",
            "stat_expected": "Ожидаемо Legendary+",
            "stat_expected_sub": "в среднем, без гарантии",
            "source_note": "Шансы: DPSquad Wiki (клиент игры v1.0.2, сборка 26611958). Независимые броски, без pity.",
            "cta": "Открыть калькулятор",
            "cta_tool": "dps-fuse-salvage-calculator",
            "hint": "Попробуйте «слияние», «разбор» или «шансы».",
        },
    },
}


def tool_by_id(tool_id):
    for t in TOOLS:
        if t["id"] == tool_id:
            return t
    raise KeyError(tool_id)


def hub_card(lang, game, t):
    ui = HUB_UI[lang]
    return (
        '<a class="hub-tool" href="%s">'
        '<span class="hub-tool-ico" aria-hidden="true">%s</span>'
        '<h3>%s</h3><p>%s</p>'
        '<span class="hub-tool-bottom">%s<span>%s</span></span></a>'
        % (tool_url(lang, t),
           ICONS.get(t["id"], ICONS["dps-fuse-salvage-calculator"]),
           t["title"][lang], t["blurb"][lang], badge(lang, t), ui["open_tool"])
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
    # Listed odds for Epic input, Lv. 20-30 bracket (bracket index 2):
    # Epic 49.88 / Legendary 50.12 — from the calculator's table, which is
    # transcribed from DPSquad Wiki (game client v1.0.2, build 26611958).
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

# DPS widget: fixed Epic, Lv. 20-30. P = 0.5012 Legendary+ per fuse
# (listed 49.88 Epic / 50.12 Legendary). fusions = floor(items / 9);
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


def hub_js(game_id, lang):
    ui = HUB_UI[lang]
    pv = HUB_PREVIEW[game_id][lang]
    b = HUB_BODY[game_id][lang]
    entries = []
    for t in tools_for(game_id):
        entries.append({"name": t["title"][lang], "key": t["blurb"][lang],
                        "href": tool_url(lang, t), "type": "tool"})
    for q, a in b["faq"]:
        entries.append({"name": q, "key": a, "href": "#faq", "type": "faq"})
    search_str = json.dumps({"noResults": ui["no_results"],
                             "tool": ui["type_tool"],
                             "faq": ui["type_faq"]}, ensure_ascii=False)
    js = HUB_SEARCH_JS.replace("__ENTRIES__", json.dumps(entries, ensure_ascii=False))
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
    else:
        wstr = json.dumps({"leftoverOne": pv["leftover_one"],
                           "leftoverMany": pv["leftover_many"]}, ensure_ascii=False)
        js += HUB_WIDGET_DPS.replace("__WIDGET_STR__", wstr)
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
    hub_path = "/%s/" % game_id if lang == "en" else "/ru/%s/" % game_id
    alt = {"en": "/%s/" % game_id, "ru": "/ru/%s/" % game_id}
    home_label = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    short = GAMES[game_id]["short"]

    # Hero: eyebrow + H1 + lede (SEO v2 copy, unchanged) + CTAs, and the
    # stat card (status pill, per-game line, honest paragraph, real stats).
    jump = "".join(
        '<a href="%s">%s</a>' % (href, label) for label, href in ui["jump"])
    hero_html = (
        '<section class="hub-hero"><div class="hub-hero-main">'
        '<p class="hub-eyebrow">%s</p><h1>%s</h1>'
        '<p class="hub-lede">%s</p>'
        '<div class="cta"><a class="btn btn-primary" href="#tools">%s</a>'
        '<a class="btn btn-secondary" href="#faq">%s</a></div></div>'
        '<aside class="hub-stat %s"><div>'
        '<span class="hub-pill"><span class="dot"></span>%s</span>'
        '<h2>%s</h2><p>%s</p></div>'
        '<div class="hub-meta"><div><strong>%d</strong><span>%s</span></div>'
        '<div><strong>2</strong><span>%s</span></div></div></aside></section>'
        '<nav class="hub-jump" aria-label="%s">%s</nav>'
        % (ui["eyebrow"], c["h1"], c["lede"], ui["cta_tools"], ui["cta_faq"],
           hero["wm"], hero["pill"], hero["h2"], hero["para"],
           len(tools), tools_meta_label(lang, len(tools)), ui["langs_meta"],
           ui["jump_label"], jump)
    )

    # Tools: one card per real tool page (live + pre-launch in one grid).
    # The GTA 6 pre-launch note still appears exactly once, under the grid.
    cards = "".join(hub_card(lang, game, t) for t in tools)
    note = ""
    if any(t["status"] == "pre-launch" for t in tools) and b.get("prelaunch_note"):
        note = '<p class="intro-note">%s</p>' % b["prelaunch_note"]
    tools_html = (
        '<section class="hub-section" id="tools">'
        '<div class="hub-sec-head"><div><p class="sec-label">%s</p>'
        '<h2>%s</h2><p class="hub-sub">%s</p></div>'
        '<a class="hub-more" href="#explore">%s %s</a></div>'
        '<div class="hub-tools">%s</div>%s</section>'
        % (ui["tools_kicker"], ui["tools_h"], ui["tools_sub"],
           ui["tools_more"], ARROW_SVG, cards, note)
    )

    # Preview: one real working mini-widget + honest bullets. The AION 2
    # reset facts live here now (no standalone Reset section).
    if game_id == "gta-6":
        widget = preview_widget_gta(lang, ui, pv)
    elif game_id == "aion-2":
        widget = preview_widget_aion(lang, ui, pv)
    else:
        widget = preview_widget_dps(lang, ui, pv)
    preview_html = (
        '<section class="hub-section" id="preview">'
        '<div class="hub-sec-head"><div><p class="sec-label">%s</p>'
        '<h2>%s</h2></div></div>'
        '<div class="hub-workspace">%s%s</div></section>'
        % (ui["preview_kicker"], ui["preview_h"], widget, preview_side(lang, ui, pv))
    )

    # Guides section only exists once a game actually has guides
    # (data/site.json top-level "guides"; an entry counts only when its
    # "game" field equals this game's id). Until then the hub shows no
    # Guides block at all. When guides land, render the list here
    # instead of the placeholder note.
    # No wiki section: no wiki data exists yet. When wiki data lands in
    # data/site.json, render it here, gated the same way as guides.
    guides_html = ""
    if [g for g in GUIDES if g.get("game") == game_id]:
        guides_html = ('<section class="hub-section"><h2 class="sec">%s</h2><p>%s</p></section>'
                       % (b["guides_h"], b["guides_note"]))

    # Explore: client-side search over this hub's real tools + FAQ, and a
    # suggest box with a real mailto link (no demo prompt/toast).
    mailto = "mailto:%s?subject=%s" % (
        EMAIL, (ui["suggest_subject"] + game["name"]["en"]).replace(" ", "%20"))
    explore_html = (
        '<section class="hub-section" id="explore">'
        '<div class="hub-sec-head"><div><p class="sec-label">%s</p>'
        '<h2>%s</h2><p class="hub-sub">%s</p></div></div>'
        '<div class="hub-explore"><div class="hub-browse">'
        '<h3>%s</h3><p class="hub-sub">%s</p>'
        '<div class="hub-searchbox">'
        '<input id="hub-search" type="search" placeholder="%s" aria-label="%s">'
        '<button id="hub-search-btn" type="button">%s</button></div>'
        '<div class="hub-chips">'
        '<button class="hub-chip selected" type="button" data-filter="all">%s</button>'
        '<button class="hub-chip" type="button" data-filter="tool">%s</button>'
        '<button class="hub-chip" type="button" data-filter="faq">%s</button></div>'
        '<div class="hub-results" id="hub-results" aria-live="polite"></div>'
        '</div>'
        '<aside class="hub-suggest"><div><p class="sec-label">%s</p>'
        '<h3>%s</h3><p>%s</p></div>'
        '<a class="btn btn-primary" href="%s">%s</a></aside></div></section>'
        % (ui["explore_kicker"], ui["explore_h"] % short, ui["explore_sub"],
           ui["explore_label"], pv["hint"], ui["explore_placeholder"],
           ui["explore_label"], ui["explore_search"],
           ui["chip_all"], ui["chip_tools"], ui["chip_faq"],
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
# Search index for the 404 page: live pages only (home, about, the three
# hubs, the six live tools). The pre-launch Wanted Helper is excluded
# (not featured), and there are no wiki/guide pages to list.
NF_HUB_CARDS = {
    "desktop-pension-squad": ("▦", "fuse or salvage calculator", "калькулятор слияния и разбора"),
    "aion-2": ("✦", "daily & weekly tracker", "трекер ежедневных и еженедельных заданий"),
    "gta-6": ("Ⅵ", "storage check, launch countdown, editions, compatibility", "проверка места, обратный отсчёт, издания, совместимость"),
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
        "hub_type": "Game hub", "tool_type": "Tool",
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
        "hub_type": "Хаб игры", "tool_type": "Инструмент",
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
    for gid in ("desktop-pension-squad", "aion-2", "gta-6"):
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
                "href": "/%s%s/%s/" % (prefix, gid, t["slug"]),
                "key": (t["title"][lang] + " " + t["blurb"][lang]).lower(),
            })
    return entries


def not_found_page(lang="en"):
    c = NF_COPY[lang]
    prefix = "" if lang == "en" else "ru/"
    cards = ""
    for gid in ("desktop-pension-squad", "aion-2", "gta-6"):
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
            % (lang, head(lang, c["title"], c["desc"], None, None, None),
               header_html(lang, "/%s404.html" % prefix, switch),
               body, footer_html(lang, ("desktop-pension-squad", "aion-2", "gta-6")), script))
    return html


# ---------------------------------------------------------------- sitemap / robots / headers
def sitemap_xml():
    urls = []

    def add(path, freq, prio):
        urls.append('  <url>\n    <loc>%s%s</loc>\n    <lastmod>2026-11-13</lastmod>\n'
                    '    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>'
                    % (BASE, path, freq, prio))

    add("/", "weekly", "1.0")
    add("/ru/", "weekly", "1.0")
    add("/about/", "monthly", "0.6")
    add("/ru/about/", "monthly", "0.6")
    for g in SITE["games"]:
        add("/%s/" % g["slug"], "weekly", "0.8")
        add("/ru/%s/" % g["slug"], "weekly", "0.8")
    for t in TOOLS:
        if t["status"] != "live":
            continue  # pre-launch tools never enter the submitted sitemap
        add("/%s/%s/" % (t["game"], t["slug"]), "weekly", "0.9")
        add("/ru/%s/%s/" % (t["game"], t["slug"]), "weekly", "0.9")
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
    for gid in ("desktop-pension-squad", "aion-2", "gta-6"):
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
