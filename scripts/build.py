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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import (BASE, EMAIL, GAMES, REVIEWED_EN, REVIEWED_RU, breadcrumb_jsonld,
                   crumbs_html, footer_html, head, header_html, org_website_jsonld, page)

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


def badge(tool):
    if tool["status"] == "pre-launch":
        return '<span class="badge prelaunch">Pre-launch</span>'
    return '<span class="badge live">Live</span>'


# ---------------------------------------------------------------- home
HOME_COPY = {
    "en": {
        "title": "BuffForge — Game tools, checked against the patch notes",
        "desc": "Small, honest tools and guides by game: reset trackers, official-spec checkers, and calculators. No login, no ads. Every number cites its source and review date.",
        "h1": 'Game tools and guides, <span>organized by game.</span>',
        "lede": "Reset trackers, official-spec checkers, and short guides for the games you actually play. No login, no ads. <b>Every number cites its source and review date.</b>",
        "secondary": "How we check our numbers",
        "featured_h": "Featured tools",
        "games_h": "Games",
        "view_all": "View all for this game",
        "open": "Open the tool",
        "trust": [
            ("Public sources only", "Numbers come from official notes, official wikis, and public APIs."),
            ("Versioned and dated", "Every tool shows its data version, sources, and review date."),
            ("Tell us when we are wrong", "If we get a number wrong, tell us. We correct it."),
        ],
        "reviewed": "Data reviewed Nov 13, 2026",
    },
    "ru": {
        "title": "BuffForge — игровые инструменты с проверенными цифрами",
        "desc": "Инструменты и гайды по играм: трекер сброса AION 2 (10:00 МСК), проверка места под GTA 6, сравнение изданий. Без регистрации и рекламы. У каждой цифры — источник и дата проверки.",
        "h1": "Инструменты и гайды <span>по играм.</span>",
        "lede": "Сброс AION 2 в 10:00 по Москве, место на диске и время выхода GTA 6 — по официальным данным, без выдуманных «системных требований». Без регистрации и рекламы. <b>Каждая цифра — с источником и датой проверки.</b>",
        "secondary": "Как мы проверяем цифры",
        "featured_h": "Главные инструменты",
        "games_h": "Игры",
        "view_all": "Все инструменты и гайды игры",
        "open": "Открыть",
        "trust": [
            ("Только открытые источники", "Цифры только из официальных заметок, официальных вики и публичных API."),
            ("Версия и дата проверки", "У каждого инструмента — версия данных, источники и дата проверки."),
            ("Напишите нам об ошибке", "Ошиблись в цифре — напишите нам, мы исправим."),
        ],
        "reviewed": "Данные проверены 13 ноября 2026 года",
    },
}


def featured_card(lang, tool):
    c = HOME_COPY[lang]
    game = GAMES_DATA[tool["game"]]
    return (
        '<a class="card" href="%s">'
        '<span class="tag">%s</span>'
        '<h3>%s</h3><p>%s</p>'
        '<span class="go">%s &rarr;</span>'
        '<div class="meta">%s &middot; %s</div></a>'
        % (tool_url(lang, tool), game["name"][lang], tool["title"][lang],
           tool["blurb"][lang], c["open"], c["reviewed"], game["name"][lang])
    )


def game_block(lang, game):
    c = HOME_COPY[lang]
    tools = tools_for(game["id"])
    rows = []
    for t in tools:
        rows.append(
            '<div class="tool-row"><div><a class="t-name" href="%s">%s</a>%s'
            '<div class="t-blurb">%s</div></div>'
            '<a class="t-go" href="%s">%s &rarr;</a></div>'
            % (tool_url(lang, t), t["title"][lang], badge(t), t["blurb"][lang],
               tool_url(lang, t), c["open"]))
    hub = game["hub"] if "hub" in game else {"en": "/%s/" % game["slug"], "ru": "/ru/%s/" % game["slug"]}
    return (
        '<article class="game-block"><div class="head"><div>'
        '<h2>%s</h2><p class="tagline">%s</p></div>'
        '<a class="view-all" href="%s">%s &rarr;</a></div>%s</article>'
        % (game["name"][lang], game["tagline"][lang], hub[lang], c["view_all"], "".join(rows))
    )


