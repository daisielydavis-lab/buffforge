#!/usr/bin/env python3
"""Build the DPS wiki search pages (EN + RU) from data/dps-wiki-v1.json.

The data is the GPT-supplied dump, verified against dpsquad.wiki
(characters / skills / pets / stages / equipment / faq / updates) and
SteamDB (app 5135440) on 2026-11-15: 403 entries, 0 value corrections
needed. Two verified additions live in the stored data: the boss-stage
mechanic now notes that a boss stage needs a map (ninth stage, first
clear), and the page FAQ notes the tenth pet, Worn Compass, which v1.0.3
hides until its pack is out.

Layout and interaction follow the GPT single-page search (search box with
multi-word AND matching, category tabs, hero / difficulty filters, first
35 results + Show more, click-to-detail panel, #entry-id deep links,
Copy entry link, View-skills button, stats row, FAQ, sources footer),
re-skinned into the Daylight Forge shell via scripts/shell.py. Entry
names stay in English in both languages (in-game terms); only the UI
strings, field labels and FAQ are translated for RU.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import BASE, breadcrumb_jsonld, crumbs_html, page  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, "data", "dps-wiki-v1.json"), encoding="utf-8") as f:
    WIKI = json.load(f)

DATA = WIKI["data"]
REF_VERSION = WIKI["referenceVersion"]  # v1.0.3
CHECKED_ON = WIKI["checkedOn"]  # 2026-11-15

WIKI_BASE = "https://dpsquad.wiki"
STEAM_SEARCH = ("https://store.steampowered.com/search/?term="
                "Desktop%20Pension%20Squad")

EN = {
    "title": "Desktop Pension Squad Wiki - Characters, Skills, Gear & Stages | BuffForge",
    "desc": ("Search the DPS: Desktop Pension Squad Wiki database on one page. "
             "Find characters, skills, equipment, pets, stage structure, and "
             "verified game mechanics."),
    "crumb": "DPS Wiki Search",
    "kicker": "Desktop idle RPG · searchable reference",
    "h1": "DPS: Desktop Pension Squad Wiki",
    "lede": ("Find heroes, active skill triggers, 180 equipment tiers, all stage IDs, "
             "pet bonuses and game rules. Browse results and read details instantly "
             "on this page."),
    "searchLabel": "Search Wiki entries",
    "searchPlaceholder": "Search Minos, Flame Eater, Spookie, Torment 4-10...",
    "clear": "Clear",
    "heroLabel": "Hero filter",
    "heroAll": "All heroes",
    "difficultyLabel": "Stage difficulty filter",
    "difficultyAll": "All difficulties",
    "tabLabel": {"All": "All data", "Character": "Characters", "Skill": "Skills",
                 "Equipment": "Equipment", "Pet": "Pets", "Stage": "Stages",
                 "Mechanic": "Game rules"},
    "typeLabel": {"Character": "Character", "Skill": "Skill",
                  "Equipment": "Equipment", "Pet": "Pet", "Stage": "Stage",
                  "Mechanic": "Game rule"},
    "groupLabel": {"Combat": "Combat", "Squad": "Squad", "Equipment": "Equipment",
                   "Workshop": "Workshop", "Pets": "Pets", "Drops": "Drops",
                   "Stages": "Stages", "Progression": "Progression"},
    "statusLabel": {},
    "statLabels": ["heroes", "active skills", "pets", "stage IDs",
                   "equipment tiers", "game-rule entries"],
    "resultsTitle": "Wiki results",
    "resultsLabel": "Wiki search results",
    "count": "{n} matching entries",
    "showMore": "Show more ({n} remaining)",
    "emptyResults": ("No matching entry in this verified dataset. Try another category "
                     "or a broader term. Missing results do not mean the item does not "
                     "exist in-game."),
    "detailEmptyTitle": "Search the database",
    "detailEmptyBody": ("Choose a verified entry to inspect it here. No pages to navigate "
                        "and no AI-generated game stats."),
    "dataStatus": "Data status:",
    "noticeBody": ("Source references are third-party reports of game-build data, not a "
                   "new independent game-file extraction. Details absent from the dataset "
                   "are never estimated."),
    "reviewSource": "Review source \u2197",
    "copyLink": "Copy entry link",
    "copied": "Copied",
    "viewSkills": "View {name} skills",
    "bossStage": "Boss stage",
    "regularStage": "Regular stage",
    "chapterWord": "Chapter",
    "notVerified": "Not verified in this release",
    "notVerifiedIndividually": "Not verified individually",
    "yes": "Yes",
    "no": "No",
    "f": {
        "mainWeapon": "Main weapon", "offhand": "Off-hand",
        "activeSkills": "Active skills", "passiveSkills": "Passive skills",
        "availability": "Availability", "dlc": "Character DLC",
        "baseRoster": "Base roster", "hero": "Hero", "type": "Type",
        "activeType": "Active", "trigger": "Activation / cooldown",
        "skillDamage": "Skill damage / level scaling", "slot": "Slot",
        "tier": "Tier", "reqLevel": "Required level",
        "rarities": "Available rarities", "gradeCount": "Number of grades",
        "exactStats": "Exact stats", "bonus": "Bonus", "unlock": "Unlock",
        "bonusUnequipped": "Bonus active while unequipped",
        "difficulty": "Difficulty", "chapter": "Chapter", "stage": "Stage",
        "boss": "Boss", "dropsMonsters": "Drops / monsters", "topic": "Topic",
    },
    "copyKicker": "What is in here",
    "copyH2": "What can you search in this wiki?",
    "notOnSale": "not on sale",
    "notObtainable": "Hidden. Not obtainable.",
    "copyP": ("This search covers five heroes in the files. Geumeum is not on sale. "
              "Chopper is the Character Pack DLC. Also here: 40 active skill names, "
              "nine obtainable pets, 160 stage identifiers, 180 equipment tiers and "
              "the rules we have checked. Worn Compass stays hidden. Character pages "
              "and player-save access are not required."),
    "faqKicker": "Questions",
    "faqH2": "Frequently asked questions",
    "faq": [
        ("How do active skills work?",
         "Active skills activate automatically when their conditions are met. A hero "
         "can equip up to three. You can search by skill name, hero and trigger in "
         "the Skills category."),
        ("How many difficulties and stages are there?",
         "The game has Normal, Torment, Nightmare and Hell; each includes four "
         "chapters with ten stages, for 160 stage identifiers in total. The tenth "
         "stage of each chapter is a boss stage. Individual enemy and drop tables "
         "are not included without source-checked values."),
        ("Does the wiki include every equipment item and passive skill?",
         "No. All 180 equipment tier names and rarity ranges are indexed, but "
         "individual grade stats and the 65 passive skill details are not included. "
         "Rather than showing fabricated effects or drop probabilities, missing "
         "fields are clearly marked. This is a functioning search page but not a "
         "complete extracted game database."),
        ("Where does the game data come from?",
         "The rows were taken from public reports of v1.0.3 (Steam build 26637932) "
         "on 15 Nov 2026. They were not extracted again from the current client. "
         "On 22 Nov 2026 DPSquad Wiki’s current data was v1.0.6, build 26804378. "
         "That page says stages, gear, boxes and the Workshop are unchanged, and "
         "that encrypted code still uses the v1.0.3 rule read. A few wording notes "
         "on this page were re-read that day. The wiki is a fan site, not official."),
        ("Why are there only nine pets?",
         "Worn Compass is in the files and hidden until its pack is out. The v1.0.6 "
         "wiki page, checked 22 Nov 2026, still says nobody can unlock or equip it, "
         "so it is not one of the nine obtainable pets. Search still finds it, marked "
         "not obtainable."),
    ],
    "dataLine": ("Extracted 15 Nov 2026 \u00b7 dataset v1.0.3 (build 26637932). "
                 "Checked 22 Nov 2026 against dpsquad.wiki v1.0.6 (build 26804378): "
                 "workshop, stages, gear and boxes reported unchanged; encrypted rules "
                 "still from v1.0.3. Not a new extract. Fan wiki, not official."),
    "sourcesLabel": "Sources:",
    "sources": [
        ("Steam", STEAM_SEARCH),
        ("Character reference", WIKI_BASE + "/characters"),
        ("Skills reference", WIKI_BASE + "/skills"),
        ("Pets reference", WIKI_BASE + "/pets"),
        ("Stage reference", WIKI_BASE + "/stages"),
        ("Equipment reference", WIKI_BASE + "/equipment"),
        ("FAQ", WIKI_BASE + "/faq"),
        ("Game updates", WIKI_BASE + "/updates"),
    ],
}

RU = {
    "title": "Desktop Pension Squad Wiki \u2014 \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0438, \u043d\u0430\u0432\u044b\u043a\u0438, \u0441\u043d\u0430\u0440\u044f\u0436\u0435\u043d\u0438\u0435 \u0438 \u044d\u0442\u0430\u043f\u044b | BuffForge",
    "desc": ("\u041f\u043e\u0438\u0441\u043a \u043f\u043e \u0431\u0430\u0437\u0435 \u0432\u0438\u043a\u0438 DPS: Desktop Pension Squad "
             "\u043d\u0430 \u043e\u0434\u043d\u043e\u0439 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0435. \u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0438, "
             "\u043d\u0430\u0432\u044b\u043a\u0438, \u0441\u043d\u0430\u0440\u044f\u0436\u0435\u043d\u0438\u0435, \u043f\u0438\u0442\u043e\u043c\u0446\u044b, "
             "\u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0430 \u044d\u0442\u0430\u043f\u043e\u0432 \u0438 \u043f\u0440\u043e\u0432\u0435\u0440\u0435\u043d\u043d\u044b\u0435 \u043c\u0435\u0445\u0430\u043d\u0438\u043a\u0438 \u0438\u0433\u0440\u044b."),
    "crumb": "\u041f\u043e\u0438\u0441\u043a \u043f\u043e \u0432\u0438\u043a\u0438 DPS",
    "kicker": "Desktop idle RPG \u00b7 \u0441\u043f\u0440\u0430\u0432\u043a\u0430 \u0441 \u043f\u043e\u0438\u0441\u043a\u043e\u043c",
    "h1": "\u0412\u0438\u043a\u0438 Desktop Pension Squad",
    "lede": ("\u041d\u0430\u0439\u0434\u0438\u0442\u0435 \u0433\u0435\u0440\u043e\u0435\u0432, \u0442\u0440\u0438\u0433\u0433\u0435\u0440\u044b \u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0445 "
             "\u043d\u0430\u0432\u044b\u043a\u043e\u0432, 180 \u0442\u0438\u0440\u043e\u0432 \u0441\u043d\u0430\u0440\u044f\u0436\u0435\u043d\u0438\u044f, \u0432\u0441\u0435 "
             "\u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440\u044b \u044d\u0442\u0430\u043f\u043e\u0432, \u0431\u043e\u043d\u0443\u0441\u044b "
             "\u043f\u0438\u0442\u043e\u043c\u0446\u0435\u0432 \u0438 \u043f\u0440\u0430\u0432\u0438\u043b\u0430 \u0438\u0433\u0440\u044b. \u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b "
             "\u0438 \u043f\u043e\u0434\u0440\u043e\u0431\u043d\u043e\u0441\u0442\u0438 \u2014 \u0441\u0440\u0430\u0437\u0443 \u043d\u0430 \u044d\u0442\u043e\u0439 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0435."),
    "searchLabel": "\u041f\u043e\u0438\u0441\u043a \u043f\u043e \u0437\u0430\u043f\u0438\u0441\u044f\u043c \u0432\u0438\u043a\u0438",
    "searchPlaceholder": "\u041f\u043e\u0438\u0441\u043a: Minos, Flame Eater, Spookie, Torment 4-10\u2026",
    "clear": "\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c",
    "heroLabel": "\u0424\u0438\u043b\u044c\u0442\u0440 \u043f\u043e \u0433\u0435\u0440\u043e\u044e",
    "heroAll": "\u0412\u0441\u0435 \u0433\u0435\u0440\u043e\u0438",
    "difficultyLabel": "\u0424\u0438\u043b\u044c\u0442\u0440 \u043f\u043e \u0441\u043b\u043e\u0436\u043d\u043e\u0441\u0442\u0438",
    "difficultyAll": "\u0412\u0441\u0435 \u0441\u043b\u043e\u0436\u043d\u043e\u0441\u0442\u0438",
    "tabLabel": {"All": "\u0412\u0441\u0435 \u0437\u0430\u043f\u0438\u0441\u0438", "Character": "\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0438",
                 "Skill": "\u041d\u0430\u0432\u044b\u043a\u0438", "Equipment": "\u0421\u043d\u0430\u0440\u044f\u0436\u0435\u043d\u0438\u0435",
                 "Pet": "\u041f\u0438\u0442\u043e\u043c\u0446\u044b", "Stage": "\u042d\u0442\u0430\u043f\u044b",
                 "Mechanic": "\u041f\u0440\u0430\u0432\u0438\u043b\u0430 \u0438\u0433\u0440\u044b"},
    "typeLabel": {"Character": "\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436", "Skill": "\u041d\u0430\u0432\u044b\u043a",
                  "Equipment": "\u0421\u043d\u0430\u0440\u044f\u0436\u0435\u043d\u0438\u0435", "Pet": "\u041f\u0438\u0442\u043e\u043c\u0435\u0446",
                  "Stage": "\u042d\u0442\u0430\u043f", "Mechanic": "\u041f\u0440\u0430\u0432\u0438\u043b\u043e"},
    "groupLabel": {"Combat": "\u0411\u043e\u0439", "Squad": "\u041e\u0442\u0440\u044f\u0434",
                   "Equipment": "\u0421\u043d\u0430\u0440\u044f\u0436\u0435\u043d\u0438\u0435", "Workshop": "\u041c\u0430\u0441\u0442\u0435\u0440\u0441\u043a\u0430\u044f",
                   "Pets": "\u041f\u0438\u0442\u043e\u043c\u0446\u044b", "Drops": "\u0414\u0440\u043e\u043f",
                   "Stages": "\u042d\u0442\u0430\u043f\u044b", "Progression": "\u041f\u0440\u043e\u0433\u0440\u0435\u0441\u0441"},
    "statusLabel": {
        "Community-reference checked": "\u041f\u0440\u043e\u0432\u0435\u0440\u0435\u043d\u043e \u043f\u043e \u0441\u043f\u0440\u0430\u0432\u043a\u0435 \u0441\u043e\u043e\u0431\u0449\u0435\u0441\u0442\u0432\u0430",
        "Stage structure verified; individual rewards not reviewed": "\u0421\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0430 \u044d\u0442\u0430\u043f\u043e\u0432 \u043f\u0440\u043e\u0432\u0435\u0440\u0435\u043d\u0430; \u043d\u0430\u0433\u0440\u0430\u0434\u044b \u043f\u043e \u043e\u0442\u0434\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u0438 \u043d\u0435 \u043f\u0440\u043e\u0432\u0435\u0440\u044f\u043b\u0438\u0441\u044c",
        "Wording checked on dpsquad.wiki 22 Nov 2026; not a new client extract": "\u0424\u043e\u0440\u043c\u0443\u043b\u0438\u0440\u043e\u0432\u043a\u0430 \u0441\u0432\u0435\u0440\u0435\u043d\u0430 \u0441 dpsquad.wiki 22 \u043d\u043e\u044f\u0431\u0440\u044f 2026; \u044d\u0442\u043e \u043d\u0435 \u043d\u043e\u0432\u0430\u044f \u0432\u044b\u0433\u0440\u0443\u0437\u043a\u0430 \u043a\u043b\u0438\u0435\u043d\u0442\u0430",
        "Structure from the v1.0.3 extract. Difficulty note checked on dpsquad.wiki 22 Nov 2026; HP not re-extracted.": "\u0421\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0430 \u0438\u0437 \u0432\u044b\u0433\u0440\u0443\u0437\u043a\u0438 v1.0.3. \u0417\u0430\u043c\u0435\u0442\u043a\u0430 \u043e \u0441\u043b\u043e\u0436\u043d\u043e\u0441\u0442\u0438 \u0441\u0432\u0435\u0440\u0435\u043d\u0430 \u0441 dpsquad.wiki 22 \u043d\u043e\u044f\u0431\u0440\u044f 2026; HP \u0437\u0430\u043d\u043e\u0432\u043e \u043d\u0435 \u0441\u043d\u0438\u043c\u0430\u043b\u0438.",
        "Hidden, not obtainable": "\u0421\u043a\u0440\u044b\u0442, \u043f\u043e\u043b\u0443\u0447\u0438\u0442\u044c \u043d\u0435\u043b\u044c\u0437\u044f",
        "Equipment tier catalog cross-checked; exact grade stats not independently verified": "\u041a\u0430\u0442\u0430\u043b\u043e\u0433 \u0442\u0438\u0440\u043e\u0432 \u0441\u0432\u0435\u0440\u0435\u043d; \u0442\u043e\u0447\u043d\u044b\u0435 \u0445\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438 \u0433\u0440\u0435\u0439\u0434\u043e\u0432 \u043d\u0435\u0437\u0430\u0432\u0438\u0441\u0438\u043c\u043e \u043d\u0435 \u043f\u0440\u043e\u0432\u0435\u0440\u0435\u043d\u044b",
    },
    "statLabels": ["\u0433\u0435\u0440\u043e\u0435\u0432", "\u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0445 \u043d\u0430\u0432\u044b\u043a\u043e\u0432",
                   "\u043f\u0438\u0442\u043e\u043c\u0446\u0435\u0432", "\u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440\u043e\u0432 \u044d\u0442\u0430\u043f\u043e\u0432",
                   "\u0442\u0438\u0440\u043e\u0432 \u0441\u043d\u0430\u0440\u044f\u0436\u0435\u043d\u0438\u044f", "\u0437\u0430\u043f\u0438\u0441\u0435\u0439 \u043e \u043f\u0440\u0430\u0432\u0438\u043b\u0430\u0445"],
    "resultsTitle": "\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u0432\u0438\u043a\u0438",
    "resultsLabel": "\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u043f\u043e\u0438\u0441\u043a\u0430 \u043f\u043e \u0432\u0438\u043a\u0438",
    "count": "\u041d\u0430\u0439\u0434\u0435\u043d\u043e \u0437\u0430\u043f\u0438\u0441\u0435\u0439: {n}",
    "showMore": "\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u0435\u0449\u0451 (\u043e\u0441\u0442\u0430\u043b\u043e\u0441\u044c: {n})",
    "emptyResults": ("\u0412 \u043f\u0440\u043e\u0432\u0435\u0440\u0435\u043d\u043d\u043e\u0439 \u0431\u0430\u0437\u0435 \u043d\u0438\u0447\u0435\u0433\u043e \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u043e. "
                     "\u041f\u043e\u043f\u0440\u043e\u0431\u0443\u0439\u0442\u0435 \u0434\u0440\u0443\u0433\u0443\u044e \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044e \u0438\u043b\u0438 \u0431\u043e\u043b\u0435\u0435 "
                     "\u043e\u0431\u0449\u0438\u0439 \u0437\u0430\u043f\u0440\u043e\u0441. \u041e\u0442\u0441\u0443\u0442\u0441\u0442\u0432\u0438\u0435 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0430 "
                     "\u043d\u0435 \u0437\u043d\u0430\u0447\u0438\u0442, \u0447\u0442\u043e \u043f\u0440\u0435\u0434\u043c\u0435\u0442\u0430 \u043d\u0435\u0442 \u0432 \u0438\u0433\u0440\u0435."),
    "detailEmptyTitle": "\u0418\u0449\u0438\u0442\u0435 \u043f\u043e \u0431\u0430\u0437\u0435",
    "detailEmptyBody": ("\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043f\u0440\u043e\u0432\u0435\u0440\u0435\u043d\u043d\u0443\u044e \u0437\u0430\u043f\u0438\u0441\u044c \u2014 "
                        "\u0435\u0451 \u0434\u0430\u043d\u043d\u044b\u0435 \u043f\u043e\u044f\u0432\u044f\u0442\u0441\u044f \u0437\u0434\u0435\u0441\u044c. \u041f\u0435\u0440\u0435\u0445\u043e\u0434\u0438\u0442\u044c "
                        "\u043f\u043e \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430\u043c \u043d\u0435 \u043d\u0443\u0436\u043d\u043e, \u0432\u044b\u0434\u0443\u043c\u0430\u043d\u043d\u044b\u0445 \u0446\u0438\u0444\u0440 \u043d\u0435\u0442."),
    "dataStatus": "\u0421\u0442\u0430\u0442\u0443\u0441 \u0434\u0430\u043d\u043d\u044b\u0445:",
    "noticeBody": ("\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0438 \u2014 \u0441\u0442\u043e\u0440\u043e\u043d\u043d\u0438\u0435 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438 "
                   "\u0434\u0430\u043d\u043d\u044b\u0445 \u0441\u0431\u043e\u0440\u043a\u0438 \u0438\u0433\u0440\u044b, \u0430 \u043d\u0435 \u043d\u043e\u0432\u0430\u044f \u043d\u0435\u0437\u0430\u0432\u0438\u0441\u0438\u043c\u0430\u044f "
                   "\u0432\u044b\u0433\u0440\u0443\u0437\u043a\u0430 \u0444\u0430\u0439\u043b\u043e\u0432. \u041d\u0435\u0434\u043e\u0441\u0442\u0430\u044e\u0449\u0438\u0435 \u0434\u0430\u043d\u043d\u044b\u0435 "
                   "\u043d\u0435 \u043e\u0446\u0435\u043d\u0438\u0432\u0430\u044e\u0442\u0441\u044f \u0438 \u043d\u0435 \u0434\u043e\u043c\u044b\u0441\u043b\u0438\u0432\u0430\u044e\u0442\u0441\u044f."),
    "reviewSource": "\u041f\u0440\u043e\u0432\u0435\u0440\u0438\u0442\u044c \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a \u2197",
    "copyLink": "\u0421\u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0441\u0441\u044b\u043b\u043a\u0443 \u043d\u0430 \u0437\u0430\u043f\u0438\u0441\u044c",
    "copied": "\u0421\u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u043d\u043e",
    "viewSkills": "\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u043d\u0430\u0432\u044b\u043a\u0438: {name}",
    "bossStage": "\u042d\u0442\u0430\u043f \u0441 \u0431\u043e\u0441\u0441\u043e\u043c",
    "regularStage": "\u041e\u0431\u044b\u0447\u043d\u044b\u0439 \u044d\u0442\u0430\u043f",
    "chapterWord": "\u0413\u043b\u0430\u0432\u0430",
    "notVerified": "\u0412 \u044d\u0442\u043e\u043c \u0432\u044b\u043f\u0443\u0441\u043a\u0435 \u043d\u0435 \u043f\u0440\u043e\u0432\u0435\u0440\u0435\u043d\u043e",
    "notVerifiedIndividually": "\u041f\u043e \u043e\u0442\u0434\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u0438 \u043d\u0435 \u043f\u0440\u043e\u0432\u0435\u0440\u0435\u043d\u043e",
    "yes": "\u0414\u0430",
    "no": "\u041d\u0435\u0442",
    "f": {
        "mainWeapon": "\u041e\u0441\u043d\u043e\u0432\u043d\u043e\u0435 \u043e\u0440\u0443\u0436\u0438\u0435", "offhand": "\u0412\u0442\u043e\u0440\u043e\u0435 \u043e\u0440\u0443\u0436\u0438\u0435",
        "activeSkills": "\u0410\u043a\u0442\u0438\u0432\u043d\u044b\u0445 \u043d\u0430\u0432\u044b\u043a\u043e\u0432", "passiveSkills": "\u041f\u0430\u0441\u0441\u0438\u0432\u043d\u044b\u0445 \u043d\u0430\u0432\u044b\u043a\u043e\u0432",
        "availability": "\u0414\u043e\u0441\u0442\u0443\u043f\u043d\u043e\u0441\u0442\u044c", "dlc": "DLC \u0441 \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0435\u043c",
        "baseRoster": "\u0411\u0430\u0437\u043e\u0432\u044b\u0439 \u0441\u043e\u0441\u0442\u0430\u0432", "hero": "\u0413\u0435\u0440\u043e\u0439", "type": "\u0422\u0438\u043f",
        "activeType": "\u0410\u043a\u0442\u0438\u0432\u043d\u044b\u0439", "trigger": "\u0421\u0440\u0430\u0431\u0430\u0442\u044b\u0432\u0430\u043d\u0438\u0435 / \u043f\u0435\u0440\u0435\u0437\u0430\u0440\u044f\u0434\u043a\u0430",
        "skillDamage": "\u0423\u0440\u043e\u043d \u043d\u0430\u0432\u044b\u043a\u0430 / \u0440\u043e\u0441\u0442 \u043f\u043e \u0443\u0440\u043e\u0432\u043d\u044f\u043c", "slot": "\u0421\u043b\u043e\u0442",
        "tier": "\u0422\u0438\u0440", "reqLevel": "\u0422\u0440\u0435\u0431\u0443\u0435\u043c\u044b\u0439 \u0443\u0440\u043e\u0432\u0435\u043d\u044c",
        "rarities": "\u0414\u043e\u0441\u0442\u0443\u043f\u043d\u044b\u0435 \u0440\u0435\u0434\u043a\u043e\u0441\u0442\u0438", "gradeCount": "\u0427\u0438\u0441\u043b\u043e \u0433\u0440\u0435\u0439\u0434\u043e\u0432",
        "exactStats": "\u0422\u043e\u0447\u043d\u044b\u0435 \u0445\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438", "bonus": "\u0411\u043e\u043d\u0443\u0441", "unlock": "\u041a\u0430\u043a \u043f\u043e\u043b\u0443\u0447\u0438\u0442\u044c",
        "bonusUnequipped": "\u0411\u043e\u043d\u0443\u0441 \u0434\u0435\u0439\u0441\u0442\u0432\u0443\u0435\u0442 \u0431\u0435\u0437 \u044d\u043a\u0438\u043f\u0438\u0440\u043e\u0432\u043a\u0438",
        "difficulty": "\u0421\u043b\u043e\u0436\u043d\u043e\u0441\u0442\u044c", "chapter": "\u0413\u043b\u0430\u0432\u0430", "stage": "\u042d\u0442\u0430\u043f",
        "boss": "\u0411\u043e\u0441\u0441", "dropsMonsters": "\u0414\u0440\u043e\u043f / \u043c\u043e\u043d\u0441\u0442\u0440\u044b", "topic": "\u0422\u0435\u043c\u0430",
    },
    "mechanicDesc": {
        "mechanic-1": "\u041a\u0430\u0436\u0434\u044b\u0439 \u0433\u0435\u0440\u043e\u0439 \u043c\u043e\u0436\u0435\u0442 \u044d\u043a\u0438\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0434\u043e \u0442\u0440\u0451\u0445 \u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0445 \u043d\u0430\u0432\u044b\u043a\u043e\u0432. \u0418\u0445 \u0443\u0441\u043b\u043e\u0432\u0438\u044f \u0441\u0440\u0430\u0431\u0430\u0442\u044b\u0432\u0430\u044e\u0442 \u0438\u0445 \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438.",
        "mechanic-2": "\u0412 \u043e\u0442\u0440\u044f\u0434\u0435 \u043c\u043e\u0436\u0435\u0442 \u0431\u044b\u0442\u044c \u0434\u043e \u0442\u0440\u0451\u0445 \u0433\u0435\u0440\u043e\u0435\u0432; Formation Engravings \u043e\u0442\u043a\u0440\u044b\u0432\u0430\u044e\u0442 \u0434\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u0441\u043b\u043e\u0442\u044b.",
        "mechanic-3": "Common \u2192 Uncommon \u2192 Rare \u2192 Unique \u2192 Epic \u2192 Legendary \u2192 Immortal \u2192 Ascendant \u2192 Primordial \u2192 Mythic.",
        "mechanic-4": "\u041c\u0430\u0441\u0442\u0435\u0440\u0441\u043a\u0430\u044f \u0440\u0430\u0441\u0445\u043e\u0434\u0443\u0435\u0442 9 \u043f\u0440\u0435\u0434\u043c\u0435\u0442\u043e\u0432 \u0441\u043d\u0430\u0440\u044f\u0436\u0435\u043d\u0438\u044f \u0438 \u0432\u044b\u0434\u0430\u0451\u0442 \u043e\u0434\u0438\u043d \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442; \u0448\u0430\u043d\u0441\u044b \u0437\u0430\u0432\u0438\u0441\u044f\u0442 \u043e\u0442 \u0440\u0435\u0446\u0435\u043f\u0442\u0430.",
        "mechanic-5": "\u0421\u043d\u0430\u0440\u044f\u0436\u0435\u043d\u0438\u0435 Legendary \u0438 \u0432\u044b\u0448\u0435 \u043c\u043e\u0436\u0435\u0442 \u043f\u0435\u0440\u0435\u043d\u043e\u0441\u0438\u0442\u044c\u0441\u044f \u0432 \u0438\u043d\u0432\u0435\u043d\u0442\u0430\u0440\u044c Steam \u0438 \u043f\u0440\u043e\u0434\u0430\u0432\u0430\u0442\u044c\u0441\u044f \u043d\u0430 \u0442\u043e\u0440\u0433\u043e\u0432\u043e\u0439 \u043f\u043b\u043e\u0449\u0430\u0434\u043a\u0435 \u2014 \u0441 \u0443\u0447\u0451\u0442\u043e\u043c \u0442\u0435\u043a\u0443\u0449\u0438\u0445 \u043e\u0433\u0440\u0430\u043d\u0438\u0447\u0435\u043d\u0438\u0439 \u0438\u0433\u0440\u044b \u0438 Steam.",
        "mechanic-6": "\u041f\u0438\u0442\u043e\u043c\u0446\u044b \u0434\u0430\u044e\u0442 \u0431\u043e\u043d\u0443\u0441\u044b \u0432\u0441\u0435\u0439 \u0433\u0440\u0443\u043f\u043f\u0435, \u0434\u0430\u0436\u0435 \u0435\u0441\u043b\u0438 \u0441\u0435\u0439\u0447\u0430\u0441 \u043d\u0435 \u0441\u043b\u0435\u0434\u0443\u044e\u0442 \u0437\u0430 \u043e\u0442\u0440\u044f\u0434\u043e\u043c.",
        "mechanic-7": "\u0417\u0430 \u0443\u0431\u0438\u0439\u0441\u0442\u0432\u0430 \u043c\u043e\u0433\u0443\u0442 \u0432\u044b\u043f\u0430\u0434\u0430\u0442\u044c \u0441\u0443\u043d\u0434\u0443\u043a\u0438; \u043d\u0430 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u0432\u043b\u0438\u044f\u044e\u0442 \u044d\u0442\u0430\u043f, \u0442\u0438\u043f \u0432\u0440\u0430\u0433\u0430 \u0438 \u0431\u043e\u043d\u0443\u0441\u044b Engraving. \u0422\u043e\u0447\u043d\u044b\u0435 \u0448\u0430\u043d\u0441\u044b \u0441\u0432\u043e\u0438 \u0434\u043b\u044f \u043a\u0430\u0436\u0434\u043e\u0433\u043e \u044d\u0442\u0430\u043f\u0430.",
        "mechanic-8": "\u0414\u0435\u0441\u044f\u0442\u044b\u0439 \u044d\u0442\u0430\u043f \u043a\u0430\u0436\u0434\u043e\u0439 \u0433\u043b\u0430\u0432\u044b \u2014 \u044d\u0442\u0430\u043f \u0441 \u0431\u043e\u0441\u0441\u043e\u043c. \u0412\u0441\u0435\u0433\u043e \u0447\u0435\u0442\u044b\u0440\u0435 \u0441\u043b\u043e\u0436\u043d\u043e\u0441\u0442\u0438 \u0438 \u0447\u0435\u0442\u044b\u0440\u0435 \u0433\u043b\u0430\u0432\u044b \u043d\u0430 \u043a\u0430\u0436\u0434\u043e\u0439. \u0414\u043b\u044f \u044d\u0442\u0430\u043f\u0430 \u0441 \u0431\u043e\u0441\u0441\u043e\u043c \u043d\u0443\u0436\u043d\u0430 \u043a\u0430\u0440\u0442\u0430 \u2014 \u0435\u0451 \u0434\u0430\u0451\u0442 \u0434\u0435\u0432\u044f\u0442\u044b\u0439 \u044d\u0442\u0430\u043f \u043f\u0440\u0438 \u043f\u0435\u0440\u0432\u043e\u043c \u043f\u0440\u043e\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u0438.",
        "mechanic-9": "\u041e\u0444\u043b\u0430\u0439\u043d-\u043d\u0430\u0433\u0440\u0430\u0434\u044b \u0435\u0441\u0442\u044c, \u043d\u043e \u0442\u043e\u0447\u043d\u044b\u0435 \u0441\u0443\u043c\u043c\u044b \u0437\u0430\u0432\u0438\u0441\u044f\u0442 \u043e\u0442 \u0442\u0435\u043a\u0443\u0449\u0438\u0445 \u043f\u0440\u0430\u0432\u0438\u043b \u0438\u0433\u0440\u044b, \u044d\u0442\u0430\u043f\u0430 \u0438 \u0443\u043b\u0443\u0447\u0448\u0435\u043d\u0438\u0439; \u043d\u0435\u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0451\u043d\u043d\u044b\u0445 \u043e\u0446\u0435\u043d\u043e\u043a \u0437\u0434\u0435\u0441\u044c \u043d\u0435\u0442.",
    },
    "copyKicker": "\u0427\u0442\u043e \u0437\u0434\u0435\u0441\u044c \u0435\u0441\u0442\u044c",
    "copyH2": "\u0427\u0442\u043e \u043c\u043e\u0436\u043d\u043e \u043d\u0430\u0439\u0442\u0438 \u0432 \u044d\u0442\u043e\u0439 \u0432\u0438\u043a\u0438?",
    "notOnSale": "\u043d\u0435 \u0432 \u043f\u0440\u043e\u0434\u0430\u0436\u0435",
    "notObtainable": "\u0421\u043a\u0440\u044b\u0442. \u041f\u043e\u043b\u0443\u0447\u0438\u0442\u044c \u043d\u0435\u043b\u044c\u0437\u044f.",
    "copyP": ("\u041f\u043e\u0438\u0441\u043a \u043e\u0445\u0432\u0430\u0442\u044b\u0432\u0430\u0435\u0442 \u043f\u044f\u0442\u044c \u0433\u0435\u0440\u043e\u0435\u0432 \u0432 \u0444\u0430\u0439\u043b\u0430\u0445. "
              "Geumeum \u043d\u0435 \u0432 \u043f\u0440\u043e\u0434\u0430\u0436\u0435. Chopper \u2014 DLC Character Pack. "
              "\u0415\u0449\u0451 \u0437\u0434\u0435\u0441\u044c: 40 \u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0445 \u043d\u0430\u0432\u044b\u043a\u043e\u0432, \u0434\u0435\u0432\u044f\u0442\u044c \u0434\u043e\u0441\u0442\u0443\u043f\u043d\u044b\u0445 "
              "\u043f\u0438\u0442\u043e\u043c\u0446\u0435\u0432, 160 \u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440\u043e\u0432 \u044d\u0442\u0430\u043f\u043e\u0432, 180 \u0442\u0438\u0440\u043e\u0432 "
              "\u0441\u043d\u0430\u0440\u044f\u0436\u0435\u043d\u0438\u044f \u0438 \u043f\u0440\u043e\u0432\u0435\u0440\u0435\u043d\u043d\u044b\u0435 \u043f\u0440\u0430\u0432\u0438\u043b\u0430. Worn Compass \u0441\u043a\u0440\u044b\u0442. "
              "\u041e\u0442\u0434\u0435\u043b\u044c\u043d\u044b\u0435 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u044b \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0435\u0439 \u043d\u0435 \u043d\u0443\u0436\u043d\u044b."),
    "faqKicker": "\u0412\u043e\u043f\u0440\u043e\u0441\u044b",
    "faqH2": "\u0427\u0430\u0441\u0442\u044b\u0435 \u0432\u043e\u043f\u0440\u043e\u0441\u044b",
    "faq": [
        ("\u041a\u0430\u043a \u0440\u0430\u0431\u043e\u0442\u0430\u044e\u0442 \u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0435 \u043d\u0430\u0432\u044b\u043a\u0438?",
         "\u0410\u043a\u0442\u0438\u0432\u043d\u044b\u0435 \u043d\u0430\u0432\u044b\u043a\u0438 \u0441\u0440\u0430\u0431\u0430\u0442\u044b\u0432\u0430\u044e\u0442 \u0441\u0430\u043c\u0438, \u043a\u043e\u0433\u0434\u0430 "
         "\u0432\u044b\u043f\u043e\u043b\u043d\u044f\u0435\u0442\u0441\u044f \u0438\u0445 \u0443\u0441\u043b\u043e\u0432\u0438\u0435. \u0413\u0435\u0440\u043e\u0439 \u043c\u043e\u0436\u0435\u0442 \u044d\u043a\u0438\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c "
         "\u0434\u043e \u0442\u0440\u0451\u0445. \u0418\u0441\u043a\u0430\u0442\u044c \u043c\u043e\u0436\u043d\u043e \u043f\u043e \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u044e \u043d\u0430\u0432\u044b\u043a\u0430, "
         "\u0433\u0435\u0440\u043e\u044e \u0438 \u0442\u0440\u0438\u0433\u0433\u0435\u0440\u0443 \u0432 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438 \u00ab\u041d\u0430\u0432\u044b\u043a\u0438\u00bb."),
        ("\u0421\u043a\u043e\u043b\u044c\u043a\u043e \u0432 \u0438\u0433\u0440\u0435 \u0441\u043b\u043e\u0436\u043d\u043e\u0441\u0442\u0435\u0439 \u0438 \u044d\u0442\u0430\u043f\u043e\u0432?",
         "\u0427\u0435\u0442\u044b\u0440\u0435 \u0441\u043b\u043e\u0436\u043d\u043e\u0441\u0442\u0438: Normal, Torment, Nightmare \u0438 Hell. \u0412 \u043a\u0430\u0436\u0434\u043e\u0439 \u2014 "
         "\u0447\u0435\u0442\u044b\u0440\u0435 \u0433\u043b\u0430\u0432\u044b \u043f\u043e \u0434\u0435\u0441\u044f\u0442\u044c \u044d\u0442\u0430\u043f\u043e\u0432, \u0432\u0441\u0435\u0433\u043e 160 "
         "\u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440\u043e\u0432. \u0414\u0435\u0441\u044f\u0442\u044b\u0439 \u044d\u0442\u0430\u043f \u043a\u0430\u0436\u0434\u043e\u0439 \u0433\u043b\u0430\u0432\u044b \u2014 "
         "\u044d\u0442\u0430\u043f \u0441 \u0431\u043e\u0441\u0441\u043e\u043c. \u0422\u0430\u0431\u043b\u0438\u0446\u044b \u0432\u0440\u0430\u0433\u043e\u0432 \u0438 \u0434\u0440\u043e\u043f\u0430 \u043f\u043e "
         "\u043e\u0442\u0434\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u0438 \u043d\u0435 \u0432\u043a\u043b\u044e\u0447\u0435\u043d\u044b, \u043f\u043e\u043a\u0430 \u0438\u0445 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f "
         "\u043d\u0435 \u043f\u0440\u043e\u0432\u0435\u0440\u0435\u043d\u044b \u043f\u043e \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0430\u043c."),
        ("\u0412 \u0432\u0438\u043a\u0438 \u0435\u0441\u0442\u044c \u0432\u0441\u0435 \u043f\u0440\u0435\u0434\u043c\u0435\u0442\u044b \u0438 \u043f\u0430\u0441\u0441\u0438\u0432\u043d\u044b\u0435 \u043d\u0430\u0432\u044b\u043a\u0438?",
         "\u041d\u0435\u0442. \u0423\u043a\u0430\u0437\u0430\u043d\u044b \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u044f \u0432\u0441\u0435\u0445 180 \u0442\u0438\u0440\u043e\u0432 \u0441\u043d\u0430\u0440\u044f\u0436\u0435\u043d\u0438\u044f "
         "\u0438 \u0438\u0445 \u0434\u0438\u0430\u043f\u0430\u0437\u043e\u043d\u044b \u0440\u0435\u0434\u043a\u043e\u0441\u0442\u0435\u0439, \u0430 \u0432\u043e\u0442 \u0445\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438 "
         "\u043e\u0442\u0434\u0435\u043b\u044c\u043d\u044b\u0445 \u0433\u0440\u0435\u0439\u0434\u043e\u0432 \u0438 \u043f\u043e\u0434\u0440\u043e\u0431\u043d\u043e\u0441\u0442\u0438 65 \u043f\u0430\u0441\u0441\u0438\u0432\u043d\u044b\u0445 "
         "\u043d\u0430\u0432\u044b\u043a\u043e\u0432 \u043d\u0435 \u0432\u043a\u043b\u044e\u0447\u0435\u043d\u044b. \u0412\u043c\u0435\u0441\u0442\u043e \u0432\u044b\u0434\u0443\u043c\u0430\u043d\u043d\u044b\u0445 \u044d\u0444\u0444\u0435\u043a\u0442\u043e\u0432 "
         "\u0438 \u0448\u0430\u043d\u0441\u043e\u0432 \u0434\u0440\u043e\u043f\u0430 \u043d\u0435\u0434\u043e\u0441\u0442\u0430\u044e\u0449\u0438\u0435 \u043f\u043e\u043b\u044f \u0447\u0435\u0441\u0442\u043d\u043e "
         "\u043f\u043e\u043c\u0435\u0447\u0435\u043d\u044b. \u042d\u0442\u043e \u0440\u0430\u0431\u043e\u0447\u0430\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 \u043f\u043e\u0438\u0441\u043a\u0430, "
         "\u0430 \u043d\u0435 \u043f\u043e\u043b\u043d\u0430\u044f \u0432\u044b\u0433\u0440\u0443\u0437\u043a\u0430 \u0431\u0430\u0437\u044b \u0438\u0433\u0440\u044b."),
        ("\u041e\u0442\u043a\u0443\u0434\u0430 \u0434\u0430\u043d\u043d\u044b\u0435 \u043e\u0431 \u0438\u0433\u0440\u0435?",
         "\u0421\u0442\u0440\u043e\u043a\u0438 \u0432\u0437\u044f\u0442\u044b \u0438\u0437 \u043e\u0442\u043a\u0440\u044b\u0442\u044b\u0445 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0439 \u043e v1.0.3 "
         "(\u0441\u0431\u043e\u0440\u043a\u0430 Steam 26637932) 15 \u043d\u043e\u044f\u0431\u0440\u044f 2026 \u0433\u043e\u0434\u0430. \u0418\u0437 \u0442\u0435\u043a\u0443\u0449\u0435\u0433\u043e \u043a\u043b\u0438\u0435\u043d\u0442\u0430 "
         "\u0438\u0445 \u0437\u0430\u043d\u043e\u0432\u043e \u043d\u0435 \u0441\u043d\u0438\u043c\u0430\u043b\u0438. 22 \u043d\u043e\u044f\u0431\u0440\u044f 2026 \u0442\u0435\u043a\u0443\u0449\u0438\u0435 \u0434\u0430\u043d\u043d\u044b\u0435 "
         "DPSquad Wiki \u0431\u044b\u043b\u0438 v1.0.6, \u0441\u0431\u043e\u0440\u043a\u0430 26804378. \u0422\u0430\u043c \u043d\u0430\u043f\u0438\u0441\u0430\u043d\u043e, \u0447\u0442\u043e \u044d\u0442\u0430\u043f\u044b, "
         "\u0441\u043d\u0430\u0440\u044f\u0436\u0435\u043d\u0438\u0435, \u0441\u0443\u043d\u0434\u0443\u043a\u0438 \u0438 Workshop \u043d\u0435 \u043c\u0435\u043d\u044f\u043b\u0438\u0441\u044c, \u0430 \u0437\u0430\u0448\u0438\u0444\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439 "
         "\u043a\u043e\u0434 \u043f\u043e-\u043f\u0440\u0435\u0436\u043d\u0435\u043c\u0443 \u0438\u0437 \u0447\u0442\u0435\u043d\u0438\u044f v1.0.3. \u041d\u0435\u0441\u043a\u043e\u043b\u044c\u043a\u043e \u0444\u043e\u0440\u043c\u0443\u043b\u0438\u0440\u043e\u0432\u043e\u043a "
         "\u043d\u0430 \u044d\u0442\u043e\u0439 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0435 \u043f\u0435\u0440\u0435\u0447\u0438\u0442\u0430\u043d\u044b \u0432 \u0442\u043e\u0442 \u0434\u0435\u043d\u044c. \u0412\u0438\u043a\u0438 \u0444\u0430\u043d\u0430\u0442\u0441\u043a\u0430\u044f, \u043d\u0435 \u043e\u0444\u0438\u0446\u0438\u0430\u043b\u044c\u043d\u0430\u044f."),
        ("\u041f\u043e\u0447\u0435\u043c\u0443 \u043f\u0438\u0442\u043e\u043c\u0446\u0435\u0432 \u0442\u043e\u043b\u044c\u043a\u043e \u0434\u0435\u0432\u044f\u0442\u044c?",
         "Worn Compass \u0435\u0441\u0442\u044c \u0432 \u0444\u0430\u0439\u043b\u0430\u0445 \u0438 \u0441\u043a\u0440\u044b\u0442 \u0434\u043e \u0432\u044b\u0445\u043e\u0434\u0430 \u043d\u0430\u0431\u043e\u0440\u0430. "
         "\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430 \u0432\u0438\u043a\u0438 v1.0.6, \u043f\u0440\u043e\u0432\u0435\u0440\u0435\u043d\u043d\u0430\u044f 22 \u043d\u043e\u044f\u0431\u0440\u044f 2026, "
         "\u043f\u043e-\u043f\u0440\u0435\u0436\u043d\u0435\u043c\u0443 \u043f\u0438\u0448\u0435\u0442, \u0447\u0442\u043e \u043f\u043e\u043b\u0443\u0447\u0438\u0442\u044c \u0438 \u043d\u0430\u0434\u0435\u0442\u044c \u0435\u0433\u043e \u043d\u0435\u043b\u044c\u0437\u044f, "
         "\u043f\u043e\u044d\u0442\u043e\u043c\u0443 \u0441\u0440\u0435\u0434\u0438 \u0434\u0435\u0432\u044f\u0442\u0438 \u0434\u043e\u0441\u0442\u0443\u043f\u043d\u044b\u0445 \u043f\u0438\u0442\u043e\u043c\u0446\u0435\u0432 \u0435\u0433\u043e \u043d\u0435\u0442. "
         "\u041f\u043e\u0438\u0441\u043a \u0435\u0433\u043e \u043d\u0430\u0445\u043e\u0434\u0438\u0442 \u0438 \u043f\u043e\u043c\u0435\u0447\u0430\u0435\u0442 \u043a\u0430\u043a \u043d\u0435\u0434\u043e\u0441\u0442\u0443\u043f\u043d\u043e\u0433\u043e."),
    ],
    "dataLine": ("\u0412\u044b\u0433\u0440\u0443\u0437\u043a\u0430 15 \u043d\u043e\u044f\u0431\u0440\u044f 2026 \u00b7 \u043d\u0430\u0431\u043e\u0440 v1.0.3 (\u0441\u0431\u043e\u0440\u043a\u0430 26637932). "
                 "\u0421\u0432\u0435\u0440\u043a\u0430 22 \u043d\u043e\u044f\u0431\u0440\u044f 2026 \u0441 dpsquad.wiki v1.0.6 (\u0441\u0431\u043e\u0440\u043a\u0430 26804378): "
                 "workshop, \u044d\u0442\u0430\u043f\u044b, \u0441\u043d\u0430\u0440\u044f\u0436\u0435\u043d\u0438\u0435 \u0438 \u0441\u0443\u043d\u0434\u0443\u043a\u0438 \u0431\u0435\u0437 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0439; "
                 "\u0437\u0430\u0448\u0438\u0444\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0435 \u043f\u0440\u0430\u0432\u0438\u043b\u0430 \u0432\u0441\u0451 \u0435\u0449\u0451 \u0438\u0437 v1.0.3. \u042d\u0442\u043e \u043d\u0435 \u043d\u043e\u0432\u0430\u044f \u0432\u044b\u0433\u0440\u0443\u0437\u043a\u0430. "
                 "\u0424\u0430\u043d\u0430\u0442\u0441\u043a\u0430\u044f \u0432\u0438\u043a\u0438, \u043d\u0435 \u043e\u0444\u0438\u0446\u0438\u0430\u043b\u044c\u043d\u0430\u044f."),
    "sourcesLabel": "\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0438:",
    "sources": [
        ("Steam", STEAM_SEARCH),
        ("\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0438", WIKI_BASE + "/characters"),
        ("\u041d\u0430\u0432\u044b\u043a\u0438", WIKI_BASE + "/skills"),
        ("\u041f\u0438\u0442\u043e\u043c\u0446\u044b", WIKI_BASE + "/pets"),
        ("\u042d\u0442\u0430\u043f\u044b", WIKI_BASE + "/stages"),
        ("\u0421\u043d\u0430\u0440\u044f\u0436\u0435\u043d\u0438\u0435", WIKI_BASE + "/equipment"),
        ("FAQ", WIKI_BASE + "/faq"),
        ("\u041e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f", WIKI_BASE + "/updates"),
    ],
}

HEROES = ["Minos", "Diana", "Mori & Gula", "Chopper", "Geumeum"]
DIFFICULTIES = ["Normal", "Torment", "Nightmare", "Hell"]
TYPES = ["All", "Character", "Skill", "Equipment", "Pet", "Stage", "Mechanic"]

JS = r"""
(function () {
  var DATA = __DATA__;
  var STR = __STR__;
  var TYPES = ['All', 'Character', 'Skill', 'Equipment', 'Pet', 'Stage', 'Mechanic'];
  var q = document.getElementById('query'), tabs = document.getElementById('tabs'),
      hero = document.getElementById('heroFilter'), difficulty = document.getElementById('difficultyFilter'),
      results = document.getElementById('results'), detail = document.getElementById('detail'),
      more = document.getElementById('more'), count = document.getElementById('count');
  var type = 'All', selected = null, limit = 35, shown = [];
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]; }); }
  var icons = {Character: '\u265F', Skill: '\u2726', Equipment: '\u2692', Pet: '\u2667', Stage: '\u2691', Mechanic: '\u25CE'};
  function titleFor(x) {
    if (x.type === 'Skill') return x.hero + ' \u00b7 ' + x.trigger;
    if (x.type === 'Character') return x.weapon + ' \u00b7 ' + x.offhand + (x.sale === false ? ' \u00b7 ' + STR.notOnSale : (x.dlc ? ' \u00b7 DLC' : ''));
    if (x.type === 'Pet' && x.obtainable === false) return STR.notObtainable;
    if (x.type === 'Equipment') return x.slot + ' \u00b7 Tier ' + x.tier + ' \u00b7 Lv.' + x.level;
    if (x.type === 'Pet') return x.effect + ' ' + x.value;
    if (x.type === 'Stage') return (x.boss ? STR.bossStage : STR.regularStage) + ' \u00b7 ' + STR.chapterWord + ' ' + x.chapter;
    return STR.groupLabel[x.group] || x.group;
  }
  function fields(x) {
    var F = STR.f;
    if (x.type === 'Character') return [[F.mainWeapon, x.weapon], [F.offhand, x.offhand], [F.activeSkills, x.active], [F.passiveSkills, x.passive], [F.availability, x.availability || (x.dlc ? F.dlc : F.baseRoster)]];
    if (x.type === 'Skill') return [[F.hero, x.hero], [F.type, F.activeType], [F.trigger, x.trigger], [F.skillDamage, STR.notVerified]];
    if (x.type === 'Equipment') return [[F.hero, x.hero], [F.slot, x.slot], [F.tier, x.tier], [F.reqLevel, x.level], [F.rarities, x.rarities], [F.gradeCount, x.gradeCount], [F.exactStats, STR.notVerified]];
    if (x.type === 'Pet') return [[F.bonus, x.effect + ' ' + x.value], [F.unlock, x.unlock], [F.bonusUnequipped, STR.yes]];
    if (x.type === 'Stage') return [[F.difficulty, x.difficulty], [F.chapter, x.chapter], [F.stage, x.stage], [F.boss, x.boss ? STR.yes : STR.no], [F.dropsMonsters, STR.notVerifiedIndividually]];
    return [[F.topic, STR.groupLabel[x.group] || x.group]];
  }
  function slugHash(id) { try { history.replaceState(null, '', '#' + encodeURIComponent(id)); } catch (e) {} }
  function drawDetail(x) {
    if (!x) {
      detail.innerHTML = '<span class="wiki-pill">Wiki</span><h2>' + esc(STR.detailEmptyTitle) + '</h2><p>' + esc(STR.detailEmptyBody) + '</p>';
      return;
    }
    var desc = (x.type === 'Mechanic' && STR.mechanicDesc && STR.mechanicDesc[x.id]) ? STR.mechanicDesc[x.id] : (x.description || '');
    var status = (STR.statusLabel && STR.statusLabel[x.status]) ? STR.statusLabel[x.status] : x.status;
    detail.innerHTML = '<span class="wiki-pill">' + esc(STR.typeLabel[x.type]) + '</span><h2>' + esc(x.name) + '</h2>'
      + '<div class="wiki-sub">Desktop Pension Squad \u00b7 ' + esc(x.version) + '</div>'
      + (desc ? '<p>' + esc(desc) + '</p>' : '')
      + '<dl class="wiki-rows">' + fields(x).map(function (kv) { return '<div class="wiki-kv"><dt>' + esc(kv[0]) + '</dt><dd>' + esc(kv[1]) + '</dd></div>'; }).join('') + '</dl>'
      + '<div class="wiki-notice"><strong>' + esc(STR.dataStatus) + '</strong> ' + esc(status) + '. ' + esc(STR.noticeBody) + '</div>'
      + '<p class="wiki-sub"><a href="' + esc(x.source) + '" target="_blank" rel="noopener noreferrer">' + esc(STR.reviewSource) + '</a> \u00b7 <button type="button" class="btn btn-secondary" id="share">' + esc(STR.copyLink) + '</button></p>'
      + (x.type === 'Character' ? '<p><button class="btn btn-primary" id="related" type="button">' + esc(STR.viewSkills.replace('{name}', x.name)) + '</button></p>' : '');
    document.getElementById('share').addEventListener('click', function () {
      var link = location.href.split('#')[0] + '#' + encodeURIComponent(x.id);
      var done = function () { document.getElementById('share').textContent = STR.copied; };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(link).then(done, function () { fallbackCopy(link); done(); });
      } else { fallbackCopy(link); done(); }
      function fallbackCopy(text) {
        var el = document.createElement('textarea');
        el.value = text; document.body.appendChild(el); el.select();
        try { document.execCommand('copy'); } catch (e) {}
        el.remove();
      }
    });
    if (x.type === 'Character') document.getElementById('related').onclick = function () {
      q.value = x.name; type = 'Skill'; hero.value = x.name; limit = 35; selected = null; render();
      document.getElementById('results').scrollIntoView({behavior: 'smooth', block: 'start'});
    };
  }
  function matches(x, needle) {
    var s = [x.name, x.type, x.hero, x.weapon, x.offhand, x.trigger, x.slot, x.tier, x.level, x.rarities, x.effect, x.value, x.unlock, x.difficulty, x.chapter, x.stage, x.description, x.group, x.availability, x.status].filter(function (v) { return v !== undefined && v !== null; }).join(' ').toLowerCase();
    return needle.trim().toLowerCase().split(/\s+/).filter(Boolean).every(function (w) { return s.indexOf(w) !== -1; });
  }
  function syncFilters() {
    hero.hidden = !(type === 'All' || type === 'Skill' || type === 'Equipment');
    difficulty.hidden = !(type === 'All' || type === 'Stage');
    tabs.innerHTML = TYPES.map(function (t) { return '<button class="wiki-tab" type="button" data-type="' + t + '" role="tab" aria-selected="' + (type === t) + '">' + esc(STR.tabLabel[t]) + '</button>'; }).join('');
  }
  function render() {
    syncFilters();
    shown = DATA.filter(function (x) {
      return (type === 'All' || x.type === type) && matches(x, q.value)
        && (!hero.value || ((x.type === 'Skill' || x.type === 'Equipment') ? (x.hero === hero.value || x.hero === 'All heroes') : true))
        && (!difficulty.value || x.type !== 'Stage' || x.difficulty === difficulty.value);
    });
    count.textContent = STR.count.replace('{n}', String(shown.length));
    results.innerHTML = shown.slice(0, limit).map(function (x) {
      return '<button class="wiki-item" type="button" data-id="' + esc(x.id) + '" aria-current="' + (selected && selected.id === x.id) + '">'
        + '<span class="wiki-glyph">' + icons[x.type] + '</span>'
        + '<span style="min-width:0;overflow:hidden"><span class="wiki-itemtitle">' + esc(x.name) + '</span><span class="wiki-itemdesc">' + esc(titleFor(x)) + '</span></span>'
        + '<span class="wiki-arrow" aria-hidden="true">\u203a</span></button>';
    }).join('') || '<div class="wiki-empty">' + esc(STR.emptyResults) + '</div>';
    more.hidden = shown.length <= limit;
    more.textContent = STR.showMore.replace('{n}', String(Math.max(0, shown.length - limit)));
    if (!selected || shown.indexOf(selected) === -1) selected = shown[0] || null;
    drawDetail(selected);
    var active = results.querySelector('[data-id="' + (selected ? selected.id : '') + '"]');
    if (active) active.setAttribute('aria-current', 'true');
  }
  q.addEventListener('input', function () { limit = 35; selected = null; render(); });
  tabs.addEventListener('click', function (e) {
    var b = e.target.closest('[data-type]');
    if (!b) return;
    type = b.dataset.type; hero.value = ''; difficulty.value = ''; limit = 35; selected = null; render();
  });
  hero.addEventListener('change', function () { limit = 35; selected = null; render(); });
  difficulty.addEventListener('change', function () { limit = 35; selected = null; render(); });
  results.addEventListener('click', function (e) {
    var b = e.target.closest('[data-id]');
    if (!b) return;
    selected = DATA.filter(function (x) { return x.id === b.dataset.id; })[0];
    slugHash(selected.id); render();
    if (window.innerWidth < 810) detail.scrollIntoView({behavior: 'smooth', block: 'start'});
  });
  more.addEventListener('click', function () { limit += 45; render(); });
  document.getElementById('clear').addEventListener('click', function () {
    q.value = ''; hero.value = ''; difficulty.value = ''; type = 'All'; selected = null; limit = 35; render(); q.focus();
  });
  function applyHash() {
    try {
      var hash = decodeURIComponent(location.hash.slice(1));
      var found = DATA.filter(function (x) { return x.id === hash; })[0];
      if (found) { type = found.type; selected = found; q.value = found.name; limit = 35; }
    } catch (e) {}
  }
  applyHash();
  window.addEventListener('hashchange', function () { applyHash(); render(); });
  render();
})();
"""

PLUS_SVG = ('<span class="plus" aria-hidden="true">'
            '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6">'
            '<path d="M6 1v10M1 6h10"/></svg></span>')
SEARCH_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
              '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>')


def counts():
    from collections import Counter
    c = Counter(x["type"] for x in DATA)
    pets = sum(1 for x in DATA if x["type"] == "Pet" and x.get("obtainable", True))
    return [c["Character"], c["Skill"], pets, c["Stage"], c["Equipment"],
            c["Mechanic"]]


def wiki_page(lang, meta):
    c = meta
    canon = ("/desktop-pension-squad/wiki/" if lang == "en"
             else "/ru/desktop-pension-squad/wiki/")
    alt = {"en": "/desktop-pension-squad/wiki/",
           "ru": "/ru/desktop-pension-squad/wiki/"}
    home_label = "Home" if lang == "en" else "\u0413\u043b\u0430\u0432\u043d\u0430\u044f"
    home_path = "/" if lang == "en" else "/ru/"
    hub_path = ("/desktop-pension-squad/" if lang == "en"
                else "/ru/desktop-pension-squad/")
    crumbs = crumbs_html(lang, [("Desktop Pension Squad", hub_path),
                                (c["crumb"], None)])

    hero_opts = "".join('<option>%s</option>' % h for h in HEROES)
    diff_opts = "".join('<option>%s</option>' % d for d in DIFFICULTIES)
    stats = "".join(
        '<div class="wiki-stat"><b>%d</b>%s</div>' % (n, label)
        for n, label in zip(counts(), c["statLabels"]))
    faq_items = "".join(
        '<details%s><summary><h3>%s</h3>%s</summary><p>%s</p></details>'
        % (" open" if i == 0 else "", q, PLUS_SVG, a)
        for i, (q, a) in enumerate(c["faq"]))
    sources = "".join(
        '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (u, t)
        for t, u in c["sources"])

    body = (
        '<main id="main"><div class="wrap">%s'
        '<section class="tool-hero"><p class="kicker">%s</p><h1>%s</h1>'
        '<p class="lede">%s</p></section>'
        '<form class="wiki-search" role="search" onsubmit="return false">%s'
        '<label class="wiki-sr" for="query">%s</label>'
        '<input id="query" autocomplete="off" placeholder="%s">'
        '<button class="btn btn-secondary" id="clear" type="button">%s</button></form>'
        '<div class="wiki-controls"><div class="wiki-tabs" id="tabs" role="tablist" aria-label="%s"></div>'
        '<label class="wiki-sr" for="heroFilter">%s</label>'
        '<select class="wiki-select" id="heroFilter"><option value="">%s</option>%s</select>'
        '<label class="wiki-sr" for="difficultyFilter">%s</label>'
        '<select class="wiki-select" id="difficultyFilter"><option value="">%s</option>%s</select></div>'
        '<div class="wiki-stats">%s</div>'
        '<div class="wiki-grid"><section aria-label="%s">'
        '<div class="wiki-sec-head"><h2 id="resultTitle">%s</h2>'
        '<div id="count" class="wiki-count" aria-live="polite"></div></div>'
        '<div class="wiki-results" id="results"></div>'
        '<div class="wiki-more"><button class="btn btn-secondary" id="more" type="button"></button></div>'
        '</section><aside id="detail" class="wiki-detail" aria-live="polite"></aside></div>'
        '<section class="wiki-copy"><p class="sec-label">%s</p><h2>%s</h2><p>%s</p>'
        '<div class="faq">%s</div></section>'
        '<p class="data-line">%s</p>'
        '<p class="wiki-sources">%s %s</p>'
        '</div></main>'
        % (crumbs, c["kicker"], c["h1"], c["lede"], SEARCH_SVG,
           c["searchLabel"], c["searchPlaceholder"], c["clear"],
           c["resultsLabel"], c["heroLabel"], c["heroAll"], hero_opts,
           c["difficultyLabel"], c["difficultyAll"], diff_opts,
           stats, c["resultsLabel"], c["resultsTitle"],
           c["copyKicker"], c["copyH2"], c["copyP"], faq_items,
           c["dataLine"], c["sourcesLabel"], sources)
    )
    jl = [
        {"@context": "https://schema.org", "@type": "WebPage",
         "name": "Desktop Pension Squad Wiki", "description": c["desc"],
         "about": {"@type": "VideoGame", "name": "DPS: Desktop Pension Squad"},
         "publisher": {"@type": "Organization", "name": "BuffForge"}},
        breadcrumb_jsonld(lang, [(home_label, home_path),
                                 ("Desktop Pension Squad", hub_path),
                                 (c["crumb"], canon)]),
    ]
    js = ("<script>\n" + JS.replace("__DATA__", json.dumps(DATA, ensure_ascii=False))
          .replace("__STR__", json.dumps(c, ensure_ascii=False)) + "\n</script>")
    return page(lang, c["title"], c["desc"], canon, alt, body, jsonld=jl, tail=js)


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", rel)


def main():
    write("desktop-pension-squad/wiki/index.html", wiki_page("en", EN))
    write("ru/desktop-pension-squad/wiki/index.html", wiki_page("ru", RU))
    print("build_dps_wiki done")


if __name__ == "__main__":
    main()
