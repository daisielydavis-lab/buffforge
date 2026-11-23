#!/usr/bin/env python3
"""GTA 6 PS5 60 FPS guide (EN + RU). Reader question, then a short free setup.

Checked 22 November 2026:
- Digital Foundry console comparison: 30 fps target, no 40/60 mode, Pro steadier
- smoovplay v0.3.8 README drawings for Connect your PS5 and Frame rate
- smoovplay v0.3.12 release (published 2026-11-21 19:42 UTC): unsigned installer,
  Auto may pick Half, F fullscreens the window's own monitor
- compare page: GTA VI clips are still Rockstar's An Extended Look as a simulated stream;
  the live PS5 recording is Gotham Knights. No live GTA 6 PS5 demo.
- chiaki-ng configuration: Settings → System → Remote Play → Enable Remote Play,
  and Link Device for a code

No HowTo schema: we have not run GTA 6 on a console.
No HDCP instructions. No millisecond figures.
"""
from shell import BASE, breadcrumb_jsonld, crumbs_html, page

DF = "https://www.digitalfoundry.net/features/gta-6-ps5-vs-ps5-pro-xbox-series-x-and-series-s-which-console-plays-best"
SP_REL = "https://github.com/smoovplay/smoovplay/releases/tag/v0.3.12"
SP_README = "https://github.com/smoovplay/smoovplay/blob/v0.3.8/README.md"
SP_README_NEW = "https://github.com/smoovplay/smoovplay/blob/v0.3.12/README.md"
SP_COMPARE = "https://smoovplay.github.io/compare/"
CK_CONF = "https://chiaki-ng.github.io/chiaki-ng/setup/configuration/"
SLUG = "60-fps-ps5"

PLUS = (
    '<span class="plus" aria-hidden="true">'
    '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6">'
    '<path d="M6 1v10M1 6h10"/></svg></span>'
)


def A(url, label):
    return '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (url, label)


def shot(src, w, h, alt, cap):
    return (
        '<figure class="shot"><img src="%s" width="%d" height="%d" alt="%s" '
        'loading="lazy" decoding="async"><figcaption>%s</figcaption></figure>'
        % (src, w, h, alt, cap)
    )


def path_svg(aria, nodes):
    """Four-stop schematic. nodes: (title, detail) x4. Not a screenshot."""
    parts = [
        '<svg class="path-svg" viewBox="0 0 360 500" role="img" aria-label="%s">' % aria
    ]
    y = 16
    for i, (title, detail) in enumerate(nodes):
        parts.append(
            '<rect x="16" y="%d" width="328" height="92" rx="12" fill="var(--paper)" stroke="var(--line)"/>'
            '<circle cx="48" cy="%d" r="14" fill="var(--teal)"/>'
            '<text x="48" y="%d" text-anchor="middle" fill="var(--teal-ink)" font-size="14" font-weight="700">%d</text>'
            '<text x="76" y="%d" fill="var(--ink)" font-size="16" font-weight="600">%s</text>'
            '<text x="76" y="%d" fill="var(--body)" font-size="14">%s</text>'
            % (y, y + 46, y + 51, i + 1, y + 38, title, y + 62, detail)
        )
        if i < 3:
            ay = y + 92
            parts.append(
                '<path d="M180 %d v16" stroke="var(--teal)" stroke-width="2" fill="none"/>'
                '<path d="M174 %d l6 8 l6-8" fill="var(--teal)"/>' % (ay, ay + 16)
            )
        y += 120
    parts.append("</svg>")
    return "".join(parts)


def _ul(items):
    return "<ul>" + "".join("<li>%s</li>" % x for x in items) + "</ul>"


def _table(rows):
    return (
        '<table class="fact-table">'
        + "".join("<tr><th>%s</th><td>%s</td></tr>" % pair for pair in rows)
        + "</table>"
    )


def _steps(items):
    bits = []
    for item in items:
        title, text = item[0], item[1]
        extra = item[2] if len(item) > 2 else ""
        bits.append('<li><span class="t">%s</span>%s%s</li>' % (title, text, extra))
    return '<ol class="setup" id="setup">%s</ol>' % "".join(bits)


def _faq(pairs):
    blocks = []
    for i, (q, a) in enumerate(pairs):
        blocks.append(
            "<details%s><summary><h3>%s</h3>%s</summary><p>%s</p></details>"
            % (" open" if i == 0 else "", q, PLUS, a)
        )
    return "".join(blocks)


