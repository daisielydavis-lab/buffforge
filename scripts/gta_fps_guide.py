#!/usr/bin/env python3
"""GTA 6 PS5 frame-interpolation guide (EN + RU).

Facts checked 19 November 2026 against primary pages, not a research summary:

- Digital Foundry, console comparison (30 fps target, no 40/60 mode; Pro steadier)
  https://www.digitalfoundry.net/features/gta-6-ps5-vs-ps5-pro-xbox-series-x-and-series-s-which-console-plays-best
- PlayStation Blog, 10 November 2026 (preload, local-midnight launch, Pro PSSR and ray-traced shadows)
  https://blog.playstation.com/2026/11/10/pre-load-grand-theft-auto-vi-on-ps5-starting-today/
- smoovplay/smoovplay tag v0.3.8 README, LICENSE (MIT), NOTICE (chiaki-ng AGPL-3.0),
  and the v0.3.8 release notes published 2026-11-19
- https://smoovplay.github.io/ , /compare/ , /how-it-works/
- chiaki-ng/chiaki-ng (AGPL-3.0; streetpea/chiaki-ng redirects here), docs, releases
  https://chiaki-ng.github.io/chiaki-ng/setup/configuration/

Button names below are the labels in those docs. This page does not describe
a SmartScreen or antivirus bypass, and it does not collect PSN credentials.
"""
from shell import BASE, breadcrumb_jsonld, crumbs_html, page

DF = "https://www.digitalfoundry.net/features/gta-6-ps5-vs-ps5-pro-xbox-series-x-and-series-s-which-console-plays-best"
PSB = "https://blog.playstation.com/2026/11/10/pre-load-grand-theft-auto-vi-on-ps5-starting-today/"
SP_REPO = "https://github.com/smoovplay/smoovplay"
SP_REL = "https://github.com/smoovplay/smoovplay/releases/latest"
SP_TAG = "https://github.com/smoovplay/smoovplay/releases/tag/v0.3.8"
SP_README = "https://github.com/smoovplay/smoovplay/blob/v0.3.8/README.md"
SP_LIC = "https://github.com/smoovplay/smoovplay/blob/v0.3.8/LICENSE"
SP_NOTICE = "https://github.com/smoovplay/smoovplay/blob/v0.3.8/NOTICE"
SP_SITE = "https://smoovplay.github.io/"
SP_COMPARE = "https://smoovplay.github.io/compare/"
SP_HOW = "https://smoovplay.github.io/how-it-works/"
CK_REPO = "https://github.com/chiaki-ng/chiaki-ng"
CK_REL = "https://github.com/chiaki-ng/chiaki-ng/releases"
CK_DOCS = "https://chiaki-ng.github.io/chiaki-ng/"
CK_CONF = "https://chiaki-ng.github.io/chiaki-ng/setup/configuration/"
CK_UPDATES = "https://chiaki-ng.github.io/chiaki-ng/updates/releases/"

ARROW = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
    '<path d="M5 12h14M13 6l6 6-6 6"/></svg>'
)
PLUS = (
    '<span class="plus" aria-hidden="true">'
    '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6">'
    '<path d="M6 1v10M1 6h10"/></svg></span>'
)


def A(url, label):
    return '<a href="%s">%s</a>' % (url, label)


def _ul(items):
    return "<ul>" + "".join("<li>%s</li>" % x for x in items) + "</ul>"


def _ol(items):
    return "<ol>" + "".join("<li>%s</li>" % x for x in items) + "</ol>"


def _table(rows):
    return (
        '<table class="fact-table">'
        + "".join("<tr><th>%s</th><td>%s</td></tr>" % pair for pair in rows)
        + "</table>"
    )


def _flow(c):
    bits = []
    for i, (title, detail) in enumerate(c["flow"], 1):
        if i > 1:
            bits.append('<div class="ff-arrow" aria-hidden="true">%s</div>' % ARROW)
        bits.append(
            '<div class="ff-step"><span class="ff-n">%d</span><b>%s</b>'
            '<span class="ff-d">%s</span></div>' % (i, title, detail)
        )
    return (
        '<figure class="guide-visual"><div class="frame-flow" role="img" aria-label="%s">%s</div>'
        '<figcaption>%s</figcaption></figure>'
        % (c["flow_aria"], "".join(bits), c["flow_cap"])
    )


def _faq(pairs):
    blocks = []
    for i, (q, a) in enumerate(pairs):
        blocks.append(
            "<details%s><summary><h3>%s</h3>%s</summary><p>%s</p></details>"
            % (" open" if i == 0 else "", q, PLUS, a)
        )
    return "".join(blocks)


def _sources(groups):
    out = []
    for heading, items in groups:
        out.append("<h3>%s</h3>%s" % (heading, _ul(items)))
    return "".join(out)


def _related(items):
    return "".join(
        '<a class="rel" href="%s"><b>%s</b><span>%s</span></a>' % triple
        for triple in items
    )


def _pair(left_h, left_html, right_h, right_html):
    return (
        '<div class="ping-fps">'
        '<article class="ping-card net"><h3>%s</h3>%s</article>'
        '<article class="ping-card fps"><h3>%s</h3>%s</article>'
        "</div>" % (left_h, left_html, right_h, right_html)
    )


def _cards(fit_h, fit, skip_h, skip):
    return _pair(fit_h, _ul(fit), skip_h, _ul(skip))