def home_page(lang):
    c = HOME_COPY[lang]
    feats = featured_for(lang)
    cards = "".join(featured_card(lang, t) for t in feats)
    grid_cls = "featured-grid one" if len(feats) == 1 else "featured-grid"
    first = feats[0] if feats else None
    primary = ('<a class="btn btn-primary" href="%s">%s</a>'
               % (tool_url(lang, first), first["title"][lang])) if first else ""
    about_url = "/about/" if lang == "en" else "/ru/about/"
    blocks = "".join(game_block(lang, g) for g in game_order(lang))
    trust_items = "".join("<li><b>%s</b>%s</li>" % (t, d) for t, d in c["trust"])
    body = (
        '<main class="wrap">'
        '<section class="hero"><h1>%s</h1><p class="lede">%s</p>'
        '<div class="cta">%s<a class="btn btn-secondary" href="%s">%s</a></div></section>'
        '<section class="block"><h2>%s</h2><div class="%s">%s</div></section>'
        '<section class="block"><h2>%s</h2>%s</section>'
        '<section class="trust"><ol>%s</ol></section>'
        '</main>'
        % (c["h1"], c["lede"], primary, about_url, c["secondary"],
           c["featured_h"], grid_cls, cards, c["games_h"], blocks, trust_items)
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
        "tm": "AION 2 is a trademark of NCSOFT. Grand Theft Auto and Rockstar Games are trademarks of Take-Two Interactive. BuffForge is not affiliated with, endorsed by, or sponsored by NCSOFT, Rockstar Games, or Take-Two Interactive.",
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
        "tm": "AION 2 — торговая марка NCSOFT. Grand Theft Auto и Rockstar Games — торговые марки Take-Two Interactive. BuffForge не связан с NCSOFT, Rockstar Games и Take-Two Interactive и не одобрен ими.",
    },
}


def about_page(lang):
    c = ABOUT_COPY[lang]
    secs = "".join(
        '<section class="block prose"><h2 class="sec">%s</h2><p>%s</p></section>' % (h, p)
        for h, p in c["sections"])
    body = (
        '<main class="wrap narrow">%s'
        '<h1 class="page-h1">%s</h1><p class="page-lede">%s</p>%s'
        '<p class="data-line">%s</p></main>'
        % (crumbs_html(lang, [(c["h1"], None)]), c["h1"], c["lede"], secs, c["tm"])
    )
    canon = "/about/" if lang == "en" else "/ru/about/"
    alt = {"en": "/about/", "ru": "/ru/about/"}
    jl = breadcrumb_jsonld(lang, [(HOME_COPY[lang]["games_h"] if False else ("Home" if lang == "en" else "Главная"), "/" if lang == "en" else "/ru/"), (c["h1"], canon)])
    return page(lang, c["title"], c["desc"], canon, alt, body, jsonld=jl)


# ---------------------------------------------------------------- hubs
HUB_COPY = {
    "aion-2": {
        "en": {
            "title": "AION 2 Tools & Guides | BuffForge",
            "desc": "BuffForge's AION 2 hub: the daily and weekly tracker for global servers. Daily reset 07:00 UTC, weekly reset Wednesday 07:00 UTC.",
            "h1": "AION 2",
            "lede": "Global service, launched Oct 5, 2026. NC America reported more than 400,000 concurrent players after launch. This hub tracks the global servers only — Korea and Taiwan reset at a different hour.",
            "tools_h": "Tools", "guides_h": "Guides",
        },
        "ru": {
            "title": "AION 2 — инструменты и гайды | BuffForge",
            "desc": "Хаб AION 2 на BuffForge: трекер ежедневных и еженедельных заданий для глобальных серверов. Сброс каждый день в 10:00 по Москве, еженедельный — в среду в 10:00 МСК.",
            "h1": "AION 2",
            "lede": "Глобальный сервис, запуск 5 октября 2026 года. По данным NC America, после запуска онлайн превышал 400 000 игроков одновременно. Этот хаб — только для глобальных серверов: Корея и Тайвань сбрасываются в другое время.",
            "tools_h": "Инструменты", "guides_h": "Гайды",
        },
    },
    "gta-6": {
        "en": {
            "title": "GTA 6 Tools & Guides | BuffForge",
            "desc": "BuffForge's GTA 6 hub: storage check, launch countdown, editions compared, and console compatibility for PS5 and Xbox Series X|S. Launches Nov 19, 2026.",
            "h1": "GTA 6",
            "lede": "Grand Theft Auto VI launches Nov 19, 2026 on PS5 (including Pro) and Xbox Series X|S. There is no PC version at launch and no PS4 version. Tools here use official facts only; pre-launch mechanics are labelled and re-checked after release.",
            "tools_h": "Tools", "guides_h": "Guides",
        },
        "ru": {
            "title": "GTA 6 — инструменты и гайды | BuffForge",
            "desc": "Хаб GTA 6 на BuffForge: проверка места на диске, обратный отсчёт до выхода, сравнение изданий и совместимость с консолями PS5 и Xbox Series X|S. Выход — 19 ноября 2026 года.",
            "h1": "GTA 6",
            "lede": "Grand Theft Auto VI выходит 19 ноября 2026 года на PS5 (включая Pro) и Xbox Series X|S. Версии для ПК на старте нет, версии для PS4 — тоже. Инструменты здесь — только по официальным данным; механики до выхода помечены и перепроверяются после релиза.",
            "tools_h": "Инструменты", "guides_h": "Гайды",
        },
    },
}


