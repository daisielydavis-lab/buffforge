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
        "secondary": "How we check our numbers",
        "featured_h": "Featured tools",
        "games_h": "Games",
        "games_intro": 'Games on BuffForge today: <a href="/aion-2/">AION 2 tools and guides</a> and <a href="/gta-6/">GTA 6 tools and guides</a>.',
        "how_h": "How we check every number",
        "faq_h": "Frequently asked questions",
        "faq": [
            ("What is BuffForge?", "A free site of game tools, trackers and calculators. Every number has a source and a review date."),
            ("Do I need an account?", "No."),
            ("Is BuffForge official?", "No. BuffForge is an independent fan project, not affiliated with any publisher."),
            ("Which games are covered?", "See the Games section below. We add a game only when we can source the numbers."),
            ("How do you check numbers?", "Public sources only. Every tool shows its data version, sources, and review date. Corrections are welcome — see About."),
        ],
        "open": "Open the tool",
        "trust": [
            ("Public sources only", "Numbers come from official notes, official wikis, and public APIs."),
            ("Versioned and dated", "Every tool shows its data version, sources, and review date."),
            ("Tell us when we are wrong", "If we get a number wrong, tell us. We correct it."),
        ],
        "reviewed": "Data reviewed Nov 13, 2026",
    },
    "ru": {
        "title": "BuffForge — игровые инструменты, трекеры и калькуляторы",
        "desc": "Бесплатные игровые инструменты, трекеры и калькуляторы. У каждой цифры — источник и дата проверки. Без регистрации и рекламы.",
        "h1": "Игровые инструменты, трекеры и калькуляторы",
        "lede": "BuffForge — бесплатные игровые инструменты, трекеры и калькуляторы. У каждой цифры есть открытый источник и дата проверки. Регистрации и рекламы нет. Инструменты сгруппированы по играм: откройте игру, чтобы найти трекеры, проверки и — когда появятся проверенные цифры — гайды. BuffForge — независимый фанатский проект, не связанный с издателями. Текстовые гайды выходят только после проверки цифр; сейчас в центре — сами инструменты.",
        "secondary": "Как мы проверяем цифры",
        "featured_h": "Главные инструменты",
        "games_h": "Игры",
        "games_intro": 'Игры на BuffForge сегодня: <a href="/ru/gta-6/">инструменты и гайды по GTA 6</a> и <a href="/ru/aion-2/">инструменты и гайды по AION 2</a>.',
        "how_h": "Как мы проверяем каждую цифру",
        "faq_h": "Частые вопросы",
        "faq": [
            ("Что такое BuffForge?", "Бесплатный сайт игровых инструментов, трекеров и калькуляторов. У каждой цифры — источник и дата проверки."),
            ("Нужна ли регистрация?", "Нет."),
            ("Это официальный сайт?", "Нет. BuffForge — независимый фанатский проект, не связанный с издателями."),
            ("По каким играм есть инструменты?", "Смотрите раздел «Игры» ниже. Игра добавляется, только когда мы можем проверить цифры."),
            ("Как вы проверяете цифры?", "Только открытые источники. У каждого инструмента — версия данных, источники и дата проверки. Об ошибках можно написать нам — смотрите «О проекте»."),
        ],
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
            % (tool_url(lang, t), t["title"][lang], badge(lang, t), t["blurb"][lang],
               tool_url(lang, t), c["open"]))
    hub = game["hub"] if "hub" in game else {"en": "/%s/" % game["slug"], "ru": "/ru/%s/" % game["slug"]}
    return (
        '<article class="game-block"><div class="head"><div>'
        '<h3>%s</h3><p class="tagline">%s</p></div>'
        '<a class="view-all" href="%s">%s &rarr;</a></div>%s</article>'
        % (game["name"][lang], game["tagline"][lang], hub[lang],
           game_anchor(lang, game), "".join(rows))
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
    faq_items = "".join("<h3>%s</h3><p>%s</p>" % (q, a) for q, a in c["faq"])
    body = (
        '<main class="wrap">'
        '<section class="hero"><h1>%s</h1><p class="lede">%s</p>'
        '<div class="cta">%s<a class="btn btn-secondary" href="%s">%s</a></div></section>'
        '<section class="block"><h2>%s</h2><div class="%s">%s</div></section>'
        '<section class="block"><h2>%s</h2><p class="intro">%s</p>%s</section>'
        '<section class="trust"><h2><a href="%s">%s</a></h2><ol>%s</ol></section>'
        '<section class="block prose faq"><h2>%s</h2>%s</section>'
        '</main>'
        % (c["h1"], c["lede"], primary, about_url, c["secondary"],
           c["featured_h"], grid_cls, cards, c["games_h"], c["games_intro"], blocks,
           about_url, c["how_h"], trust_items, c["faq_h"], faq_items)
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
            "title": "AION 2 tools and guides — BuffForge",
            "desc": "AION 2 tools and guides: daily and weekly tracker, reset times (07:00 UTC), and sourced checklists for global servers. No login, no ads.",
            "h1": "AION 2 tools and guides",
            "lede": "This is the BuffForge hub for AION 2 tools and guides on the global servers. The live tool is a daily and weekly tracker: tick duties off and watch the countdown to the 07:00 UTC daily reset and the Wednesday weekly reset. Reset times and any figures we publish cite public sources and a review date. Guides will appear here only when we can source them. BuffForge is an independent fan project, not affiliated with NC. No login, no ads.",
            "tools_h": "Tools", "guides_h": "Guides",
        },
        "ru": {
            "title": "AION 2: трекер и гайды, сброс 10:00 МСК — BuffForge",
            "desc": "Инструменты и гайды по AION 2: трекер ежедневных заданий, время сброса 10:00 МСК, чек-листы для глобальных серверов. Без регистрации и рекламы.",
            "h1": "Инструменты и гайды по AION 2",
            "lede": "Это хаб BuffForge с инструментами и гайдами по AION 2 для глобальных серверов. Живой инструмент — трекер ежедневных и еженедельных заданий: отмечайте задания и следите за обратным отсчётом до сброса в 10:00 по Москве и еженедельного сброса в среду в 10:00 МСК. Время сброса и все цифры мы публикуем с указанием открытых источников и даты проверки. Гайды появятся здесь, только когда мы сможем проверить цифры. BuffForge — независимый фанатский проект, не связанный с NC. Без регистрации и рекламы.",
            "tools_h": "Инструменты", "guides_h": "Гайды",
        },
    },
    "gta-6": {
        "en": {
            "title": "GTA 6 tools and guides — BuffForge",
            "desc": "GTA 6 tools and guides: storage check (at least 212 GB), Nov 19 unlock time, Standard vs Ultimate, and console compatibility. Official public figures only.",
            "h1": "GTA 6 tools and guides",
            "lede": "This is the BuffForge hub for GTA 6 tools and guides. Four tools use official facts only: a storage check (at least 212 GB), a Nov 19 launch countdown by store region, a Standard vs Ultimate comparison ($79.99 vs $99.99, US MSRP from Take-Two), and a console compatibility check. There is no officially announced PC version. BuffForge is an independent fan project, not affiliated with Rockstar Games or Take-Two Interactive. No login, no ads.",
            "tools_h": "Tools — official facts", "guides_h": "Guides",
        },
        "ru": {
            "title": "GTA 6 инструменты и гайды: 212 ГБ, 19 ноября — BuffForge",
            "desc": "Инструменты и гайды по GTA 6: сколько весит (не менее 212 ГБ), во сколько выйдет 19 ноября, издания и совместимость. Только официальные цифры.",
            "h1": "Инструменты и гайды по GTA 6",
            "lede": "Это хаб BuffForge с инструментами и гайдами по GTA 6. Четыре инструмента — только по официальным цифрам: проверка места (не менее 212 ГБ), обратный отсчёт до 19 ноября по региону магазина, сравнение изданий Standard и Ultimate ($79.99 и $99.99, рекомендованные цены Take-Two в США) и проверка совместимости консолей. Версия для ПК официально не анонсирована. BuffForge — независимый фанатский проект, не связанный с Rockstar Games и Take-Two Interactive. Без регистрации и рекламы.",
            "tools_h": "Инструменты — официальные данные", "guides_h": "Гайды",
        },
    },
}