def en():
    return {
        "title": "GTA 6 PS5 30 FPS: free open-source frame interpolation and its limits — BuffForge",
        "desc": "GTA 6 targets 30 FPS on PS5, with no 40 or 60 mode. How a free open-source Windows app draws extra frames from Remote Play, and where that path stops.",
        "h1": "GTA 6 on PS5 targets 30 FPS: free open-source frame interpolation, and its limits",
        "crumb": "PS5 frame interpolation",
        "lede": "The PS5 still targets 30 frames a second. A Windows PC can draw the pictures in between, and only on its own monitor.",
        "updated": "Checked 19 November 2026. SmoovPlay release read that day: v0.3.8.",
        "note": (
            "GTA 6 on a real console has not been run through this path by us, and SmoovPlay has not published a real-PS5 GTA 6 recording. "
            "The GTA VI clips on their %s are Rockstar's trailer, An Extended Look, replayed as a simulated 1080p30 Remote Play stream. "
            "The real PS5 recording they show is Gotham Knights. The steps below are the setup in the docs we read on 19 November 2026."
        ) % A(SP_COMPARE, "compare page"),
        "alt": "Official Grand Theft Auto VI key art: a collage of characters, vehicles and the VI logo.",
        "cap": "Official key art. © Rockstar Games. Not a gameplay frame, and not a frame-rate test.",
        "short_h": "The short answer",
        "short": [
            (
                "%s, which we read on 19 November 2026, says PS5, PS5 Pro, Xbox Series X and Series S all target 30 fps, and that none of them has a 40 or 60 fps mode. "
                "PS5 Pro holds that 30 more steadily. A steadier 30 is still a 30."
            ) % A(DF, "Digital Foundry's console comparison"),
            (
                "The %s, 10 November 2026, is about preload and a rolling local-midnight launch on 19 November. "
                "For PS5 Pro it describes clearer picture quality, through PSSR, and ray-traced shadows. It does not describe a higher frame-rate mode."
            ) % A(PSB, "PlayStation Blog post"),
            (
                "The free tool that changes the picture on a monitor is %s, an early open-source Windows app. "
                "A PS5 with Remote Play on sends a 1080p stream. %s, the open-source Remote Play client, receives it. "
                "SmoovPlay then draws extra frames on the PC graphics card with RIFE. "
                "A 60 Hz monitor can show 60 pictures a second, a 90 Hz monitor 90, and a 120 Hz or faster monitor up to 120. "
                "The console is not modified. The game keeps its own response rate. "
                "SmoovPlay's own code is MIT. The Remote Play piece depends on chiaki-ng, which is AGPL-3.0."
            ) % (A(SP_REPO, "SmoovPlay"), A(CK_REPO, "chiaki-ng")),
        ],
        "who_h": "Who it is for",
        "who_lead": "This runs only when the picture is on a Windows PC.",
        "fit_h": "Worth setting up",
        "fit": [
            "You have a Windows 10 or 11 PC and an NVIDIA GeForce RTX 30, 40, or 50 series card. That is the range SmoovPlay marks as tested.",
            "You can play on that PC's monitor, controller paired to the PC, on a screen at 60 Hz or faster.",
            "You want smoother motion in a 30 fps game and can accept the stream's delay plus the frame generator's delay.",
        ],
        "skip_h": "Leave it",
        "skip": [
            "You only have a PS5 and a TV. The extra frames never reach a screen plugged into the console.",
            "You want the game itself to render or respond at 60. It keeps the 30 fps target Digital Foundry measured.",
            "You were counting on AMD, Intel, an Xbox app, or a capture card as the same setup. The project marks those Experimental.",
        ],
        "flow_h": "30 real frames, then extra pictures",
        "flow_lead": "Four stops. The game is the first. The monitor is only a display.",
        "flow_aria": "PS5 sends real frames at a 30 fps target. chiaki-ng carries the 1080p Remote Play stream. SmoovPlay on Windows draws the in-between frames. The PC monitor shows 60, 90, or up to 120 pictures.",
        "flow": [
            ("PS5", "Real frames. The game targets 30 fps."),
            ("Remote Play", "chiaki-ng carries a 1080p stream. No extra frames yet."),
            ("Windows", "SmoovPlay draws the in-between frames with RIFE."),
            ("PC monitor", "60, 90, or up to 120 pictures, matching the screen."),
        ],
        "flow_cap": "The console does not start rendering at 60. The extra pictures are drawn on the PC, after the stream arrives.",
        "send_h": "What the PS5 sends",
        "send_p": "Real frames at a 30 fps target. Button timing stays the game's own rate, then the stream adds its own wait.",
        "show_h": "What the monitor shows",
        "show_p": "60 pictures on a 60 Hz screen, 90 on 90 Hz, and up to 120 only if the screen is 120 Hz or faster. Each extra picture is drawn from the real frames on either side.",
        "hw_h": "What you need",
        "hw_lead": (
            "From the %s hardware table, tag v0.3.8. Where the project says Tested or Experimental, that word is kept."
        ) % A(SP_README, "SmoovPlay README"),
        "hw": [
            ("PC", "Windows 10 or 11, 64-bit. 8 GB of memory. 12 GB free during setup."),
            ("Graphics card",
             "NVIDIA GeForce RTX 30, 40 or 50 series, marked Tested. The machines they name are an RTX 4070 Ti SUPER on Windows 10, and a contributor's RTX 5070 Ti on Windows 11. RTX 20 cards and laptops are not tested yet. "
             "AMD Radeon and Intel Arc are Experimental, through DirectML. The project says that path is about 1.7 times slower and has not met a real game on a real AMD or Intel card yet."),
            ("Console",
             "A PS5 with Remote Play turned on. That is the tested path. A capture card, or a game shown inside an app window, is Experimental."),
            ("Network",
             "Ethernet for the console and the PC, or 5 GHz or 6 GHz Wi-Fi. A capture card does not need it. The README says a wired link is the smoothest."),
            ("Screen",
             "Any refresh rate: 60 Hz gets 60 fps, 90 Hz gets 90, 120 Hz or faster gets up to 120. G-Sync or FreeSync helps, per the README."),
            ("Where you sit",
             "Controller on the PC. Eyes on the PC monitor. A TV cabled to the PS5 keeps the console's own picture."),
            ("On the PS5", "Nothing is installed."),
        ],
        "hw_after": (
            "The README's Experimental capture-card line names one player's AVerMedia Live Gamer 4K (GC573) as working since 0.3.1, with its sound still waiting on their word as of 0.3.2. "
            "Other cards were tried with recordings standing in for a card. The Xbox app has been recognised from a player's report; a real Xbox stream is not confirmed. "
            "Use the PS5 Remote Play path if you want the one the project calls tested."
        ),
        "setup_h": "Set it up",
        "setup_lead": (
            "Labels below are the ones in the %s and on %s. "
            "If a button on your build has moved, follow the text in the app. v0.3.8 shipped on 19 November 2026, and this is an early release."
        ) % (A(SP_README, "v0.3.8 README"), A(CK_CONF, "chiaki-ng's configuration page")),
        "steps": [
            (
                "On the PS5, open <b>Settings → System → Remote Play</b> and turn on <b>Enable Remote Play</b>. "
                "That menu is the one chiaki-ng documents. To wake the console from rest, the same page also lists "
                "<b>Settings → System → Power Saving → Features Available in Rest Mode</b>, then <b>Stay Connected to the Internet</b> and <b>Enable Turning on PS5 from Network</b>. "
                "Keep the PS5 and the PC on the same home network."
            ),
            (
                "On the Windows PC, download <b>SmoovPlay-Setup.exe</b> only from the %s. "
                "The tag we read is %s. The installer is an early build and is not code-signed, so the browser or Windows may warn you. "
                "Keep SmartScreen, antivirus, and the rest of your protection as they are. "
                "To check the file, compare its SHA-256 with the hash on that Releases page. The README's PowerShell command is <b>Get-FileHash</b> on the installer. "
                "Skip search ads, re-uploads, and any page that asks you to type a PSN password into it."
            ) % (A(SP_REL, "official Releases page"), A(SP_TAG, "v0.3.8")),
            (
                "Run that installer. The project says setup takes 10 to 20 minutes, installs for the current Windows user, and does not request administrator rights. "
                "It checks the PC and downloads about 5 GB — Python, PyTorch, and NVIDIA TensorRT — from those projects' own sources. "
                "It finishes by picking settings from a short test of your graphics card and display."
            ),
            (
                "In the app, follow <b>Connect your PS5</b>. Turn Remote Play on if it is still off, sign in to PSN inside chiaki-ng, and register the console. "
                "The project says this is about five minutes, once. The sign-in stays in that client and on Sony's own page, the same kind of step as Sony's Remote Play app. "
                "BuffForge never asks for the password, the account ID, or a redirect link. "
                "If the client asks for a Remote Play code, the console shows one at <b>Settings → System → Remote Play → Link Device</b>. Enter the code in the client. "
                "When the screens diverge from these labels, use %s."
            ) % A(CK_CONF, "chiaki-ng's configuration page"),
            (
                "Pair the controller with the PC the way that controller usually pairs. You play looking at the PC monitor. "
                "The television plugged into the PS5 keeps showing the console's own picture."
            ),
            (
                "Press <b>Play</b>. In the video window the README lists <b>M</b> for the live menu, <b>F</b> for fullscreen (called the lowest delay), "
                "<b>I</b> to turn the extra frames off and on, <b>L</b> for the delay test, and <b>Esc</b> or <b>Q</b> to stop. "
                "As of v0.3.8, <b>Capture card resolution</b> stays grey unless the source really is a capture card, because PS5 Remote Play is 1080p at most. "
                "<b>Minimise chiaki-ng</b> stays grey unless PS5 Remote Play is the source. A grey 1440p or 4K choice is not a higher Remote Play stream."
            ),
        ],
        "keys_lead": "Keys for the video window, from the README. The controller plays the game. The keyboard runs SmoovPlay.",
        "keys": [
            ("M", "Menu: every setting, live."),
            ("F", "Fullscreen. The README calls this the lowest delay."),
            ("I", "Extra frames off and on, so you can compare."),
            ("L", "Delay test for PS5 Remote Play."),
            ("Esc or Q", "Stop."),
        ],
        "keys_after": (
            "On the Experimental app-window path the other app keeps the keyboard, and the README moves these shortcuts to Ctrl+Alt. "
            "An update from inside the app has to carry SmoovPlay's signature before it runs. From 0.3.1, <b>Check for updates</b> sits in the launcher side bar."
        ),
        "start_h": "A starting point, not a tuned profile",
        "start_lead": (
            "Leave the choices the installer just made. <b>Auto-detect</b> on the Settings page runs the short test again after you change monitors. "
            "Nothing in this table is a GTA 6 setting we measured. We have not played the game through this path."
        ),
        "start": [
            ("Output",
             "Keep Auto-detect's choice. 60 Hz shows 60, 90 Hz shows 90. Up to 120 needs a 120 Hz or faster screen. "
             "The README says 60 and 90 are what it has shown and measured live. 120 draws three in-between frames the same way, and no 120 fps clip or live measurement is published yet."),
            ("Uneven 30",
             "If a locked 30 fps game looks uneven, set <b>Settings → Smoothness → Game frame rate</b> to <b>30 fps</b>. "
             "On Auto, the project says that since 0.3.4 it usually reads a wired 30 fps stream from the picture, and that a still or dark scene can still fool it."),
            ("One generator",
             "While SmoovPlay and chiaki-ng are running, leave NVIDIA Smooth Motion, AMD Fluid Motion Frames, and Lossless Scaling off. "
             "The README lists that as a conflict. Quitting this app leaves your other games alone."),
            ("Model",
             "Stay on RIFE. That is the model this project runs by default. NVIDIA's Video Frame Generation is optional, not included, and only offered on RTX 40 and 50 after you accept NVIDIA's licence."),
        ],
        "chiaki_h": "chiaki-ng carries the stream",
        "chiaki": [
            (
                "chiaki-ng receives Remote Play, plays the sound, and sends your buttons back. "
                "SmoovPlay's %s calls that the transport: a small frame tap hands each decoded frame across, and SmoovPlay is where the extra frames are drawn. "
                "chiaki-ng's %s describe Remote Play setup. They do not describe a frame-generation mode. On its own, chiaki-ng shows the stream the console sent."
            ) % (A(SP_HOW, "how-it-works page"), A(CK_DOCS, "own docs")),
            (
                "SmoovPlay's %s at tag v0.3.8 says SmoovPlay's own code is MIT (%s), and the patched chiaki-ng remains a separate program under the GNU AGPL 3.0. "
                "For this path, <b>Connect your PS5</b> inside SmoovPlay is the setup. A second installer should not be required. "
                "If you do install chiaki-ng by itself, use only %s and %s. The old streetpea/chiaki-ng address redirects there."
            ) % (A(SP_NOTICE, "NOTICE"), A(SP_LIC, "LICENSE"), A(CK_REPO, "its repository"), A(CK_REL, "its releases")),
        ],
        "fix_h": "Delay, picture, and fixes from the docs",
        "fix": [
            (
                "SmoovPlay's own timing in the v0.3.8 README, not a measurement of ours and not a GTA 6 session: about 36 ms at a 90 fps output and about 20 ms at 60, on top of Remote Play. "
                "In two live Ethernet sessions of a 30 fps PS5 game the medians were 35.4 ms and 35.8 ms. The 60 fps figure is from a recorded clip. "
                "About 22 ms of that is the wait while the in-between frames are shown. Press <b>L</b> for the project's delay test, which times a button all the way to the screen. "
                "The project points the result at driving, exploring, and story play."
            ),
            (
                "The stream arrives at 1080p, so the picture is a little softer than HDMI straight from the console. "
                "That 1080p is the Remote Play limit this project documents. It is not a measurement of the resolution the game renders at."
            ),
            (
                "HUD text over fast motion, very fast camera turns, and thin objects crossing each other can wobble. Press <b>I</b> to compare with the extra frames off. "
                "chiaki-ng holds the sound back by as long as the picture spends in SmoovPlay, so the two stay in step."
            ),
            (
                "A game already running at 60 passes through at 60, because there are no gaps to fill. "
                "A 30 fps game that dips freezes for a moment and jumps at each dip. <b>Dip smoothing</b> is Experimental, off by default, and the README says it adds about 17 to 50 ms and more graphics work, only while the game is dipping. "
                "This page is not claiming that GTA 6 dips, and it leaves Digital Foundry's specific drop counts out."
            ),
            (
                "On Wi-Fi, frames can arrive late and in bunches, which shows up as a hitch however fast the PC is. "
                "The README's advice is to plug the PS5 and the PC into the router."
            ),
            (
                "A black picture, or the PS5 saying the content can't be shown: <b>Settings → System → HDMI</b>, turn off <b>Enable HDCP</b>, connect again, and turn HDCP back on before video apps such as Netflix. "
                "If it is still black, press <b>Q</b>, then <b>Help → Copy diagnostics</b>, and paste that into a %s. Send that paste to the project, not to this site."
            ) % A(SP_REPO + "/issues", "SmoovPlay issue"),
        ],
        "know_h": "What is checked, and what is still open",
        "know_lead": "Read on 19 November 2026.",
        "checked_h": "Checked",
        "checked": [
            "Digital Foundry: a 30 fps target on PS5, PS5 Pro, Series X and Series S, no 40 or 60 mode, and a steadier 30 on PS5 Pro.",
            "PlayStation Blog, 10 November 2026: preload, a local-midnight launch on 19 November, and Pro picture claims (PSSR, ray-traced shadows). No frame-rate mode in that post.",
            "SmoovPlay v0.3.8 README, LICENSE, NOTICE, release notes, the project site, the compare page, and the how-it-works page: the setup, the hardware table, the keys, and the project's own timings.",
            "chiaki-ng's repository, listed on GitHub as AGPL-3.0, plus its documentation and releases. streetpea/chiaki-ng redirects to chiaki-ng/chiaki-ng.",
        ],
        "open_h": "Still open",
        "open": [
            "A real GTA 6 session on this path. We have not played the game on a console. The compare page captions its GTA VI clips as a simulated stream of Rockstar's trailer.",
            "Any latency or wobble number for GTA 6. The milliseconds above are the project's, from other sessions, including the Gotham Knights recording.",
            "AMD, Intel, Xbox, and capture cards beyond the Experimental labels in the README.",
            "A live 120 fps measurement. The README says none is published.",
            "A future patch that would add a 60 mode. Nothing we read announced one.",
        ],
        "faq_h": "Questions",
        "faq": [
            ("Does GTA 6 on PS5 render at 60 FPS with this?",
             "No. Digital Foundry found a 30 fps target and no 40 or 60 mode. SmoovPlay draws extra pictures on the PC between frames the console already sent. The game still renders and responds at its own rate."),
            ("I only have a PS5 and a TV. Does any of this apply?",
             "No. The extra frames are drawn on a Windows PC, and you watch them on that PC's monitor, with the controller paired to the PC. A TV plugged into the PS5 shows the console's own picture."),
            ("Is chiaki-ng another way to raise the frame rate?",
             "No. chiaki-ng is the Remote Play client. It carries the stream, the sound, and your buttons. It does not generate frames. Without SmoovPlay you are watching the 1080p stream the console sent."),
            ("Has this been tried on a real PS5 copy of GTA 6?",
             "Not by us. SmoovPlay's public GTA VI clips are Rockstar's trailer, An Extended Look, played as a simulated 1080p30 stream. The real PS5 recording on their compare page is Gotham Knights."),
            ("Will the controls feel faster?",
             "The project says no. Motion looks smoother, and the game still responds like 30 fps, a little later than Remote Play alone. Their note points this at driving, exploring, and story play rather than competitive matches."),
            ("Where is the real download, and is it free?",
             "SmoovPlay's own code is MIT. The project says the app is free, with no account, no ads, and no tracking, and that it only talks to GitHub for updates. chiaki-ng is AGPL-3.0. The Windows installer is an early unsigned build. Download SmoovPlay only from its GitHub Releases, and chiaki-ng only from its own repository and releases."),
        ],
        "src_h": "Sources",
        "src_lead": "Two kinds of claim. Digital Foundry measured consoles. The frame-generation numbers are what SmoovPlay reports about its own app.",
        "sources": [
            ("Independent measurement", [
                A(DF, "Digital Foundry: GTA 6 on PS5, PS5 Pro, Xbox Series X and Series S") + " — read 19 November 2026. Frame-rate target and the absence of a 40 or 60 mode. This page does not repeat their resolution figures or their specific dip counts.",
            ]),
            ("Official", [
                A(PSB, "PlayStation Blog, 10 November 2026: pre-load Grand Theft Auto VI on PS5") + " — preload, the 19 November local-midnight launch, PSSR and ray-traced shadows on PS5 Pro.",
            ]),
            ("What the projects say about themselves", [
                A(SP_README, "SmoovPlay README at tag v0.3.8") + ", " + A(SP_TAG, "release v0.3.8") + " (published 19 November 2026), " + A(SP_LIC, "LICENSE") + " (MIT), " + A(SP_NOTICE, "NOTICE") + " (chiaki-ng under AGPL-3.0).",
                A(SP_SITE, "smoovplay.github.io") + ", " + A(SP_COMPARE, "compare page") + " (trailer versus the Gotham Knights PS5 recording), " + A(SP_HOW, "how it works") + ".",
                A(CK_REPO, "chiaki-ng repository") + " (AGPL-3.0), " + A(CK_DOCS, "documentation") + ", " + A(CK_CONF, "configuration") + ", " + A(CK_REL, "releases") + ", " + A(CK_UPDATES, "release notes in the docs") + ".",
            ]),
        ],
        "related_h": "More GTA 6 tools",
        "related": [
            ("/gta-6/compatibility/", "Can My Console Run GTA 6?", "PS5, PS5 Pro and Xbox Series X|S, from official listings."),
            ("/gta-6/storage-check/", "GTA 6 Storage & Preload Check", "PlayStation's 212 GB free-space figure, checked against your drive."),
            ("/gta-6/editions/", "GTA 6 Editions Compared", "Standard and Ultimate, limited to what Take-Two has published."),
        ],
        "foot": (
            "BuffForge is an independent fan project. Not affiliated with Rockstar Games, Take-Two Interactive, Sony Interactive Entertainment, or the authors of SmoovPlay and chiaki-ng. "
            "Sources read 19 November 2026, when SmoovPlay's latest release was v0.3.8."
        ),
    }


