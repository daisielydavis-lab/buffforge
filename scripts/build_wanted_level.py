#!/usr/bin/env python3
"""GTA 6 Wanted Level & Evidence Helper (EN + RU).

Run:  cd <repo root> && python3 scripts/build_wanted_level.py
Rebuild of the user-supplied demo (2026-11-23) in the Daylight Forge light
system. The interactive logic is the demo's (6 stars, 6 police states,
7 Heat evidence icons, 4 situation selects, generated escape checklist,
progress, Copy / Share / Print, ?s= share links, Reset) — only the styling
is the site's own (.wlh-* classes in assets/site.css), plus two verified
additions: the yellow-vs-red vehicle tracker distinction and the
blood-stain / dye-pack shower tip. No per-star trigger crimes are listed
(Rockstar never published exact thresholds).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import (EMAIL, breadcrumb_jsonld, crumbs_html, page)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://buffforge.com"
CANON = {"en": "/gta-6/wanted-evidence-helper/",
         "ru": "/ru/gta-6/wanted-evidence-helper/"}

GTABASE_URL = "https://www.gtabase.com/articles/gta-6/gta-6-wanted-level-explained-police-system-guide"
POLYGON_URL = "https://www.polygon.com/gta-6-wanted-level-heat-how-to-lower-grand-theft-auto/"

WLH = {
    "en": {
        "title": "GTA 6 Wanted Level Helper \u2013 Clear Heat & Lose Cops | BuffForge",
        "desc": ("Interactive GTA 6 Wanted Level Helper. Select your wanted stars, "
                 "police search state and evidence icons to get a step-by-step "
                 "escape and heat-clearing plan."),
        "h1": "GTA 6 Wanted Level & Evidence Helper",
        "card_title": "Wanted Level & Evidence Helper",
        "eyebrow": "GTA VI / Interactive game tools",
        "lede": ("See what the police know. Select your wanted stars, search status, "
                 "and Heat icons to build a practical escape checklist for your "
                 "current situation."),
        "pills": ["\u2605 1\u20136 Star Wanted Levels", "7 Heat Evidence Types",
                  "Personalized Escape Checklist", "No Login Needed"],
        "panel_h": "Build your escape plan",
        "panel_sub": "Match the settings to what you see in your game HUD.",
        "sec1": "Wanted stars",
        "stars_note": ("Stars indicate pursuit intensity; they do not determine which "
                       "evidence has been recorded."),
        "sec2": "Current police status",
        "sec2_note": "Choose one",
        "sec3": "Red Heat / evidence icons",
        "sec3_note": " selected",
        "ev_note": ("Select only icons visible on your screen. No icons? "
                    "Leave all unchecked."),
        "sec4": "Situation details",
        "sec4_note": "Improve recommendations",
        "opt_mission": ("Activity",
                        [("free", "Free roam"),
                         ("mission", "Story / scripted mission"),
                         ("robbery", "Robbery / business alarm")]),
        "opt_movement": ("Escape options",
                         [("both", "Car and on-foot routes"),
                          ("car", "Vehicle available"),
                          ("foot", "On foot only")]),
        "opt_clothes": ("Change of clothes",
                        [("yes", "Accessible"),
                         ("no", "Not accessible now")]),
        "opt_tracker": ("Vehicle tracker",
                        [("unknown", "Unknown / not relevant"),
                         ("yes", "Tracker present"),
                         ("no", "No tracker observed")]),
        "btn_generate": "Generate escape plan \u2197",
        "btn_reset": "Reset",
        "result_eyebrow": "PERSONALIZED STRATEGY",
        "result_h": "Your Escape Plan",
        "result_default": ("Generate a checklist based on your current police "
                           "status and known evidence."),
        "readout_stars": "Wanted level",
        "readout_ev": "Evidence tracked",
        "empty_h": "Ready when you are",
        "empty_p": "Choose your situation and select <strong>Generate escape plan</strong>.",
        "guide_eyebrow": "GTA 6 Wanted & Heat Guide",
        "guide_h1": "How the GTA 6 Wanted Level system works",
        "guide_p1": ("Unlike a simple five-star chase, GTA VI uses up to six wanted "
                     "stars alongside a recognition-based Heat system. Police can react "
                     "to reports from witnesses and alarms, and the icons beneath your "
                     "stars represent identifying information. Escaping the immediate "
                     "pursuit and reducing recognition are related, but separate tasks. "
                     "This tool helps you plan both, based on manually entered game state."),
        "guide_h2": "GTA 6 Heat icons explained",
        "cards": [
            ("\u25c9 Appearance / Face",
             "Police have your physical description. Changing accessories or "
             "hairstyle, or removing a mask after escaping sight, can alter recognition."),
            ("\u2667 Outfit",
             "Police know the clothes you wore. Change the full outfit, not just one small accessory."),
            ("\u25a3 Vehicle",
             "The vehicle has been identified. Switching vehicles or respraying may help; tracker restrictions can apply."),
            ("\u2301 Visible weapon",
             "Visible weapons attract attention. Holster a concealable weapon or stow a long gun."),
            ("\u2667\u2667 Partner",
             "Jason and Lucia were seen together. Separating the pair can reduce that particular identifier."),
            ("\u25a4 CCTV",
             "Ordinary locally stored footage may be destructible. Check the location before assuming the recording is gone."),
            ("\u2601 Cloud CCTV",
             "Cloud-stored evidence cannot be cleared by destroying a local recorder. Reduce other identifiers and exit the area."),
        ],
        "tracker_para": ("<b>Vehicle trackers: yellow vs red.</b> A standard yellow tracker "
                         "only alerts after the car has come to a complete stop for a few "
                         "seconds, and registering the car at a Pay \u2018n\u2019 Spray \u2014 from "
                         "Chapter 3 \u2014 removes it for good. An advanced red tracker alerts "
                         "after about five seconds below the speed limit, and Pay \u2018n\u2019 Spray "
                         "usually refuses the car until the advanced tracker service is "
                         "unlocked through Randy\u2019s vehicle-theft line."),
        "blood_para": ("<b>Blood stains and dye packs.</b> They make you easier to "
                       "recognise \u2014 a shower at a safehouse clears them."),
        "strat_h": "Escape strategy: pursue, evade, then clear Heat",
        "strat_p1": ("<strong>First, break line of sight.</strong> Use available cover and "
                    "a route that avoids the search area. <strong>Second, check the Heat "
                    "icons.</strong> If police know your clothes, car or face, address each "
                    "independently. <strong>Third, avoid re-entering the active Heat zone."
                    "</strong> A pursuit can end while the area remains hot, making renewed "
                    "detection possible."),
        "strat_p2": ("Mission objectives can temporarily override ordinary free-roam "
                     "behavior. If your icon will not clear after an otherwise valid "
                     "action, check the mission objective and whether police still have a "
                     "direct visual on you. The tool does not guarantee that a specific "
                     "icon will disappear."),
        "faq_h": "Frequently asked questions",
        "faq": [
            ("How do I lose cops in GTA 6?",
             "Break their line of sight, leave the active search area, then reduce "
             "the identity details shown by your red Heat icons. Choose your status "
             "and known evidence above for an actionable checklist."),
            ("What do the red icons under wanted stars mean?",
             "They are recognition or evidence indicators: your appearance, outfit, "
             "car, visible weapon, partner and CCTV records. Cloud-stored CCTV may "
             "be represented separately."),
            ("Why is the outfit icon still red after changing clothes?",
             "Ensure you changed the full outfit rather than only an accessory. Some "
             "missions may control when an icon clears, and other identifiers remain "
             "independent. This is not proof of a bug by itself."),
            ("Can changing my car remove all Heat?",
             "No. Vehicle evidence is separate from appearance, outfit and CCTV. "
             "Some tracked vehicles can also have special restrictions."),
            ("Can I delete cloud CCTV evidence?",
             "Published guides distinguish cloud CCTV from on-site footage: the cloud "
             "recording cannot be erased by destroying a local device. Focus on "
             "escaping and addressing other recognition details."),
            ("Is this connected to my GTA 6 game?",
             "No. This is an offline-in-the-browser decision helper. It does not read "
             "live HUD data, modify game files, remove police Heat or access Rockstar accounts."),
        ],
        "research": (
            "Reviewed 23 November 2026. Based on published game guides; details can "
            "change with patches, missions and discoveries. Sources: "
            "<a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">GTABase Wanted &amp; Heat Guide</a>, "
            "<a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">Polygon: How to lower your wanted and heat level in GTA 6</a>, "
            "GameSpot GTA 6 robbery / CCTV guide. "
            "BuffForge is an independent fan-made tools site and is not affiliated "
            "with Rockstar Games or Take-Two Interactive. Spotted a mistake? Email "
            "<a href=\"mailto:%s\">%s</a>." % (GTABASE_URL, POLYGON_URL, EMAIL, EMAIL)),
        "webapp_desc": ("Interactive GTA VI wanted level and heat evidence checklist "
                        "for planning a police escape."),
        "js": {
            "statuses": [
                {"id": "responding", "emoji": "\U0001f4e2", "title": "Cops responding",
                 "sub": "Reported, not on scene"},
                {"id": "unknown", "emoji": "\u2754", "title": "Suspect unknown",
                 "sub": "Police lack your identity"},
                {"id": "pursuit", "emoji": "\U0001f6a8", "title": "In pursuit",
                 "sub": "Police have visual"},
                {"id": "lost", "emoji": "\U0001f441", "title": "Visual lost",
                 "sub": "Still searching"},
                {"id": "heat", "emoji": "\U0001f321", "title": "Heat area",
                 "sub": "Chase ended, area hot"},
                {"id": "clear", "emoji": "\u2713", "title": "No active wanted",
                 "sub": "Avoid new recognition"},
            ],
            "evidence": [
                {"id": "appearance", "emoji": "\u25c9", "title": "Appearance",
                 "sub": "Face / description", "weight": 3,
                 "head": "Change your recognizable appearance",
                 "desc": "Once out of police sight, change or remove conspicuous accessories, use a different hairstyle, or switch out of a mask worn during the incident. Monitor whether the appearance icon actually clears."},
                {"id": "outfit", "emoji": "\u2667", "title": "Outfit",
                 "sub": "Clothing recognized", "weight": 2,
                 "head": "Change your full outfit",
                 "desc": "Swap the complete outfit rather than only a hat or glasses. A spare set in a personal vehicle trunk or available clothing location may help."},
                {"id": "vehicle", "emoji": "\u25a3", "title": "Vehicle",
                 "sub": "Vehicle identified", "weight": 1,
                 "head": "Ditch or change the identified vehicle",
                 "desc": "Switch into a different vehicle once you are out of sight, or consider a Pay \u2018n\u2019 Spray when accessible. Check whether the vehicle Heat icon disappears."},
                {"id": "weapon", "emoji": "\u2301", "title": "Visible weapon",
                 "sub": "Weapon exposed", "weight": 4,
                 "head": "Conceal the visible weapon",
                 "desc": "Holster a concealable firearm. If it is a long gun, stow it in a vehicle trunk or put it away rather than moving openly with it."},
                {"id": "partner", "emoji": "\u2667\u2667", "title": "Partner",
                 "sub": "Jason & Lucia together", "weight": 2,
                 "head": "Separate the identified pair",
                 "desc": "If the game permits it, separate Jason and Lucia after reaching safety. A paired sighting is an identifier independent of clothing or vehicles."},
                {"id": "cctv", "emoji": "\u25a4", "title": "Local CCTV",
                 "sub": "On-site footage", "weight": 5,
                 "head": "Assess on-site CCTV evidence",
                 "desc": "Some regular security recordings are stored locally and can be destroyed in-game. Only attempt this if the recorder is accessible and it does not force you back into the active search area; otherwise prioritize escape."},
                {"id": "cloud", "emoji": "\u2601", "title": "Cloud CCTV",
                 "sub": "Cloud-stored video", "weight": 6,
                 "head": "Do not chase an unremovable cloud recording",
                 "desc": "Cloud-stored recordings cannot be erased by destroying a local CCTV device. Focus on escaping the search area and changing the other recognized identifiers."},
            ],
            "star_label": "{n} of 6 stars",
            "star_aria": "{n} wanted stars",
            "ev_1": "type", "ev_234": "types", "ev_5": "types",
            "step_response": ["Leave the incident area before police arrive",
                              "A reported incident does not always mean police have identified you yet. Move away without causing another report and avoid approaching responding units."],
            "step_unknown": ["Preserve your unknown-suspect status",
                             "Avoid drawing attention or revealing additional details. Move away before the police can establish your identity."],
            "step_pursuit": ["Break direct police line of sight first",
                             "Use alleyways, accessible buildings, corners and cover. Do not pause to change clothing while police have clear visual contact.",
                             "Use turns, cover and a route away from the active search zone; only swap vehicles after breaking visual contact.",
                             "Use turns or cover to lose visual contact, then consider leaving the vehicle to traverse a narrow pedestrian route."],
            "step_lost": ["Exit the active police search radius",
                          "Police have temporarily lost sight of you but are still searching. Remain out of sight and move beyond the search radius instead of immediately doubling back."],
            "step_heat": ["Avoid returning to the hot zone",
                          "The immediate pursuit has ended, but local Heat can trigger renewed attention. Stay away from the marked area until it cools."],
            "step_clear": ["Keep your current low profile",
                           "No active chase is selected. If Heat indicators remain, changing recognized details may reduce future recognition; otherwise you do not need to manufacture a new escape action."],
            "step_high": ["Favor concealment over prolonged open pursuit",
                          "At {n} stars, expect a more demanding response. Avoid relying on a long, exposed straight-line escape; use cover and alternate routes. This is a tactical recommendation, not a guaranteed timer."],
            "step_tracker": ["Account for the vehicle tracker",
                             "A tracker may reveal your vehicle or restrict modification. Prefer a different untracked vehicle once it is safe; do not assume respraying alone will remove tracking."],
            "step_noev": ["No red evidence icon selected",
                          "If the HUD shows no recognized details, prioritize leaving police sight and the search area. Heat may still persist geographically."],
            "step_mission": ["Check for scripted mission restrictions",
                             "Some mission sections control when Heat icons or wanted stars clear. An icon that persists after changing clothes does not necessarily mean your action was incorrect."],
            "step_robbery": ["Avoid the reported robbery location",
                             "Witnesses and alarms may have already dispatched police. Do not return to the scene to handle optional evidence while active police are nearby."],
            "step_final": ["Recheck the HUD after escaping",
                           "Confirm that pursuit has ended. If the area still shows Heat, continue avoiding recognized identifiers and the hot zone. Clearing one Heat icon does not automatically clear the others."],
            "ov_outfit_no": "You have no accessible outfit now. Prioritize escaping and locating a safe change point; changing a hat alone may not clear full outfit recognition.",
            "ov_vehicle_foot": "You are currently on foot. Keep distance from the identified vehicle; do not return to it while Heat persists. Check the vehicle icon after you move away.",
            "ov_vehicle_tracker": "An identified vehicle with a tracker is a stronger reason to abandon it when safely possible. Some tracked vehicles may not qualify for ordinary respraying.",
            "ov_cctv_mission": "Regular footage may be locally destructible, but scripted missions can limit how and when a recording is handled. Follow the objective and do not assume the CCTV icon will clear immediately.",
            "tag_priority": "PRIORITY", "tag_check": "CHECK",
            "tag_evidence": "EVIDENCE", "tag_conditional": "CONDITIONAL",
            "tag_not_removable": "NOT REMOVABLE", "tag_mission": "MISSION",
            "list_h": "Action checklist",
            "result_default": ("Generate a checklist based on your current police "
                               "status and known evidence."),
            "empty_h": "Ready when you are",
            "empty_p": "Choose your situation and select <strong>Generate escape plan</strong>.",
            "complete": "{a}/{b} complete",
            "progress_label": "Checklist {p}% complete",
            "note": "Guidance is based on published GTA VI mechanics, not a live game connection. Actions are not guaranteed to clear an icon; scripted missions and patches may behave differently.",
            "btn_copy": "Copy plan", "btn_share": "Copy share link",
            "btn_print": "Print checklist",
            "toast_copied": "Copied to clipboard",
            "toast_nocopy": "Copy is unavailable in this browser",
            "toast_reset": "Selection reset",
            "plain_title": "GTA 6 Wanted Level & Evidence Helper | BuffForge",
            "plain_stars": "{n} wanted stars | {status}",
            "plain_ev": "Evidence: {list}",
            "plain_ev_none": "Evidence: None selected",
            "plain_footer": "Game guide only; verify with in-game HUD. buffforge.com/gta-6/wanted-evidence-helper/",
        },
    },
    "ru": {
        "title": "Помощник по розыску GTA 6 — как сбросить звёзды и улики | BuffForge",
        "desc": ("Интерактивный помощник по розыску в GTA 6. Выберите звёзды, "
                 "статус полиции и значки улик — и получите пошаговый план побега "
                 "и снятия розыска."),
        "h1": "Помощник по розыску и уликам в GTA 6",
        "card_title": "Помощник по розыску и уликам",
        "eyebrow": "GTA VI / Интерактивные игровые инструменты",
        "lede": ("Посмотрите, что о вас знает полиция. Выберите звёзды розыска, "
                 "статус поисков и значки улик — и составьте практичный план побега "
                 "для вашей ситуации."),
        "pills": ["\u2605 Розыск от 1 до 6 звёзд", "7 видов улик",
                  "Персональный план побега", "Без регистрации"],
        "panel_h": "Составьте план побега",
        "panel_sub": "Настройте параметры под то, что видите в игре.",
        "sec1": "Звёзды розыска",
        "stars_note": ("Звёзды показывают силу погони, но не говорят, какие улики "
                       "уже зафиксированы."),
        "sec2": "Текущий статус полиции",
        "sec2_note": "Выберите один",
        "sec3": "Красные значки улик",
        "sec3_note": "Выбрано: ",
        "ev_note": ("Отмечайте только те значки, которые видны на экране. "
                    "Нет значков? Оставьте всё пустым."),
        "sec4": "Детали ситуации",
        "sec4_note": "Улучшают рекомендации",
        "opt_mission": ("Занятие",
                        [("free", "Свободная игра"),
                         ("mission", "Сюжетная миссия"),
                         ("robbery", "Ограбление / сработала сигнализация")]),
        "opt_movement": ("Варианты побега",
                         [("both", "Машина и пешком"),
                          ("car", "Есть транспорт"),
                          ("foot", "Только пешком")]),
        "opt_clothes": ("Смена одежды",
                        [("yes", "Доступна"),
                         ("no", "Сейчас недоступна")]),
        "opt_tracker": ("Трекер на машине",
                        [("unknown", "Неизвестно / не важно"),
                         ("yes", "Трекер есть"),
                         ("no", "Трекера не замечено")]),
        "btn_generate": "Составить план побега \u2197",
        "btn_reset": "Сбросить",
        "result_eyebrow": "ПЕРСОНАЛЬНАЯ СТРАТЕГИЯ",
        "result_h": "Ваш план побега",
        "result_default": ("Составьте чек-лист по текущему статусу полиции "
                           "и известным уликам."),
        "readout_stars": "Уровень розыска",
        "readout_ev": "Улик учтено",
        "empty_h": "Готовы, когда вы готовы",
        "empty_p": "Выберите ситуацию и нажмите «Составить план побега».",
        "guide_eyebrow": "Гайд по розыску и уликам GTA 6",
        "guide_h1": "Как работает система розыска в GTA 6",
        "guide_p1": ("В отличие от простой пятизвёздочной погони, в GTA VI — до шести "
                     "звёзд розыска и система опознания по уликам. Полиция реагирует на "
                     "сообщения свидетелей и сигнализации, а значки под звёздами — это "
                     "информация, по которой вас могут узнать. Уйти от погони и снизить "
                     "узнаваемость — связанные, но отдельные задачи. Этот инструмент "
                     "помогает спланировать обе — по вручную введённому состоянию игры."),
        "guide_h2": "Значки улик в GTA 6",
        "cards": [
            ("\u25c9 Внешность / лицо",
             "Полиция знает ваше описание. Смена аксессуаров или причёски либо "
             "снятие маски после выхода из поля зрения может изменить опознание."),
            ("\u2667 Одежда",
             "Полиция знает, во что вы были одеты. Смените весь комплект, а не один маленький аксессуар."),
            ("\u25a3 Транспорт",
             "Машина опознана. Помогают смена машины или перекраска; могут действовать ограничения из-за трекера."),
            ("\u2301 Оружие на виду",
             "Заметное оружие привлекает внимание. Уберите пистолет в кобуру или спрячьте длинноствольное оружие."),
            ("\u2667\u2667 Напарник",
             "Джейсона и Люсию видели вместе. Разделение пары может снять этот конкретный признак."),
            ("\u25a4 Камеры",
             "Обычную запись, хранящуюся на месте, можно уничтожить. Проверьте место, прежде чем считать запись исчезнувшей."),
            ("\u2601 Облачные камеры",
             "Запись в облаке нельзя стереть, уничтожив местный регистратор. Снижайте другие признаки и покидайте район."),
        ],
        "tracker_para": ("<b>Трекеры: жёлтый и красный.</b> Обычный жёлтый трекер "
                         "срабатывает, только если машина полностью остановилась на "
                         "несколько секунд, а регистрация машины в Pay \u2018n\u2019 Spray "
                         "— с 3-й главы — убирает его навсегда. Продвинутый красный "
                         "трекер срабатывает примерно через пять секунд езды ниже лимита "
                         "скорости, а Pay \u2018n\u2019 Spray обычно отказывается принимать "
                         "такую машину, пока услуга продвинутого трекера не разблокирована "
                         "через линию угона автомобилей у Рэнди."),
        "blood_para": ("<b>Пятна крови и пакеты с красителем.</b> Они делают вас "
                       "заметнее — душ в убежище всё смывает."),
        "strat_h": "Стратегия побега: уйти, скрыться, снять улики",
        "strat_p1": ("<strong>Сначала разорвите видимость.</strong> Используйте укрытия "
                    "и маршрут в обход зоны поисков. <strong>Затем проверьте значки "
                    "улик.</strong> Если полиция знает вашу одежду, машину или лицо, "
                    "разберитесь с каждым признаком отдельно. <strong>В-третьих, не "
                    "возвращайтесь в активную горячую зону.</strong> Погоня может "
                    "закончиться, а район останется горячим — и вас снова заметят."),
        "strat_p2": ("Задачи миссии могут временно отменять обычное поведение в "
                     "свободной игре. Если значок не снимается после вроде бы верного "
                     "действия, проверьте задачу миссии и то, видит ли вас полиция "
                     "напрямую. Инструмент не гарантирует, что конкретный значок исчезнет."),
        "faq_h": "Частые вопросы",
        "faq": [
            ("Как уйти от полиции в GTA 6?",
             "Разорвите видимость, покиньте активную зону поисков, а затем снимите "
             "те признаки, которые показывают красные значки улик. Выберите статус "
             "и известные улики выше — получите готовый чек-лист."),
            ("Что означают красные значки под звёздами розыска?",
             "Это признаки опознания: внешность, одежда, машина, оружие на виду, "
             "напарник и записи с камер. Облачные записи могут показываться "
             "отдельным значком."),
            ("Почему значок одежды остался красным после смены одежды?",
             "Убедитесь, что сменили весь комплект, а не только аксессуар. "
             "Некоторые миссии управляют тем, когда снимается значок, а остальные "
             "признаки независимы. Само по себе это ещё не доказательство бага."),
            ("Может ли смена машины снять весь розыск?",
             "Нет. Улики по машине отделены от внешности, одежды и записей с камер. "
             "У некоторых машин с трекером есть особые ограничения."),
            ("Можно ли удалить облачную запись с камер?",
             "Опубликованные гайды отличают облачные камеры от обычных: облачную "
             "запись нельзя стереть, уничтожив местное устройство. Сосредоточьтесь "
             "на побеге и других признаках опознания."),
            ("Инструмент связан с моей игрой GTA 6?",
             "Нет. Это офлайн-помощник в браузере. Он не читает данные игры, не "
             "меняет файлы, не снимает розыск и не подключается к аккаунтам Rockstar."),
        ],
        "research": (
            "Проверено 23 ноября 2026 года. По опубликованным гайдам; детали могут "
            "меняться с патчами, миссиями и открытиями. Источники: "
            "<a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">GTABase Wanted &amp; Heat Guide</a>, "
            "<a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">Polygon: How to lower your wanted and heat level in GTA 6</a>, "
            "гайд GameSpot по ограблениям и камерам в GTA 6. "
            "BuffForge — независимый фанатский проект, не связанный с Rockstar Games "
            "и Take-Two Interactive. Нашли ошибку? Напишите на "
            "<a href=\"mailto:%s\">%s</a>." % (GTABASE_URL, POLYGON_URL, EMAIL, EMAIL)),
        "webapp_desc": ("Интерактивный чек-лист розыска и улик GTA VI для планирования "
                        "побега от полиции."),
        "js": {
            "statuses": [
                {"id": "responding", "emoji": "\U0001f4e2", "title": "Полиция едет",
                 "sub": "Вызов принят, на месте ещё нет"},
                {"id": "unknown", "emoji": "\u2754", "title": "Подозреваемый неизвестен",
                 "sub": "Полиция не знает, кто вы"},
                {"id": "pursuit", "emoji": "\U0001f6a8", "title": "Погоня",
                 "sub": "Полиция вас видит"},
                {"id": "lost", "emoji": "\U0001f441", "title": "Потеряли из виду",
                 "sub": "Поиски продолжаются"},
                {"id": "heat", "emoji": "\U0001f321", "title": "Зона розыска",
                 "sub": "Погоня окончена, район горячий"},
                {"id": "clear", "emoji": "\u2713", "title": "Розыска нет",
                 "sub": "Не привлекайте внимания"},
            ],
            "evidence": [
                {"id": "appearance", "emoji": "\u25c9", "title": "Внешность",
                 "sub": "Лицо / описание", "weight": 3,
                 "head": "Измените узнаваемую внешность",
                 "desc": "Оторвавшись от полиции, снимите или смените заметные аксессуары, поменяйте причёску или снимите маску, в которой были на деле. Проверьте, исчез ли значок внешности."},
                {"id": "outfit", "emoji": "\u2667", "title": "Одежда",
                 "sub": "Одежда опознана", "weight": 2,
                 "head": "Смените одежду полностью",
                 "desc": "Меняйте весь комплект, а не только шапку или очки. Может помочь запасной комплект в багажнике личной машины или в доступном месте с одеждой."},
                {"id": "vehicle", "emoji": "\u25a3", "title": "Транспорт",
                 "sub": "Машина опознана", "weight": 1,
                 "head": "Бросьте опознанную машину или пересядьте",
                 "desc": "Пересядьте в другую машину, когда выйдете из поля зрения, или заедьте в Pay \u2018n\u2019 Spray, если он доступен. Проверьте, исчез ли значок транспорта."},
                {"id": "weapon", "emoji": "\u2301", "title": "Оружие на виду",
                 "sub": "Оружие заметно", "weight": 4,
                 "head": "Спрячьте оружие",
                 "desc": "Пистолет можно убрать в кобуру. Длинноствольное оружие уберите в багажник или выбросьте, а не носите открыто."},
                {"id": "partner", "emoji": "\u2667\u2667", "title": "Напарник",
                 "sub": "Джейсон и Люсия вместе", "weight": 2,
                 "head": "Разделите опознанную пару",
                 "desc": "Если игра позволяет, разойдитесь с Джейсоном или Люсией, когда доберётесь до безопасного места. Совместное появление — отдельная улика, независимая от одежды и машин."},
                {"id": "cctv", "emoji": "\u25a4", "title": "Камеры",
                 "sub": "Запись на месте", "weight": 5,
                 "head": "Оцените запись с местных камер",
                 "desc": "Некоторые обычные записи хранятся на месте, и их можно уничтожить в игре. Пытайтесь, только если регистратор доступен и это не вернёт вас в зону поисков; иначе сначала спасайтесь."},
                {"id": "cloud", "emoji": "\u2601", "title": "Облачные камеры",
                 "sub": "Запись в облаке", "weight": 6,
                 "head": "Не гонитесь за неудаляемой облачной записью",
                 "desc": "Облачные записи нельзя стереть, уничтожив местное устройство. Сосредоточьтесь на побеге из зоны поисков и смене других опознанных деталей."},
            ],
            "star_label": "{n} из 6 звёзд",
            "star_aria": "{n} звёзд розыска",
            "ev_1": "вид", "ev_234": "вида", "ev_5": "видов",
            "step_response": ["Покиньте место происшествия до приезда полиции",
                              "Сообщение о преступлении ещё не значит, что полиция вас опознала. Уходите, не создавая новых поводов для вызова, и не подходите к прибывающим нарядам."],
            "step_unknown": ["Сохраните статус неизвестного подозреваемого",
                             "Не привлекайте внимания и не раскрывайте лишних деталей. Уходите, пока полиция не установила вашу личность."],
            "step_pursuit": ["Сначала разорвите прямую видимость полиции",
                             "Используйте переулки, доступные здания, углы и укрытия. Не останавливайтесь переодеваться, пока полиция вас чётко видит.",
                             "Используйте повороты, укрытия и маршрут вдали от активной зоны поисков; пересаживайтесь, только разорвав визуальный контакт.",
                             "Используйте повороты или укрытия, чтобы потерять визуальный контакт, а затем при необходимости бросьте машину и уйдите пешком по узкому маршруту."],
            "step_lost": ["Выйдите из активного радиуса поисков полиции",
                          "Полиция временно потеряла вас из виду, но поиски продолжаются. Оставайтесь вне поля зрения и уйдите за радиус поисков, а не возвращайтесь сразу обратно."],
            "step_heat": ["Не возвращайтесь в горячую зону",
                          "Погоня окончена, но местный розыск может снова привлечь внимание. Держитесь подальше от отмеченной зоны, пока она не остынет."],
            "step_clear": ["Сохраняйте низкий профиль",
                           "Активной погони нет. Если значки улик остались, смена опознанных деталей может снизить риск будущего опознания; специально создавать новые действия для побега не нужно."],
            "step_high": ["Выбирайте скрытность, а не долгое открытое бегство",
                          "При {n} звёздах ждите более жёсткой реакции. Не полагайтесь на долгую прямую погоню по открытой местности; используйте укрытия и обходные маршруты. Это тактическая рекомендация, а не гарантированный таймер."],
            "step_tracker": ["Учтите трекер на машине",
                             "Трекер может выдать вашу машину или ограничить её переделку. Когда станет безопасно, лучше пересесть в другую машину без трекера; не думайте, что одной перекраски хватит, чтобы снять слежку."],
            "step_noev": ["Красных значков улик не выбрано",
                          "Если на экране нет опознанных деталей, сначала разорвите визуальный контакт с полицией и покиньте зону поисков. Розыск в районе может сохраняться."],
            "step_mission": ["Проверьте ограничения сюжетной миссии",
                             "Некоторые эпизоды миссий управляют тем, когда снимаются значки улик и звёзды розыска. Если значок остался после смены одежды, это не обязательно значит, что вы сделали что-то не так."],
            "step_robbery": ["Не возвращайтесь к месту ограбления",
                             "Свидетели и сигнализация уже могли вызвать полицию. Не возвращайтесь на место ради необязательных улик, пока рядом активная полиция."],
            "step_final": ["После побега сверьтесь с экраном",
                           "Убедитесь, что погоня окончена. Если район всё ещё горячий, продолжайте избегать опознанных деталей и горячей зоны. Снятие одного значка не снимает остальные автоматически."],
            "ov_outfit_no": "Сменить одежду сейчас негде. Сначала спасайтесь и найдите безопасное место для переодевания: одна только смена шапки может не снять опознание одежды.",
            "ov_vehicle_foot": "Сейчас вы пешком. Держитесь подальше от опознанной машины; не возвращайтесь к ней, пока действует розыск. Отойдя, проверьте значок транспорта.",
            "ov_vehicle_tracker": "Опознанная машина с трекером — веская причина бросить её, когда станет безопасно. Некоторые машины с трекером могут не подходить для обычной перекраски.",
            "ov_cctv_mission": "Обычную запись иногда можно уничтожить на месте, но сюжетные миссии могут ограничивать, как и когда обрабатывается запись. Следуйте задаче и не думайте, что значок камер исчезнет сразу.",
            "tag_priority": "ПРИОРИТЕТ", "tag_check": "ПРОВЕРИТЬ",
            "tag_evidence": "УЛИКА", "tag_conditional": "УСЛОВНО",
            "tag_not_removable": "НЕ УБРАТЬ", "tag_mission": "МИССИЯ",
            "list_h": "Чек-лист действий",
            "result_default": ("Составьте чек-лист по текущему статусу полиции "
                               "и известным уликам."),
            "empty_h": "Готовы, когда вы готовы",
            "empty_p": "Выберите ситуацию и нажмите «Составить план побега».",
            "complete": "{a}/{b} выполнено",
            "progress_label": "Чек-лист выполнен на {p}%",
            "note": "Советы основаны на опубликованных механиках GTA VI, а не на живой связи с игрой. Действия не гарантируют снятие значка: сюжетные миссии и патчи могут вести себя иначе.",
            "btn_copy": "Скопировать план", "btn_share": "Скопировать ссылку",
            "btn_print": "Печать чек-листа",
            "toast_copied": "Скопировано в буфер обмена",
            "toast_nocopy": "Копирование недоступно в этом браузере",
            "toast_reset": "Выбор сброшен",
            "plain_title": "Помощник по розыску и уликам в GTA 6 | BuffForge",
            "plain_stars": "{n} звёзд | {status}",
            "plain_ev": "Улики: {list}",
            "plain_ev_none": "Улики: не выбраны",
            "plain_footer": "Только гайд по игре; сверяйтесь с экраном. buffforge.com/ru/gta-6/wanted-evidence-helper/",
        },
    },
}


def _select(c, key, field_id):
    label, opts = c[key]
    options = "".join('<option value="%s">%s</option>' % (v, l) for v, l in opts)
    return ('<div class="field"><label for="%s">%s</label>'
            '<div class="select-wrap"><select id="%s">%s</select></div></div>'
            % (field_id, label, field_id, options))


def body_html(lang):
    c = WLH[lang]
    pills = "".join('<span class="wlh-pill">%s</span>' % p for p in c["pills"])
    cards = "".join('<div class="wlh-guide-card"><b>%s</b><p>%s</p></div>' % (t, d)
                    for t, d in c["cards"])
    faq = "".join(
        '<details><summary><h3>%s</h3><span class="plus">+</span></summary>'
        '<p>%s</p></details>' % (q, a) for q, a in c["faq"])
    if lang == "en":
        ev_count = '<span id="evidence-count">2</span>%s' % c["sec3_note"]
        aria_workspace = "Interactive wanted level helper"
        aria_stars = "Select wanted star level"
        aria_result = "Your escape plan"
    else:
        ev_count = '%s<span id="evidence-count">2</span>' % c["sec3_note"]
        aria_workspace = "Интерактивный помощник по розыску"
        aria_stars = "Выберите уровень розыска"
        aria_result = "Ваш план побега"
    return (
        '<section class="tool-hero">'
        '<p class="wlh-eyebrow">%s</p><h1>%s</h1>'
        '<p class="lede">%s</p><div class="wlh-pills">%s</div></section>'
        '<section class="wlh-workspace" aria-label="%s">'
        '<div class="panel">'
        '<div class="panel-title"><h2>%s</h2></div>'
        '<p class="wlh-small">%s</p>'
        '<div class="wlh-sec"><div class="wlh-sec-head"><h3><span class="wlh-num">01</span>%s</h3>'
        '<span class="wlh-small" id="star-label">%s</span></div>'
        '<div class="wlh-stars" id="stars" role="group" aria-label="%s"></div>'
        '<p class="wlh-tiny">%s</p></div>'
        '<div class="wlh-sec"><div class="wlh-sec-head"><h3><span class="wlh-num">02</span>%s</h3>'
        '<span class="wlh-small">%s</span></div>'
        '<div class="wlh-choice-grid" id="statuses"></div></div>'
        '<div class="wlh-sec"><div class="wlh-sec-head"><h3><span class="wlh-num">03</span>%s</h3>'
        '<span class="wlh-small">%s</span></div>'
        '<div class="wlh-ev-grid" id="evidence"></div>'
        '<p class="wlh-tiny">%s</p></div>'
        '<div class="wlh-sec"><div class="wlh-sec-head"><h3><span class="wlh-num">04</span>%s</h3>'
        '<span class="wlh-small">%s</span></div>'
        '<div class="wlh-extras">%s%s%s%s</div></div>'
        '<div class="wlh-actions">'
        '<button class="btn btn-primary" id="generate" type="button">%s</button>'
        '<button class="btn btn-secondary" id="reset" type="button">%s</button>'
        '</div></div>'
        '<aside class="panel wlh-result" id="result" aria-label="%s">'
        '<div class="wlh-result-head"><p class="wlh-eyebrow">%s</p><h2>%s</h2>'
        '<p id="result-summary">%s</p>'
        '<div class="wlh-readout"><div><small>%s</small><strong id="readout-stars">'
        '\u2605\u2605\u2605\u2606\u2606\u2606</strong></div>'
        '<div><small>%s</small><strong id="readout-evidence">%s</strong></div></div></div>'
        '<div class="wlh-result-body" id="result-body">'
        '<div class="wlh-empty"><span class="wlh-sym">\U0001f6e1\ufe0f</span>'
        '<b>%s</b><p>%s</p></div></div></aside></section>'
        '<article class="wlh-article" id="guide">'
        '<p class="wlh-eyebrow">%s</p><h2>%s</h2><p>%s</p>'
        '<h2>%s</h2><div class="wlh-guide-grid">%s</div>'
        '<p>%s</p><p>%s</p>'
        '<h2>%s</h2><p>%s</p><p>%s</p>'
        '<div class="faq"><h2>%s</h2>%s</div></article>'
        '<p class="data-line">%s</p>'
        '<div class="wlh-toast" id="toast" role="status" aria-live="polite"></div>'
        % (c["eyebrow"], c["h1"], c["lede"], pills,
           aria_workspace, c["panel_h"], c["panel_sub"],
           c["sec1"], c["js"]["star_label"].replace("{n}", "3"), aria_stars,
           c["stars_note"],
           c["sec2"], c["sec2_note"],
           c["sec3"], ev_count, c["ev_note"],
           c["sec4"], c["sec4_note"],
           _select(c, "opt_mission", "mission"), _select(c, "opt_movement", "movement"),
           _select(c, "opt_clothes", "clothes"), _select(c, "opt_tracker", "tracker"),
           c["btn_generate"], c["btn_reset"],
           aria_result, c["result_eyebrow"], c["result_h"], c["result_default"],
           c["readout_stars"], c["readout_ev"],
           "2 types" if lang == "en" else "2 \u0432\u0438\u0434\u0430",
           c["empty_h"], c["empty_p"],
           c["guide_eyebrow"], c["guide_h1"], c["guide_p1"],
           c["guide_h2"], cards, c["tracker_para"], c["blood_para"],
           c["strat_h"], c["strat_p1"], c["strat_p2"],
           c["faq_h"], faq, c["research"]))


WLH_JS = r"""
(()=>{'use strict';
const STR=__STR__;
const $=id=>document.getElementById(id);
const statusOptions=STR.statuses;
const evTypes=STR.evidence;
const defaults={stars:3,status:'lost',evidence:['outfit','vehicle'],mission:'free',movement:'both',clothes:'yes',tracker:'unknown'};
let state={...defaults,evidence:[...defaults.evidence]},plan=[],checked=new Set(),generated=false;
const params=new URLSearchParams(location.search);
if(params.has('s')){try{const q=JSON.parse(decodeURIComponent(params.get('s')));if(Number.isInteger(q.stars)&&q.stars>=1&&q.stars<=6)state.stars=q.stars;if(statusOptions.some(x=>x.id===q.status))state.status=q.status;if(Array.isArray(q.evidence))state.evidence=[...new Set(q.evidence.filter(x=>evTypes.some(e=>e.id===x)))];for(const key of ['mission','movement','clothes','tracker']){const opts={mission:['free','mission','robbery'],movement:['both','car','foot'],clothes:['yes','no'],tracker:['unknown','yes','no']};if(opts[key].includes(q[key]))state[key]=q[key]}}catch(e){}}
function evWord(n){if(n%10===1&&n%100!==11)return STR.ev_1;if(n%10>=2&&n%10<=4&&(n%100<10||n%100>=20))return STR.ev_234;return STR.ev_5}
function escapeText(x){return String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function toast(s){$('toast').textContent=s;$('toast').classList.add('show');clearTimeout(toast.timer);toast.timer=setTimeout(()=>$('toast').classList.remove('show'),2400)}
function renderInputs(){
$('stars').innerHTML=Array.from({length:6},(_,i)=>`<button type="button" class="wlh-star ${i<state.stars?'is-on':''}" data-star="${i+1}" aria-pressed="${i+1===state.stars}" aria-label="${STR.star_aria.replace('{n}',i+1)}">\u2605</button>`).join('');
$('star-label').textContent=STR.star_label.replace('{n}',state.stars);
$('statuses').innerHTML=statusOptions.map(s=>`<button type="button" class="wlh-choice ${state.status===s.id?'active':''}" data-status="${s.id}" aria-pressed="${state.status===s.id}"><span class="wlh-sym" aria-hidden="true">${s.emoji}</span><span><b>${s.title}</b><small>${s.sub}</small></span></button>`).join('');
$('evidence').innerHTML=evTypes.map(e=>`<button type="button" class="wlh-ev ${state.evidence.includes(e.id)?'active':''}" data-evidence="${e.id}" aria-pressed="${state.evidence.includes(e.id)}"><span class="wlh-sym" aria-hidden="true">${e.emoji}</span><span><b>${e.title}</b><small>${e.sub}</small></span><span class="wlh-check" aria-hidden="true">\u2713</span></button>`).join('');
$('evidence-count').textContent=state.evidence.length;
for(const key of ['mission','movement','clothes','tracker'])$(key).value=state[key];
$('readout-stars').textContent='\u2605'.repeat(state.stars)+'\u2606'.repeat(6-state.stars);
$('readout-evidence').textContent=state.evidence.length+' '+evWord(state.evidence.length);
}
function add(id,head,desc,tag=''){if(!plan.some(p=>p.id===id))plan.push({id,head,desc,tag})}
function buildPlan(){plan=[];const s=state;const has=id=>s.evidence.includes(id);
const active=['pursuit','lost'].includes(s.status);
if(s.status==='responding')add('response',STR.step_response[0],STR.step_response[1]);
if(s.status==='unknown')add('unknown',STR.step_unknown[0],STR.step_unknown[1]);
if(s.status==='pursuit')add('break-sight',STR.step_pursuit[0],s.movement==='foot'?STR.step_pursuit[1]:s.movement==='car'?STR.step_pursuit[2]:STR.step_pursuit[3],STR.tag_priority);
if(s.status==='lost')add('leave-search',STR.step_lost[0],STR.step_lost[1],STR.tag_priority);
if(s.status==='heat')add('heat-zone',STR.step_heat[0],STR.step_heat[1],STR.tag_priority);
if(s.status==='clear')add('no-chase',STR.step_clear[0],STR.step_clear[1]);
if(active&&s.stars>=4)add('high-stars',STR.step_high[0],STR.step_high[1].replace('{n}',s.stars));
if(s.tracker==='yes'&&s.movement!=='foot')add('tracker',STR.step_tracker[0],STR.step_tracker[1],STR.tag_check);
if(s.evidence.length){evTypes.filter(e=>has(e.id)).sort((a,b)=>a.weight-b.weight).forEach(e=>{
let desc=e.desc;if(e.id==='outfit'&&s.clothes==='no')desc=STR.ov_outfit_no;
if(e.id==='vehicle'&&s.movement==='foot')desc=STR.ov_vehicle_foot;
if(e.id==='vehicle'&&s.tracker==='yes')desc=STR.ov_vehicle_tracker;
if(e.id==='cctv'&&s.mission==='mission')desc=STR.ov_cctv_mission;
add(e.id,e.head,desc,e.id==='cloud'?STR.tag_not_removable:e.id==='cctv'?STR.tag_conditional:STR.tag_evidence);
});}else add('no-evidence',STR.step_noev[0],STR.step_noev[1]);
if(s.mission==='mission')add('mission',STR.step_mission[0],STR.step_mission[1],STR.tag_mission);
if(s.mission==='robbery')add('alarm',STR.step_robbery[0],STR.step_robbery[1]);
if(s.status!=='heat'&&s.status!=='clear')add('final-check',STR.step_final[0],STR.step_final[1]);
checked=new Set();generated=true;renderResult();
}
function renderResult(){if(!generated)return;
const pct=plan.length?Math.round(100*checked.size/plan.length):0;
$('result-summary').textContent=statusOptions.find(x=>x.id===state.status).title+' \u00b7 '+state.evidence.length+' '+evWord(state.evidence.length);
$('result-body').innerHTML=`<div class="wlh-sec-head"><h3>${STR.list_h}</h3><span class="wlh-small">${STR.complete.replace('{a}',checked.size).replace('{b}',plan.length)}</span></div><div class="wlh-progress" aria-label="${STR.progress_label.replace('{p}',pct)}"><span style="width:${pct}%"></span></div><ol class="wlh-steps">${plan.map((p,i)=>`<li class="${checked.has(p.id)?'done':''}"><input type="checkbox" id="step-${i}" data-step="${escapeText(p.id)}" ${checked.has(p.id)?'checked':''}><label for="step-${i}">${p.tag?`<span class="wlh-tag ${p.tag===STR.tag_not_removable||p.tag===STR.tag_mission?'warn':p.tag===STR.tag_priority?'good':''}">${escapeText(p.tag)}</span>`:''}<strong>${i+1}. ${escapeText(p.head)}</strong><p>${escapeText(p.desc)}</p></label></li>`).join('')}</ol><p class="wlh-note">${STR.note}</p><div class="wlh-result-btns"><button class="btn btn-secondary" type="button" id="copy-plan">${STR.btn_copy}</button><button class="btn btn-secondary" type="button" id="share-plan">${STR.btn_share}</button><button class="btn btn-secondary" type="button" id="print-plan">${STR.btn_print}</button></div>`;
}
function plainPlan(){return STR.plain_title+'\n'+STR.plain_stars.replace('{n}',state.stars).replace('{status}',statusOptions.find(x=>x.id===state.status).title)+'\n'+(state.evidence.length?STR.plain_ev.replace('{list}',state.evidence.map(id=>evTypes.find(e=>e.id===id).title).join(', ')):STR.plain_ev_none)+'\n\n'+plan.map((p,i)=>`${checked.has(p.id)?'[x]':'[ ]'} ${i+1}. ${p.head}\n${p.desc}`).join('\n\n')+'\n\n'+STR.plain_footer;}
async function copy(str){try{await navigator.clipboard.writeText(str);toast(STR.toast_copied);}catch(e){const ta=document.createElement('textarea');ta.value=str;ta.style.position='fixed';ta.style.left='-9999px';document.body.appendChild(ta);ta.select();try{document.execCommand('copy');toast(STR.toast_copied)}catch(x){toast(STR.toast_nocopy)}ta.remove()}}
$('stars').addEventListener('click',e=>{const btn=e.target.closest('[data-star]');if(!btn)return;state.stars=Number(btn.dataset.star);renderInputs()});
$('statuses').addEventListener('click',e=>{const btn=e.target.closest('[data-status]');if(!btn)return;state.status=btn.dataset.status;renderInputs()});
$('evidence').addEventListener('click',e=>{const btn=e.target.closest('[data-evidence]');if(!btn)return;const id=btn.dataset.evidence;state.evidence=state.evidence.includes(id)?state.evidence.filter(x=>x!==id):[...state.evidence,id];renderInputs()});
for(const key of ['mission','movement','clothes','tracker'])$(key).addEventListener('change',e=>{state[key]=e.target.value});
$('generate').addEventListener('click',()=>{buildPlan();if(window.matchMedia('(max-width:880px)').matches)$('result').scrollIntoView({behavior:'smooth',block:'start'})});
$('reset').addEventListener('click',()=>{state={...defaults,evidence:[...defaults.evidence]};checked=new Set();generated=false;history.replaceState(null,'',location.pathname);renderInputs();$('result-summary').textContent=STR.result_default;$('result-body').innerHTML='<div class="wlh-empty"><span class="wlh-sym">\U0001f6e1\ufe0f</span><b>'+STR.empty_h+'</b><p>'+STR.empty_p+'</p></div>';toast(STR.toast_reset)});
$('result-body').addEventListener('change',e=>{if(!e.target.matches('[data-step]'))return;if(e.target.checked)checked.add(e.target.dataset.step);else checked.delete(e.target.dataset.step);renderResult()});
$('result-body').addEventListener('click',e=>{if(e.target.id==='copy-plan')copy(plainPlan());if(e.target.id==='share-plan'){const url=new URL(location.href);url.searchParams.set('s',encodeURIComponent(JSON.stringify(state)));copy(url.toString())}if(e.target.id==='print-plan')window.print()});
renderInputs();if(params.has('s'))buildPlan();
})();
"""


def script_for(lang):
    return WLH_JS.replace("__STR__", json.dumps(WLH[lang]["js"], ensure_ascii=False))


def wanted_page(lang):
    c = WLH[lang]
    home = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    hub_path = "/gta-6/" if lang == "en" else "/ru/gta-6/"
    canon = CANON[lang]
    alt = {"en": CANON["en"], "ru": CANON["ru"]}
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": a}}
                             for q, a in c["faq"]]}
    jl = [breadcrumb_jsonld(lang, [(home, home_path), ("GTA 6", hub_path),
                                   (c["card_title"], canon)]),
          {"@context": "https://schema.org", "@type": "WebApplication",
           "name": c["h1"], "url": BASE + canon, "inLanguage": lang,
           "description": c["webapp_desc"], "applicationCategory": "GameApplication",
           "operatingSystem": "Any modern browser",
           "offers": {"@type": "Offer", "price": "0"}},
          faq_ld]
    body = ('<main id="main" class="wrap">%s%s</main>'
            % (crumbs_html(lang, [("GTA 6", hub_path), (c["card_title"], None)]),
               body_html(lang)))
    return page(lang, c["title"], c["desc"], canon, alt, body, jsonld=jl,
                games=("gta-6",), tail="<script>%s</script>\n" % script_for(lang))


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", rel)


def main():
    write("gta-6/wanted-evidence-helper/index.html", wanted_page("en"))
    write("ru/gta-6/wanted-evidence-helper/index.html", wanted_page("ru"))
    print("wanted level helper done")


if __name__ == "__main__":
    main()