def _more(summary, paragraphs):
    body = "".join("<p>%s</p>" % p for p in paragraphs)
    return '<details class="more"><summary>%s</summary>%s</details>' % (summary, body)


def _pair(left_h, left_html, right_h, right_html):
    return (
        '<div class="ping-fps">'
        '<article class="ping-card net"><h3>%s</h3>%s</article>'
        '<article class="ping-card fps"><h3>%s</h3>%s</article>'
        "</div>" % (left_h, left_html, right_h, right_html)
    )


def en():
    rel = A(SP_REL, "GitHub Releases")
    readme = A(SP_README, "SmoovPlay README")
    return {
        "title": "GTA 6 at 60 FPS on PS5? Free Remote Play Guide — BuffForge",
        "desc": "GTA 6 stays at a native 30 FPS on PS5 with no 60 mode; a free Windows app can add frames to Remote Play if you play on that PC.",
        "h1": "GTA 6 at 60 FPS on PS5? Free Remote Play guide",
        "crumb": "60 FPS on PS5",
        "lede": (
            "GTA 6 targets 30 FPS on PS5 and PS5 Pro, with no 60 mode. "
            "Free SmoovPlay on a Windows PC can draw extra frames from Remote Play, so the PC monitor looks smoother. "
            "The game stays at 30. This is unproven on a live PS5 copy of GTA 6."
        ),
        "safety": "Download SmoovPlay only from its %s. The Windows installer is an early unsigned build." % rel,
        "jump": [("#need", "What you need"), ("#setup", "Set it up"), ("#feel", "Will it feel like 60?"), ("#faq", "Questions")],
        "art_alt": "Official Grand Theft Auto VI key art: a collage of characters, vehicles and the VI logo.",
        "art_cap": "Official key art. © Rockstar Games. Not a gameplay frame, and not a frame-rate test.",
        "who_h": "Only a TV, or a Windows PC?",
        "bridge": (
            'PS5 can run the game. The console list is the <a href="/gta-6/compatibility/">compatibility check</a>. '
            'The other GTA 6 tools are on the <a href="/gta-6/">GTA 6 hub</a>.'
        ),
        "path_aria": "Diagram. PS5 sends real frames at 30. Remote Play carries a 1080p stream. Windows draws extra frames. The monitor shows 60.",
        "path_nodes": [
            ("PS5", "Real frames, target 30"),
            ("Remote Play", "1080p stream"),
            ("Windows PC", "Extra frames drawn here"),
            ("PC monitor", "Can show 60 pictures"),
        ],
        "path_cap": "Diagram only, not a screenshot. The console does not start rendering at 60.",
        "df_line": "That 30 FPS target, and the missing 60 mode, is %s measurement. Tested and Experimental are SmoovPlay's own labels." % A(DF, "Digital Foundry's"),
        "yes_h": "This can help",
        "yes": [
            "Windows 10 or 11, and an NVIDIA RTX 30, 40, or 50 card. That range is marked Tested.",
            "You play on the PC monitor, with the controller paired to the PC.",
            "You can live with extra delay.",
        ],
        "no_h": "This will not help",
        "no": [
            "You only have a PS5 and a TV.",
            "You want the game itself to run at 60.",
            "You expected AMD, Intel, Xbox, or a capture card. Those are Experimental.",
        ],
        "need_h": "What you need",
        "need_id": "need",
        "need_lead": "Labels below are the project's own, from the %s." % readme,
        "need": [
            ("PC", "Windows 10 or 11, 64-bit."),
            ("Graphics", "NVIDIA RTX 30, 40, or 50 — Tested. AMD and Intel — Experimental."),
            ("Console", "A PS5 with Remote Play on — Tested. An Xbox app or a capture card — Experimental."),
            ("Network", "Ethernet, or 5 GHz or 6 GHz Wi-Fi."),
            ("Screen", "60 Hz or faster. You watch this monitor, not the TV on the PS5."),
        ],
        "setup_h": "Set it up",
        "steps": [
            ("Turn on Remote Play",
             "On the PS5, open <b>Settings → System → Remote Play</b> and turn on <b>Enable Remote Play</b>. Keep the PS5 and the PC on the same home network."),
            ("Download the installer",
             "On the PC, download <b>SmoovPlay-Setup.exe</b> from the official %s only." % rel),
            ("Install it",
             "Run that file and wait until setup finishes. The project says this takes about 10 to 20 minutes."),
            ("Connect the PS5",
             "In the app, follow <b>Connect your PS5</b>, sign in to PSN there, and register the console. chiaki-ng only carries the Remote Play stream; if it asks for a code, the PS5 shows one at <b>Remote Play → Link Device</b>.",
             shot(
                 "/assets/gta-6/smoov-connect.webp", 800, 688,
                 "SmoovPlay illustration: Connect your PS5, with Remote Play, optional wake from rest, and PSN sign-in in chiaki-ng.",
                 "From the %s (v0.3.8, MIT): their drawing of <b>Connect your PS5</b>. Wake-from-rest is optional; the menu names are on %s. Not a photo from our PC, not a v0.3.12 screenshot, and not GTA 6 on a console."
                 % (readme, A(CK_CONF, "chiaki-ng's configuration page")),
             )),
            ("Pair the controller",
             "Connect the controller to the PC. Play looking at the PC monitor."),
            ("Press Play, then pick 60",
             "Press <b>Play</b>. Press <b>M</b> and set the frame rate to <b>60</b> on a 60 Hz screen.",
             shot(
                 "/assets/gta-6/smoov-framerate.webp", 800, 666,
                 "SmoovPlay illustration: Frame rate set to 60 fps, with Auto-detect.",
                 "From the same v0.3.8 README: <b>Frame rate</b> on 60 fps, beside <b>Auto-detect</b>. An illustration of the control, not our screenshot and not a v0.3.12 screenshot.",
             )),
        ],
        "keys_h": "Keys",
        "keys_lead": "The controller plays the game. These keys run SmoovPlay, from the README.",
        "keys": [
            ("M", "Settings while you play, including the frame rate."),
            ("F", "Fullscreen on the monitor the window is already on. v0.3.12 changed this; older builds filled the main monitor."),
            ("I", "Extra frames off and on."),
            ("Esc or Q", "Stop."),
        ],
        "feel_h": "Will it feel like 60?",
        "feel": [
            "The extra frames are drawn on the PC after the stream arrives. The console does not start rendering at 60.",
            "The game stays at its native 30, so the controls do not become a 60 FPS game. The stream and the extra frames add delay.",
            "HUD text, fast camera turns, and thin objects that cross can wobble. The picture arrives at 1080p, a little softer than HDMI from the console.",
            "The GTA pictures on %s are Rockstar's trailer, An Extended Look, played as a simulated stream. Their live PS5 recording is Gotham Knights." % A(SP_COMPARE, "SmoovPlay's compare page"),
        ],
        "more": [
            ("More settings", [
                "Press <b>Auto-detect</b> on the Settings page if you change monitors. If a 30 FPS game looks uneven, set <b>Settings → Smoothness → Game frame rate</b> to <b>30 fps</b>. In v0.3.12, Auto motion detail picks Half when Full cannot hold the frame rate you chose. The release notes name an RTX 2080 Ti as a card that does not keep Full even at 60. That note is not a new Tested hardware list. On an existing install, run Auto-detect once.",
                "On a faster screen the project also lists 90, and up to 120. It says no live 120 measurement is published.",
                "While SmoovPlay is open, leave NVIDIA Smooth Motion, AMD Fluid Motion Frames, and Lossless Scaling off.",
            ]),
            ("Check the download", [
                "The release used for these steps is v0.3.12, published 21 November 2026 at 19:42 UTC. The drawings above stay the v0.3.8 README illustrations. The installer is still not code-signed. GitHub’s asset digest for SmoovPlay-Setup.exe is sha256 7939d7a5c48ba227bf78a84268a0f1d1783a6d8a0b8af34f50d7586a6cd442aa. In PowerShell, <b>Get-FileHash</b> on the installer should match that digest.",
                "Leave Windows protection as it is. Do not type a PSN password into any site except the sign-in the app opens.",
            ]),
            ("If the picture hitches", [
                "Plug the PS5 and the PC into the router. Wi-Fi can bunch frames.",
                "If it still fails, press <b>Q</b>, then <b>Help → Copy diagnostics</b>, and send that to a SmoovPlay issue. Not to this site.",
            ]),
        ],
        "faq_h": "Questions",
        "faq": [
            ("Why is GTA 6 only 30 FPS on PS5?",
             "Digital Foundry measured a 30 FPS target on PS5 and PS5 Pro, and found no 40 or 60 mode. PS5 Pro holds that 30 more steadily. It is not a 60 mode."),
            ("Is GTA 6 locked to 30 FPS?",
             "On current consoles, yes. The same test found no 40 or 60 option on PS5, PS5 Pro, or Xbox Series X and Series S."),
            ("Will GTA 6 run at 60 FPS on PS5 Pro?",
             "Not as a mode in the game. PS5 Pro uses the same 30 FPS target. This guide's 60 is extra pictures on a PC, and the game stays at 30."),
            ("Has this been shown on a real PS5 copy of GTA 6?",
             "Not as a live recording of the game. SmoovPlay's GTA VI clips are Rockstar's trailer, An Extended Look, played as a simulated stream. The live PS5 recording they show is Gotham Knights."),
            ("I only have a PS5 and a TV. Does this help?",
             "No. The extra frames are drawn on a Windows PC, and you watch them on that PC's monitor."),
        ],
        "src_h": "Sources",
        "src_lead": "The 30 FPS target is Digital Foundry's measurement. The setup and the Tested / Experimental labels are SmoovPlay's.",
        "sources": [
            A(DF, "Digital Foundry: GTA 6 on PS5, PS5 Pro, Xbox Series X and Series S") + " — 30 FPS target, no 40 or 60 mode.",
            A(SP_REL, "SmoovPlay Releases") + " — the only download. Own code is MIT. The Remote Play client it uses, chiaki-ng, is AGPL-3.0.",
            A(SP_README, "SmoovPlay README at v0.3.8") + " — the drawings on this page, hardware labels, Connect your PS5, Play, and the M key.",
            A(SP_REL, "SmoovPlay v0.3.12") + " — installer still unsigned; Auto may pick Half; F uses the window’s monitor. " + A(SP_README_NEW, "README at v0.3.12") + ".",
            A(SP_COMPARE, "SmoovPlay compare page") + " — GTA VI clips are a simulated trailer; the live PS5 clip is Gotham Knights.",
            A(CK_CONF, "chiaki-ng configuration") + " — Remote Play and Link Device menu names. chiaki-ng does not add frames.",
        ],
        "hub": "More GTA 6 tools are on the <a href=\"/gta-6/\">GTA 6 hub</a>.",
    }