def ru():
    return {
        "title": "GTA 6 на PS5 — 30 кадров: бесплатная открытая вставка кадров и её пределы — BuffForge",
        "desc": "GTA 6 на PS5 целится в 30 кадров, режима 40 или 60 нет. Как бесплатная открытая программа на Windows дорисовывает кадры из Remote Play и где этот путь кончается.",
        "h1": "GTA 6 на PS5 целится в 30 кадров: бесплатная вставка кадров и её пределы",
        "crumb": "Вставка кадров на PS5",
        "lede": "PS5 по-прежнему целится в 30 кадров. Компьютер на Windows может дорисовать картинки между ними — и только на своём мониторе.",
        "updated": "Проверено 19 ноября 2026 года. Релиз SmoovPlay, который мы читали в этот день: v0.3.8.",
        "note": (
            "Живую GTA 6 на приставке через эту схему мы не запускали, и у SmoovPlay нет опубликованной записи настоящей PS5 с GTA 6. "
            "Ролики GTA VI на %s — трейлер Rockstar An Extended Look, прогнанный как имитация потока Remote Play 1080p30. "
            "Запись с настоящей PS5 у проекта — Gotham Knights. Шаги ниже взяты из документации, которую мы читали 19 ноября 2026 года."
        ) % A(SP_COMPARE, "их странице сравнения"),
        "alt": "Официальный постер Grand Theft Auto VI: коллаж персонажей, техники и логотипа VI.",
        "cap": "Официальный постер. © Rockstar Games. Это не кадр из игры и не замер частоты.",
        "short_h": "Коротко",
        "short": [
            (
                "Если вы пришли включить в GTA 6 на PS5 родные 60 кадров, такого режима нет. "
                "%s, которое мы читали 19 ноября 2026 года, пишет: PS5, PS5 Pro, Xbox Series X и Series S целятся в 30 кадров, режима 40 или 60 нет ни на одной платформе. "
                "PS5 Pro держит эти 30 ровнее. Ровнее — это всё ещё 30."
            ) % A(DF, "Сравнение консолей Digital Foundry"),
            (
                "%s от 10 ноября 2026 года — про предзагрузку и старт в местную полночь 19 ноября. "
                "Про PS5 Pro там яснее картинка за счёт PSSR и трассированные тени. Отдельного режима с большей частотой кадров в этом тексте нет."
            ) % A(PSB, "Запись в блоге PlayStation"),
            (
                "Бесплатный способ меняет картинку на мониторе, а не частоту самой игры. Это %s — ранняя открытая программа для Windows. "
                "PS5 с включённой удалённой игрой отдаёт поток 1080p. Его принимает %s, открытый клиент Remote Play. "
                "Дальше видеокарта компьютера в SmoovPlay дорисовывает кадры моделью RIFE. "
                "Монитор 60 Гц может показать 60 картинок в секунду, 90 Гц — 90, 120 Гц и выше — до 120. "
                "На приставку ничего не ставится, и игра отвечает в своём прежнем темпе. "
                "Свой код SmoovPlay — MIT. Remote Play у него идёт через chiaki-ng, а это AGPL-3.0."
            ) % (A(SP_REPO, "SmoovPlay"), A(CK_REPO, "chiaki-ng")),
        ],
        "who_h": "Кому это подходит",
        "who_lead": "Схема работает, только когда картинка идёт на компьютер с Windows.",
        "fit_h": "Имеет смысл",
        "fit": [
            "Есть компьютер на Windows 10 или 11 и видеокарта NVIDIA GeForce RTX 30, 40 или 50 серии. Именно этот ряд SmoovPlay помечает как проверенный.",
            "Играть будете на мониторе этого компьютера, геймпад подключён к ПК, экран 60 Гц или быстрее.",
            "Нужна более плавная картинка в игре на 30 кадрах, и вы готовы к задержке потока плюс задержке вставки кадров.",
        ],
        "skip_h": "Лучше не начинать",
        "skip": [
            "Есть только PS5 и телевизор. Лишние кадры до экрана, воткнутого в приставку, не доходят.",
            "Нужно, чтобы сама игра рисовала и отвечала на 60. Цель остаётся 30 кадров — это замер Digital Foundry.",
            "Расчёт на AMD, Intel, приложение Xbox или карту захвата как на тот же готовый путь. У проекта это Experimental.",
        ],
        "flow_h": "30 настоящих кадров, потом лишние картинки",
        "flow_lead": "Четыре остановки. Игра — первая. Монитор только показывает.",
        "flow_aria": "PS5 отдаёт настоящие кадры с целью 30. chiaki-ng несёт поток Remote Play 1080p. SmoovPlay на Windows дорисовывает промежуточные кадры. Монитор ПК показывает 60, 90 или до 120 картинок.",
        "flow": [
            ("PS5", "Настоящие кадры. Цель игры — 30 в секунду."),
            ("Remote Play", "chiaki-ng несёт поток 1080p. Лишних кадров ещё нет."),
            ("Windows", "SmoovPlay дорисовывает промежуточные кадры моделью RIFE."),
            ("Монитор ПК", "60, 90 или до 120 картинок — по герцовке экрана."),
        ],
        "flow_cap": "Приставка не начинает рисовать в 60. Лишние картинки появляются на компьютере, уже после того как поток пришёл.",
        "send_h": "Что отдаёт PS5",
        "send_p": "Настоящие кадры с целью 30. Отклик остаётся темпом игры, а поток добавляет своё ожидание.",
        "show_h": "Что показывает монитор",
        "show_p": "60 картинок на экране 60 Гц, 90 на 90 Гц и до 120 только если экран 120 Гц или быстрее. Каждая лишняя картинка строится по настоящим кадрам с обеих сторон.",
        "hw_h": "Что нужно иметь",
        "hw_lead": (
            "Таблица из %s, тег v0.3.8. Где проект пишет Tested или Experimental, это слово оставлено как есть."
        ) % A(SP_README, "README SmoovPlay"),
        "hw": [
            ("Компьютер", "Windows 10 или 11, 64 бита. 8 ГБ памяти. 12 ГБ свободных на время установки."),
            ("Видеокарта",
             "NVIDIA GeForce RTX 30, 40 или 50 серии — у проекта это Tested. Названные машины: RTX 4070 Ti SUPER на Windows 10 и RTX 5070 Ti участника на Windows 11. RTX 20 и ноутбуки пока не проверяли. "
             "AMD Radeon и Intel Arc — Experimental, через DirectML. Проект пишет, что этот путь примерно в 1,7 раза медленнее и ещё не встречался с живой игрой на настоящей карте AMD или Intel."),
            ("Приставка",
             "PS5 с включённой удалённой игрой. Это проверенный путь. Карта захвата или картинка из окна другой программы — Experimental."),
            ("Сеть",
             "Кабель в приставку и в компьютер либо Wi-Fi 5 или 6 ГГц. Карте захвата сеть не нужна. В README ровнее всего именно кабель."),
            ("Экран",
             "Любая герцовка: 60 Гц дают 60 кадров, 90 Гц — 90, 120 Гц и выше — до 120. G-Sync или FreeSync помогают, так пишет README."),
            ("Где вы сидите",
             "Геймпад на компьютере. Смотрите в монитор ПК. Телевизор, подключённый к PS5, показывает картинку самой приставки."),
            ("На PS5", "Ничего ставить не нужно."),
        ],
        "hw_after": (
            "В строке Experimental про карту захвата README называет AVerMedia Live Gamer 4K (GC573) одного игрока: с 0.3.1 она работает, звук на 0.3.2 всё ещё ждут подтверждения. "
            "Остальные карты гоняли на записях вместо живой карты. Приложение Xbox узнаётся по отчёту игрока, живой поток с Xbox не подтверждён. "
            "Если нужен путь, который проект сам называет проверенным, это Remote Play с PS5."
        ),
        "setup_h": "Как включить",
        "setup_lead": (
            "Названия кнопок — из %s и со %s. "
            "Если на вашей сборке подпись уже другая, верьте тексту в программе. v0.3.8 вышел 19 ноября 2026 года, релиз ранний."
        ) % (A(SP_README, "README v0.3.8"), A(CK_CONF, "страницы настройки chiaki-ng")),
        "steps": [
            (
                "На PS5 откройте <b>Settings → System → Remote Play</b> и включите <b>Enable Remote Play</b>. "
                "Так пункт записан в документации chiaki-ng: удалённая игра должна быть включена. Русские подписи меню на консоли могут отличаться, ищите тот же раздел. "
                "Чтобы приставка просыпалась из покоя, там же указан путь <b>Settings → System → Power Saving → Features Available in Rest Mode</b>, "
                "пункты <b>Stay Connected to the Internet</b> и <b>Enable Turning on PS5 from Network</b>. "
                "PS5 и компьютер должны быть в одной домашней сети."
            ),
            (
                "На компьютере скачайте <b>SmoovPlay-Setup.exe</b> только с %s. "
                "Тег, который мы читали, — %s. Установщик ранний и без подписи кода, поэтому браузер или Windows могут предупредить. "
                "SmartScreen, антивирус и остальную защиту оставьте как есть. "
                "Сверить файл можно по SHA-256 с хешем на той же странице релизов. Команда из README в PowerShell — <b>Get-FileHash</b> по файлу установщика. "
                "Рекламу в поиске, перезаливки и любую страницу, которая просит ввести пароль PSN, пропускайте."
            ) % (A(SP_REL, "официальной страницы релизов"), A(SP_TAG, "v0.3.8")),
            (
                "Запустите этот установщик. По словам проекта, установка занимает 10–20 минут, ставится для текущего пользователя Windows и не просит права администратора. "
                "Она проверяет компьютер и качает около 5 ГБ — Python, PyTorch и NVIDIA TensorRT — с сайтов этих проектов. "
                "В конце сама выбирает настройки по короткому тесту видеокарты и экрана."
            ),
            (
                "В программе пройдите <b>Connect your PS5</b>. Если удалённая игра ещё выключена, включите её, войдите в PSN внутри chiaki-ng и зарегистрируйте приставку. "
                "Проект отводит на это около пяти минут, один раз. Вход остаётся в этом клиенте и на странице Sony — тот же род шага, что в приложении Remote Play от Sony. "
                "BuffForge не спрашивает пароль, идентификатор аккаунта и ссылку редиректа. "
                "Если клиент просит код Remote Play, приставка показывает его в <b>Settings → System → Remote Play → Link Device</b>. Код вводите в клиент. "
                "Когда экраны не совпадают с этими подписями, откройте %s."
            ) % A(CK_CONF, "страницу настройки chiaki-ng"),
            (
                "Подключите геймпад к компьютеру так, как он обычно сопрягается. Смотреть будете в монитор ПК. "
                "Телевизор, воткнутый в PS5, продолжит показывать картинку самой приставки."
            ),
            (
                "Нажмите <b>Play</b>. В окне видео README даёт <b>M</b> — меню на ходу, <b>F</b> — полный экран (так у них меньше всего задержка), "
                "<b>I</b> — выключить и включить лишние кадры, <b>L</b> — тест задержки, <b>Esc</b> или <b>Q</b> — стоп. "
                "С v0.3.8 пункт <b>Capture card resolution</b> серый, пока источник правда не карта захвата: поток PS5 Remote Play не выше 1080p. "
                "<b>Minimise chiaki-ng</b> серый, пока источник не PS5 Remote Play. Серые 1440p или 4K — это не спрятанный поток выше 1080p."
            ),
        ],
        "keys_lead": "Клавиши окна видео из README. Геймпад играет. Клавиатура управляет SmoovPlay.",
        "keys": [
            ("M", "Меню: все настройки, на ходу."),
            ("F", "Полный экран. В README это наименьшая задержка."),
            ("I", "Лишние кадры выкл и вкл, чтобы сравнить."),
            ("L", "Тест задержки для PS5 Remote Play."),
            ("Esc или Q", "Стоп."),
        ],
        "keys_after": (
            "На экспериментальном пути «окно программы» клавиатуру держит другое приложение, и README переносит эти сочетания на Ctrl+Alt. "
            "Обновление из самой программы должно нести подпись SmoovPlay, иначе оно не запустится. С 0.3.1 кнопка <b>Check for updates</b> стоит в боковой панели лаунчера."
        ),
        "start_h": "С чего начать, а не «лучший пресет»",
        "start_lead": (
            "Оставьте то, что установщик только что выбрал. <b>Auto-detect</b> на странице Settings повторяет короткий тест, если вы сменили монитор. "
            "В этой таблице нет настроек GTA 6, которые мы замерили. Через этот путь мы в игру не играли."
        ),
        "start": [
            ("Частота показа",
             "Оставьте выбор Auto-detect. 60 Гц показывают 60, 90 Гц — 90. «До 120» требует экран 120 Гц или быстрее. "
             "README пишет, что вживую показаны и замерены 60 и 90. На 120 рисуются три промежуточных кадра тем же способом, а живого замера или ролика на 120 fps проект ещё не публиковал."),
            ("30 выглядят рвано",
             "Если игра, запертая на 30, выглядит неровно, поставьте <b>Settings → Smoothness → Game frame rate</b> в <b>30 fps</b>. "
             "На Auto проект пишет, что с версии 0.3.4 проводной поток 30 кадров обычно узнаётся по картинке, но неподвижная или тёмная сцена всё ещё может обмануть."),
            ("Один генератор",
             "Пока работают SmoovPlay и chiaki-ng, NVIDIA Smooth Motion, AMD Fluid Motion Frames и Lossless Scaling должны быть выключены. "
             "README называет это конфликтом. Когда вы закроете программу, остальные игры она не трогает."),
            ("Модель",
             "Оставайтесь на RIFE. Это модель, которую проект запускает по умолчанию. NVIDIA Video Frame Generation — отдельная необязательная загрузка, в состав SmoovPlay не входит и предлагается только на RTX 40 и 50 после принятия лицензии NVIDIA."),
        ],
        "chiaki_h": "chiaki-ng только несёт поток",
        "chiaki": [
            (
                "chiaki-ng принимает Remote Play, играет звук и отправляет нажатия обратно. "
                "На %s у SmoovPlay это названо транспортом: небольшой отвод кадров (frame tap) отдаёт каждый декодированный кадр дальше, а лишние кадры рисует уже SmoovPlay. "
                "%s описывает настройку Remote Play. Режима генерации кадров там нет. Сама по себе chiaki-ng показывает поток, который прислала приставка."
            ) % (A(SP_HOW, "странице «как это работает»"), A(CK_DOCS, "Документация chiaki-ng")),
            (
                "В %s на теге v0.3.8 сказано: свой код — MIT (%s), а пропатченная chiaki-ng остаётся отдельной программой под GNU AGPL 3.0. "
                "Для этого пути хватает <b>Connect your PS5</b> внутри SmoovPlay. Второй установщик не нужен. "
                "Если chiaki-ng всё же ставите отдельно, берите её только из %s и %s. Старый адрес streetpea/chiaki-ng перенаправляет туда."
            ) % (A(SP_NOTICE, "NOTICE SmoovPlay"), A(SP_LIC, "LICENSE"), A(CK_REPO, "её репозитория"), A(CK_REL, "её релизов")),
        ],
        "fix_h": "Задержка, картинка и что делать по документации",
        "fix": [
            (
                "Собственный замер SmoovPlay в README v0.3.8, не наш и не сессия GTA 6: около 36 мс при выводе 90 кадров и около 20 мс при 60, сверх задержки самого Remote Play. "
                "В двух живых сессиях по кабелю на игре PS5 в 30 кадров медианы были 35,4 и 35,8 мс. Цифра для 60 кадров взята с записанного ролика. "
                "Около 22 мс из этого — ожидание, пока показываются промежуточные кадры. Клавиша <b>L</b> запускает их тест задержки: от нажатия кнопки до картинки на экране. "
                "Сами они относят это к езде, прогулке и сюжету."
            ),
            (
                "Поток приходит в 1080p, поэтому картинка чуть мягче, чем HDMI прямо с приставки. "
                "Эти 1080p — предел Remote Play, который описывает проект. Это не замер разрешения, в котором игра рисует кадр."
            ),
            (
                "Текст интерфейса на быстром движении, очень резкий поворот камеры и тонкие предметы, которые пересекаются, могут подрагивать. <b>I</b> сравнивает картинку без лишних кадров. "
                "chiaki-ng задерживает звук на то время, которое картинка проводит в SmoovPlay, чтобы они шли вместе."
            ),
            (
                "Игра, которая уже идёт в 60, проходит как есть: заполнять нечего. "
                "Игра на 30, которая проседает, на каждом провале на миг замирает и прыгает. <b>Dip smoothing</b> — Experimental, по умолчанию выключен, и README пишет, что он добавляет примерно 17–50 мс и больше работы видеокарте, только пока игра проседает. "
                "Мы не утверждаем, что GTA 6 проседает, и конкретные цифры провалов Digital Foundry сюда не переносим."
            ),
            (
                "По Wi-Fi кадры могут приходить поздно и пачками — это видно как заминку, какой бы ни была видеокарта. "
                "Совет README: воткнуть и PS5, и компьютер в роутер."
            ),
            (
                "Чёрный экран или сообщение PS5, что содержимое нельзя показать: <b>Settings → System → HDMI</b>, выключите <b>Enable HDCP</b>, подключитесь снова и включите HDCP обратно перед видеоприложениями вроде Netflix. "
                "Если экран всё ещё чёрный, нажмите <b>Q</b>, затем <b>Help → Copy diagnostics</b> и вставьте это в %s. Эту вставку отправляют проекту, не на наш сайт."
            ) % A(SP_REPO + "/issues", "issue SmoovPlay"),
        ],
        "know_h": "Что сверено и что ещё открыто",
        "know_lead": "Читали 19 ноября 2026 года.",
        "checked_h": "Сверено",
        "checked": [
            "Digital Foundry: цель 30 кадров на PS5, PS5 Pro, Series X и Series S, режима 40 или 60 нет, на PS5 Pro эти 30 ровнее.",
            "Блог PlayStation, 10 ноября 2026: предзагрузка, старт в местную полночь 19 ноября, заявления про картинку Pro (PSSR и трассированные тени). Режима частоты кадров в том тексте нет.",
            "README, LICENSE, NOTICE, заметки релиза v0.3.8, сайт проекта, страница сравнения и страница «как это работает»: установка, таблица железа, клавиши и собственные замеры проекта.",
            "Репозиторий chiaki-ng, на GitHub указан как AGPL-3.0, плюс документация и релизы. streetpea/chiaki-ng перенаправляет на chiaki-ng/chiaki-ng.",
        ],
        "open_h": "Пока открыто",
        "open": [
            "Живая сессия GTA 6 на этом пути. Мы не играли в неё на приставке. Подпись к роликам GTA VI на странице сравнения — имитация потока из трейлера Rockstar.",
            "Любая цифра задержки или дрожания именно для GTA 6. Миллисекунды выше — замеры проекта на других сессиях, включая запись Gotham Knights.",
            "AMD, Intel, Xbox и карты захвата дальше пометки Experimental в README.",
            "Живой замер 120 кадров. README пишет, что его не публиковали.",
            "Будущий патч с режимом 60. В прочитанном такого объявления нет.",
        ],
        "faq_h": "Вопросы",
        "faq": [
            ("Это откроет 60 кадров в GTA 6 на PS5?",
             "Нет. У Digital Foundry цель — 30 кадров, режима 40 или 60 нет. SmoovPlay дорисовывает картинки на компьютере между кадрами, которые приставка уже отправила. Игра по-прежнему рисует и отвечает в своём темпе."),
            ("У меня только PS5 и телевизор. Мне это подойдёт?",
             "Нет. Лишние кадры рисуются на компьютере с Windows, и смотреть их нужно на мониторе этого компьютера, геймпад подключён к ПК. Телевизор, воткнутый в PS5, показывает картинку самой приставки."),
            ("chiaki-ng — это второй способ поднять частоту?",
             "Нет. chiaki-ng — клиент Remote Play. Она несёт поток, звук и нажатия. Кадры она не генерирует. Без SmoovPlay вы смотрите поток 1080p, который прислала приставка."),
            ("Это проверяли на настоящей GTA 6 с PS5?",
             "Мы — нет. Публичные ролики GTA VI у SmoovPlay — трейлер Rockstar An Extended Look, прогнанный как имитация потока 1080p30. Запись с настоящей PS5 на их странице сравнения — Gotham Knights."),
            ("Управление станет быстрее?",
             "Проект пишет, что нет. Движение выглядит плавнее, а игра всё ещё отвечает как 30 кадров, чуть позже, чем один Remote Play. Сами они относят это к езде, прогулке и сюжету, а не к соревновательной игре."),
            ("Где настоящий файл и это бесплатно?",
             "Свой код SmoovPlay — MIT. Проект пишет, что программа бесплатная, без аккаунта, рекламы и слежки, и что она обращается к GitHub только за обновлениями. chiaki-ng — AGPL-3.0. Установщик Windows — ранняя сборка без подписи. SmoovPlay качайте только с её релизов на GitHub, chiaki-ng — только из её репозитория и релизов."),
        ],
        "src_h": "Источники",
        "src_lead": "Два разных рода утверждений. Digital Foundry мерили приставки. Цифры вставки кадров — это то, что SmoovPlay сообщает о своей программе.",
        "sources": [
            ("Независимый замер", [
                A(DF, "Digital Foundry: GTA 6 на PS5, PS5 Pro, Xbox Series X и Series S") + " — читали 19 ноября 2026 года. Цель по кадрам и отсутствие режима 40 или 60. Разрешение рендера и конкретные цифры просадок оттуда на эту страницу не переносились.",
            ]),
            ("Официальное", [
                A(PSB, "Блог PlayStation, 10 ноября 2026: предзагрузка Grand Theft Auto VI на PS5") + " — предзагрузка, старт 19 ноября в местную полночь, PSSR и трассированные тени на PS5 Pro.",
            ]),
            ("Что проекты говорят о себе", [
                A(SP_README, "README SmoovPlay на теге v0.3.8") + ", " + A(SP_TAG, "релиз v0.3.8") + " (опубликован 19 ноября 2026), " + A(SP_LIC, "LICENSE") + " (MIT), " + A(SP_NOTICE, "NOTICE") + " (chiaki-ng под AGPL-3.0).",
                A(SP_SITE, "smoovplay.github.io") + ", " + A(SP_COMPARE, "страница сравнения") + " (трейлер против записи Gotham Knights с PS5), " + A(SP_HOW, "как это работает") + ".",
                A(CK_REPO, "Репозиторий chiaki-ng") + " (AGPL-3.0), " + A(CK_DOCS, "документация") + ", " + A(CK_CONF, "настройка") + ", " + A(CK_REL, "релизы") + ", " + A(CK_UPDATES, "заметки о релизах в документации") + ".",
            ]),
        ],
        "related_h": "Другие инструменты по GTA 6",
        "related": [
            ("/ru/gta-6/compatibility/", "На чём можно играть в GTA 6?", "PS5, PS5 Pro и Xbox Series X|S — по официальным спискам."),
            ("/ru/gta-6/storage-check/", "Проверка места под GTA 6", "Цифра PlayStation: не менее 212 ГБ свободного места."),
            ("/ru/gta-6/editions/", "Сравнение изданий GTA 6", "Standard и Ultimate — только то, что опубликовала Take-Two."),
        ],
        "foot": (
            "BuffForge — независимый фанатский проект. Не связан с Rockstar Games, Take-Two Interactive, Sony Interactive Entertainment и авторами SmoovPlay и chiaki-ng. "
            "Источники читали 19 ноября 2026 года, когда последним релизом SmoovPlay был v0.3.8."
        ),
    }