def hub_page(game_id, lang):
    c = HUB_COPY[game_id][lang]
    game = GAMES_DATA[game_id]
    tools = tools_for(game_id)
    cards = []
    for t in tools:
        cards.append(
            '<a class="card" href="%s"><span class="tag">%s &middot; %s</span>'
            '<h3>%s</h3><p>%s</p>'
            '<span class="go">%s &rarr;</span>'
            '<div class="meta">%s</div></a>'
            % (tool_url(lang, t), game["name"][lang],
               "Live" if t["status"] == "live" else "Pre-launch",
               t["title"][lang],
               t["blurb"][lang],
               HOME_COPY[lang]["open"],
               HOME_COPY[lang]["reviewed"]))
    hub_path = "/%s/" % game_id if lang == "en" else "/ru/%s/" % game_id
    alt = {"en": "/%s/" % game_id, "ru": "/ru/%s/" % game_id}
    home_label = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    body = (
        '<main class="wrap">%s'
        '<section class="tool-hero"><h1>%s</h1><p class="sub">%s</p></section>'
        '<h2 class="sec">%s</h2>%s'
        '</main>'
        % (crumbs_html(lang, [(home_label, home_path), (game["name"][lang], None)]),
           c["h1"], c["lede"], c["tools_h"], "".join(cards))
    )
    jl = breadcrumb_jsonld(lang, [(home_label, home_path), (game["name"][lang], hub_path)])
    return page(lang, c["title"], c["desc"], hub_path, alt, body,
                jsonld=jl, games=(game_id,))


# ---------------------------------------------------------------- 404
def not_found_page():
    body = (
        '<main class="wrap narrow">'
        '<h1 class="page-h1">Page not found</h1>'
        '<div class="prose"><p>This page does not exist on BuffForge. It may have moved, or the address was typed wrong.</p>'
        '<p><a href="/">Go to the BuffForge home page</a> or pick a game:</p>'
        '<ul><li><a href="/aion-2/">AION 2</a> — daily &amp; weekly tracker</li>'
        '<li><a href="/gta-6/">GTA 6</a> — storage check, launch countdown, editions, compatibility</li></ul>'
        '<p>Russian version: <a href="/ru/">BuffForge на русском</a>.</p></div></main>'
    )
    # 404 page: no hreflang pair, noindex, canonical to itself.
    html = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n%s\n</head>\n<body>\n%s\n%s\n%s\n</body>\n</html>\n'
            % (head("en", "Page Not Found — BuffForge",
                    "This page does not exist on BuffForge.",
                    "/404.html", None, None),
               header_html("en", "/404.html", "/ru/"),
               body, footer_html("en", ("aion-2", "gta-6"))))
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
    for gid in ("aion-2", "gta-6"):
        write("%s/index.html" % gid, hub_page(gid, "en"))
        write("ru/%s/index.html" % gid, hub_page(gid, "ru"))
    write("404.html", not_found_page())
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
