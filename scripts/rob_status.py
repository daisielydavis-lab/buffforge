#!/usr/bin/env python3
"""ROB RUN server-status pages. Static, and honest about that.

Reviewed 15 Nov 2026 against public official text. This module does not
fetch anything at build time and does not invent a live feed.

What the sources actually show:
- Steam news gid 717921532895036325, posttime 1794690004
  (14 Nov 2026, 21:00:04 UTC), updatetime 1794694755
  (14 Nov 2026, 22:19:15 UTC). English body: Kefir is aware of login
  issues and instability on EU servers; US servers are not affected;
  "UPD (23:20 CET): The servers will be restarted shortly."
  Russian body of the same post omits that UPD line. Neither language
  says the restart finished or that login works again.
- Steam news gid 717921532895036113 (13 Nov 2026, 13:17:13 UTC): server
  instability and DDoS among issues they were working on; switching
  servers means surrendering and returning to prison; Asia or Oceania
  will not be possible until at least the end of the year.
- Steam news gid 712291399099220569 (4 Nov 2026): two regions, EU and
  East US; at least one fresh server a day at 5 PM UTC and 8 PM ET,
  plus extras. A schedule is not a status reading.
- Kefir Help Center error-code article and the communities article.
  The two articles publish different support emails. No status page
  is listed.

Not used as region health: Steam player counts, whether a website
loads, browser timing to a third party, local questionnaires.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import BASE, breadcrumb_jsonld, crumbs_html, page  # noqa: E402

NEWS_EU = "https://store.steampowered.com/news/app/4262460/view/717921532895036325"
NEWS_FAQ = "https://store.steampowered.com/news/app/4262460/view/717921532895036113"
NEWS_SCHED = "https://store.steampowered.com/news/app/4262460/view/712291399099220569"
NEWS_HUB = "https://store.steampowered.com/news/app/4262460"
STORE = "https://store.steampowered.com/app/4262460/ROB_RUN/"
HC_ERR = {
    "en": "https://kefirgames.helpshift.com/hc/en/14-rob-run/faq/1377-what-should-i-do-if-i-get-an-error-code/?l=en",
    "ru": "https://kefirgames.helpshift.com/hc/ru/14-rob-run/faq/1377-what-should-i-do-if-i-get-an-error-code/?l=ru",
}
HC_COMM = {
    "en": "https://kefirgames.helpshift.com/hc/en/14-rob-run/faq/1381-how-do-i-contact-support-and-find-official-communities/?l=en",
    "ru": "https://kefirgames.helpshift.com/hc/ru/14-rob-run/faq/1381-how-do-i-contact-support-and-find-official-communities/?l=ru",
}
HC_SERVER = {
    "en": "https://kefirgames.helpshift.com/hc/en/14-rob-run/faq/1382-how-to-invite-a-friend-to-a-party-if-it-says-they-are-on-another-server/?l=en",
    "ru": "https://kefirgames.helpshift.com/hc/ru/14-rob-run/faq/1382-how-to-invite-a-friend-to-a-party-if-it-says-they-are-on-another-server/?l=ru",
}
CHANNELS = [
    ("Discord", "https://discord.gg/robrun"),
    ("X", "https://x.com/ROBRUNGame"),
    ("Steam", STORE),
    ("Facebook", "https://www.facebook.com/robrungame"),
    ("Instagram", "https://www.instagram.com/robrungame"),
    ("VK", "https://vk.ru/robrungame"),
    ("Telegram", "https://t.me/robrungame"),
]

# kind "link": Kefir describes a failed connection. That is not proof a
# region is down. kind "local": Kefir's written fix is on the PC,
# account, files, or input devices. Still not a region measurement.
CODES = [
    ("E-0101 / E-0110", "link",
     {"en": "The game cannot connect to the server to download configuration or startup data.",
      "ru": "Игра не может связаться с сервером для загрузки настроек или стартовых данных."},
     {"en": "Check your internet connection and make sure websites load correctly.",
      "ru": "Проверьте интернет-соединение и убедитесь, что сайты открываются корректно."}),
    ("E-0102", "local",
     {"en": "Data downloaded with errors or was blocked on its way to your PC. Kefir says this often happens on guest networks (hotels, cafes, public Wi-Fi) or because of antivirus or firewall interference.",
      "ru": "Данные загрузились с ошибкой или заблокированы на пути к компьютеру. Kefir пишет, что так часто бывает в гостевых сетях (отели, кафе, общественный Wi-Fi) или из-за сетевого фильтра антивируса."},
     {"en": "Switch to a home network without an authorization page, disable proxy, or temporarily pause HTTPS scanning in your antivirus settings.",
      "ru": "Переключитесь на домашнюю сеть без страницы авторизации, отключите прокси или временно приостановите HTTPS-сканирование в настройках антивируса."}),
    ("E-0124", "local",
     {"en": "An internal game asset loading system error.",
      "ru": "Сбой встроенной системы загрузки игровых ресурсов."},
     {"en": "Verify the integrity of game files via Properties in Steam.",
      "ru": "Проверьте целостность файлов игры через свойства в Steam."}),
    ("E-0201", "link",
     {"en": "The game was already running, but the connection to the game server was lost and was not restored.",
      "ru": "Игра уже работала, связь с игровым сервером пропала и не восстановилась."},
     {"en": "Check your connection and restart the game.",
      "ru": "Проверьте стабильность соединения и перезапустите игру."}),
    ("E-0301 / E-0302", "local",
     {"en": "An outdated version of the game.",
      "ru": "Установлена устаревшая версия игры."},
     {"en": "Close the game, restart Steam, and update the game.",
      "ru": "Полностью закройте игру, перезапустите клиент Steam и обновите игру."}),
    ("E-0303 / E-0304", "local",
     {"en": "Game data was downloaded corrupted or does not match the current game version.",
      "ru": "Игровые данные скачались повреждёнными либо не соответствуют текущей версии игры."},
     {"en": "Wait 10–15 minutes, disable proxy, verify the integrity of game files via Properties in Steam, and update the game.",
      "ru": "Подождите 10–15 минут, отключите прокси, выполните проверку целостности файлов через свойства игры в Steam и обновите игру."}),
    ("E-0401", "local",
     {"en": "Failed to authenticate the Steam account.",
      "ru": "Не удалось подтвердить учётную запись Steam."},
     {"en": "Make sure Steam is running in online mode and you are logged into the correct account. Restart Steam and the game.",
      "ru": "Убедитесь, что Steam запущен в режиме онлайн и вход выполнен в нужный аккаунт. Перезапустите Steam и игру."}),
    ("E-0403 / E-0404", "local",
     {"en": "Authorization issues (Epic Online Services).",
      "ru": "Неполадки при авторизации (Epic Online Services)."},
     {"en": "Verify the integrity of files via Steam, add the game to your antivirus exceptions, and restart your PC.",
      "ru": "Проверьте целостность файлов через Steam, добавьте игру в исключения антивируса и перезапустите ПК."}),
    ("E-0405", "local",
     {"en": "Steam is not responding, or an antivirus blocked the game’s system library.",
      "ru": "Клиент Steam не отвечает, либо антивирус заблокировал служебную библиотеку игры."},
     {"en": "Check your antivirus quarantine, launch Steam, and verify the integrity of game files. Launch the game directly from your Steam library.",
      "ru": "Проверьте карантин антивируса, запустите Steam и выполните проверку целостности файлов игры. Запустите игру строго из библиотеки Steam."}),
    ("E-0501 / E-0502", "local",
     {"en": "Easy Anti-Cheat is not running, corrupted, or blocked by third-party software.",
      "ru": "Служба Easy Anti-Cheat не запущена, повреждена или заблокирована сторонним ПО."},
     {"en": "Launch the game exclusively through Steam, stop your antivirus, verify file integrity via Properties in Steam, and restart your PC.",
      "ru": "Запускайте игру исключительно через Steam, остановите работу антивируса, проверьте целостность файлов через свойства игры в Steam и перезапустите ПК."}),
    ("E-0601", "local",
     {"en": "Basic input devices (keyboard and mouse) were not detected. Kefir says this often happens over Remote Desktop or cloud streaming.",
      "ru": "Не обнаружены базовые устройства ввода (клавиатура и мышь). Kefir пишет, что сбой часто возникает при игре через удалённый рабочий стол или облачный стриминг."},
     {"en": "Connect a physical keyboard and mouse directly to the PC before launching the game and avoid remote access sessions.",
      "ru": "Подключите физическую клавиатуру и мышь напрямую к ПК до запуска игры и избегайте сессий через удалённый доступ."}),
    ("E-0904", "local",
     {"en": "An unexpected internal in-game error.",
      "ru": "Непредвиденный внутренний сбой в игре."},
     {"en": "Restart the game. If the error persists, copy the text from the error window and send it to support (robrun.support@kefirgames.com).",
      "ru": "Перезапустите игру. Если ошибка повторяется, скопируйте текст из окна ошибки и отправьте его в техподдержку (robrun.support@kefirgames.com)."}),
]

PATHS = {"en": "/rob-run/server-status/", "ru": "/ru/rob-run/server-ne-rabotaet/"}

COPY = {
    "en": {
        "title": "ROB RUN official Steam server news — BuffForge",
        "desc": "Official Steam community announcements for ROB RUN, requested when you open the page. Not a live check of the EU or East US game servers.",
        "h1": "ROB RUN server news",
        "crumb": "Server news",
        "lede": "This page requests Kefir’s official Steam announcements. It does not measure whether the EU or East US game servers are up.",
        "reviewed": "The list below is requested from Steam. A separate note further down was read by hand on 15 Nov 2026.",
        "limit_h": "Steam announcements, not a server probe",
        "limit_p": "Each card is one Steam community announcement, with the time Steam published it. The words in a post are not a green or red light. A quiet feed is not an all-clear. X, Discord, Telegram, and VK are not included.",
        "regions_h": "Regions",
        "regions_p": "On 4 Nov 2026 Kefir wrote that two regions were available, EU and East US, and that more would be added when they can. The same note plans at least one fresh server a day — EU at 5 PM UTC, East US at 8 PM ET — plus extra servers outside those times. A planned opening is not a status reading.",
        "eu_name": "Europe (EU)",
        "us_name": "East US",
        "unknown": "Unknown",
        "metrics": "Login availability: not measured. Latency: not measured from this page. Maintenance: no live feed.",
        "eu_ann": "Latest official announcement we reviewed, not a current reading. Steam, 14 Nov 2026, 21:00:04 UTC: Kefir wrote that they were aware of login issues and instability on the EU servers. The English text adds a line labeled “UPD (23:20 CET)”: “The servers will be restarted shortly.” Steam’s update time on that post is 14 Nov 2026, 22:19:15 UTC. The Russian text of the same post does not include that line. Neither language says the restart finished or that login works again.",
        "us_ann": "The same announcement said “US servers are not affected.” That sentence describes that post, not East US right now. This page has no later all-clear and no live reading, so East US stays unknown too.",
        "open_ann": "Open the 14 Nov 2026 announcement",
        "where_h": "Where Kefir posts news",
        "where_p": "The help article lists these communities. This page does not read them, and none of the links is a live status board.",
        "mail_p": "The support address is not the same on every help page. The error-code article says robrun.support@kefirgames.com. The communities article says robrun.support@kefircyprus.com. Use the address on the article you are writing from.",
        "switch_h": "Changing server",
        "switch_p": "On 13 Nov 2026 Kefir wrote that switching servers still means surrendering and going back to prison, and that they plan to make the choice simpler. The same FAQ says servers in other regions, such as Asia or Oceania, will not be possible until at least the end of this year. Kefir’s help article describes the prison step. This page does not repeat it.",
        "switch_a": "Kefir’s help article on changing server",
        "faq_link": "13 Nov 2026 FAQ",
        "sched_link": "4 Nov 2026 server note",
        "feed_h": "Official Steam announcements",
        "feed_p": "Opening this page, pressing refresh, and a visible tab about every 90 seconds each ask BuffForge. BuffForge reuses a successful Steam response for about a minute. That is a page request, not a monitor running all day. “Steam fetch” is when that response was retrieved. “Shown” is when this browser received it.",
        "refresh_btn": "Refresh announcements",
        "hand_h": "Hand-checked copy from 15 Nov 2026",
        "hand_p": "This note is not the live list. It is the EU post as read on 15 Nov 2026, so the page still cites it if the request fails.",
        "match_h": "Match a symptom to Kefir’s help text",
        "match_p": "Your answers pick a paragraph Kefir already published. They do not test a region. The result will not say the servers are up, and it will not declare an outage.",
        "region_label": "Region you play on",
        "sym_label": "What is happening",
        "code_label": "Error code, if the game shows one",
        "scope_label": "Who else is affected",
        "opt_login": "I can’t get in",
        "opt_disconnect": "I was playing, then the game dropped",
        "opt_ping": "High ping or rubber-banding",
        "opt_other": "Something else",
        "opt_nocode": "No code shown",
        "opt_only": "Only me, as far as I know",
        "opt_others": "Other people on this server too",
        "opt_unsure": "I’m not sure",
        "reg_eu": "EU",
        "reg_us": "East US",
        "reg_unk": "I don’t know",
        "diag_btn": "Show the matching help text",
        "copy_btn": "Copy this guidance",
        "codes_h": "Error codes from Kefir",
        "codes_p": "Wording below follows Kefir’s help article, reviewed 15 Nov 2026. The article’s own “last updated” label is a relative time, so this page does not turn it into a calendar date.",
        "col_means": "What Kefir says",
        "col_fix": "Kefir’s fix",
        "wont_h": "What this page does not do",
        "wont": [
            "It does not read Steam’s player count. A global number is not EU or East US health.",
            "It does not treat “this site loaded” or “Steam’s website loaded” as the game being up.",
            "It does not store reports or add them up across visitors. A questionnaire is not detection.",
            "It does not open private game addresses or pick a host to probe.",
            "It does not sell a route optimizer or list a price. A route optimizer only changes the path to official servers. It cannot repair a server that is not answering. High ping is not measured here.",
        ],
        "ping_h": "High ping is a different question",
        "ping_p": "If you are in the game and the delay is high, that is not something this page can time. The checks above are for login and error codes. A product that only changes your route still needs the official server to answer.",
        "noscript": "JavaScript is off, so the Steam list does not load. The hand-checked note, the error-code table, and the official links still apply. The symptom matcher does not run.",
        "related_h": "Other ROB RUN pages",
        "rel": [
            ("/rob-run/federal-raid-countdown/", "Federal Raid countdown", "Seven days from the opening you enter."),
            ("/rob-run/loot-profit-calculator/", "Loot profit calculator", "You type every cash amount."),
            ("/rob-run/squad-loot-splitter/", "Squad loot splitter", "Equal split, or your own weights."),
        ],
        "src_h": "Sources",
    },
    "ru": {
        "title": "ROB RUN не работает: официальные новости Steam — BuffForge",
        "desc": "Официальные объявления Steam о ROB RUN. Страница запрашивает их при открытии. Это не проверка, работают ли серверы EU и East US.",
        "h1": "ROB RUN не работает: новости серверов",
        "crumb": "Сервер не работает",
        "lede": "Здесь запрос официальных объявлений Kefir в Steam. Страница не измеряет, отвечают ли игровые серверы EU и East US.",
        "reviewed": "Список ниже запрашивается у Steam. Отдельная заметка дальше сверена вручную 15 ноября 2026 года.",
        "limit_h": "Объявления Steam, не проверка серверов",
        "limit_p": "Каждая карточка — одно объявление сообщества Steam и время его публикации. Текст поста — не зелёный и не красный сигнал. Молчание ленты не значит, что всё починили. X, Discord, Telegram и VK сюда не входят.",
        "regions_h": "Регионы",
        "regions_p": "4 ноября 2026 года Kefir написал: «Сейчас в ROB RUN доступны два региона: EU и East US». Другие обещали добавлять по мере возможности. В той же заметке — минимум один свежий сервер в день: EU в 17:00 UTC, East US в 20:00 ET, плюс дополнительные серверы вне этого времени. Расписание открытия — не замер статуса.",
        "eu_name": "Европа (EU)",
        "us_name": "East US",
        "unknown": "Неизвестно",
        "metrics": "Вход: не измерен. Задержка: с этой страницы не измеряется. Обслуживание: живой ленты нет.",
        "eu_ann": "Последнее официальное объявление, которое мы сверили. Это не замер текущего момента. Steam, 14 ноября 2026 года, 21:00:04 UTC. Русский текст: «Нам известно о проблемах со входом и нестабильной работе EU-серверов. Наша команда уже занимается этим. US-серверы не затронуты. Приносим извинения за неудобства. Мы сообщим, как только проблемы будут решены.» В английской версии той же записи есть строка «UPD (23:20 CET)»: серверы скоро перезапустят. Время обновления записи в Steam — 14 ноября 2026 года, 22:19:15 UTC. В русском тексте этой строки нет. Ни английский, ни русский текст не говорит, что перезапуск закончился или что вход снова работает.",
        "us_ann": "Та же запись говорит, что US-серверы не затронуты. Фраза относится к тому посту, а не к East US прямо сейчас. Более позднего «всё снова работает» мы не видели, живого замера нет, поэтому East US тоже неизвестен.",
        "open_ann": "Открыть объявление от 14 ноября 2026 года",
        "where_h": "Где Kefir пишет новости",
        "where_p": "Справка перечисляет эти сообщества. Страница их не читает, и ни одна ссылка не является живым табло статуса.",
        "mail_p": "Адрес поддержки в статьях разный. В статье про коды ошибок указан robrun.support@kefirgames.com. В статье про сообщества — robrun.support@kefircyprus.com. Пишите на адрес той статьи, с которой пишете.",
        "switch_h": "Смена сервера",
        "switch_p": "13 ноября 2026 года Kefir написал: чтобы сменить сервер, приходится сдаваться и возвращаться в тюрьму, и что выбор сервера планируют сделать проще. В том же FAQ: серверы в других регионах, например в Азии или Океании, как минимум до конца этого года невозможны. Шаги в тюрьме описаны в справке Kefir и, с картинками, в гайде про лаги. Здесь их нет.",
        "switch_a": "Справка Kefir: смена сервера",
        "faq_link": "FAQ от 13 ноября 2026 года",
        "sched_link": "Заметка о серверах от 4 ноября 2026 года",
        "feed_h": "Официальные объявления Steam",
        "feed_p": "Страница спрашивает BuffForge при открытии, по кнопке и примерно раз в полторы минуты, пока вкладка видна. Удачный ответ Steam переиспользуется около минуты. Это запрос со страницы, а не круглосуточный монитор. «Запрос к Steam» — когда этот ответ получили. «Показано» — когда его увидел этот браузер.",
        "refresh_btn": "Обновить объявления",
        "hand_h": "Копия, сверенная 15 ноября 2026 года",
        "hand_p": "Это не живой список. Так выглядел пост про EU, когда его читали 15 ноября 2026 года. Он остаётся на странице, если запрос не удастся.",
        "match_h": "Сопоставить симптом со справкой Kefir",
        "match_p": "Ответы выбирают уже опубликованный абзац Kefir. Регион они не тестируют. Результат не скажет, что серверы работают, и не объявит сбой.",
        "region_label": "Регион, на котором вы играете",
        "sym_label": "Что происходит",
        "code_label": "Код ошибки, если игра его показывает",
        "scope_label": "Кого ещё это касается",
        "opt_login": "Не пускает в игру",
        "opt_disconnect": "Игра шла, потом связь пропала",
        "opt_ping": "Высокий пинг или «резинка»",
        "opt_other": "Что-то другое",
        "opt_nocode": "Кода нет",
        "opt_only": "Насколько я вижу, только у меня",
        "opt_others": "И у других на этом сервере",
        "opt_unsure": "Не уверен",
        "reg_eu": "EU",
        "reg_us": "East US",
        "reg_unk": "Не знаю",
        "diag_btn": "Показать текст из справки",
        "copy_btn": "Скопировать эту подсказку",
        "codes_h": "Коды ошибок Kefir",
        "codes_p": "Формулировки ниже следуют справке Kefir, сверено 15 ноября 2026 года. Пометка «обновлено» в самой статье — относительное время, поэтому в календарную дату мы её не переводим.",
        "col_means": "Что пишет Kefir",
        "col_fix": "Что сделать по справке",
        "wont_h": "Чего эта страница не делает",
        "wont": [
            "Не читает число игроков Steam. Общая цифра — это не здоровье EU или East US.",
            "Не считает «сайт открылся» или «открылся сайт Steam» признаком того, что игра работает.",
            "Не хранит жалобы и не суммирует их по посетителям. Анкета — не обнаружение сбоя.",
            "Не открывает закрытые адреса игры и не выбирает цель для пробы.",
            "Не продаёт ускоритель и не пишет цены. Ускоритель только меняет маршрут до официальных серверов. Сервер, который не отвечает, он не поднимет.",
        ],
        "ping_h": "Высокий пинг — другая страница",
        "ping_p": "Если вы уже в игре и задержка высокая, эта страница время не замерит. Выше — вход и коды ошибок. Что сделать с маршрутом до официальных серверов, без цен и без обещания починить молчащий сервер, — в гайде <a href=\"/ru/rob-run/kak-ubrat-lagi/\">лаги и высокий пинг</a>.",
        "noscript": "JavaScript выключен, поэтому список Steam не загружается. Ручная заметка, таблица кодов и официальные ссылки на месте. Подбор симптома не работает.",
        "related_h": "Ещё по ROB RUN",
        "rel": [
            ("/ru/rob-run/kak-ubrat-lagi/", "Лаги и высокий пинг", "Маршрут до EU, FPS и что сделать бесплатно. Не статус сервера."),
            ("/ru/rob-run/federal-raid-countdown/", "Отсчёт до Федеральной облавы", "Семь дней от открытия, которое вводите вы."),
            ("/ru/rob-run/loot-profit-calculator/", "Калькулятор добычи", "Каждую сумму вводите вы."),
            ("/ru/rob-run/squad-loot-splitter/", "Делёж добычи в отряде", "Поровну или со своим весом."),
        ],
        "src_h": "Источники",
    },
}

JS_COPY = {
    "en": {
        "locale": "en-US",
        "lagHref": "",
        "lagLabel": "",
        "loading": "Loading official Steam announcements…",
        "cardKicker": "Steam announcement",
        "published": "Published",
        "openPost": "Open this Steam post",
        "empty": "Steam returned no community announcements. That is an empty feed, not an all-clear.",
        "offline": "This browser reports no network. The list was not refreshed.",
        "timeout": "The request for Steam announcements timed out.",
        "malformed": "The announcement response was not usable. Nothing was filled in.",
        "upstream": "Steam’s news feed did not return a usable list.",
        "kept": "The cards below are the previous response, not a new reading.",
        "metaFresh": "{n} announcement(s). Steam fetch {fetched}. Shown {served}. Fresh for this page request.",
        "metaStale": "{n} announcement(s) from the last successful Steam fetch at {fetched}. Shown {served}. This copy is stale. It is not a current server reading.",
        "title": "Next checks, not a server verdict",
        "notATest": "This matches your answers to text Kefir already published. It is not a test of EU or East US.",
        "codeLead": "{code}. Kefir: {meaning} Kefir’s fix: {fix}",
        "ping": "High ping and rubber-banding are not measured here. A route optimizer only changes the path to official servers. It cannot repair a server that is not answering. This page does not name a product or a price.",
        "others": "You said other people are affected too. That can be the game service, and it can be a network you share. Your answer is not a measurement. Read Kefir’s announcement, linked above. This page will not mark the region down or up from it.",
        "onlyLocal": "Kefir’s help text for this code describes a fix on your PC, account, or files. That still does not say whether EU or East US is up.",
        "onlyLink": "Kefir tells you to check your connection and restart. The help text does not say this code proves a region is down. If it is only you, start there. Regional status on this page stays unknown.",
        "loginUnknown": "A failed login or a dropped session can be the game service or the path to it. This page cannot tell those apart, and it does not mark a region operational or down.",
        "unsure": "These answers are not enough to separate your PC from the game service. Status stays unknown.",
        "regionNote": {
            "eu": "EU: read the dated Steam posts above. A sentence in one of them is not EU health right now.",
            "us": "East US: a post can say US servers were unaffected at the time it was written. That is not East US right now.",
            "unknown": "You did not pick a region. The posts above are still announcements, not a health reading.",
        },
        "stamp": "Guidance assembled in this browser at {time}. That clock is not a server timestamp.",
        "copied": "Copied.",
        "copyFail": "Clipboard is not available in this browser.",
        "copyEmpty": "Show the help text first.",
    },
    "ru": {
        "locale": "ru-RU",
        "lagHref": "/ru/rob-run/kak-ubrat-lagi/",
        "lagLabel": "Гайд: лаги и высокий пинг",
        "loading": "Загружаем официальные объявления Steam…",
        "cardKicker": "Объявление Steam",
        "published": "Опубликовано",
        "openPost": "Открыть этот пост Steam",
        "empty": "Steam не вернул объявлений сообщества. Пустая лента — не отбой.",
        "offline": "Браузер сообщает, что сети нет. Список не обновлялся.",
        "timeout": "Запрос объявлений Steam не успел завершиться.",
        "malformed": "Ответ с объявлениями нельзя разобрать. Ничего не подставлено.",
        "upstream": "Лента новостей Steam не вернула пригодный список.",
        "kept": "Карточки ниже — предыдущий ответ, не новый замер.",
        "metaFresh": "Объявлений: {n}. Запрос к Steam: {fetched}. Показано: {served}. Для этого открытия страницы ответ свежий.",
        "metaStale": "Объявлений: {n}. Последний удачный запрос к Steam: {fetched}. Показано: {served}. Эта копия устарела. Это не текущее состояние серверов.",
        "title": "Дальше — проверки, а не вердикт по серверу",
        "notATest": "Это ваши ответы, сопоставленные с уже опубликованным текстом Kefir. Это не проверка EU или East US.",
        "codeLead": "{code}. Kefir: {meaning} Шаг из справки: {fix}",
        "ping": "Высокий пинг и «резинку» эта страница не измеряет. Ускоритель только меняет маршрут до официальных серверов. Сервер, который не отвечает, он не поднимет. Цен и названий продуктов здесь нет.",
        "others": "Вы написали, что это не только у вас. Так бывает, когда не отвечает сама игра, и так бывает в общей сети. Ответ — не замер. Прочитайте объявление Kefir по ссылке выше. Регион из этого ответа страница не пометит ни как лежащий, ни как рабочий.",
        "onlyLocal": "Для этого кода справка Kefir описывает шаг на вашем компьютере, в аккаунте или в файлах. Работают ли при этом EU или East US, из кода не следует.",
        "onlyLink": "Kefir просит проверить соединение и перезапустить игру. В справке не сказано, что код доказывает простой региона. Если это только у вас, начните с этого шага. Статус региона на странице остаётся неизвестным.",
        "loginUnknown": "Отказ на входе или обрыв сессии может быть и службой игры, и путём до неё. Страница их не различает и не помечает регион ни рабочим, ни лежащим.",
        "unsure": "Этих ответов мало, чтобы отделить ваш компьютер от службы игры. Статус остаётся неизвестным.",
        "regionNote": {
            "eu": "EU: смотрите датированные посты Steam выше. Фраза в одном из них — не здоровье EU прямо сейчас.",
            "us": "East US: в посте может быть сказано, что US-серверы тогда не затронуты. Это не East US прямо сейчас.",
            "unknown": "Регион вы не выбрали. Посты выше — объявления, а не замер состояния.",
        },
        "stamp": "Подсказка собрана в этом браузере в {time}. Эти часы — не отметка сервера.",
        "copied": "Скопировано.",
        "copyFail": "Буфер обмена в этом браузере недоступен.",
        "copyEmpty": "Сначала покажите текст из справки.",
    },
}

FAQ = {
    "en": [
        ("Is the ROB RUN EU server down right now?",
         "This page cannot say. It shows official Steam community announcements and the time each one was published. On 14 Nov 2026 at 21:00 UTC, Kefir wrote that EU login was unstable and that US servers were not affected at that time. An English line labeled 23:20 CET said a restart would happen shortly. The post does not confirm that the restart finished. A later silence is not an all-clear."),
        ("Does this page read every official channel?",
         "No. It requests Steam’s public news for community announcements only. Kefir also posts on X, Discord, Telegram, and VK. Those channels are linked on this page and are not read by it."),
        ("What does error E-0101 mean?",
         "Kefir’s help text: the game cannot connect to the server to download configuration or startup data. Their fix is to check your internet connection and make sure websites load. The help text does not say this code proves the EU or East US region is down."),
        ("Where does Kefir announce server trouble?",
         "Kefir’s help article lists Discord, X, the Steam store page, Facebook, Instagram, VK, and Telegram. This page reads only the Steam community-announcement feed. It does not read the other channels, and none of the links is a live status board."),
    ],
    "ru": [
        ("ROB RUN не работает — сервер EU лежит прямо сейчас?",
         "Эта страница так не отвечает. Она показывает официальные объявления сообщества Steam и время публикации каждого. 14 ноября 2026 года в 21:00 UTC Kefir написал, что вход на EU нестабилен и что US-серверы в тот момент не затронуты. В английской строке «UPD (23:20 CET)» сказано, что серверы скоро перезапустят. Подтверждения, что перезапуск закончился, в посте нет. Молчание после поста — не отбой."),
        ("Страница читает все официальные каналы?",
         "Нет. Запрос идёт только к публичным новостям Steam и только к объявлениям сообщества. Kefir также пишет в X, Discord, Telegram и VK. Эти каналы даны ссылками, страница их не читает."),
        ("Что значит ошибка E-0101?",
         "В справке Kefir: игра не может связаться с сервером для загрузки настроек или стартовых данных. Их шаг — проверить интернет и что сайты открываются. В справке не сказано, что этот код доказывает простой региона EU или East US."),
        ("Где Kefir пишет о проблемах с серверами?",
         "В справке перечислены Discord, X, страница игры в Steam, Facebook, Instagram, VK и Telegram. Эта страница читает только ленту объявлений сообщества Steam. Остальные каналы она не читает, и живого табло среди ссылок нет."),
    ],
}

STATUS_JS = r"""
<script>
(function () {
  var STR = __STR__;
  var CODES = __CODES__;
  var refreshBtn = document.getElementById('refreshBtn');
  var feedMeta = document.getElementById('feedMeta');
  var feedList = document.getElementById('feedList');
  var diagBtn = document.getElementById('diagBtn');
  var diagResult = document.getElementById('diagResult');
  var copyBtn = document.getElementById('copyBtn');
  var copyNote = document.getElementById('copyNote');
  var lastSummary = '';
  var inFlight = false;
  var pollTimer = 0;

  function clockOptions() {
    return {
      year: 'numeric', month: 'short', day: 'numeric',
      hour: '2-digit', minute: '2-digit', timeZoneName: 'short'
    };
  }
  function fmt(iso) {
    var when = new Date(iso);
    if (!iso || isNaN(when.getTime())) return '—';
    return new Intl.DateTimeFormat(STR.locale, clockOptions()).format(when);
  }
  function nowLabel() {
    return new Intl.DateTimeFormat(STR.locale, clockOptions()).format(new Date());
  }
  function fill(el, title, paras, steps, extraLink) {
    el.className = 'result show neutral';
    while (el.firstChild) el.removeChild(el.firstChild);
    var h = document.createElement('b');
    h.className = 'big';
    h.textContent = title;
    el.appendChild(h);
    paras.forEach(function (text) {
      var p = document.createElement('p');
      p.textContent = text;
      el.appendChild(p);
    });
    if (steps.length) {
      var ol = document.createElement('ol');
      steps.forEach(function (text) {
        var li = document.createElement('li');
        li.textContent = text;
        ol.appendChild(li);
      });
      el.appendChild(ol);
    }
    if (extraLink) {
      var p2 = document.createElement('p');
      var a = document.createElement('a');
      a.href = extraLink.href;
      a.textContent = extraLink.label;
      p2.appendChild(a);
      el.appendChild(p2);
    }
  }
  function paintFeed(data) {
    while (feedList.firstChild) feedList.removeChild(feedList.firstChild);
    var items = data && Array.isArray(data.items) ? data.items : [];
    if (!data || (!data.ok && !items.length)) {
      var code = (data && data.upstreamError) || 'upstream';
      feedMeta.textContent = STR[code] || STR.upstream;
      return;
    }
    if (!items.length) {
      feedMeta.textContent = STR.empty;
      return;
    }
    var template = data.fresh ? STR.metaFresh : STR.metaStale;
    feedMeta.textContent = template
      .replace('{n}', String(items.length))
      .replace('{fetched}', fmt(data.sourceFetchedAt))
      .replace('{served}', fmt(data.servedAt));
    items.forEach(function (item) {
      var art = document.createElement('article');
      art.className = 'note-box';
      var kicker = document.createElement('p');
      kicker.className = 'status-k';
      kicker.textContent = STR.cardKicker;
      var title = document.createElement('h3');
      title.textContent = item.title || '';
      var when = document.createElement('p');
      var time = document.createElement('time');
      time.dateTime = item.publishedAt || '';
      time.textContent = STR.published + ' ' + fmt(item.publishedAt);
      when.appendChild(time);
      var body = document.createElement('p');
      body.textContent = item.excerpt || '';
      art.appendChild(kicker);
      art.appendChild(title);
      art.appendChild(when);
      art.appendChild(body);
      var linkOk = false;
      try {
        var parsed = new URL(item.link || '');
        linkOk = parsed.protocol === 'https:' && (
          parsed.hostname === 'store.steampowered.com' ||
          parsed.hostname === 'steamcommunity.com' ||
          (parsed.hostname === 'steamstore-a.akamaihd.net' &&
            parsed.pathname === '/news/externalpost/steam_community_announcements/' + item.gid)
        );
      } catch (err) { linkOk = false; }
      if (linkOk) {
        var link = document.createElement('a');
        link.href = item.link;
        link.rel = 'noopener noreferrer';
        link.target = '_blank';
        link.textContent = STR.openPost;
        art.appendChild(link);
      }
      feedList.appendChild(art);
    });
  }
  async function loadFeed() {
    if (inFlight) return;
    inFlight = true;
    refreshBtn.disabled = true;
    if (!feedList.firstChild) feedMeta.textContent = STR.loading;
    try {
      if (!navigator.onLine) {
        feedMeta.textContent = STR.offline;
        return;
      }
      var ctrl = new AbortController();
      var timer = setTimeout(function () { ctrl.abort(); }, 12000);
      var res;
      try {
        res = await fetch('/api/rob-run/announcements', { cache: 'no-store', signal: ctrl.signal });
      } finally {
        clearTimeout(timer);
      }
      var data = null;
      try { data = await res.json(); } catch (err) { data = null; }
      if (!data || data.mode !== 'live' || !Array.isArray(data.items)) {
        feedMeta.textContent = STR.malformed;
        return;
      }
      paintFeed(data);
    } catch (err) {
      console.error(JSON.stringify({ event: "rob_run_news_client", name: err && err.name, message: err && err.message }));
      var fail = err && err.name === 'AbortError' ? STR.timeout : STR.upstream;
      feedMeta.textContent = feedList.firstChild ? fail + ' ' + STR.kept : fail;
    } finally {
      inFlight = false;
      refreshBtn.disabled = false;
    }
  }
  function selectedRegion() {
    var buttons = document.querySelectorAll('#regionChoices button');
    for (var i = 0; i < buttons.length; i++) {
      if (buttons[i].getAttribute('aria-pressed') === 'true') return buttons[i].getAttribute('data-value');
    }
    return 'unknown';
  }
  function diagnose() {
    var region = selectedRegion();
    var symptom = document.getElementById('symptom').value;
    var codeId = document.getElementById('code').value;
    var scope = document.getElementById('scope').value;
    var code = null;
    for (var i = 0; i < CODES.length; i++) if (CODES[i].id === codeId) code = CODES[i];
    var steps = [];
    if (code) {
      steps.push(STR.codeLead.replace('{code}', code.id).replace('{meaning}', code.meaning).replace('{fix}', code.fix));
    }
    if (symptom === 'ping') steps.push(STR.ping);
    if (scope === 'others') steps.push(STR.others);
    else if (scope === 'only' && code && code.kind === 'local') steps.push(STR.onlyLocal);
    else if (scope === 'only' && code && code.kind === 'link') steps.push(STR.onlyLink);
    else if (symptom === 'ping') { /* ping step already states the limit */ }
    else if (symptom === 'login' || symptom === 'disconnect') steps.push(STR.loginUnknown);
    else steps.push(STR.unsure);
    steps.push(STR.regionNote[region] || STR.regionNote.unknown);
    var stamp = STR.stamp.replace('{time}', nowLabel());
    var link = (symptom === 'ping' && STR.lagHref) ? { href: STR.lagHref, label: STR.lagLabel } : null;
    fill(diagResult, STR.title, [STR.notATest, stamp], steps, link);
    lastSummary = STR.title + '\n' + STR.notATest + '\n' + stamp + '\n' +
      steps.map(function (s, n) { return (n + 1) + '. ' + s; }).join('\n');
    if (link) lastSummary += '\n' + link.label + ' ' + link.href;
    copyBtn.disabled = false;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    diagResult.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'nearest' });
  }
  refreshBtn.addEventListener('click', loadFeed);
  diagBtn.addEventListener('click', diagnose);
  document.querySelectorAll('#regionChoices button').forEach(function (btn) {
    btn.addEventListener('click', function () {
      document.querySelectorAll('#regionChoices button').forEach(function (b) {
        var on = b === btn;
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
        b.classList.toggle('is-on', on);
      });
    });
  });
  function armPoll() {
    clearTimeout(pollTimer);
    pollTimer = setTimeout(function () {
      if (document.visibilityState === 'visible') loadFeed();
      armPoll();
    }, 90000);
  }
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'visible') loadFeed();
  });
  loadFeed();
  armPoll();
  copyBtn.addEventListener('click', function () {
    if (!lastSummary) { copyNote.textContent = STR.copyEmpty; return; }
    if (!navigator.clipboard || !navigator.clipboard.writeText) {
      copyNote.textContent = STR.copyFail;
      return;
    }
    navigator.clipboard.writeText(lastSummary).then(function () {
      copyNote.textContent = STR.copied;
    }, function () {
      copyNote.textContent = STR.copyFail;
    });
  });
})();
</script>
"""


def _a(href, label):
    return '<a href="%s">%s</a>' % (href, label)


def _region_card(name, unknown, metrics, announcement, link_label):
    return (
        '<article class="note-box"><p class="status-k">%s</p>'
        '<p class="status-v">%s</p><p>%s</p><p>%s</p><p>%s</p></article>'
        % (name, unknown, metrics, announcement, _a(NEWS_EU, link_label))
    )


def _faq_html(lang):
    bits = []
    for i, (q, a) in enumerate(FAQ[lang]):
        bits.append(
            '<details%s><summary><h3>%s</h3>'
            '<span class="plus" aria-hidden="true">'
            '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6">'
            '<path d="M6 1v10M1 6h10"/></svg></span></summary><p>%s</p></details>'
            % (" open" if i == 0 else "", q, a)
        )
    return "".join(bits)


def render(lang):
    c = COPY[lang]
    canon = PATHS[lang]
    alt = dict(PATHS)
    home = "Home" if lang == "en" else "Главная"
    home_path = "/" if lang == "en" else "/ru/"
    hub = "/rob-run/" if lang == "en" else "/ru/rob-run/"
    channels = "".join("<li>%s</li>" % _a(href, name) for name, href in CHANNELS)
    rows = []
    for code, _kind, meaning, fix in CODES:
        rows.append("<tr><th>%s</th><td>%s %s</td></tr>" % (
            code, meaning[lang], fix[lang]))
    wont = "".join("<li>%s</li>" % item for item in c["wont"])
    rel = "".join(
        '<a class="rel" href="%s"><b>%s</b><span>%s</span></a>' % item
        for item in c["rel"])
    code_opts = '<option value="">%s</option>' % c["opt_nocode"]
    code_opts += "".join('<option value="%s">%s</option>' % (code, code) for code, _k, _m, _f in CODES)
    js_codes = [{"id": code, "kind": kind, "meaning": meaning[lang], "fix": fix[lang]}
                for code, kind, meaning, fix in CODES]
    js = (STATUS_JS.replace("__STR__", json.dumps(JS_COPY[lang], ensure_ascii=False))
          .replace("__CODES__", json.dumps(js_codes, ensure_ascii=False)))
    pressed = ' class="btn btn-secondary" aria-pressed="true"'
    idle = ' class="btn btn-secondary" aria-pressed="false"'
    help_name = "Help Center" if lang == "en" else "Справка Kefir"
    news_name = "Steam news" if lang == "en" else "Новости Steam"
    faq_h = "Frequently asked questions" if lang == "en" else "Частые вопросы"
    src_bits = [
        _a(NEWS_EU, "14 Nov 2026" if lang == "en" else "14 ноября 2026"),
        _a(NEWS_FAQ, "13 Nov 2026" if lang == "en" else "13 ноября 2026"),
        _a(NEWS_SCHED, "4 Nov 2026" if lang == "en" else "4 ноября 2026"),
        _a(HC_ERR[lang], "error codes" if lang == "en" else "коды ошибок"),
        _a(HC_COMM[lang], "communities" if lang == "en" else "сообщества"),
    ]
    hand = (
        '<article class="note-box"><h3>%s</h3><p>%s</p><p>%s</p><p>%s</p></article>'
        % (c["eu_name"], c["eu_ann"], c["us_ann"], _a(NEWS_EU, c["open_ann"]))
    )
    body = (
        '<main id="main" class="wrap narrow">'
        + crumbs_html(lang, [("ROB RUN", hub), (c["crumb"], None)])
        + '<h1 class="page-h1">%s</h1>' % c["h1"]
        + '<p class="page-lede">%s</p>' % c["lede"]
        + '<p class="intro-note">%s</p>' % c["reviewed"]
        + '<div class="note-box amber"><h2>%s</h2><p>%s</p></div>' % (c["limit_h"], c["limit_p"])
        + '<noscript><p class="intro-note">%s</p></noscript>' % c["noscript"]
        + '<div class="prose"><h2 class="sec" id="announcements">%s</h2><p>%s</p></div>' % (c["feed_h"], c["feed_p"])
        + '<div class="checker"><div class="actions">'
        + '<button type="button" class="btn btn-primary" id="refreshBtn">%s</button></div>' % c["refresh_btn"]
        + '<p id="feedMeta" aria-live="polite">%s</p>' % (
            "Loading official Steam announcements…" if lang == "en" else "Загружаем официальные объявления Steam…")
        + '<div id="feedList" class="feed-list"></div></div>'
        + '<div class="prose">'
        + '<h2 class="sec" id="hand">%s</h2><p>%s</p>' % (c["hand_h"], c["hand_p"])
        + hand
        + '<h2 class="sec" id="regions">%s</h2><p>%s</p>' % (c["regions_h"], c["regions_p"])
        + '<p>%s %s. %s.</p>' % (
            ("Read the notes:" if lang == "en" else "Тексты:"),
            _a(NEWS_SCHED, c["sched_link"]), _a(NEWS_FAQ, c["faq_link"]))
        + '<h2 class="sec" id="channels">%s</h2><p>%s</p><ul>%s</ul>' % (c["where_h"], c["where_p"], channels)
        + '<p>%s</p>' % (
            ("The list is on the %s. Every Steam post is under %s." if lang == "en"
             else "Список — в статье %s. Все записи Steam — в разделе %s.")
            % (_a(HC_COMM[lang], help_name), _a(NEWS_HUB, news_name)))
        + '<p>%s</p>' % c["mail_p"]
        + '<h2 class="sec">%s</h2><p>%s</p><p>%s. %s.</p>' % (
            c["switch_h"], c["switch_p"], _a(HC_SERVER[lang], c["switch_a"]), _a(NEWS_FAQ, c["faq_link"]))
        + '</div>'
        + '<div class="prose"><h2 class="sec" id="match">%s</h2><p>%s</p></div>' % (c["match_h"], c["match_p"])
        + '<div class="checker">'
        + '<p id="regionLabel" class="field-label">%s</p>' % c["region_label"]
        + '<div class="mode-row" id="regionChoices" role="group" aria-labelledby="regionLabel">'
        + '<button type="button" data-value="eu"%s>%s</button>' % (idle, c["reg_eu"])
        + '<button type="button" data-value="us"%s>%s</button>' % (idle, c["reg_us"])
        + '<button type="button" data-value="unknown"%s>%s</button>' % (pressed, c["reg_unk"])
        + '</div>'
        + '<label for="symptom">%s</label>' % c["sym_label"]
        + '<select id="symptom"><option value="login">%s</option>' % c["opt_login"]
        + '<option value="disconnect">%s</option><option value="ping">%s</option>' % (c["opt_disconnect"], c["opt_ping"])
        + '<option value="other">%s</option></select>' % c["opt_other"]
        + '<label for="code">%s</label><select id="code">%s</select>' % (c["code_label"], code_opts)
        + '<label for="scope">%s</label><select id="scope">' % c["scope_label"]
        + '<option value="unsure">%s</option><option value="only">%s</option>' % (c["opt_unsure"], c["opt_only"])
        + '<option value="others">%s</option></select>' % c["opt_others"]
        + '<div class="actions"><button type="button" class="btn btn-primary" id="diagBtn">%s</button>' % c["diag_btn"]
        + '<button type="button" class="btn btn-secondary" id="copyBtn" disabled>%s</button></div>' % c["copy_btn"]
        + '<p class="hint" id="copyNote" aria-live="polite"></p>'
        + '<div id="diagResult" class="result" aria-live="polite"></div></div>'
        + '<div class="prose"><h2 class="sec" id="codes">%s</h2><p>%s</p>' % (c["codes_h"], c["codes_p"])
        + '<p>%s.</p>' % _a(HC_ERR[lang], help_name)
        + '<div class="table-scroll"><table class="fact-table">%s</table></div>' % "".join(rows)
        + '<h2 class="sec">%s</h2><ul>%s</ul>' % (c["wont_h"], wont)
        + '<h2 class="sec" id="ping">%s</h2><p>%s</p>' % (c["ping_h"], c["ping_p"])
        + '<section class="faq" id="faq"><h2 class="sec">%s</h2>%s</section>' % (faq_h, _faq_html(lang))
        + '</div>'
        + '<section class="related"><h2>%s</h2><div class="related-grid">%s</div></section>' % (c["related_h"], rel)
        + '<p class="data-line">%s %s.</p></main>' % (c["src_h"], ". ".join(src_bits))
    )
    jl = [
        breadcrumb_jsonld(lang, [(home, home_path), ("ROB RUN", hub), (c["h1"], canon)]),
        {"@context": "https://schema.org", "@type": "WebApplication",
         "name": c["h1"], "url": BASE + canon, "inLanguage": lang,
         "description": c["desc"], "applicationCategory": "UtilitiesApplication",
         "operatingSystem": "Any modern browser",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [
             {"@type": "Question", "name": q,
              "acceptedAnswer": {"@type": "Answer", "text": a}}
             for q, a in FAQ[lang]]},
    ]
    return page(lang, c["title"], c["desc"], canon, alt, body + js, jsonld=jl, games=("rob-run",))


def rel_path(lang):
    return ("rob-run/server-status/index.html" if lang == "en"
            else "ru/rob-run/server-ne-rabotaet/index.html")