HUB_BODY = {
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
            "other": [("GTA 6 tools and guides", "/gta-6/"),
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
            "other": [("инструменты и гайды по GTA 6", "/ru/gta-6/"),
                      ("игровые инструменты и трекеры BuffForge", "/ru/")],
        },
    },
    "gta-6": {
        "en": {
            "prelaunch_h": "Pre-launch tool",
            "prelaunch_note": "Based on pre-release previews. Mechanics will be verified in-game after launch on Nov 19, 2026. This tool is not featured and is not in the sitemap.",
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
                ("Can I play on PS4 or Xbox One?", "No. GTA 6 launches on PS5 (including Pro) and Xbox Series X|S only."),
            ],
            "other_h": "Other games on BuffForge",
            "other": [("AION 2 tools and guides", "/aion-2/"),
                      ("BuffForge game tools and trackers", "/")],
        },
        "ru": {
            "prelaunch_h": "Инструмент до выхода",
            "prelaunch_note": "По материалам превью до выхода. После 19 ноября 2026 года сверим механику с игрой. Инструмент не входит в главный блок и не входит в sitemap.",
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
                ("Можно ли купить GTA 6 в официальном магазине в России?", "По состоянию на ноябрь 2026 года купить игру в российском PlayStation Store или через Microsoft Store в России по официальным каналам нельзя."),
                ("Standard или Ultimate — что выбрать?", "Standard — $79.99, Ultimate — $99.99 (рекомендованные цены Take-Two в США). Что входит в каждое издание — на странице сравнения."),
            ],
            "other_h": "Другие игры на BuffForge",
            "other": [("инструменты и гайды по AION 2", "/ru/aion-2/"),
                      ("игровые инструменты и трекеры BuffForge", "/ru/")],
        },
    },
}