def guide_body(lang):
    c = en() if lang == "en" else ru()
    hub = "/gta-6/" if lang == "en" else "/ru/gta-6/"
    parts = [
        '<main id="main" class="wrap narrow">',
        crumbs_html(lang, [("GTA 6", hub), (c["crumb"], None)]),
        '<h1 class="page-h1">%s</h1>' % c["h1"],
        '<p class="page-lede">%s</p>' % c["lede"],
        '<p class="intro-note">%s</p>' % c["updated"],
        '<div class="note-box amber"><p>%s</p></div>' % c["note"],
        '<div class="prose">',
        '<h2 class="sec">%s</h2>' % c["short_h"],
    ]
    parts.extend("<p>%s</p>" % p for p in c["short"])
    parts.append(
        (
            '<figure class="shot"><img src="/assets/games/gta-6-wide.jpg" width="1200" height="630" '
            'alt="%s" decoding="async"><figcaption>%s</figcaption></figure>'
        ) % (c["alt"], c["cap"])
    )
    parts += [
        '<h2 class="sec">%s</h2>' % c["who_h"],
        "<p>%s</p>" % c["who_lead"],
        _cards(c["fit_h"], c["fit"], c["skip_h"], c["skip"]),
        '<h2 class="sec">%s</h2>' % c["flow_h"],
        "<p>%s</p>" % c["flow_lead"],
        _flow(c),
        _pair(c["send_h"], "<p>%s</p>" % c["send_p"], c["show_h"], "<p>%s</p>" % c["show_p"]),
        '<h2 class="sec">%s</h2>' % c["hw_h"],
        "<p>%s</p>" % c["hw_lead"],
        _table(c["hw"]),
        "<p>%s</p>" % c["hw_after"],
        '<h2 class="sec">%s</h2>' % c["setup_h"],
        "<p>%s</p>" % c["setup_lead"],
        _ol(c["steps"]),
        "<p>%s</p>" % c["keys_lead"],
        _table(c["keys"]),
        "<p>%s</p>" % c["keys_after"],
        '<h2 class="sec">%s</h2>' % c["start_h"],
        "<p>%s</p>" % c["start_lead"],
        _table(c["start"]),
        '<h2 class="sec">%s</h2>' % c["chiaki_h"],
    ]
    parts.extend("<p>%s</p>" % p for p in c["chiaki"])
    parts.append('<h2 class="sec">%s</h2>' % c["fix_h"])
    parts.extend("<p>%s</p>" % p for p in c["fix"])
    parts += [
        '<h2 class="sec">%s</h2>' % c["know_h"],
        "<p>%s</p>" % c["know_lead"],
        "<h3>%s</h3>" % c["checked_h"],
        _ul(c["checked"]),
        "<h3>%s</h3>" % c["open_h"],
        _ul(c["open"]),
        '<section class="faq" id="faq"><h2 class="sec">%s</h2>%s</section>'
        % (c["faq_h"], _faq(c["faq"])),
        '<h2 class="sec" id="sources">%s</h2>' % c["src_h"],
        "<p>%s</p>" % c["src_lead"],
        _sources(c["sources"]),
        "</div>",
        '<section class="related"><h2>%s</h2><div class="related-grid">%s</div></section>'
        % (c["related_h"], _related(c["related"])),
        '<p class="data-line">%s</p>' % c["foot"],
        "</main>",
    ]
    return "\n".join(parts), c


def guide_page(lang):
    body, c = guide_body(lang)
    canon = "/gta-6/ps5-frame-interpolation/" if lang == "en" else "/ru/gta-6/ps5-frame-interpolation/"
    alt = {
        "en": "/gta-6/ps5-frame-interpolation/",
        "ru": "/ru/gta-6/ps5-frame-interpolation/",
    }
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
            "dateModified": "2026-11-19",
            "author": {"@type": "Organization", "name": "BuffForge", "url": BASE},
            "publisher": {"@type": "Organization", "name": "BuffForge", "url": BASE},
            "mainEntityOfPage": {"@type": "WebPage", "@id": BASE + canon},
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in c["faq"]
            ],
        },
    ]
    return page(
        lang, c["title"], c["desc"], canon, alt, body,
        jsonld=jl, switch_path=alt["ru" if lang == "en" else "en"],
        games=("gta-6",),
    )