def ru():
    rel = A(SP_REL, "Releases на GitHub")
    readme = A(SP_README, "README SmoovPlay")
    return {
        "title": "60 FPS в GTA 6 на PS5? Бесплатно, через компьютер — BuffForge",
        "desc": "На PS5 у GTA 6 родные 30 кадров и нет режима 60; бесплатная программа на Windows дорисовывает кадры Remote Play, если играть на мониторе ПК.",
        "h1": "60 FPS в GTA 6 на PS5? Бесплатно, через компьютер",
        "crumb": "60 FPS на PS5",
        "lede": (
            "В GTA 6 на PS5 и PS5 Pro цель — 30 кадров, режима 60 нет. "
            "Бесплатная SmoovPlay на компьютере с Windows дорисовывает кадры из Remote Play, и на мониторе ПК движение выглядит плавнее. "
            "Игра остаётся на 30. На живой копии с PS5 это ещё не показано."
        ),
        "safety": "Качайте SmoovPlay только со страницы %s. Установщик Windows — ранняя сборка без подписи." % rel,
        "jump": [("#need", "Что нужно"), ("#setup", "Как включить"), ("#feel", "Это как 60?"), ("#faq", "Вопросы")],
        "art_alt": "Официальный постер Grand Theft Auto VI: коллаж персонажей, техники и логотипа VI.",
        "art_cap": "Официальный постер. © Rockstar Games. Это не кадр из игры и не замер частоты.",
        "who_h": "Только телевизор или компьютер?",
        "bridge": (
            'PS5 игру запускает. Полный список приставок — на <a href="/ru/gta-6/compatibility/">проверке совместимости</a>. '
            'Остальные инструменты — на <a href="/ru/gta-6/">хабе GTA 6</a>.'
        ),
        "path_aria": "Схема. PS5 отдаёт настоящие кадры с целью 30. Remote Play несёт поток 1080p. Windows дорисовывает кадры. Монитор может показать 60.",
        "path_nodes": [
            ("PS5", "Настоящие кадры, цель 30"),
            ("Remote Play", "Поток 1080p"),
            ("Windows", "Здесь дорисовывают кадры"),
            ("Монитор ПК", "Может показать 60"),
        ],
        "path_cap": "Только схема, не скриншот. Приставка не начинает рисовать в 60.",
        "df_line": "Цель в 30 кадров и отсутствие режима 60 — это замер %s. Пометки Tested и Experimental — слова SmoovPlay." % A(DF, "Digital Foundry"),
        "yes_h": "Подойдёт",
        "yes": [
            "Windows 10 или 11 и карта NVIDIA RTX 30, 40 или 50. Этот ряд помечен Tested.",
            "Играете на мониторе этого ПК, геймпад подключён к компьютеру.",
            "Готовы к дополнительной задержке.",
        ],
        "no_h": "Не подойдёт",
        "no": [
            "Есть только PS5 и телевизор.",
            "Нужно, чтобы сама игра шла в 60.",
            "Расчёт на AMD, Intel, Xbox или карту захвата. У проекта это Experimental.",
        ],
        "need_h": "Что нужно",
        "need_lead": "Пометки ниже — собственные, из %s." % readme,
        "need": [
            ("Компьютер", "Windows 10 или 11, 64 бита."),
            ("Видеокарта", "NVIDIA RTX 30, 40 или 50 — Tested. AMD и Intel — Experimental."),
            ("Приставка", "PS5 с включённой удалённой игрой — Tested. Приложение Xbox или карта захвата — Experimental."),
            ("Сеть", "Кабель либо Wi-Fi 5 или 6 ГГц."),
            ("Экран", "60 Гц или быстрее. Смотрите в этот монитор, не в телевизор на PS5."),
        ],
        "setup_h": "Как включить",
        "steps": [
            ("Включите Remote Play",
             "На PS5 откройте <b>Settings → System → Remote Play</b> и включите <b>Enable Remote Play</b>. PS5 и компьютер должны быть в одной домашней сети."),
            ("Скачайте установщик",
             "На компьютере скачайте <b>SmoovPlay-Setup.exe</b> только с официальной страницы %s." % rel),
            ("Установите",
             "Запустите файл и дождитесь конца установки. По словам проекта, это около 10–20 минут."),
            ("Подключите PS5",
             "В программе пройдите <b>Connect your PS5</b>, войдите в PSN там и зарегистрируйте приставку. chiaki-ng только несёт поток Remote Play; если просит код, он на PS5 в <b>Remote Play → Link Device</b>.",
             shot(
                 "/assets/gta-6/smoov-connect.webp", 800, 688,
                 "Рисунок SmoovPlay: экран Connect your PS5 — Remote Play, необязательное пробуждение и вход в PSN через chiaki-ng.",
                 "Из %s (v0.3.8, MIT): их рисунок экрана <b>Connect your PS5</b>. Пробуждение из покоя необязательно; названия пунктов — на %s. Это не фото с нашего компьютера, не скриншот v0.3.12 и не GTA 6 на приставке."
                 % (readme, A(CK_CONF, "странице настройки chiaki-ng")),
             )),
            ("Подключите геймпад",
             "Соедините геймпад с компьютером. Смотрите в монитор ПК."),
            ("Нажмите Play и выберите 60",
             "Нажмите <b>Play</b>. Клавишей <b>M</b> поставьте частоту <b>60</b> на экране 60 Гц.",
             shot(
                 "/assets/gta-6/smoov-framerate.webp", 800, 666,
                 "Рисунок SmoovPlay: частота кадров стоит на 60 fps, рядом кнопка Auto-detect.",
                 "Из того же README v0.3.8: <b>Frame rate</b> на 60 fps и кнопка <b>Auto-detect</b>. Рисунок органа управления, не наш скриншот и не скриншот v0.3.12.",
             )),
        ],
        "keys_h": "Клавиши",
        "keys_lead": "Геймпад играет. Эти клавиши управляют SmoovPlay, как в README.",
        "keys": [
            ("M", "Настройки во время игры, в том числе частота кадров."),
            ("F", "Полный экран на том мониторе, где уже стоит окно. Так с v0.3.12; раньше заполнялся главный монитор."),
            ("I", "Лишние кадры выкл и вкл."),
            ("Esc или Q", "Стоп."),
        ],
        "feel_h": "Это будет как 60?",
        "feel": [
            "Лишние кадры рисуются на компьютере, уже после потока. Приставка не начинает рисовать в 60.",
            "Игра остаётся на родных 30, поэтому управление не становится игрой в 60. Поток и лишние кадры добавляют задержку.",
            "Текст интерфейса, резкий поворот камеры и тонкие пересекающиеся предметы могут дрожать. Картинка приходит в 1080p, чуть мягче, чем HDMI с приставки.",
            "Картинки GTA на %s — трейлер Rockstar An Extended Look, прогнанный как имитация потока. Живая запись с PS5 у них — Gotham Knights." % A(SP_COMPARE, "странице сравнения SmoovPlay"),
        ],
        "more": [
            ("Ещё настройки", [
                "Если сменили монитор, нажмите <b>Auto-detect</b> на странице Settings. Если игра на 30 выглядит рвано, поставьте <b>Settings → Smoothness → Game frame rate</b> в <b>30 fps</b>. В v0.3.12 Auto motion detail выбирает Half, если Full не держит выбранную частоту. В заметках релиза RTX 2080 Ti названа картой, которая не держит Full даже на 60. Это не новый список Tested. На уже установленной копии один раз нажмите Auto-detect.",
                "На более быстром экране проект также указывает 90 и до 120. Живой замер 120 он не публиковал.",
                "Пока открыта SmoovPlay, NVIDIA Smooth Motion, AMD Fluid Motion Frames и Lossless Scaling должны быть выключены.",
            ]),
            ("Проверить файл", [
                "Шаги сверены с релизом v0.3.12, опубликованным 21 ноября 2026 года в 19:42 UTC. Рисунки выше остаются иллюстрациями README v0.3.8. Установщик по-прежнему без подписи. Дайджест файла SmoovPlay-Setup.exe на GitHub: sha256 7939d7a5c48ba227bf78a84268a0f1d1783a6d8a0b8af34f50d7586a6cd442aa. В PowerShell <b>Get-FileHash</b> по установщику должен совпасть с этим дайджестом.",
                "Защиту Windows не отключайте. Пароль PSN вводите только на странице входа, которую открывает программа.",
            ]),
            ("Если картинка дёргается", [
                "Воткните PS5 и компьютер в роутер. По Wi-Fi кадры могут приходить пачками.",
                "Если всё равно не выходит, нажмите <b>Q</b>, затем <b>Help → Copy diagnostics</b> и отправьте это в issue SmoovPlay. Не на этот сайт.",
            ]),
        ],
        "faq_h": "Вопросы",
        "faq": [
            ("Почему в GTA 6 на PS5 только 30 кадров?",
             "Digital Foundry замерили цель 30 кадров на PS5 и PS5 Pro и не нашли режима 40 или 60. На PS5 Pro эти 30 ровнее. Это не режим 60."),
            ("GTA 6 заперта на 30 кадрах?",
             "На нынешних приставках — да. Тот же замер не нашёл 40 или 60 на PS5, PS5 Pro, Xbox Series X и Series S."),
            ("Будет ли 60 FPS на PS5 Pro?",
             "Как режим в игре — нет. У PS5 Pro та же цель в 30 кадров. 60 в этом гайде — лишние картинки на компьютере, игра остаётся на 30."),
            ("Это показывали на настоящей GTA 6 с PS5?",
             "Живой записи игры нет. Ролики GTA VI у SmoovPlay — трейлер Rockstar An Extended Look, прогнанный как имитация потока. Живая запись с PS5 у них — Gotham Knights."),
            ("У меня только PS5 и телевизор. Это поможет?",
             "Нет. Лишние кадры рисуются на компьютере с Windows, и смотреть их нужно на мониторе этого компьютера."),
        ],
        "src_h": "Источники",
        "src_lead": "Цель в 30 кадров — замер Digital Foundry. Установка и пометки Tested / Experimental — слова SmoovPlay.",
        "sources": [
            A(DF, "Digital Foundry: GTA 6 на PS5, PS5 Pro, Xbox Series X и Series S") + " — цель 30 кадров, режима 40 или 60 нет.",
            A(SP_REL, "Релизы SmoovPlay") + " — единственная загрузка. Свой код — MIT. Клиент Remote Play, которым она пользуется, chiaki-ng, — AGPL-3.0.",
            A(SP_README, "README SmoovPlay, тег v0.3.8") + " — рисунки на этой странице, пометки железа, Connect your PS5, Play и клавиша M.",
            A(SP_REL, "SmoovPlay v0.3.12") + " — установщик без подписи; Auto может выбрать Half; F берёт монитор окна. " + A(SP_README_NEW, "README на теге v0.3.12") + ".",
            A(SP_COMPARE, "Страница сравнения SmoovPlay") + " — ролики GTA VI это имитация трейлера; живой ролик с PS5 — Gotham Knights.",
            A(CK_CONF, "Настройка chiaki-ng") + " — названия пунктов Remote Play и Link Device. Кадры chiaki-ng не добавляет.",
        ],
        "hub": "Другие инструменты по GTA 6 — на <a href=\"/ru/gta-6/\">хабе GTA 6</a>.",
    }


