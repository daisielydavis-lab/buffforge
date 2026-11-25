#!/usr/bin/env python3
"""Path of Exile 2 tools (EN + RU): launch countdown, class selector,
resistance calculator, campaign checklist.

Run:  cd <repo root> && python3 scripts/build_poe2.py
Rebuild of the user-supplied demo (2026-11-25) in the Daylight Forge light
system. The interactive logic is the demo's — only the styling is the
site's own (.poe-* classes in assets/site.css), plus the verified notes
below. No Google Fonts. No live data: every number is Early Access 0.5.5
or the confirmed 1.0 date.

Verified vs the demo (facts checked 2026-11-25):
- 1.0 launches 11 Dec 2026 (PST), free to play; exact launch hour not
  announced (Steam API, app 2694490; GGG ExileCon announcement). The
  countdown tracks the confirmed calendar date only, never an assumed hour.
- Resistance: default max 75%, hard cap 90%; penalty Act 2 -10%, Act 3
  -20%, Act 4 -30%, area 54-59 -40%, 60-64 -50%, 65+ -60%; penalty does
  NOT apply to chaos (poe2wiki Resistance, read live 25 Nov 2026). The
  wiki has no 1.0 entry, so the presets stay labelled Early Access.
- Campaign checklist: all 27 entries cross-checked against Gamers.Wiki
  (permanent stat rewards, 0.5.5) and pathofexile.gg (full walkthrough,
  0.5.5). Spirit total +100 (30 + 30 + 40); weapon-set points +24
  (12 x +2). A 13th weapon-set source (Trial of the Ancestors, Act 4)
  is listed by pathofexile.gg but not by the other sources, so it stays
  excluded with the note, exactly as the demo flags it.
- Classes: 8 Early Access classes (Warrior, Monk, Ranger, Mercenary,
  Witch, Sorceress, Huntress, Druid). Shadow and Duelist arrive with
  1.0 and are not scored until their final mechanics are verified.
- Review date 25 November 2026.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import (BASE, breadcrumb_jsonld, crumbs_html, page)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STEAM_URL = "https://store.steampowered.com/app/2694490/Path_of_Exile_2/"
WIKI_RES_URL = "https://www.poe2wiki.net/wiki/Resistance"
POE2REF_URL = "https://poe2ref.com/guides/resistances"
WIKI_CLASS_URL = "https://www.poe2wiki.net/wiki/Category:Character_classes"
POE2DB_CLASS_URL = "https://poe2db.tw/us/Character_class"
GAMERS_WIKI_URL = "https://gamers.wiki/en/games/path-of-exile-2/lists/poe-2-permanent-stat-rewards-checklist"
POEGG_URL = "https://pathofexile.gg/campaign/"
EXILEDB_URL = "https://exiledb.com/tools/campaign"

CANON = {
    "countdown": {"en": "/path-of-exile-2/launch-countdown/",
                  "ru": "/ru/path-of-exile-2/launch-countdown/"},
    "class": {"en": "/path-of-exile-2/class-selector/",
              "ru": "/ru/path-of-exile-2/class-selector/"},
    "resistance": {"en": "/path-of-exile-2/resistance-calculator/",
                   "ru": "/ru/path-of-exile-2/resistance-calculator/"},
    "checklist": {"en": "/path-of-exile-2/campaign-checklist/",
                  "ru": "/ru/path-of-exile-2/campaign-checklist/"},
}

# Checklist data: [act, boss, zone, reward, weapon-set points, spirit].
# Boss and zone names stay in English in both languages (in-game names).
CHECKLIST_EN = [
    ["Act 1", "Beira", "Clearfell", "Cold resistance +10%", 0, 0],
    ["Act 1", "Crowbell", "Hunting Grounds", "Weapon-set points +2", 2, 0],
    ["Act 1", "King in the Mists", "Freythorn", "Spirit +30", 0, 30],
    ["Act 1", "Una\u2019s Lute", "Ogham Farmlands", "Weapon-set points +2", 2, 0],
    ["Act 1", "Candlemass", "Ogham Manor", "Maximum life +20", 0, 0],
    ["Act 2", "Kabala", "Keth", "Weapon-set points +2", 2, 0],
    ["Act 2", "Final Letter", "Deshar", "Weapon-set points +2", 2, 0],
    ["Act 2", "Garukhan shrine", "Spires of Deshar", "Lightning resistance +10%", 0, 0],
    ["Act 2", "Relic Altar", "Valley of the Titans", "Charm slot and selectable bonus", 0, 0],
    ["Act 3", "Mighty Silverfist", "Jungle Ruins", "Weapon-set points +2", 2, 0],
    ["Act 3", "Blackjaw", "Jiquani\u2019s Machinarium", "Fire resistance +10%", 0, 0],
    ["Act 3", "Ignagduk", "Azak Bog", "Spirit +30", 0, 30],
    ["Act 3", "Sacrificial Heart", "Aggorat", "Weapon-set points +2", 2, 0],
    ["Act 3", "Venom Draught", "Venom Crypts", "Selectable permanent modifier", 0, 0],
    ["Act 4", "Shark Fin", "Whakapanu Island", "Defence choice", 0, 0],
    ["Act 4", "Goddess of Justice", "Abandoned Prison", "Flask recovery choice", 0, 0],
    ["Act 4", "Silent Hall", "Eye of Hinekora", "Maximum mana +5%", 0, 0],
    ["Act 4", "Tattoo tests", "Halls of the Dead", "Attribute or resistance choices", 0, 0],
    ["Act 4", "Yama", "Halls of the Dead", "Weapon-set points +2", 2, 0],
    ["Act 4", "Omniphobia", "Journey\u2019s End", "Weapon-set points +2", 2, 0],
    ["Interlude I", "Oswin", "Wolvenhold", "Weapon-set points +2", 2, 0],
    ["Interlude II", "Akthi and Anundr", "Khari Crossing", "Weapon-set points +2", 2, 0],
    ["Interlude II", "Molten One\u2019s Gift", "Skullmaw Stairway", "Maximum life +5%", 0, 0],
    ["Interlude II", "Orbala\u2019s Pillar", "Qimah", "Selectable boon", 0, 0],
    ["Interlude III", "Lythara", "Kriar Village", "Spirit +40", 0, 40],
    ["Interlude III", "Hilda", "Glacial Tarn", "Weapon-set points +2", 2, 0],
    ["Interlude III", "Hooded One", "After all interludes", "Weapon-set points +2", 2, 0],
]

# Same rows, Russian act names and reward strings.
CHECKLIST_RU = [
    ["Акт 1", "Beira", "Clearfell", "Сопротивление холоду +10%", 0, 0],
    ["Акт 1", "Crowbell", "Hunting Grounds", "Очки комплектов оружия +2", 2, 0],
    ["Акт 1", "King in the Mists", "Freythorn", "Дух +30", 0, 30],
    ["Акт 1", "Una\u2019s Lute", "Ogham Farmlands", "Очки комплектов оружия +2", 2, 0],
    ["Акт 1", "Candlemass", "Ogham Manor", "Максимум жизни +20", 0, 0],
    ["Акт 2", "Kabala", "Keth", "Очки комплектов оружия +2", 2, 0],
    ["Акт 2", "Final Letter", "Deshar", "Очки комплектов оружия +2", 2, 0],
    ["Акт 2", "Garukhan shrine", "Spires of Deshar", "Сопротивление молнии +10%", 0, 0],
    ["Акт 2", "Relic Altar", "Valley of the Titans", "Ячейка амулета и выбираемый бонус", 0, 0],
    ["Акт 3", "Mighty Silverfist", "Jungle Ruins", "Очки комплектов оружия +2", 2, 0],
    ["Акт 3", "Blackjaw", "Jiquani\u2019s Machinarium", "Сопротивление огню +10%", 0, 0],
    ["Акт 3", "Ignagduk", "Azak Bog", "Дух +30", 0, 30],
    ["Акт 3", "Sacrificial Heart", "Aggorat", "Очки комплектов оружия +2", 2, 0],
    ["Акт 3", "Venom Draught", "Venom Crypts", "Выбираемый постоянный модификатор", 0, 0],
    ["Акт 4", "Shark Fin", "Whakapanu Island", "Выбор защиты", 0, 0],
    ["Акт 4", "Goddess of Justice", "Abandoned Prison", "Выбор восстановления флаконов", 0, 0],
    ["Акт 4", "Silent Hall", "Eye of Hinekora", "Максимум маны +5%", 0, 0],
    ["Акт 4", "Tattoo tests", "Halls of the Dead", "Выбор характеристик или сопротивлений", 0, 0],
    ["Акт 4", "Yama", "Halls of the Dead", "Очки комплектов оружия +2", 2, 0],
    ["Акт 4", "Omniphobia", "Journey\u2019s End", "Очки комплектов оружия +2", 2, 0],
    ["Интерлюдия I", "Oswin", "Wolvenhold", "Очки комплектов оружия +2", 2, 0],
    ["Интерлюдия II", "Akthi and Anundr", "Khari Crossing", "Очки комплектов оружия +2", 2, 0],
    ["Интерлюдия II", "Molten One\u2019s Gift", "Skullmaw Stairway", "Максимум жизни +5%", 0, 0],
    ["Интерлюдия II", "Orbala\u2019s Pillar", "Qimah", "Выбираемое благословение", 0, 0],
    ["Интерлюдия III", "Lythara", "Kriar Village", "Дух +40", 0, 40],
    ["Интерлюдия III", "Hilda", "Glacial Tarn", "Очки комплектов оружия +2", 2, 0],
    ["Интерлюдия III", "Hooded One", "After all interludes", "Очки комплектов оружия +2", 2, 0],
]

# Class data: [name, combat, weapon, pace, ease, mobility, impact, blurb].
CLASSES_EN = [
    ["Warrior", "Melee", "Heavy weapons", "Deliberate", 3, 1, 3, "Heavy hits and armour-oriented starting area."],
    ["Monk", "Melee", "Combos", "Fast", 1, 3, 2, "Mobile strikes and elemental combo potential."],
    ["Ranger", "Ranged", "Bows", "Fast", 2, 3, 1, "Bow attacks and movement-oriented play."],
    ["Mercenary", "Ranged", "Crossbows", "Deliberate", 2, 2, 2, "Crossbow ammunition and tactical attacks."],
    ["Witch", "Minions", "Summons", "Deliberate", 3, 1, 2, "Minion and occult skill themes."],
    ["Sorceress", "Spells", "Elements", "Deliberate", 2, 2, 3, "Elemental spellcasting and ranged damage."],
    ["Huntress", "Melee", "Spears", "Fast", 1, 3, 2, "Spear skills with mobile hybrid combat."],
    ["Druid", "Spells", "Shapeshifting", "Flexible", 1, 2, 3, "Shapeshifting and spell-oriented hybrid play."],
]

CLASSES_RU = [
    ["Warrior", "Ближний бой", "Тяжёлое оружие", "Размеренный", 3, 1, 3, "Тяжёлые удары и стартовая область с упором на броню."],
    ["Monk", "Ближний бой", "Комбо", "Быстрый", 1, 3, 2, "Мобильные удары и потенциал стихийных комбо."],
    ["Ranger", "Дальний бой", "Луки", "Быстрый", 2, 3, 1, "Атаки из лука и игра на подвижности."],
    ["Mercenary", "Дальний бой", "Арбалеты", "Размеренный", 2, 2, 2, "Боеприпасы арбалета и тактические атаки."],
    ["Witch", "Приспешники", "Призыв", "Размеренный", 3, 1, 2, "Приспешники и оккультные навыки."],
    ["Sorceress", "Заклинания", "Стихии", "Размеренный", 2, 2, 3, "Стихийные заклинания и урон на дистанции."],
    ["Huntress", "Ближний бой", "Копья", "Быстрый", 1, 3, 2, "Навыки копья и мобильный гибридный бой."],
    ["Druid", "Заклинания", "Смена облика", "Гибкий", 1, 2, 3, "Смена облика и гибрид на заклинаниях."],
]

# Resistance penalty presets: (value, label). Values verified on poe2wiki.
PENALTIES_EN = [
    (0, "Act 1 · 0%"), (10, "Act 2 · −10%"), (20, "Act 3 · −20%"),
    (30, "Act 4 · −30%"), (40, "Area level 54–59 · −40%"),
    (50, "Area level 60–64 · −50%"), (60, "Area level 65+ · −60%"),
]
PENALTIES_RU = [
    (0, "Акт 1 · 0%"), (10, "Акт 2 · −10%"), (20, "Акт 3 · −20%"),
    (30, "Акт 4 · −30%"), (40, "Уровень зоны 54–59 · −40%"),
    (50, "Уровень зоны 60–64 · −50%"), (60, "Уровень зоны 65+ · −60%"),
]

POE = {
    "en": {
        "eyebrow": "Path of Exile 2 / Interactive game tools",
        "reviewed": "Data reviewed 25 Nov 2026 · Early Access 0.5.5",
        "sources_h": "Sources",
        "explore_h": "Explore more tools",
        "countdown": {
            "title": "PoE 2 Release Date & Countdown | BuffForge",
            "desc": "Track the confirmed release date and understand the launch window in your local time.",
            "h1": "Path of Exile 2 Full Release Countdown",
            "lede": "Track the confirmed release date and understand the launch window in your local time.",
            "card_title": "Release Countdown",
            "pills": ["Release date: 11 Dec 2026 (PST)", "Free to play", "Exact hour: not announced"],
            "date_label": "Release date",
            "date_val": "Dec 11, 2026 (PST)",
            "access_label": "Access",
            "access_val": "Free to play",
            "hour_label": "Exact hour",
            "hour_val": "Not confirmed",
            "window_h": "Possible local release window",
            "window_p": "Shows the full confirmed calendar day in PST, not an announced launch time.",
            "zone_label": "Time zone",
            "what_h": "What\u2019s changing in 1.0?",
            "what_p": "Six-act campaign, two additional classes and weapon types, balance changes and a new challenge league. Preload details remain to be verified.",
            "steam_link": "Official Steam listing and announcement",
            "faq": [
                ("When does Path of Exile 2 1.0 come out?",
                 "11 Dec 2026 (PST). The exact launch hour has not been announced. The game becomes free to play at launch."),
                ("What time exactly does it launch?",
                 "The exact hour has not been announced. This page counts down to the confirmed calendar date, 11 Dec 2026 PST, and shows that whole day in your time zone — it does not assume a launch hour."),
                ("Is PoE 2 free to play at 1.0?",
                 "Yes. The full release on 11 Dec 2026 (PST) is free to play on Steam, PlayStation 5 and Xbox Series X|S."),
            ],
            "sources": [("Grinding Gear Games: Path of Exile 2 1.0 announcement (ExileCon 2026)", "https://www.pathofexile2.com/", "1.0 date and free-to-play launch"),
                        ("Steam store page (Path of Exile 2)", STEAM_URL, "Dec 11, 2026 release date")],
            "js": {"days_one": "day", "days_few": "days", "days_many": "days",
                   "until_suffix": "until release date",
                   "released": "Release date is here",
                   "date_only": "Date countdown only — no exact launch hour is assumed.",
                   "check_official": "Check the official announcement for live availability."},
        },
        "class": {
            "title": "PoE 2 Class Selector – Find Your Playstyle | BuffForge",
            "desc": "Compare eight Early Access classes by playstyle. Recommendations are editorial matches, not a damage ranking.",
            "h1": "Path of Exile 2 Class Selector",
            "lede": "Compare eight Early Access classes by playstyle. Recommendations are editorial matches, not a damage ranking.",
            "card_title": "Class Selector",
            "pills": ["8 Early Access classes", "Shadow & Duelist in 1.0", "Editorial matches, not a ranking"],
            "combat_label": "Combat style",
            "weapon_label": "Preferred weapon or theme",
            "pace_label": "Combat pace",
            "priority_label": "Priority",
            "any": "Any",
            "priorities": ["Ease of entry", "Mobility", "Heavy hits / spell impact"],
            "reset": "Reset preferences",
            "top_h": "Your top matches",
            "all_h": "Compare all classes",
            "note": "Shadow and Duelist are expected for 1.0; not scored before their final mechanics are verified. Builds are not locked to a class\u2019s typical weapons.",
            "guide_h": "Choosing your first class",
            "guide_p": "Start with the combat pattern you enjoy. Check skill requirements, survivability and resource costs before committing to a build. Ascendancy and balance changes may alter your choice.",
            "guide_link": "Class reference",
            "faq": [
                ("Is this a damage ranking?",
                 "No. The selector matches classes to the playstyle you pick — combat style, weapon theme and pace — and the scores are editorial. It does not rank damage or clear speed."),
                ("Why are Shadow and Duelist missing?",
                 "They arrive with 1.0 on 11 Dec 2026. Their final mechanics are not verified yet, so they are not scored. The note above says so, and they will be added once their numbers are confirmed."),
                ("Can a class use other weapons?",
                 "Yes. The class decides where you start on the passive tree and which ascendancies you get, not which weapons you are allowed to use."),
            ],
            "sources": [("Path of Exile 2 Wiki: Classes", WIKI_CLASS_URL, "class list"),
                        ("PoE2DB: Character classes", POE2DB_CLASS_URL, "class reference")],
            "js": {"match": "MATCH", "matches": "Matches:", "score": "Preference score:"},
        },
        "resistance": {
            "title": "PoE 2 Resistance Calculator – Caps & Gear Swaps | BuffForge",
            "desc": "Compare uncapped resistances, gear changes and campaign penalties without double-counting.",
            "h1": "Path of Exile 2 Resistance Calculator",
            "lede": "Compare uncapped resistances, gear changes and campaign penalties without double-counting.",
            "card_title": "Resistance Calculator",
            "pills": ["Default max: 75%", "Hard cap: 90%", "Penalty: up to \u221260%"],
            "mode_label": "Input mode",
            "mode_sheet": "Sheet value (after penalty)",
            "mode_raw": "Total bonuses (before penalty)",
            "pen_label": "Current elemental penalty",
            "target_label": "Target elemental penalty",
            "target_same": "Same as current",
            "hint": "Use uncapped totals, not the displayed capped number alone. Old/new gear values represent resistance bonuses on the swapped item.",
            "th_element": "Element", "th_input": "Input %", "th_old": "Old gear",
            "th_new": "New gear", "th_max": "Max %", "th_result": "Projected result",
            "reset": "Reset example",
            "guide_h": "How resistance works",
            "guide_p": "Default maximum resistance is 75%; maximum can be increased to 90%. Negative resistance increases incoming damage. Campaign penalty affects elemental resistances, not chaos. The stage presets reflect Early Access and must be reviewed for 1.0.",
            "guide_link1": "Resistance mechanics",
            "guide_link2": "Penalty reference",
            "faq": [
                ("What is the resistance cap?",
                 "75% by default. It can be raised to a hard cap of 90% with modifiers that increase maximum resistance."),
                ("Does the campaign penalty hit chaos resistance?",
                 "No. The penalty applies to fire, cold and lightning only. Chaos resistance is unaffected, and the calculator skips the penalty for the chaos row."),
                ("Why does the calculator ask for uncapped numbers?",
                 "The character sheet shows the capped value, which hides how much you actually have. Enter the uncapped total so a gear swap or a new penalty stage is calculated from the real number."),
            ],
            "sources": [("Path of Exile 2 Wiki: Resistance", WIKI_RES_URL, "caps and penalty table"),
                        ("poe2ref.com: Resistance guide", POE2REF_URL, "penalty reference")],
            "js": {"uncapped": "Uncapped", "gap": "Gap", "overcap": "Overcap",
                   "summary": "Combined resistance shortfall: {n} percentage points (not interchangeable between elements)."},
        },
        "checklist": {
            "title": "PoE 2 Campaign Checklist – Permanent Rewards Tracker | BuffForge",
            "desc": "Track a cross-checked selection of Early Access 0.5.5 permanent rewards. Acts 5–6 are pending verified data.",
            "h1": "Path of Exile 2 Campaign Reward Tracker",
            "lede": "Track a cross-checked selection of Early Access 0.5.5 permanent rewards. Acts 5–6 are pending verified data.",
            "card_title": "Campaign Checklist",
            "pills": ["27 tracked rewards", "Spirit total: +100", "Weapon-set points: +24"],
            "note": "Early Access checklist, not a complete 1.0 database. Sources disagree on an additional Act 4 passive reward; it is excluded until resolved.",
            "claimed_label": "Tracked rewards claimed",
            "points_label": "Weapon-set points claimed",
            "spirit_label": "Campaign Spirit claimed",
            "chapter_label": "Chapter",
            "search_label": "Search",
            "search_ph": "Boss, zone, reward",
            "status_label": "Status",
            "all": "All", "missing": "Missing", "claimed": "Claimed",
            "profile_label": "Character profile",
            "export": "Export progress",
            "reset": "Reset this profile",
            "saved": "Saved on this browser.",
            "no_storage": "Local storage unavailable; export progress before closing.",
            "reset_confirm": "Reset this character\u2019s progress?",
            "no_match": "No matching rewards.",
            "guide_h": "How to claim permanent rewards",
            "guide_p": "Mark a reward only after consuming the relevant item or completing the final interaction. A defeated boss alone may not apply the reward. Use a different profile name for each character.",
            "src1": "Permanent stats", "src2": "Campaign walkthrough", "src3": "Additional cross-check",
            "faq": [
                ("Do I have to kill the boss to get the reward?",
                 "Not always. Several rewards come from consuming an item the boss drops — a skull, an essence, a heart — or from an interaction such as paying respects or applying a tattoo. Mark a row only after that final step."),
                ("What is the +24 weapon-set points total?",
                 "Twelve +2 rewards across Acts 1–4 and the three Interludes. A 13th source (Trial of the Ancestors, Act 4) is listed by one walkthrough but not by the other sources, so it is excluded until resolved."),
                ("Does the checklist cover Acts 5–6?",
                 "No. Acts 5–6 arrive with 1.0 on 11 Dec 2026 and their rewards are not verified yet. This is an Early Access 0.5.5 checklist."),
            ],
            "sources": [("Gamers.Wiki: PoE 2 Permanent Stat Rewards Checklist", GAMERS_WIKI_URL, "0.5.5 reward table"),
                        ("pathofexile.gg: Campaign Full Walkthrough (0.5.5)", POEGG_URL, "route and rewards"),
                        ("ExileDB: PoE2 Campaign Checklist (0.5.5)", EXILEDB_URL, "cross-check")],
            "js": {"profile_default": "Default"},
        },
    },

    "ru": {
        "eyebrow": "Path of Exile 2 / Интерактивные инструменты",
        "reviewed": "Данные сверены 25 ноября 2026 · Ранний доступ 0.5.5",
        "sources_h": "Источники",
        "explore_h": "Другие инструменты",
        "countdown": {
            "title": "Дата выхода PoE 2 и отсчёт до 1.0 | BuffForge",
            "desc": "Следите за подтверждённой датой выхода и поймите окно запуска в вашем часовом поясе.",
            "h1": "Отсчёт до полного выхода Path of Exile 2",
            "lede": "Следите за подтверждённой датой выхода и поймите окно запуска в вашем часовом поясе.",
            "card_title": "Отсчёт до выхода",
            "pills": ["Дата выхода: 11 декабря 2026 (Тихоокеанское время)", "Бесплатно", "Точный час не объявлен"],
            "date_label": "Дата выхода",
            "date_val": "11 декабря 2026 (Тихоокеанское время)",
            "access_label": "Доступ",
            "access_val": "Бесплатно",
            "hour_label": "Точный час",
            "hour_val": "Не подтверждён",
            "window_h": "Возможное окно выхода по местному времени",
            "window_p": "Показан весь подтверждённый календарный день по тихоокеанскому времени, а не объявленное время запуска.",
            "zone_label": "Часовой пояс",
            "what_h": "Что меняется в 1.0?",
            "what_p": "Кампания из шести актов, два новых класса и вида оружия, правки баланса и новая лига испытаний. Детали предзагрузки пока не проверены.",
            "steam_link": "Официальная страница и объявление в Steam",
            "faq": [
                ("Когда выходит Path of Exile 2 1.0?",
                 "11 декабря 2026 года (тихоокеанское время). Точный час запуска не объявлен. При выходе игра становится бесплатной."),
                ("Во сколько именно запуск?",
                 "Точный час не объявлен. Эта страница считает дни до подтверждённой календарной даты, 11 декабря 2026 года по тихоокеанскому времени, и показывает этот день целиком в вашем часовом поясе — час запуска не предполагается."),
                ("PoE 2 будет бесплатной в 1.0?",
                 "Да. Полный выход 11 декабря 2026 года (тихоокеанское время) — бесплатный, в Steam, на PlayStation 5 и Xbox Series X|S."),
            ],
            "sources": [("Grinding Gear Games: анонс Path of Exile 2 1.0 (ExileCon 2026)", "https://www.pathofexile2.com/", "дата 1.0 и бесплатный выход"),
                        ("Страница в Steam (Path of Exile 2)", STEAM_URL, "дата выхода 11 декабря 2026")],
            "js": {"days_one": "день", "days_few": "дня", "days_many": "дней",
                   "until_suffix": "до даты выхода",
                   "released": "День выхода настал",
                   "date_only": "Только отсчёт до даты — точный час запуска не предполагается.",
                   "check_official": "Смотрите официальное объявление о доступности."},
        },
        "class": {
            "title": "Подборщик классов PoE 2 — найдите свой стиль игры | BuffForge",
            "desc": "Сравните восемь классов раннего доступа по стилю игры. Рекомендации — подбор по стилю, а не рейтинг урона.",
            "h1": "Подборщик классов Path of Exile 2",
            "lede": "Сравните восемь классов раннего доступа по стилю игры. Рекомендации — подбор по стилю, а не рейтинг урона.",
            "card_title": "Подборщик классов",
            "pills": ["8 классов раннего доступа", "Тень и Дуэлянт — в 1.0", "Подбор по стилю, а не рейтинг"],
            "combat_label": "Стиль боя",
            "weapon_label": "Оружие или тема",
            "pace_label": "Темп боя",
            "priority_label": "Приоритет",
            "any": "Любой",
            "priorities": ["Лёгкость входа", "Подвижность", "Тяжёлые удары / мощь заклинаний"],
            "reset": "Сбросить настройки",
            "top_h": "Ваши лучшие совпадения",
            "all_h": "Сравнить все классы",
            "note": "Тень и Дуэлянт ожидаются в 1.0; они не оцениваются, пока их финальная механика не проверена. Сборки не привязаны к типичному оружию класса.",
            "guide_h": "Выбор первого класса",
            "guide_p": "Начните с того стиля боя, который нравится. Перед выбором сборки проверьте требования навыков, живучесть и затраты ресурсов. Возвышения и баланс могут изменить выбор.",
            "guide_link": "Справочник классов",
            "faq": [
                ("Это рейтинг урона?",
                 "Нет. Подборщик сопоставляет классы с выбранным вами стилем игры — стилем боя, темой оружия и темпом, — а оценки редакционные. Урон и скорость зачистки он не ранжирует."),
                ("Почему нет Тени и Дуэлянта?",
                 "Они появятся в 1.0 11 декабря 2026 года. Их финальная механика ещё не проверена, поэтому они не оцениваются. Об этом сказано в примечании выше; классы будут добавлены, когда их цифры подтвердятся."),
                ("Может ли класс использовать другое оружие?",
                 "Да. Класс определяет, где вы начинаете на дереве пассивных навыков и какие возвышения получаете, а не какое оружие вам разрешено использовать."),
            ],
            "sources": [("Path of Exile 2 Wiki: классы", WIKI_CLASS_URL, "список классов"),
                        ("PoE2DB: классы персонажей", POE2DB_CLASS_URL, "справочник классов")],
            "js": {"match": "СОВПАДЕНИЕ", "matches": "Совпадает:", "score": "Оценка предпочтения:"},
        },
        "resistance": {
            "title": "Калькулятор сопротивлений PoE 2 — капы и замена вещей | BuffForge",
            "desc": "Сравните сопротивления без капа, смену вещей и штрафы кампании без двойного учёта.",
            "h1": "Калькулятор сопротивлений Path of Exile 2",
            "lede": "Сравните сопротивления без капа, смену вещей и штрафы кампании без двойного учёта.",
            "card_title": "Калькулятор сопротивлений",
            "pills": ["Максимум по умолчанию: 75%", "Жёсткий кап: 90%", "Штраф: до −60%"],
            "mode_label": "Режим ввода",
            "mode_sheet": "Текущее (после штрафа)",
            "mode_raw": "Сумма бонусов (до штрафа)",
            "pen_label": "Текущий штраф стихий",
            "target_label": "Целевой штраф стихий",
            "target_same": "Как сейчас",
            "hint": "Вводите суммы без капа, а не только отображаемое число с капом. Значения старой/новой вещи — это бонусы сопротивления на заменяемом предмете.",
            "th_element": "Стихия", "th_input": "Ввод %", "th_old": "Старая вещь",
            "th_new": "Новая вещь", "th_max": "Макс %", "th_result": "Прогноз",
            "reset": "Сбросить пример",
            "guide_h": "Как работают сопротивления",
            "guide_p": "Максимум сопротивления по умолчанию — 75%; его можно поднять до 90%. Отрицательное сопротивление увеличивает входящий урон. Штраф кампании действует на сопротивления стихиям, а не на хаос. Пресеты этапов — по раннему доступу, для 1.0 их нужно перепроверить.",
            "guide_link1": "Механика сопротивлений",
            "guide_link2": "Справочник по штрафам",
            "faq": [
                ("Какой кап сопротивлений?",
                 "75% по умолчанию. Его можно поднять до жёсткого капа в 90% модификаторами, увеличивающими максимум сопротивления."),
                ("Штраф кампании бьёт по сопротивлению хаосу?",
                 "Нет. Штраф действует только на огонь, холод и молнию. Сопротивление хаосу не затрагивается, и калькулятор пропускает штраф для строки хаоса."),
                ("Зачем калькулятор просит числа без капа?",
                 "На панели персонажа показано значение с капом, которое скрывает реальную сумму. Введите сумму без капа, чтобы замена вещи или новый этап штрафа считались от настоящего числа."),
            ],
            "sources": [("Path of Exile 2 Wiki: сопротивления", WIKI_RES_URL, "капы и таблица штрафов"),
                        ("poe2ref.com: гайд по сопротивлениям", POE2REF_URL, "справочник по штрафам")],
            "js": {"uncapped": "Без капа", "gap": "Не хватает", "overcap": "Сверх капа",
                   "summary": "Общий дефицит сопротивлений: {n} процентных пунктов (между стихиями не переносится)."},
        },
        "checklist": {
            "title": "Чек-лист кампании PoE 2 — трекер постоянных наград | BuffForge",
            "desc": "Отмечайте сверенную подборку постоянных наград раннего доступа 0.5.5. Акты 5–6 — после сверки данных.",
            "h1": "Трекер наград кампании Path of Exile 2",
            "lede": "Отмечайте сверенную подборку постоянных наград раннего доступа 0.5.5. Акты 5–6 — после сверки данных.",
            "card_title": "Чек-лист кампании",
            "pills": ["27 отслеживаемых наград", "Всего духа: +100", "Очков комплектов: +24"],
            "note": "Чек-лист раннего доступа, а не полная база 1.0. Источники расходятся по дополнительной пассивной награде Акта 4; она исключена до разрешения.",
            "claimed_label": "Отмечено наград",
            "points_label": "Получено очков комплектов",
            "spirit_label": "Получено духа кампании",
            "chapter_label": "Глава",
            "search_label": "Поиск",
            "search_ph": "Босс, зона, награда",
            "status_label": "Статус",
            "all": "Все", "missing": "Не получено", "claimed": "Получено",
            "profile_label": "Профиль персонажа",
            "export": "Экспорт прогресса",
            "reset": "Сбросить профиль",
            "saved": "Сохранено в этом браузере.",
            "no_storage": "Локальное хранилище недоступно; экспортируйте прогресс до закрытия.",
            "reset_confirm": "Сбросить прогресс этого персонажа?",
            "no_match": "Нет подходящих наград.",
            "guide_h": "Как получить постоянные награды",
            "guide_p": "Отмечайте награду только после использования предмета или завершения финального взаимодействия. Победа над боссом сама по себе может не дать награду. Для каждого персонажа используйте отдельное имя профиля.",
            "src1": "Постоянные характеристики", "src2": "Прохождение кампании", "src3": "Дополнительная сверка",
            "faq": [
                ("Нужно ли убить босса, чтобы получить награду?",
                 "Не всегда. Часть наград даётся за использование предмета, выпавшего с босса, — черепа, эссенции, сердца, — или за взаимодействие: почтить память или нанести татуировку. Отмечайте строку только после этого финального шага."),
                ("Откуда сумма +24 очка комплектов оружия?",
                 "Двенадцать наград по +2 в актах 1–4 и трёх интерлюдиях. Тринадцатый источник (Испытание предков, Акт 4) есть в одном прохождении, но не в других источниках, поэтому он исключён до разрешения."),
                ("Чек-лист покрывает акты 5–6?",
                 "Нет. Акты 5–6 появятся в 1.0 11 декабря 2026 года, и их награды ещё не проверены. Это чек-лист раннего доступа 0.5.5."),
            ],
            "sources": [("Gamers.Wiki: чек-лист постоянных характеристик PoE 2", GAMERS_WIKI_URL, "таблица наград 0.5.5"),
                        ("pathofexile.gg: полное прохождение кампании (0.5.5)", POEGG_URL, "маршрут и награды"),
                        ("ExileDB: чек-лист кампании PoE2 (0.5.5)", EXILEDB_URL, "дополнительная сверка")],
            "js": {"profile_default": "По умолчанию"},
        },
    },
}


def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def hero(lang, c):
    pills = "".join('<span class="wlh-pill">%s</span>' % p for p in c["pills"])
    return ('<section class="tool-hero">'
            '<p class="wlh-eyebrow">%s</p><h1>%s</h1>'
            '<p class="lede">%s</p><div class="wlh-pills">%s</div>'
            '<p class="field-help" style="margin-top:14px">%s</p></section>'
            % (POE[lang]["eyebrow"], c["h1"], c["lede"], pills, POE[lang]["reviewed"]))


def sources_block(lang, c):
    items = "".join(
        '<li><a href="%s" target="_blank" rel="noopener noreferrer">%s</a> (%s)</li>'
        % (url, text, note) for text, url, note in c["sources"])
    return '<section class="panel"><h2>%s</h2><ul>%s</ul></section>' % (POE[lang]["sources_h"], items)


def faq_block(lang, c):
    items = "".join(
        '<details><summary><h3>%s</h3><span class="plus">+</span></summary>'
        '<p>%s</p></details>' % (q, a) for q, a in c["faq"])
    return '<section><h2>%s</h2>%s</section>' % (
        "Frequently asked questions" if lang == "en" else "Частые вопросы", items)


def related_block(lang, current):
    others = [k for k in ("countdown", "class", "resistance", "checklist") if k != current]
    cards = "".join(
        '<a class="rel" href="%s"><b>%s</b><span>%s</span></a>'
        % (CANON[k][lang], POE[lang][k]["card_title"], POE[lang][k]["lede"])
        for k in others)
    return ('<section class="related"><h2>%s</h2>'
            '<div class="related-grid">%s</div></section>'
            % (POE[lang]["explore_h"], cards))


def tool_page(lang, key, body, js):
    c = POE[lang][key]
    home = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    hub_path = "/path-of-exile-2/" if lang == "en" else "/ru/path-of-exile-2/"
    canon = CANON[key][lang]
    alt = {"en": CANON[key]["en"], "ru": CANON[key]["ru"]}
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
                             for q, a in c["faq"]]}
    jl = [breadcrumb_jsonld(lang, [(home, home_path), ("Path of Exile 2", hub_path),
                                   (c["card_title"], canon)]),
          {"@context": "https://schema.org", "@type": "WebApplication",
           "name": c["h1"], "url": BASE + canon, "inLanguage": lang,
           "description": c["desc"], "applicationCategory": "GameApplication",
           "operatingSystem": "Any modern browser",
           "offers": {"@type": "Offer", "price": "0"}},
          faq_ld]
    full = ('<main id="main" class="wrap">%s%s%s%s%s</main>'
            % (crumbs_html(lang, [("Path of Exile 2", hub_path), (c["card_title"], None)]),
               body, sources_block(lang, c), faq_block(lang, c), related_block(lang, key)))
    return page(lang, c["title"], c["desc"], canon, alt, full, jsonld=jl,
                games=("path-of-exile-2",), tail="<script>%s</script>\n" % js)


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", rel)


def countdown_body(lang):
    c = POE[lang]["countdown"]
    zones = ["America/Los_Angeles", "America/New_York", "Europe/London",
             "Europe/Berlin", "Europe/Moscow", "Asia/Shanghai", "Asia/Tokyo",
             "America/Sao_Paulo"]
    opts = "".join('<option value="%s">%s</option>' % (z, z) for z in zones)
    pending = ("Confirmed date · Exact hour pending" if lang == "en"
               else "Подтверждённая дата · точный час неизвестен")
    return (
        hero(lang, c)
        + '<section class="panel"><p class="wlh-eyebrow">%s</p>' % pending
        + '<div class="countdown-big" id="cdDays">--</div>'
        + '<p id="cdStatus"></p>'
        + '<div class="wlh-progress"><span id="cdBar" style="width:0%"></span></div></section>'
        + '<div class="stats">'
        + '<div class="stat"><em>%s</em><strong>%s</strong></div>' % (c["date_label"], c["date_val"])
        + '<div class="stat"><em>%s</em><strong>%s</strong></div>' % (c["access_label"], c["access_val"])
        + '<div class="stat"><em>%s</em><strong>%s</strong></div></div>' % (c["hour_label"], c["hour_val"])
        + '<section class="panel"><h2>%s</h2><p>%s</p>' % (c["window_h"], c["window_p"])
        + '<div class="field"><label for="cdZone">%s</label>'
          '<div class="select-wrap"><select id="cdZone">%s</select></div></div>' % (c["zone_label"], opts)
        + '<div class="poe-window" id="cdWindow" style="margin-top:14px"></div></section>'
        + '<section class="panel"><h2>%s</h2><p>%s</p>' % (c["what_h"], c["what_p"])
        + '<p><a href="%s" target="_blank" rel="noopener noreferrer">%s</a></p></section>'
        % (STEAM_URL, c["steam_link"])
    )


CD_JS = """
(function () {
  var STR = __STR__;
  var start = new Date('2026-12-11T00:00:00-08:00'),
      end = new Date('2026-12-12T00:00:00-08:00');
  var z = document.getElementById('cdZone');
  var tz = null;
  try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone; } catch (e) {}
  if (tz) {
    var found = false;
    for (var i = 0; i < z.options.length; i++) if (z.options[i].value === tz) found = true;
    if (!found) z.insertBefore(new Option(tz, tz), z.firstChild);
    z.value = tz;
  }
  function plural(n, forms) {
    var m = Math.abs(n) % 100, d = m % 10;
    if (m > 10 && m < 20) return forms[2];
    if (d > 1 && d < 5) return forms[1];
    if (d === 1) return forms[0];
    return forms[2];
  }
  function update() {
    var n = Date.now();
    var daysEl = document.getElementById('cdDays');
    var statusEl = document.getElementById('cdStatus');
    var barEl = document.getElementById('cdBar');
    if (n < start) {
      var d = Math.max(0, Math.ceil((start - n) / 86400000));
      daysEl.textContent = d + ' ' + plural(d, [STR.days_one, STR.days_few, STR.days_many]) + ' ' + STR.until_suffix;
      statusEl.textContent = STR.date_only;
    } else {
      daysEl.textContent = STR.released;
      statusEl.textContent = STR.check_official;
    }
    barEl.style.width = Math.min(100, Math.max(0, (1 - (start - n) / (16 * 86400000)) * 100)) + '%';
    try {
      var f = new Intl.DateTimeFormat('en', {timeZone: z.value, dateStyle: 'medium', timeStyle: 'short'});
      document.getElementById('cdWindow').textContent = f.format(start) + ' \\u2013 ' + f.format(end);
    } catch (e) {}
  }
  z.addEventListener('change', update);
  update();
  setInterval(update, 60000);
})();
"""


def countdown_page(lang):
    c = POE[lang]["countdown"]
    js = CD_JS.replace("__STR__", json.dumps(c["js"], ensure_ascii=False))
    return tool_page(lang, "countdown", countdown_body(lang), js)


CLASS_OPTIONS = {
    "en": {
        "combat": ["Melee", "Ranged", "Spells", "Minions"],
        "weapon": ["Heavy weapons", "Combos", "Bows", "Crossbows", "Summons",
                   "Elements", "Spears", "Shapeshifting"],
        "pace": ["Fast", "Deliberate", "Flexible"],
    },
    "ru": {
        "combat": ["Ближний бой", "Дальний бой", "Заклинания", "Приспешники"],
        "weapon": ["Тяжёлое оружие", "Комбо", "Луки", "Арбалеты", "Призыв",
                   "Стихии", "Копья", "Смена облика"],
        "pace": ["Быстрый", "Размеренный", "Гибкий"],
    },
}


def _select_opts(options, any_label):
    out = '<option>%s</option>' % any_label
    out += "".join('<option>%s</option>' % o for o in options)
    return out


def class_body(lang):
    c = POE[lang]["class"]
    o = CLASS_OPTIONS[lang]
    pr_opts = "".join('<option value="%d">%s</option>' % (i, p)
                      for i, p in enumerate(c["priorities"]))
    return (
        hero(lang, c)
        + '<section class="panel"><div class="poe-grid4">'
        + '<div class="field"><label for="combat">%s</label><div class="select-wrap">'
          '<select id="combat">%s</select></div></div>' % (c["combat_label"], _select_opts(o["combat"], c["any"]))
        + '<div class="field"><label for="weapon">%s</label><div class="select-wrap">'
          '<select id="weapon">%s</select></div></div>' % (c["weapon_label"], _select_opts(o["weapon"], c["any"]))
        + '<div class="field"><label for="pace">%s</label><div class="select-wrap">'
          '<select id="pace">%s</select></div></div>' % (c["pace_label"], _select_opts(o["pace"], c["any"]))
        + '<div class="field"><label for="priority">%s</label><div class="select-wrap">'
          '<select id="priority">%s</select></div></div></div>' % (c["priority_label"], pr_opts)
        + '<p style="margin-top:16px"><button id="reset" type="button" class="btn btn-secondary">%s</button></p></section>'
        % c["reset"]
        + '<section><h2>%s</h2><div id="results" class="poe-grid"></div></section>' % c["top_h"]
        + '<section><h2>%s</h2><div id="all" class="poe-grid"></div></section>' % c["all_h"]
        + '<div class="note-box amber"><p>%s</p></div>' % c["note"]
        + '<section class="panel"><h2 id="guide">%s</h2><p>%s</p>' % (c["guide_h"], c["guide_p"])
        + '<p><a href="%s" target="_blank" rel="noopener noreferrer">%s</a></p></section>'
        % (POE2DB_CLASS_URL, c["guide_link"])
    )


CLASS_JS = """
(function () {
  var STR = __STR__;
  var data = __DATA__;
  function el(id) { return document.getElementById(id); }
  function render() {
    var ranked = data.map(function (x) {
      var score = Number(x[4 + Number(el('priority').value)]), why = [];
      [['combat', 1, 5], ['weapon', 2, 6], ['pace', 3, 3]].forEach(function (t) {
        if (el(t[0]).value === x[t[1]]) { score += t[2]; why.push(x[t[1]]); }
      });
      return {x: x, score: score, why: why};
    }).sort(function (a, b) { return b.score - a.score; });
    function card(r, i) {
      var tag = i !== undefined ? STR.match + ' ' + (i + 1) : r.x[1];
      var html = '<div class="card"><span class="tag">' + tag + '</span><h3>' + r.x[0] + '</h3><p>' + r.x[7] + '</p><small>' + r.x[2] + ' \\u00b7 ' + r.x[3] + '</small>';
      if (r.why.length) html += '<p class="poe-good">' + STR.matches + ' ' + r.why.join(', ') + '</p>';
      if (i !== undefined) html += '<p>' + STR.score + ' ' + r.score + '</p>';
      return html + '</div>';
    }
    el('results').innerHTML = ranked.slice(0, 3).map(function (r, i) { return card(r, i); }).join('');
    el('all').innerHTML = data.map(function (x) { return card({x: x, why: []}); }).join('');
  }
  document.querySelectorAll('select').forEach(function (x) { x.addEventListener('change', render); });
  el('reset').addEventListener('click', function () {
    document.querySelectorAll('select').forEach(function (x) { x.selectedIndex = 0; });
    render();
  });
  render();
})();
"""


def class_page(lang):
    c = POE[lang]["class"]
    data = CLASSES_EN if lang == "en" else CLASSES_RU
    js = CLASS_JS.replace("__STR__", json.dumps(c["js"], ensure_ascii=False))
    js = js.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    return tool_page(lang, "class", class_body(lang), js)


def resistance_body(lang):
    c = POE[lang]["resistance"]
    pens = PENALTIES_EN if lang == "en" else PENALTIES_RU
    pen_opts = "".join('<option value="%s">%s</option>' % (-v, l) for v, l in pens)
    tgt_opts = ('<option value="same">%s</option>' % c["target_same"]
                + "".join('<option value="%s">\u2212%s%%</option>' % (-v, v) for v, _ in pens))
    elements = ([("Fire", 45), ("Cold", 62), ("Lightning", 80), ("Chaos", -15)] if lang == "en"
                else [("Огонь", 45), ("Холод", 62), ("Молния", 80), ("Хаос", -15)])
    rows = ""
    for name, val in elements:
        rows += ('<tr><th>%s</th>'
                 '<td><input aria-label="%s current" type="number" value="%s" data-k="current"></td>'
                 '<td><input aria-label="%s old gear" type="number" value="0" data-k="old"></td>'
                 '<td><input aria-label="%s new gear" type="number" value="0" data-k="new"></td>'
                 '<td><input aria-label="%s cap" type="number" min="0" max="90" value="75" data-k="cap"></td>'
                 '<td data-out></td></tr>'
                 % (name, name, val, name, name, name))
    return (
        hero(lang, c)
        + '<section class="panel"><div class="poe-grid4">'
        + '<div class="field"><label for="mode">%s</label><div class="select-wrap">'
          '<select id="mode"><option value="sheet">%s</option><option value="raw">%s</option></select></div></div>'
          % (c["mode_label"], c["mode_sheet"], c["mode_raw"])
        + '<div class="field"><label for="pen">%s</label><div class="select-wrap">'
          '<select id="pen">%s</select></div></div>' % (c["pen_label"], pen_opts)
        + '<div class="field"><label for="target">%s</label><div class="select-wrap">'
          '<select id="target">%s</select></div></div></div>' % (c["target_label"], tgt_opts)
        + '<p class="field-help" style="margin-top:14px">%s</p>' % c["hint"]
        + '<div class="table-scroll"><table class="poe-table"><thead><tr>'
        + '<th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th>'
          % (c["th_element"], c["th_input"], c["th_old"], c["th_new"], c["th_max"], c["th_result"])
        + '</tr></thead><tbody>%s</tbody></table></div>' % rows
        + '<p id="summary" style="margin-top:14px"></p>'
        + '<p><button id="reset" type="button" class="btn btn-secondary">%s</button></p></section>'
        % c["reset"]
        + '<section class="panel"><h2 id="guide">%s</h2><p>%s</p>' % (c["guide_h"], c["guide_p"])
        + '<p><a href="%s" target="_blank" rel="noopener noreferrer">%s</a> \u00b7 '
          '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a></p></section>'
        % (WIKI_RES_URL, c["guide_link1"], POE2REF_URL, c["guide_link2"])
    )


RES_JS = """
(function () {
  var STR = __STR__;
  var rows = Array.prototype.slice.call(document.querySelectorAll('tbody tr'));
  var pen = document.getElementById('pen');
  var target = document.getElementById('target');
  var mode = document.getElementById('mode');
  var summary = document.getElementById('summary');
  function calc() {
    var current = +pen.value, targetP = target.value === 'same' ? current : +target.value, total = 0;
    rows.forEach(function (r, i) {
      var vals = Array.prototype.slice.call(r.querySelectorAll('input')).map(function (x) { return Number(x.value); });
      var base = vals[0], old = vals[1], nw = vals[2], cap = vals[3];
      cap = Math.min(90, Math.max(0, cap));
      var raw = base - old + nw - (i === 3 ? 0 : (mode.value === 'raw' ? targetP : targetP - current));
      var effective = Math.min(raw, cap);
      var gap = Math.max(0, cap - raw);
      var over = Math.max(0, raw - cap);
      total += gap;
      r.querySelector('[data-out]').innerHTML = '<strong class="' + (gap ? 'poe-bad' : 'poe-good') + '">' + effective.toFixed(1) + '%</strong><br><small>' + STR.uncapped + ' ' + raw.toFixed(1) + '% \\u00b7 ' + (gap ? STR.gap + ' ' + gap.toFixed(1) : STR.overcap + ' ' + over.toFixed(1)) + '%</small>';
    });
    summary.textContent = STR.summary.replace('{n}', total.toFixed(1));
  }
  document.querySelectorAll('input,select').forEach(function (x) { x.addEventListener('input', calc); });
  document.getElementById('reset').addEventListener('click', function () {
    rows.forEach(function (r, i) {
      r.querySelectorAll('input').forEach(function (x, j) {
        x.value = [[45, 62, 80, -15][i], 0, 0, 75][j];
      });
    });
    mode.selectedIndex = 0; pen.selectedIndex = 0; target.selectedIndex = 0;
    calc();
  });
  calc();
})();
"""


def resistance_page(lang):
    c = POE[lang]["resistance"]
    js = RES_JS.replace("__STR__", json.dumps(c["js"], ensure_ascii=False))
    return tool_page(lang, "resistance", resistance_body(lang), js)


def checklist_body(lang):
    c = POE[lang]["checklist"]
    return (
        hero(lang, c)
        + '<div class="note-box amber"><p>%s</p></div>' % c["note"]
        + '<div class="stats">'
        + '<div class="stat"><em>%s</em><strong id="count"></strong></div>' % c["claimed_label"]
        + '<div class="stat"><em>%s</em><strong id="points"></strong></div>' % c["points_label"]
        + '<div class="stat"><em>%s</em><strong id="spirit"></strong></div></div>' % c["spirit_label"]
        + '<div class="wlh-progress"><span id="progress" style="width:0%"></span></div>'
        + '<section class="panel"><div class="poe-grid4">'
        + '<div class="field"><label for="act">%s</label><div class="select-wrap">'
          '<select id="act"><option>%s</option></select></div></div>' % (c["chapter_label"], c["all"])
        + '<div class="field"><label for="search">%s</label>'
          '<input id="search" type="text" placeholder="%s"></div>' % (c["search_label"], c["search_ph"])
        + '<div class="field"><label for="filter">%s</label><div class="select-wrap">'
          '<select id="filter"><option>%s</option><option>%s</option><option>%s</option></select></div></div>'
          % (c["status_label"], c["all"], c["missing"], c["claimed"])
        + '<div class="field"><label for="profile">%s</label>'
          '<input id="profile" type="text" value="Default" maxlength="40"></div></div>' % c["profile_label"]
        + '<p style="margin-top:16px">'
        + '<button class="btn btn-secondary" id="exportBtn" type="button">%s</button> ' % c["export"]
        + '<button class="btn btn-secondary" id="reset" type="button">%s</button></p>' % c["reset"]
        + '<small id="saveState"></small></section>'
        + '<section class="panel" id="list"></section>'
        + '<section class="panel"><h2 id="guide">%s</h2><p>%s</p>' % (c["guide_h"], c["guide_p"])
        + '<p><a href="%s" target="_blank" rel="noopener noreferrer">%s</a> \u00b7 '
          '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a> \u00b7 '
          '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a></p></section>'
        % (GAMERS_WIKI_URL, c["src1"], POEGG_URL, c["src2"], EXILEDB_URL, c["src3"])
    )


CHECK_JS = """
(function () {
  var STR = __STR__;
  var data = __DATA__;
  var state = {};
  function el(id) { return document.getElementById(id); }
  try { state = JSON.parse(localStorage.getItem('bf-poe2-checklist-v1') || '{}') || {}; } catch (e) {}
  function key() { return 'character:' + el('profile').value.trim().toLowerCase(); }
  function done() { return state[key()] || []; }
  function save() {
    try {
      localStorage.setItem('bf-poe2-checklist-v1', JSON.stringify(state));
      el('saveState').textContent = STR.saved;
    } catch (e) {
      el('saveState').textContent = STR.no_storage;
    }
  }
  var totalPoints = data.reduce(function (s, x) { return s + x[4]; }, 0);
  var totalSpirit = data.reduce(function (s, x) { return s + x[5]; }, 0);
  var acts = [];
  data.forEach(function (x) { if (acts.indexOf(x[0]) === -1) acts.push(x[0]); });
  acts.forEach(function (a) { el('act').add(new Option(a, a)); });
  function render() {
    var ids = done();
    el('count').textContent = ids.length + ' / ' + data.length;
    el('points').textContent = ids.reduce(function (s, i) { return s + ((data[i] || [])[4] || 0); }, 0) + ' / ' + totalPoints;
    el('spirit').textContent = ids.reduce(function (s, i) { return s + ((data[i] || [])[5] || 0); }, 0) + ' / ' + totalSpirit;
    el('progress').style.width = ids.length / data.length * 100 + '%';
    var q = el('search').value.toLowerCase();
    var html = data.map(function (x, i) { return {x: x, i: i}; }).filter(function (o) {
      return (el('act').value === STR.all || o.x[0] === el('act').value)
        && o.x.join(' ').toLowerCase().indexOf(q) !== -1
        && (el('filter').value === STR.all || (el('filter').value === STR.claimed) === (ids.indexOf(o.i) !== -1));
    }).map(function (o) {
      var x = o.x, i = o.i, checked = ids.indexOf(i) !== -1;
      return '<div class="poe-reward' + (checked ? ' done' : '') + '"><input type="checkbox" id="r' + i + '" data-id="' + i + '"' + (checked ? ' checked' : '') + '><label for="r' + i + '"><strong>' + x[1] + '</strong> \\u2014 ' + x[3] + '<br><small>' + x[0] + ' \\u00b7 ' + x[2] + '</small></label></div>';
    }).join('') || '<p>' + STR.no_match + '</p>';
    el('list').innerHTML = html;
    el('list').querySelectorAll('input').forEach(function (x) {
      x.addEventListener('change', function () {
        var i = +x.getAttribute('data-id');
        var cur = done();
        state[key()] = x.checked ? Array.from(new Set(cur.concat([i]))) : cur.filter(function (v) { return v !== i; });
        save();
        render();
      });
    });
  }
  ['act', 'search', 'filter', 'profile'].forEach(function (id) { el(id).addEventListener('input', render); });
  el('reset').addEventListener('click', function () {
    if (confirm(STR.reset_confirm)) { state[key()] = []; save(); render(); }
  });
  el('exportBtn').addEventListener('click', function () {
    var a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([JSON.stringify({version: '0.5.5', profile: el('profile').value, claimed: done().map(function (i) { return data[i]; })}, null, 2)], {type: 'application/json'}));
    a.download = 'poe2-progress.json';
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
  });
  render();
})();
"""


def checklist_page(lang):
    c = POE[lang]["checklist"]
    data = CHECKLIST_EN if lang == "en" else CHECKLIST_RU
    str_obj = dict(c["js"])
    str_obj.update({"all": c["all"], "claimed": c["claimed"],
                    "saved": c["saved"], "no_storage": c["no_storage"],
                    "reset_confirm": c["reset_confirm"],
                    "no_match": c["no_match"]})
    js = CHECK_JS.replace("__STR__", json.dumps(str_obj, ensure_ascii=False))
    js = js.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    return tool_page(lang, "checklist", checklist_body(lang), js)


def main():
    write("path-of-exile-2/launch-countdown/index.html", countdown_page("en"))
    write("ru/path-of-exile-2/launch-countdown/index.html", countdown_page("ru"))
    write("path-of-exile-2/class-selector/index.html", class_page("en"))
    write("ru/path-of-exile-2/class-selector/index.html", class_page("ru"))
    write("path-of-exile-2/resistance-calculator/index.html", resistance_page("en"))
    write("ru/path-of-exile-2/resistance-calculator/index.html", resistance_page("ru"))
    write("path-of-exile-2/campaign-checklist/index.html", checklist_page("en"))
    write("ru/path-of-exile-2/campaign-checklist/index.html", checklist_page("ru"))
    print("poe2 tools done")


if __name__ == "__main__":
    main()