def hub_card(lang, game, t):
    status = "Live" if t["status"] == "live" else "Pre-launch"
    if lang == "ru":
        status = "Доступно" if t["status"] == "live" else "До выхода"
    return (
        '<a class="card" href="%s"><span class="tag">%s &middot; %s</span>'
        '<h3>%s</h3><p>%s</p>'
        '<span class="go">%s &rarr;</span>'
        '<div class="meta">%s</div></a>'
        % (tool_url(lang, t), game["name"][lang], status,
           t["title"][lang], t["blurb"][lang],
           HOME_COPY[lang]["open"], HOME_COPY[lang]["reviewed"])
    )


def hub_page(game_id, lang):
    c = HUB_COPY[game_id][lang]
    b = HUB_BODY[game_id][lang]
    game = GAMES_DATA[game_id]
    tools = tools_for(game_id)
    live_cards = "".join(hub_card(lang, game, t) for t in tools if t["status"] == "live")
    pre_cards = "".join(hub_card(lang, game, t) for t in tools if t["status"] == "pre-launch")
    hub_path = "/%s/" % game_id if lang == "en" else "/ru/%s/" % game_id
    alt = {"en": "/%s/" % game_id, "ru": "/ru/%s/" % game_id}
    home_label = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    secs = ['<h2 class="sec">%s</h2>%s' % (c["tools_h"], live_cards)]
    if pre_cards:
        secs.append('<h2 class="sec">%s</h2><p class="intro-note">%s</p>%s'
                    % (b["prelaunch_h"], b["prelaunch_note"], pre_cards))
    if "reset" in b:
        reset_rows = "".join("<h3>%s</h3><p>%s</p>" % (h, p) for h, p in b["reset"])
        secs.append('<section class="block prose"><h2 class="sec">%s</h2>%s</section>'
                    % (b["reset_h"], reset_rows))
    secs.append('<section class="block prose"><h2 class="sec">%s</h2><p>%s</p></section>'
                % (b["guides_h"], b["guides_note"]))
    planned_items = "".join("<li>%s</li>" % p for p in b["planned"])
    secs.append('<section class="block prose"><h2 class="sec">%s</h2><ul>%s</ul></section>'
                % (b["planned_h"], planned_items))
    faq_items = "".join("<h3>%s</h3><p>%s</p>" % (q, a) for q, a in b["faq"])
    secs.append('<section class="block prose faq"><h2 class="sec">%s</h2>%s</section>'
                % (b["faq_h"], faq_items))
    other_links = " &middot; ".join('<a href="%s">%s</a>' % (href, label)
                                     for label, href in b["other"])
    secs.append('<section class="block"><h2 class="sec">%s</h2><p>%s</p></section>'
                % (b["other_h"], other_links))
    body = (
        '<main class="wrap">%s'
        '<section class="tool-hero"><h1>%s</h1><p class="sub">%s</p></section>'
        '%s'
        '</main>'
        % (crumbs_html(lang, [(home_label, home_path), (game["name"][lang], None)]),
           c["h1"], c["lede"], "".join(secs))
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