def guide_body(lang):
    c = en() if lang == "en" else ru()
    hub = "/gta-6/" if lang == "en" else "/ru/gta-6/"
    parts = [
        '<main id="main" class="wrap narrow">',
        crumbs_html(lang, [("GTA 6", hub), (c["crumb"], None)]),
        '<h1 class="page-h1">%s</h1>' % c["h1"],
        '<p class="page-lede">%s</p>' % c["lede"],
        '<p class="intro-note">%s</p>' % c["safety"],
        '<nav class="guide-jump" aria-label="%s">%s</nav>' % (
            "On this page" if lang == "en" else "На этой странице",
            "".join('<a href="%s">%s</a>' % pair for pair in c["jump"]),
        ),
        '<div class="prose">',
        '<h2 class="sec" id="who">%s</h2>' % c["who_h"],
        _pair(c["yes_h"], _ul(c["yes"]), c["no_h"], _ul(c["no"])),
        (
            '<figure class="shot"><img src="/assets/games/gta-6-wide.jpg" width="1200" height="630" '
            'alt="%s" loading="lazy" decoding="async"><figcaption>%s</figcaption></figure>'
        ) % (c["art_alt"], c["art_cap"]),
        "<p>%s</p>" % c["bridge"],
        "<p>%s</p>" % c["df_line"],
        path_svg(c["path_aria"], c["path_nodes"]),
        "<p>%s</p>" % c["path_cap"],
        '<h2 class="sec" id="need">%s</h2>' % c["need_h"],
        "<p>%s</p>" % c["need_lead"],
        _table(c["need"]),
        '<h2 class="sec" id="setup">%s</h2>' % c["setup_h"],
        _steps(c["steps"]),
        '<h2 class="sec" id="keys">%s</h2>' % c["keys_h"],
        "<p>%s</p>" % c["keys_lead"],
        _table(c["keys"]),
        '<h2 class="sec" id="feel">%s</h2>' % c["feel_h"],
    ]
    parts.extend("<p>%s</p>" % p for p in c["feel"])
    parts.extend(_more(title, paras) for title, paras in c["more"])
    parts += [
        '<section class="faq" id="faq"><h2 class="sec">%s</h2>%s</section>'
        % (c["faq_h"], _faq(c["faq"])),
        '<h2 class="sec" id="sources">%s</h2>' % c["src_h"],
        "<p>%s</p>" % c["src_lead"],
        _ul(c["sources"]),
        "<p>%s</p>" % c["hub"],
        "</div>",
        "</main>",
    ]
    return "\n".join(parts), c


def guide_page(lang):
    body, c = guide_body(lang)
    canon = "/gta-6/%s/" % SLUG if lang == "en" else "/ru/gta-6/%s/" % SLUG
    alt = {"en": "/gta-6/%s/" % SLUG, "ru": "/ru/gta-6/%s/" % SLUG}
    hub = "/gta-6/" if lang == "en" else "/ru/gta-6/"
    home = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    jl = [
        breadcrumb_jsonld(lang, [
            (home, home_path),
            ("GTA 6", hub),
            (c["crumb"], canon),
        ]),
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": c["h1"],
            "description": c["desc"],
            "inLanguage": lang,
            "datePublished": "2026-11-19",
            "dateModified": "2026-11-22",
            "author": {"@type": "Organization", "name": "BuffForge", "url": BASE},
            "publisher": {"@type": "Organization", "name": "BuffForge", "url": BASE},
            "mainEntityOfPage": {"@type": "WebPage", "@id": BASE + canon},
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in c["faq"]
            ],
        },
    ]
    return page(
        lang, c["title"], c["desc"], canon, alt, body,
        jsonld=jl, switch_path=alt["ru" if lang == "en" else "en"],
        games=("gta-6",),
    )
