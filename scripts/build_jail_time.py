#!/usr/bin/env python3
"""ROB RUN Jail Time & Authority Calculator (EN + RU).

Run:  cd <repo root> && python3 scripts/build_jail_time.py
Rebuild of the user-supplied demo (2026-11-24) in the Daylight Forge light
system. The interactive logic is the demo's (wipe calculator, $/hr farming
routes, 20 unlock milestones, goal tracker + wipe log, guide + FAQ) — only
the styling is the site's own (.jt-* classes in assets/site.css), plus the
verified fixes listed below. Chart.js is dropped; the $/hr chart is plain
CSS bars. No Google Fonts.

Verified fixes vs the demo (facts checked 2026-11-24):
- The 6 jail-gated unlocks the demo omits are added (30 Small Security
  Cabinet, 75 Racing Rotor, 105 Alarm System, 140 Medium Security Cabinet,
  225 Steel Plate, 500 Large Security Cabinet); the roadmap covers all 20.
- The unverified "(requires MC-10 Mk1)" note on CB45 Mk1 is dropped.
- Heists and Clan Battles are labelled "est." in the rate cell: Timesaver
  gives per-run / per-objective figures, not per-hour; $1M/h and $900K/h
  assume ~1 run/objective per hour. Maxed Grow Room $500K+/h is one
  player's estimate — also "est.". Grow Room 6 Uncommon $129.6K/h is
  marked Disputed (Timesaver's own label).
- One-line caveat in the guide: some guides (robrun.info, Indiatimes)
  list a 1-year starting sentence on top of the $500K formula; this
  calculator follows the Steam breakdown thread and robrunwiki (no
  automatic +1 year), capped at 40 years per server.
- The 40-year/24h and 1,200-year caps are community-tracked figures
  (robrun.info, post-Nov 17 patch); Kefir confirmed only that day +
  overall limits exist, never the numbers. The attribution stays visible.
- Review date 24 November 2026.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import (EMAIL, breadcrumb_jsonld, crumbs_html, page)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://buffforge.com"
CANON = {"en": "/rob-run/jail-time-authority-calculator/",
         "ru": "/ru/rob-run/jail-time-authority-calculator/"}

KEFIR_URL = "https://kefirgames.helpshift.com/hc/en/14-rob-run/faq/1346-what-is-the-federal-raid-wipe/"
WIKI_URL = "https://robrunwiki.net/jail-time/"
TS_JAIL_URL = "https://timesaver.gg/blog/rob-run-jail-time"
TS_MONEY_URL = "https://timesaver.gg/blog/rob-run-how-to-make-money-fast"
ROBRUNGAME_URL = "https://robrungame.com/faq/rob-run-wipe-schedule/"

JT = {
    "en": {
        "title": "ROB RUN Jail Time & Authority Calculator (2026) | BuffForge",
        "desc": ("Calculate ROB RUN Jail Time and Authority progress, compare solo "
                 "and squad farming routes per hour, check 40-year wipe caps, and "
                 "track unlock milestones."),
        "h1": "ROB RUN Jail Time & Authority Calculator",
        "canonical": "/rob-run/jail-time-authority-calculator/",
        "card_title": "Jail Time & Authority Calculator",
        "eyebrow": "ROB RUN / Interactive game tools",
        "lede": ("Calculate your Federal Raid wipe sentence, estimate hours and "
                 "wipe cycles to your next Authority unlock, compare solo and squad "
                 "farming routes, and track permanent progression \u2014 all "
                 "client-side with zero login."),
        "pills": ["Formula: $500,000 = +1 Year", "Cap: 40 Yrs / Server & 24h",
                  "Max Authority: 1,200 Years", "Lenny's Debt: $1M = +10 Years"],
        "kpi1": "Target Progress",
        "kpi2": "Projected This Wipe",
        "kpi3": "Total Assets Needed",
        "kpi4": "Est. Farm Time",
        "tab1": "Progress & Wipe Calculator",
        "tab2": "Farming Routes & $/hr",
        "tab3": "Authority Unlocks & Rules",
        "tab4": "Goal Tracker",
        "calc_h": "Your Current Stats & Target",
        "reset": "Reset defaults",
        "cur_label": "Current Jail Time / Authority (Years)",
        "cur_hint": "Carries over every wipe \u00b7 Max 1,200 yrs",
        "tgt_label": "Target Authority Level (Years)",
        "quick_label": "Quick-pick key Authority milestones:",
        "assets_label": "Expected Server Assets at Wipe ($)",
        "assets_hint": ("Counts clean bank cash, items, vehicles, land plots, real "
                        "estate, unlocked research, and clan/bribe spend."),
        "lenny_title": "Include Lenny's $1M Debt",
        "lenny_sub": "One-time +10 yrs (5x value, stacks over 40-yr cap)",
        "daily_label": "Daily Playtime",
        "method_label": "Farming Method",
        "brk_h": "Wipe Breakdown & Strategy",
        "cap_label": "Server 40-Year Cap Progress",
        "kv1": "Total Authority After Wipe",
        "kv2": "Remaining After This Wipe",
        "kv3": "Min Wipe Cycles (40-yr Cap)",
        "kv4": "Active Route Time / Year",
        "kv5": "Next Unlock Milestone",
        "meth_h": "ROB RUN Farming Routes: Yield vs. Jail Time Cost",
        "meth_sub": ("Converted at $500,000 = +1 Year Jail Time \u00b7 Click "
                     "\u201cUse Route\u201d to update your ETA above."),
        "filter_all": "All Routes",
        "filter_noplot": "No Plot Needed",
        "filter_solo": "Solo Friendly",
        "filter_squad": "Squad / Clan",
        "bench_label": "Contraband Workbenches:",
        "grow_label": "Grow Room Setup:",
        "bars_h": "Estimated Hourly Revenue by Playstyle (USD / Hour)",
        "bars_src": "Source: Timesaver.gg & robrun.info (Nov 2026)",
        "th1": "Playstyle Route",
        "th2": "Est. $/Hour",
        "th3": "Hrs / +1 Year",
        "th4": "Hrs for 40-Yr Cap",
        "th5": "Requirements & Risk",
        "th6": "Action",
        "unlock_h": "Authority Unlock Roadmap (1 to 1,200 Years)",
        "unlock_sub": ("All 20 jail-gated unlocks, 1\u20131,200 years. Tattoos are "
                       "claimed from the Prison Tattoo Artist; weapons and gear "
                       "unlock in Shipments & Research."),
        "conv_h": "Federal Raid Wipe: Converts vs. Keeps",
        "conv_ok": "Converts to Jail Time",
        "conv_warn": "Kept Permanently",
        "conv_list": ["Clean banked cash", "Inventory & stash items",
                      "Vehicles, houses & land plots",
                      "Unlocked research / Shipments", "Clan & bribe spending"],
        "keep_list": ["Accumulated Jail Time / Authority",
                      "All tattoos & cosmetics", "B-Coin balance",
                      "Character appearance & name",
                      "Tutorial progress & settings"],
        "rules_h": "Key Patch Rules (Nov 17, 2026)",
        "rules": [
            ("<b>No early surrender needed:</b> Your assets convert "
             "automatically during the 7-day wipe, even offline."),
            ("<b>Cop arrests give 0 years:</b> Only Federal Raids, Federal "
             "Surrender, or Lenny's debt grant Jail Time."),
            ("<b>Launder Dirty Cash first:</b> Official wipe notes explicitly "
             "list Clean Money \u2014 unlaundered cash is unconfirmed and "
             "stealable."),
        ],
        "trk_h": "Saved Authority Goals",
        "trk_sub": ("Stored locally in your browser. Syncs live with your "
                    "current Jail Time."),
        "trk_add": "+ Add Current Target",
        "trk_empty_b": "No goals tracked yet",
        "trk_empty_p": ("Click \u201c+ Add Current Target\u201d to pin your next "
                        "weapon, tattoo, or Silence Mask milestone."),
        "log_h": "Log Wipe / Surrender Payout",
        "log_sub": "Automatically adds earned years to your Current Jail Time.",
        "log_years": "Years Earned",
        "log_assets": "Assets Converted ($, optional)",
        "log_note": "Server / Route Note",
        "log_note_ph": "e.g. EU Wipe #2 \u00b7 Store runs + Grow Room",
        "log_submit": "Log Wipe & Update Total",
        "hist_h": "Wipe History Log",
        "hist_clear": "Clear all",
        "hist_empty": "No wipe logs recorded yet.",
        "guide_h": "How ROB RUN Jail Time & Authority Work (2026 Guide)",
        "guide_p1": ("In <b>ROB RUN</b>, there is no traditional XP bar. Every "
                     "seven days, the <b>Federal Raid</b> wipes all plots, bases, "
                     "weapons, vehicles, and cash on your server and converts that "
                     "wealth into permanent <b>Jail Time</b> \u2014 which directly "
                     "equals your <b>Authority</b> level."),
        "guide_h3a": "The $500,000-Per-Year Conversion Formula & Caps",
        "guide_p2": ("Based on community testing across Steam discussions and "
                     "game-data wikis, every <b>$500,000</b> in confiscated assets "
                     "awards <b>+1 year</b> of Jail Time (rounded down), capped at "
                     "<b>40 years per server</b> (~$20,000,000 in assets). Following "
                     "Kefir's November 17, 2026 patch, community trackers also list "
                     "a <b>40 years per 24-hour daily limit</b> and a "
                     "<b>1,200-year overall account cap</b>."),
        "caveat": ("<b>Note on the +1 year:</b> some guides (robrun.info, "
                   "Indiatimes) list a 1-year starting sentence on top of the "
                   "$500K formula. This calculator follows the Steam breakdown "
                   "thread and robrunwiki (no automatic +1 year), capped at 40 "
                   "years per server."),
        "guide_h3b": "Why Lenny's $1,000,000 Debt Is the Fastest Early Boost",
        "guide_p3": ("Paying off Lenny's $1,000,000 debt awards the New Chapter "
                     "skin plus a one-time <b>+10 years of Jail Time</b> that "
                     "stacks on top of the 40-year server cap. At <b>$100,000 per "
                     "year</b>, it is <b>5x more efficient</b> than standard "
                     "Federal Raid asset conversion."),
        "guide_h3c": "Data Sources & Review Date",
        "sources": [
            ("Kefir ROB RUN Help Center \u2014 Federal Raid (Wipe) FAQ",
             KEFIR_URL, "official carry-over rules"),
            ("ROB RUN Wiki \u2014 Jail Time & Authority Unlocks",
             WIKI_URL, "unlock thresholds & Lenny's debt stacking"),
            ("Timesaver.gg \u2014 ROB RUN Jail Time & Nov 17 Patch Limits",
             TS_JAIL_URL, "40/day & 1,200 total caps \u2014 community-tracked"),
            ("Timesaver.gg \u2014 ROB RUN Money Methods Ranked (Nov 2026)",
             TS_MONEY_URL, "verified $/hr benchmarks"),
            ("robrungame.com \u2014 ROB RUN Wipe Schedule",
             ROBRUNGAME_URL, "unlock table, game config 0.7.0"),
        ],
        "faq_h": "Frequently Asked Questions",
        "faq": [
            ("How is Jail Time calculated at the Federal Raid?",
             "Players report 1 year of Jail Time per $500,000 of confiscated "
             "server assets, rounded down, up to 40 years ($20M) per server cycle."),
            ("Do I need to surrender to the Feds before the wipe?",
             "No. Your server assets convert automatically during the 7-day "
             "Federal Raid wipe even while offline. Early Federal Surrender is "
             "mainly used to switch servers immediately."),
            ("What is the fastest solo route to farm Authority?",
             "Without a plot, solo Store Runs sold to the Fence average "
             "~$200,000/hr (~2.5 hrs/year). Once you own a plot, a maxed Grow "
             "Room can exceed $500,000/hr if defended against base raids."),
            ("Does getting arrested by a player cop give Jail Time?",
             "No. Player police arrests confiscate your bag loot but grant 0 "
             "Jail Time. Only Federal Raid wipes, Federal Surrender, and "
             "Lenny's $1M debt add permanent Authority."),
            ("What is the highest Authority reward in ROB RUN?",
             "On the prison Tattoo Artist \u201cTrust No One\u201d track, the final "
             "cosmetic reward is the legendary Silence Mask at 800 Authority. "
             "In Shipments, the DRM-14 Mk3 unlocks at 1,000 years."),
        ],
        "research": (
            "Reviewed 24 November 2026. Based on published game guides; details "
            "can change with patches and discoveries. Sources: "
            "<a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">Kefir Federal Raid (Wipe) FAQ</a>, "
            "<a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">ROB RUN Wiki: Jail Time</a>, "
            "<a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">Timesaver.gg: Jail Time & Nov 17 Limits</a>, "
            "<a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">Timesaver.gg: Money Methods Ranked</a>, "
            "<a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">robrungame.com: Wipe Schedule</a>. "
            "BuffForge is an independent fan-made tools site and is not affiliated "
            "with Kefir or Valve. Spotted a mistake? Email "
            "<a href=\"mailto:%s\">%s</a>." % (KEFIR_URL, WIKI_URL, TS_JAIL_URL, TS_MONEY_URL, ROBRUNGAME_URL, EMAIL, EMAIL)),
        "webapp_desc": ("Interactive ROB RUN calculator for Jail Time, Authority "
                        "unlocks, Federal Raid asset conversion, and farming "
                        "efficiency."),
    "js": {
    "dec": ".",
    "locale": "en-US",
    "storage_key": "buffforge_rob_jailtime_v1-en",
    "goal_target": "Target",
    "goal_current": "Current",
    "goal_remain": "Remaining",
    "goal_hours": "Hours",
    "goal_load": "Load",
    "goal_delete": "Delete",
    "deleted": "Deleted.",
    "log_deleted": "Log deleted.",
    "log_saved": "Wipe logged.",
    "log_years_err": "Enter a valid number of years earned",
    "logs_cleared": "Wipe history cleared",
    "reset_done": "Reset to default values",
    "saved": "Goal saved.",
    "loaded": "Goal loaded.",
    "empty_goals": "Goal Tracker is full (max 20 goals)",
    "yr_1": "yr", "yr_234": "yrs", "yr_5": "yrs",
    "w_1": "wipe", "w_234": "wipes", "w_5": "wipes",
    "cw_1": "cycle", "cw_234": "cycles", "cw_5": "cycles",
    "d_1": "day", "d_234": "days", "d_5": "days",
    "h_1": "hr", "h_234": "hrs", "h_5": "hrs",
    "day_word": "day",
    "milestones": [
        {"years": 1, "title": "Chance Tattoo & Hub Voice Chat",
         "detail": "Trust No One track 1/23; unlocks Prison & Lenny's Motel voice chat requirement"},
        {"years": 5, "title": "Fearlessness Tattoo + AFAK",
         "detail": "Track 2/23; unlocks AFAK medical item in Shipments"},
        {"years": 15, "title": "Joy Tattoo + CB45 Mk1 (SMG)",
         "detail": "Track 3/23; unlocks CB45 Mk1 in Shipments"},
        {"years": 25, "title": "CB45 Mk2",
         "detail": "Shipments tier 2 SMG unlock"},
        {"years": 30, "title": "Small Security Cabinet",
         "detail": "Jail Time unlock \u2014 threshold from the robrungame.com unlock table"},
        {"years": 35, "title": "CB45 Mk3",
         "detail": "Shipments tier 3 SMG unlock"},
        {"years": 40, "title": "Single-Server Wipe Cap & Tattoo Track",
         "detail": "Max years from one server (~$20M); a new tattoo every 20 years from 40"},
        {"years": 60, "title": "Police Radio (Tool)",
         "detail": "Research tree unlock for handheld police radio"},
        {"years": 75, "title": "Racing Rotor",
         "detail": "Jail Time unlock \u2014 threshold from the robrungame.com unlock table"},
        {"years": 105, "title": "Alarm System",
         "detail": "Jail Time unlock \u2014 threshold from the robrungame.com unlock table"},
        {"years": 140, "title": "Medium Security Cabinet",
         "detail": "Jail Time unlock \u2014 threshold from the robrungame.com unlock table"},
        {"years": 180, "title": "STAR-H Mk1 / Mk2 / Mk3 Rifle",
         "detail": "Shipments rifle line at 180 / 190 / 200 years"},
        {"years": 225, "title": "Steel Plate",
         "detail": "Jail Time unlock \u2014 threshold from the robrungame.com unlock table"},
        {"years": 275, "title": "Police Radio (Car Upgrade)",
         "detail": "Vehicle-mounted police radio upgrade"},
        {"years": 335, "title": "Laboratory Scales",
         "detail": "Lab Table production upgrade"},
        {"years": 410, "title": "Cargo Sheet (Cumulative)",
         "detail": "Cumulative cargo logistics upgrade"},
        {"years": 500, "title": "Large Security Cabinet",
         "detail": "Jail Time unlock \u2014 threshold from the robrungame.com unlock table"},
        {"years": 800, "title": "Silence Mask (Legendary)",
         "detail": "Final reward (23 of 23) on the Trust No One Authority track"},
        {"years": 950, "title": "DRM-14 Mk1 / Mk2 / Mk3",
         "detail": "Endgame semi-auto rifle line at 950 / 975 / 1,000 years"},
        {"years": 1200, "title": "Overall Account Jail Time Cap",
         "detail": "Post-Nov 17 community-tracked maximum total Jail Time"},
    ],
    "methods": [
        {"id": "store_runs", "name": "Store Runs \u2192 Fence", "rate": 200000,
         "tags": ["noplot", "solo"], "setup": "No plot needed \u00b7 Solo Notoriety 4 start",
         "risk": "Medium-High (cops & players)", "riskClass": "jt-c-amber",
         "note": "Solo report: ~$600K per 3h", "est": False, "disputed": False},
        {"id": "grow_room", "name": "Grow Room (6 Uncommon)", "rate": 129600,
         "tags": ["solo"], "setup": "Plot + Grow Room ($250K+ setup)",
         "risk": "Medium-High (base raids)", "riskClass": "jt-c-amber",
         "note": "6 Uncommon: $129.6K/h net \u00b7 Timesaver: Disputed",
         "est": False, "disputed": True,
         "maxName": "Grow Room (Maxed Farm)", "maxRate": 500000,
         "maxNote": "Maxed farm: $500K+/h (one player's estimate)"},
        {"id": "contraband", "name": "Contraband Workbench", "rate": 49795,
         "tags": ["solo"], "setup": "Plot + Workbench ($40K/bench)",
         "risk": "Medium (drop-off camping)", "riskClass": "jt-c-teal",
         "note": "$49,795/h net per bench \u00b7 scales linearly",
         "est": False, "disputed": False},
        {"id": "police_shifts", "name": "Police Shifts", "rate": 40000,
         "tags": ["noplot", "solo"], "setup": "$0 startup \u00b7 issued gear & patrol car",
         "risk": "Low ($1M cap per shift)", "riskClass": "jt-c-teal",
         "note": "$30K normal / $100K peak per 45-min shift",
         "est": False, "disputed": False},
        {"id": "big_heists", "name": "Bank & Grand Hotel Heists", "rate": 1000000,
         "tags": ["squad"], "setup": "Squad + drill / jammer prep",
         "risk": "Very High (heavy PvP & police)", "riskClass": "jt-c-rose",
         "note": "$424K\u2013$5.9M per heist (est. ~1 run/hr)",
         "est": True, "disputed": False},
        {"id": "clan_battles", "name": "Clan Business Battles", "rate": 900000,
         "tags": ["squad"], "setup": "3+ player clan + bid deposit",
         "risk": "High (3v3 / 6v6 / 12v12 PvP)", "riskClass": "jt-c-rose",
         "note": "$250K / $500K / $900K per objective + taxes",
         "est": True, "disputed": False},
    ],
    "unlocks_prefix": "Unlocks: ",
    "next_ms": "Next milestone: ",
    "all_ms": "At or past all tracked milestones",
    "goal_reached": "Goal Reached!",
    "yrs_left_tpl": "{n} {w} left",
    "cap_reached": "40-yr server cap reached",
    "to_cap_tpl": "{m} to 40-yr server cap",
    "no_wipes": "No additional wipes needed",
    "wipes_tpl": "Min {n} wipe {w} (7d each)",
    "wipes_tpl2": "Min {n} {cw} (7d each)",
    "complete": "Complete",
    "target_met": "Target met this wipe!",
    "all_unlocked": "All milestones unlocked",
    "unlocked": "Unlocked",
    "locked": "Locked",
    "target_tag": "Target",
    "set_target": "Set Target",
    "load": "Load",
    "completed": "Completed!",
    "left_hours_tpl": "{n} {w} left (~{h}h)",
    "default_note": "Federal Raid Wipe",
    "active": "Active",
    "use_route": "Use Route",
    "per_hour": "/h",
    "hrs_per_year_tpl": "{h} {hw} / {yw}",
    "next_year_tpl": "Add {m} more in wipe assets to unlock the next year (+{n} yrs total).",
    "cap_hint": "You hit the 40-year server wipe cap ($20M). Extra assets on this server will not grant more years.",
    "over_cap_tpl": "Over-cap warning: {m} exceeds the $20M / 40-year server cap. Spend surplus cash before the wipe rather than hoarding it.",
    "lenny_on": "Enabled: $1M for +10 yrs (saves $4M equivalent farming)",
    "lenny_off": "Off: standard $500,000/yr rate",
    "advice_goal": "Goal complete! Your current Authority meets or exceeds {t} years. Set a higher target like STAR-H (180 yrs) or Silence Mask (800 yrs) to keep tracking.",
    "advice_lenny": "Efficiency tip: If you have not paid Lenny's $1,000,000 debt yet, prioritize it first\u2014it yields +10 years at $100K/year (5x better than standard wipe conversion) and stacks over the 40-year cap.",
    "advice_under": "Heads up: Assets under $500,000 round down to 0 years at wipe. Run Store Runs or Police Shifts to reach at least $500K in clean banked cash before the Federal Raid.",
    "advice_route": "Route plan: Using {method} ({rate}/hr), reaching {t} years takes ~{h} hrs. Launder Dirty Cash before wipe and aim for $500K multiples to avoid rounding loss.",
    "toast_saved": "Saved goal: {label}",
    "toast_dup": "{t} yrs is already in your Goal Tracker",
    "toast_reset": "Reset to default values",
    "toast_route": "Active route set to: {name}",
    "toast_target": "Target updated to {t} years",
    "toast_logged": "Logged +{y} yrs \u00b7 Total: {t} yrs",
    "toast_invalid": "Enter a valid number of years earned",
    "toast_cleared": "Wipe history cleared",
    "est": "est.",
    "disputed": "Disputed",
    "cap_suffix": "40-yr cap",
    "risk_label": "Risk: ",
    "daily_tpl": "{h} hrs/day",
    "hrs_day_tpl": "{d} {dw} at {h}h/{day} \u00b7 {method}",
    "min_wipes_tpl": "{n} {w} ({d} {dw})",
    "yrs_unit": "yrs",
    },
    },
    "ru": {
    "title": "\u041a\u0430\u043b\u044c\u043a\u0443\u043b\u044f\u0442\u043e\u0440 \u0442\u044e\u0440\u0435\u043c\u043d\u043e\u0433\u043e \u0441\u0440\u043e\u043a\u0430 \u0438 \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442\u0430 \u0432 ROB RUN (2026) | BuffForge",
    "desc": ("\u0420\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u0439\u0442\u0435 \u043f\u0440\u043e\u0433\u0440\u0435\u0441\u0441 "
             "\u0442\u044e\u0440\u0435\u043c\u043d\u043e\u0433\u043e \u0441\u0440\u043e\u043a\u0430 \u0438 \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442\u0430 "
             "ROB RUN, \u0441\u0440\u0430\u0432\u043d\u0438\u0442\u0435 \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u044b \u0444\u0430\u0440\u043c\u0430 "
             "\u0441\u043e\u043b\u043e \u0438 \u0432 \u043e\u0442\u0440\u044f\u0434\u0435 \u0432 \u0447\u0430\u0441, \u043f\u0440\u043e\u0432\u0435\u0440\u044c\u0442\u0435 "
             "\u043b\u0438\u043c\u0438\u0442\u044b \u0432\u0430\u0439\u043f\u0430 \u0432 40 \u043b\u0435\u0442 \u0438 \u043e\u0442\u0441\u043b\u0435\u0436\u0438\u0432\u0430\u0439\u0442\u0435 "
             "\u0440\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0438."),
    "h1": "\u041a\u0430\u043b\u044c\u043a\u0443\u043b\u044f\u0442\u043e\u0440 \u0442\u044e\u0440\u0435\u043c\u043d\u043e\u0433\u043e \u0441\u0440\u043e\u043a\u0430 \u0438 \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442\u0430 \u0432 ROB RUN",
    "canonical": "/ru/rob-run/jail-time-authority-calculator/",
    "card_title": "\u041a\u0430\u043b\u044c\u043a\u0443\u043b\u044f\u0442\u043e\u0440 \u0442\u044e\u0440\u0435\u043c\u043d\u043e\u0433\u043e \u0441\u0440\u043e\u043a\u0430 \u0438 \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442\u0430",
    "eyebrow": "ROB RUN / \u0418\u043d\u0442\u0435\u0440\u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0435 \u0438\u0433\u0440\u043e\u0432\u044b\u0435 \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u044b",
    "lede": ("\u0420\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u0439\u0442\u0435 \u0441\u0440\u043e\u043a \u0437\u0430 \u0432\u0430\u0439\u043f "
             "\u0424\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u0431\u043b\u0430\u0432\u044b, \u043e\u0446\u0435\u043d\u0438\u0442\u0435 \u0447\u0430\u0441\u044b "
             "\u0438 \u0447\u0438\u0441\u043b\u043e \u0432\u0430\u0439\u043f\u043e\u0432 \u0434\u043e \u0441\u043b\u0435\u0434\u0443\u044e\u0449\u0435\u0439 "
             "\u0440\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0438 \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442\u0430, \u0441\u0440\u0430\u0432\u043d\u0438\u0442\u0435 "
             "\u043c\u0430\u0440\u0448\u0440\u0443\u0442\u044b \u0444\u0430\u0440\u043c\u0430 \u0441\u043e\u043b\u043e \u0438 \u0432 \u043e\u0442\u0440\u044f\u0434\u0435 "
             "\u0438 \u043e\u0442\u0441\u043b\u0435\u0436\u0438\u0432\u0430\u0439\u0442\u0435 \u043f\u043e\u0441\u0442\u043e\u044f\u043d\u043d\u044b\u0439 \u043f\u0440\u043e\u0433\u0440\u0435\u0441\u0441 "
             "\u2014 \u0432\u0441\u0451 \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u043e \u0432 \u0431\u0440\u0430\u0443\u0437\u0435\u0440\u0435, \u0431\u0435\u0437 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438."),
    "pills": ["\u0424\u043e\u0440\u043c\u0443\u043b\u0430: $500 000 = +1 \u0433\u043e\u0434",
              "\u041b\u0438\u043c\u0438\u0442: 40 \u043b\u0435\u0442 / \u0441\u0435\u0440\u0432\u0435\u0440 \u0438 24 \u0447",
              "\u041c\u0430\u043a\u0441. \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442: 1 200 \u043b\u0435\u0442",
              "\u0414\u043e\u043b\u0433 \u041b\u0435\u043d\u043d\u0438: $1 \u043c\u043b\u043d = +10 \u043b\u0435\u0442"],
    "kpi1": "\u041f\u0440\u043e\u0433\u0440\u0435\u0441\u0441 \u043a \u0446\u0435\u043b\u0438",
    "kpi2": "\u041f\u0440\u043e\u0433\u043d\u043e\u0437 \u043d\u0430 \u044d\u0442\u043e\u0442 \u0432\u0430\u0439\u043f",
    "kpi3": "\u0412\u0441\u0435\u0433\u043e \u0430\u043a\u0442\u0438\u0432\u043e\u0432 \u043d\u0443\u0436\u043d\u043e",
    "kpi4": "\u0412\u0440\u0435\u043c\u044f \u0444\u0430\u0440\u043c\u0430 (\u043e\u0446\u0435\u043d\u043a\u0430)",
    "tab1": "\u041a\u0430\u043b\u044c\u043a\u0443\u043b\u044f\u0442\u043e\u0440 \u043f\u0440\u043e\u0433\u0440\u0435\u0441\u0441\u0430 \u0438 \u0432\u0430\u0439\u043f\u0430",
    "tab2": "\u041c\u0430\u0440\u0448\u0440\u0443\u0442\u044b \u0444\u0430\u0440\u043c\u0430 \u0438 $/\u0447\u0430\u0441",
    "tab3": "\u0420\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0438 \u0438 \u043f\u0440\u0430\u0432\u0438\u043b\u0430",
    "tab4": "\u0422\u0440\u0435\u043a\u0435\u0440 \u0446\u0435\u043b\u0435\u0439",
    "calc_h": "\u0412\u0430\u0448\u0438 \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0438 \u0438 \u0446\u0435\u043b\u044c",
    "reset": "\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c",
    "cur_label": "\u0422\u0435\u043a\u0443\u0449\u0438\u0439 \u0442\u044e\u0440\u0435\u043c\u043d\u044b\u0439 \u0441\u0440\u043e\u043a / \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442 (\u043b\u0435\u0442)",
    "cur_hint": "\u0421\u043e\u0445\u0440\u0430\u043d\u044f\u0435\u0442\u0441\u044f \u043f\u043e\u0441\u043b\u0435 \u043a\u0430\u0436\u0434\u043e\u0433\u043e \u0432\u0430\u0439\u043f\u0430 \u00b7 \u041c\u0430\u043a\u0441. 1 200 \u043b\u0435\u0442",
    "tgt_label": "\u0426\u0435\u043b\u0435\u0432\u043e\u0439 \u0443\u0440\u043e\u0432\u0435\u043d\u044c \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442\u0430 (\u043b\u0435\u0442)",
    "quick_label": "\u0411\u044b\u0441\u0442\u0440\u044b\u0439 \u0432\u044b\u0431\u043e\u0440 \u043a\u043b\u044e\u0447\u0435\u0432\u044b\u0445 \u0432\u0435\u0445 \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442\u0430:",
    "assets_label": "\u041e\u0436\u0438\u0434\u0430\u0435\u043c\u044b\u0435 \u0430\u043a\u0442\u0438\u0432\u044b \u0441\u0435\u0440\u0432\u0435\u0440\u0430 \u043a \u0432\u0430\u0439\u043f\u0443 ($)",
    "assets_hint": ("\u0423\u0447\u0438\u0442\u044b\u0432\u0430\u044e\u0442\u0441\u044f \u0447\u0438\u0441\u0442\u044b\u0435 \u0434\u0435\u043d\u044c\u0433\u0438 \u0432 \u0431\u0430\u043d\u043a\u0435, "
                    "\u043f\u0440\u0435\u0434\u043c\u0435\u0442\u044b, \u0442\u0440\u0430\u043d\u0441\u043f\u043e\u0440\u0442, \u0443\u0447\u0430\u0441\u0442\u043a\u0438 \u0438 \u0434\u043e\u043c\u0430, "
                    "\u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u043d\u0438\u044f \u0438 \u0442\u0440\u0430\u0442\u044b \u043a\u043b\u0430\u043d\u0430 \u0438 \u043d\u0430 \u0432\u0437\u044f\u0442\u043a\u0438."),
    "lenny_title": "\u0423\u0447\u0435\u0441\u0442\u044c \u0434\u043e\u043b\u0433 \u041b\u0435\u043d\u043d\u0438 $1 \u043c\u043b\u043d",
    "lenny_sub": "\u0420\u0430\u0437\u043e\u0432\u043e +10 \u043b\u0435\u0442 (\u0432 5 \u0440\u0430\u0437 \u0432\u044b\u0433\u043e\u0434\u043d\u0435\u0435, \u0441\u0432\u0435\u0440\u0445 \u043b\u0438\u043c\u0438\u0442\u0430 40 \u043b\u0435\u0442)",
    "daily_label": "\u0418\u0433\u0440\u043e\u0432\u043e\u0435 \u0432\u0440\u0435\u043c\u044f \u0432 \u0434\u0435\u043d\u044c",
    "method_label": "\u041c\u0435\u0442\u043e\u0434 \u0444\u0430\u0440\u043c\u0430",
    "brk_h": "\u0420\u0430\u0437\u0431\u043e\u0440 \u0432\u0430\u0439\u043f\u0430 \u0438 \u0441\u0442\u0440\u0430\u0442\u0435\u0433\u0438\u044f",
    "cap_label": "\u041f\u0440\u043e\u0433\u0440\u0435\u0441\u0441 \u043a \u043b\u0438\u043c\u0438\u0442\u0443 \u0441\u0435\u0440\u0432\u0435\u0440\u0430 40 \u043b\u0435\u0442",
    "kv1": "\u0412\u0441\u0435\u0433\u043e \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442\u0430 \u043f\u043e\u0441\u043b\u0435 \u0432\u0430\u0439\u043f\u0430",
    "kv2": "\u041e\u0441\u0442\u0430\u043d\u0435\u0442\u0441\u044f \u043f\u043e\u0441\u043b\u0435 \u044d\u0442\u043e\u0433\u043e \u0432\u0430\u0439\u043f\u0430",
    "kv3": "\u041c\u0438\u043d. \u0446\u0438\u043a\u043b\u043e\u0432 \u0432\u0430\u0439\u043f\u0430 (\u043b\u0438\u043c\u0438\u0442 40 \u043b\u0435\u0442)",
    "kv4": "\u0412\u0440\u0435\u043c\u044f \u0430\u043a\u0442\u0438\u0432\u043d\u043e\u0433\u043e \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u0430 / \u0433\u043e\u0434",
    "kv5": "\u0421\u043b\u0435\u0434\u0443\u044e\u0449\u0430\u044f \u0440\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0430",
    "meth_h": "\u041c\u0430\u0440\u0448\u0440\u0443\u0442\u044b \u0444\u0430\u0440\u043c\u0430 \u0432 ROB RUN: \u0434\u043e\u0445\u043e\u0434 \u0438 \u0446\u0435\u043d\u0430 \u0432 \u0433\u043e\u0434\u0430\u0445",
    "meth_sub": ("\u041f\u0435\u0440\u0435\u0441\u0447\u0451\u0442: $500 000 = +1 \u0433\u043e\u0434 \u0442\u044e\u0440\u0435\u043c\u043d\u043e\u0433\u043e "
                 "\u0441\u0440\u043e\u043a\u0430 \u00b7 \u041d\u0430\u0436\u043c\u0438\u0442\u0435 \u00ab\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u044c "
                 "\u043c\u0430\u0440\u0448\u0440\u0443\u0442\u00bb, \u0447\u0442\u043e\u0431\u044b \u043e\u0431\u043d\u043e\u0432\u0438\u0442\u044c \u043e\u0446\u0435\u043d\u043a\u0443 \u0432\u044b\u0448\u0435."),
    "filter_all": "\u0412\u0441\u0435 \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u044b",
    "filter_noplot": "\u0411\u0435\u0437 \u0443\u0447\u0430\u0441\u0442\u043a\u0430",
    "filter_solo": "\u0423\u0434\u043e\u0431\u043d\u043e \u0441\u043e\u043b\u043e",
    "filter_squad": "\u041e\u0442\u0440\u044f\u0434 / \u043a\u043b\u0430\u043d",
    "bench_label": "\u0412\u0435\u0440\u0441\u0442\u0430\u043a\u0438 \u043a\u043e\u043d\u0442\u0440\u0430\u0431\u0430\u043d\u0434\u044b:",
    "grow_label": "\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430 \u0433\u0440\u043e\u0443\u0440\u0443\u043c\u0430:",
    "bars_h": "\u041e\u0446\u0435\u043d\u043a\u0430 \u0434\u043e\u0445\u043e\u0434\u0430 \u0432 \u0447\u0430\u0441 \u043f\u043e \u0441\u0442\u0438\u043b\u044e \u0438\u0433\u0440\u044b (USD / \u0447\u0430\u0441)",
    "bars_src": "\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a: Timesaver.gg \u0438 robrun.info (\u043d\u043e\u044f\u0431. 2026)",
    "th1": "\u041c\u0430\u0440\u0448\u0440\u0443\u0442",
    "th2": "\u041e\u0446\u0435\u043d\u043a\u0430 $/\u0447\u0430\u0441",
    "th3": "\u0427\u0430\u0441\u043e\u0432 \u043d\u0430 +1 \u0433\u043e\u0434",
    "th4": "\u0427\u0430\u0441\u043e\u0432 \u0434\u043e \u043b\u0438\u043c\u0438\u0442\u0430 40 \u043b\u0435\u0442",
    "th5": "\u0422\u0440\u0435\u0431\u043e\u0432\u0430\u043d\u0438\u044f \u0438 \u0440\u0438\u0441\u043a",
    "th6": "\u0414\u0435\u0439\u0441\u0442\u0432\u0438\u0435",
    "unlock_h": "\u0414\u043e\u0440\u043e\u0436\u043d\u0430\u044f \u043a\u0430\u0440\u0442\u0430 \u0440\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043e\u043a \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442\u0430 (1\u20131 200 \u043b\u0435\u0442)",
    "unlock_sub": ("\u0412\u0441\u0435 20 \u0440\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043e\u043a \u0437\u0430 \u0442\u044e\u0440\u0435\u043c\u043d\u044b\u0439 "
                   "\u0441\u0440\u043e\u043a, 1\u20131 200 \u043b\u0435\u0442. \u0422\u0430\u0442\u0443 \u0437\u0430\u0431\u0438\u0440\u0430\u044e\u0442\u0441\u044f "
                   "\u0443 \u0442\u0430\u0442\u0443-\u043c\u0430\u0441\u0442\u0435\u0440\u0430 \u0432 \u0442\u044e\u0440\u044c\u043c\u0435; \u043e\u0440\u0443\u0436\u0438\u0435 "
                   "\u0438 \u0441\u043d\u0430\u0440\u044f\u0436\u0435\u043d\u0438\u0435 \u043e\u0442\u043a\u0440\u044b\u0432\u0430\u044e\u0442\u0441\u044f \u0432 \u041f\u043e\u0441\u0442\u0430\u0432\u043a\u0430\u0445 "
                   "\u0438 \u0418\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u043d\u0438\u044f\u0445."),
    "conv_h": "\u0412\u0430\u0439\u043f \u0424\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u0431\u043b\u0430\u0432\u044b: \u0447\u0442\u043e \u043f\u0435\u0440\u0435\u0445\u043e\u0434\u0438\u0442, \u0430 \u0447\u0442\u043e \u043e\u0441\u0442\u0430\u0451\u0442\u0441\u044f",
    "conv_ok": "\u041f\u0435\u0440\u0435\u0445\u043e\u0434\u0438\u0442 \u0432 \u0442\u044e\u0440\u0435\u043c\u043d\u044b\u0439 \u0441\u0440\u043e\u043a",
    "conv_warn": "\u041e\u0441\u0442\u0430\u0451\u0442\u0441\u044f \u043d\u0430\u0432\u0441\u0435\u0433\u0434\u0430",
    "conv_list": ["\u0427\u0438\u0441\u0442\u044b\u0435 \u0434\u0435\u043d\u044c\u0433\u0438 \u0432 \u0431\u0430\u043d\u043a\u0435",
                  "\u041f\u0440\u0435\u0434\u043c\u0435\u0442\u044b \u0432 \u0438\u043d\u0432\u0435\u043d\u0442\u0430\u0440\u0435 \u0438 \u0442\u0430\u0439\u043d\u0438\u043a\u0435",
                  "\u0422\u0440\u0430\u043d\u0441\u043f\u043e\u0440\u0442, \u0434\u043e\u043c\u0430 \u0438 \u0443\u0447\u0430\u0441\u0442\u043a\u0438",
                  "\u041e\u0442\u043a\u0440\u044b\u0442\u044b\u0435 \u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u043d\u0438\u044f / \u041f\u043e\u0441\u0442\u0430\u0432\u043a\u0438",
                  "\u0422\u0440\u0430\u0442\u044b \u043a\u043b\u0430\u043d\u0430 \u0438 \u043d\u0430 \u0432\u0437\u044f\u0442\u043a\u0438"],
    "keep_list": ["\u041d\u0430\u043a\u043e\u043f\u043b\u0435\u043d\u043d\u044b\u0439 \u0442\u044e\u0440\u0435\u043c\u043d\u044b\u0439 \u0441\u0440\u043e\u043a / \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442",
                  "\u0412\u0441\u0435 \u0442\u0430\u0442\u0443 \u0438 \u043a\u043e\u0441\u043c\u0435\u0442\u0438\u043a\u0430",
                  "\u0411\u0430\u043b\u0430\u043d\u0441 B-Coin",
                  "\u0412\u043d\u0435\u0448\u043d\u043e\u0441\u0442\u044c \u0438 \u0438\u043c\u044f \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0430",
                  "\u041f\u0440\u043e\u0433\u0440\u0435\u0441\u0441 \u043e\u0431\u0443\u0447\u0435\u043d\u0438\u044f \u0438 \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438"],
    "rules_h": "\u041a\u043b\u044e\u0447\u0435\u0432\u044b\u0435 \u043f\u0440\u0430\u0432\u0438\u043b\u0430 \u043f\u0430\u0442\u0447\u0430 (17 \u043d\u043e\u044f\u0431\u0440\u044f 2026)",
    "rules": [
        ("<b>\u0420\u0430\u043d\u043d\u044f\u044f \u0441\u0434\u0430\u0447\u0430 \u043d\u0435 \u043d\u0443\u0436\u043d\u0430:</b> \u0432\u0430\u0448\u0438 "
         "\u0430\u043a\u0442\u0438\u0432\u044b \u043a\u043e\u043d\u0432\u0435\u0440\u0442\u0438\u0440\u0443\u044e\u0442\u0441\u044f \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438 "
         "\u0432\u043e \u0432\u0440\u0435\u043c\u044f 7-\u0434\u043d\u0435\u0432\u043d\u043e\u0433\u043e \u0432\u0430\u0439\u043f\u0430, \u0434\u0430\u0436\u0435 \u043e\u0444\u043b\u0430\u0439\u043d."),
        ("<b>\u0410\u0440\u0435\u0441\u0442 \u043a\u043e\u043f\u043e\u043c \u0434\u0430\u0451\u0442 0 \u043b\u0435\u0442:</b> \u0442\u044e\u0440\u0435\u043c\u043d\u044b\u0439 "
         "\u0441\u0440\u043e\u043a \u0434\u0430\u044e\u0442 \u0442\u043e\u043b\u044c\u043a\u043e \u0432\u0430\u0439\u043f\u044b \u0424\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u043e\u0439 "
         "\u043e\u0431\u043b\u0430\u0432\u044b, \u0441\u0434\u0430\u0447\u0430 \u0444\u0435\u0434\u0435\u0440\u0430\u043b\u0430\u043c \u0438\u043b\u0438 \u0434\u043e\u043b\u0433 \u041b\u0435\u043d\u043d\u0438."),
        ("<b>\u0421\u043d\u0430\u0447\u0430\u043b\u0430 \u043e\u0442\u043c\u043e\u0439\u0442\u0435 \u0433\u0440\u044f\u0437\u043d\u044b\u0435 \u0434\u0435\u043d\u044c\u0433\u0438:</b> "
         "\u0432 \u043e\u0444\u0438\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0445 \u0437\u0430\u043c\u0435\u0442\u043a\u0430\u0445 \u043a \u0432\u0430\u0439\u043f\u0443 \u043f\u0440\u044f\u043c\u043e "
         "\u0443\u043a\u0430\u0437\u0430\u043d\u044b \u0447\u0438\u0441\u0442\u044b\u0435 \u0434\u0435\u043d\u044c\u0433\u0438 \u2014 \u043d\u0435\u043e\u0442\u043c\u044b\u0442\u044b\u0435 "
         "\u043d\u0435 \u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u044b \u0438 \u0438\u0445 \u043c\u043e\u0433\u0443\u0442 \u0443\u043a\u0440\u0430\u0441\u0442\u044c."),
    ],
    "trk_h": "\u0421\u043e\u0445\u0440\u0430\u043d\u0451\u043d\u043d\u044b\u0435 \u0446\u0435\u043b\u0438 \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442\u0430",
    "trk_sub": ("\u0425\u0440\u0430\u043d\u044f\u0442\u0441\u044f \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u043e \u0432 \u0432\u0430\u0448\u0435\u043c \u0431\u0440\u0430\u0443\u0437\u0435\u0440\u0435. "
                "\u0421\u0438\u043d\u0445\u0440\u043e\u043d\u0438\u0437\u0438\u0440\u0443\u044e\u0442\u0441\u044f \u0441 \u0442\u0435\u043a\u0443\u0449\u0438\u043c \u0442\u044e\u0440\u0435\u043c\u043d\u044b\u043c \u0441\u0440\u043e\u043a\u043e\u043c."),
    "trk_add": "+ \u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0442\u0435\u043a\u0443\u0449\u0443\u044e \u0446\u0435\u043b\u044c",
    "trk_empty_b": "\u0426\u0435\u043b\u0435\u0439 \u043f\u043e\u043a\u0430 \u043d\u0435\u0442",
    "trk_empty_p": ("\u041d\u0430\u0436\u043c\u0438\u0442\u0435 \u00ab+ \u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0442\u0435\u043a\u0443\u0449\u0443\u044e "
                    "\u0446\u0435\u043b\u044c\u00bb, \u0447\u0442\u043e\u0431\u044b \u0437\u0430\u043a\u0440\u0435\u043f\u0438\u0442\u044c \u0441\u043b\u0435\u0434\u0443\u044e\u0449\u0435\u0435 "
                    "\u043e\u0440\u0443\u0436\u0438\u0435, \u0442\u0430\u0442\u0443 \u0438\u043b\u0438 \u041c\u0430\u0441\u043a\u0443 \u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044f."),
    "log_h": "\u0417\u0430\u043f\u0438\u0441\u0430\u0442\u044c \u0432\u044b\u043f\u043b\u0430\u0442\u0443 \u0437\u0430 \u0432\u0430\u0439\u043f / \u0441\u0434\u0430\u0447\u0443",
    "log_sub": "\u0410\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438 \u0434\u043e\u0431\u0430\u0432\u043b\u044f\u0435\u0442 \u0437\u0430\u0440\u0430\u0431\u043e\u0442\u0430\u043d\u043d\u044b\u0435 \u0433\u043e\u0434\u044b \u043a \u0442\u0435\u043a\u0443\u0449\u0435\u043c\u0443 \u0442\u044e\u0440\u0435\u043c\u043d\u043e\u043c\u0443 \u0441\u0440\u043e\u043a\u0443.",
    "log_years": "\u041f\u043e\u043b\u0443\u0447\u0435\u043d\u043e \u043b\u0435\u0442",
    "log_assets": "\u041a\u043e\u043d\u0432\u0435\u0440\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u043e \u0430\u043a\u0442\u0438\u0432\u043e\u0432 ($, \u043d\u0435\u043e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u043e)",
    "log_note": "\u0417\u0430\u043c\u0435\u0442\u043a\u0430 \u043e \u0441\u0435\u0440\u0432\u0435\u0440\u0435 / \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u0435",
    "log_note_ph": "\u043d\u0430\u043f\u0440\u0438\u043c\u0435\u0440, EU \u0432\u0430\u0439\u043f #2 \u00b7 \u043e\u0433\u0440\u0430\u0431\u043b\u0435\u043d\u0438\u044f \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u043e\u0432 + \u0433\u0440\u043e\u0443\u0440\u0443\u043c",
    "log_submit": "\u0417\u0430\u043f\u0438\u0441\u0430\u0442\u044c \u0432\u0430\u0439\u043f \u0438 \u043e\u0431\u043d\u043e\u0432\u0438\u0442\u044c \u0438\u0442\u043e\u0433",
    "hist_h": "\u0418\u0441\u0442\u043e\u0440\u0438\u044f \u0432\u0430\u0439\u043f\u043e\u0432",
    "hist_clear": "\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c \u0432\u0441\u0451",
    "hist_empty": "\u0417\u0430\u043f\u0438\u0441\u0435\u0439 \u043e \u0432\u0430\u0439\u043f\u0430\u0445 \u043f\u043e\u043a\u0430 \u043d\u0435\u0442.",
    "guide_h": "\u041a\u0430\u043a \u0440\u0430\u0431\u043e\u0442\u0430\u044e\u0442 \u0442\u044e\u0440\u0435\u043c\u043d\u044b\u0439 \u0441\u0440\u043e\u043a \u0438 \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442 \u0432 ROB RUN (\u0433\u0430\u0439\u0434 2026)",
    "guide_p1": ("\u0412 <b>ROB RUN</b> \u043d\u0435\u0442 \u043f\u0440\u0438\u0432\u044b\u0447\u043d\u043e\u0439 \u0448\u043a\u0430\u043b\u044b "
                 "\u043e\u043f\u044b\u0442\u0430. \u041a\u0430\u0436\u0434\u044b\u0435 \u0441\u0435\u043c\u044c \u0434\u043d\u0435\u0439 <b>\u0424\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u0430\u044f "
                 "\u043e\u0431\u043b\u0430\u0432\u0430</b> \u0441\u0442\u0438\u0440\u0430\u0435\u0442 \u0432\u0441\u0435 \u0443\u0447\u0430\u0441\u0442\u043a\u0438, \u0431\u0430\u0437\u044b, "
                 "\u043e\u0440\u0443\u0436\u0438\u0435, \u0442\u0440\u0430\u043d\u0441\u043f\u043e\u0440\u0442 \u0438 \u0434\u0435\u043d\u044c\u0433\u0438 \u043d\u0430 \u0432\u0430\u0448\u0435\u043c "
                 "\u0441\u0435\u0440\u0432\u0435\u0440\u0435 \u0438 \u043f\u0440\u0435\u0432\u0440\u0430\u0449\u0430\u0435\u0442 \u044d\u0442\u043e \u0431\u043e\u0433\u0430\u0442\u0441\u0442\u0432\u043e "
                 "\u0432 \u043f\u043e\u0441\u0442\u043e\u044f\u043d\u043d\u044b\u0439 <b>\u0442\u044e\u0440\u0435\u043c\u043d\u044b\u0439 \u0441\u0440\u043e\u043a</b> \u2014 "
                 "\u0430 \u043e\u043d \u043d\u0430\u043f\u0440\u044f\u043c\u0443\u044e \u0440\u0430\u0432\u0435\u043d \u0432\u0430\u0448\u0435\u043c\u0443 \u0443\u0440\u043e\u0432\u043d\u044e "
                 "<b>\u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442\u0430</b>."),
    "guide_h3a": "\u0424\u043e\u0440\u043c\u0443\u043b\u0430 \u043a\u043e\u043d\u0432\u0435\u0440\u0442\u0430\u0446\u0438\u0438 $500 000 \u0437\u0430 \u0433\u043e\u0434 \u0438 \u043b\u0438\u043c\u0438\u0442\u044b",
    "guide_p2": ("\u041f\u043e \u0434\u0430\u043d\u043d\u044b\u043c \u0441\u043e\u043e\u0431\u0449\u0435\u0441\u0442\u0432\u0430 \u0438\u0437 \u043e\u0431\u0441\u0443\u0436\u0434\u0435\u043d\u0438\u0439 "
                 "Steam \u0438 \u0438\u0433\u0440\u043e\u0432\u044b\u0445 \u0432\u0438\u043a\u0438, \u043a\u0430\u0436\u0434\u044b\u0435 <b>$500 000</b> "
                 "\u043a\u043e\u043d\u0444\u0438\u0441\u043a\u043e\u0432\u0430\u043d\u043d\u044b\u0445 \u0430\u043a\u0442\u0438\u0432\u043e\u0432 \u0434\u0430\u044e\u0442 "
                 "<b>+1 \u0433\u043e\u0434</b> \u0442\u044e\u0440\u0435\u043c\u043d\u043e\u0433\u043e \u0441\u0440\u043e\u043a\u0430 (\u0441 \u043e\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u0435\u043c "
                 "\u0432\u043d\u0438\u0437), \u043c\u0430\u043a\u0441\u0438\u043c\u0443\u043c <b>40 \u043b\u0435\u0442 \u043d\u0430 \u0441\u0435\u0440\u0432\u0435\u0440</b> "
                 "(~$20 000 000 \u0430\u043a\u0442\u0438\u0432\u043e\u0432). \u041f\u043e\u0441\u043b\u0435 \u043f\u0430\u0442\u0447\u0430 Kefir \u043e\u0442 "
                 "17 \u043d\u043e\u044f\u0431\u0440\u044f 2026 \u0433\u043e\u0434\u0430 \u0442\u0440\u0435\u043a\u0435\u0440\u044b \u0441\u043e\u043e\u0431\u0449\u0435\u0441\u0442\u0432\u0430 "
                 "\u0442\u0430\u043a\u0436\u0435 \u0443\u043a\u0430\u0437\u044b\u0432\u0430\u044e\u0442 <b>\u0434\u043d\u0435\u0432\u043d\u043e\u0439 \u043b\u0438\u043c\u0438\u0442 40 \u043b\u0435\u0442 "
                 "\u0437\u0430 24 \u0447\u0430\u0441\u0430</b> \u0438 <b>\u043e\u0431\u0449\u0438\u0439 \u043b\u0438\u043c\u0438\u0442 \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430 "
                 "1 200 \u043b\u0435\u0442</b>."),
    "caveat": ("<b>\u041f\u0440\u0438\u043c\u0435\u0447\u0430\u043d\u0438\u0435 \u043f\u0440\u043e +1 \u0433\u043e\u0434:</b> \u0432 \u043d\u0435\u043a\u043e\u0442\u043e\u0440\u044b\u0445 "
               "\u0433\u0430\u0439\u0434\u0430\u0445 (robrun.info, Indiatimes) \u043a \u0444\u043e\u0440\u043c\u0443\u043b\u0435 $500 000 "
               "\u0434\u043e\u0431\u0430\u0432\u043b\u044f\u0435\u0442\u0441\u044f \u0441\u0442\u0430\u0440\u0442\u043e\u0432\u044b\u0439 \u0441\u0440\u043e\u043a \u0432 1 \u0433\u043e\u0434. "
               "\u042d\u0442\u043e\u0442 \u043a\u0430\u043b\u044c\u043a\u0443\u043b\u044f\u0442\u043e\u0440 \u0441\u043b\u0435\u0434\u0443\u0435\u0442 \u0440\u0430\u0437\u0431\u043e\u0440\u0443 \u0438\u0437 "
               "Steam \u0438 robrunwiki (\u0431\u0435\u0437 \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u043e\u0433\u043e +1 \u0433\u043e\u0434\u0430), "
               "\u0441 \u043b\u0438\u043c\u0438\u0442\u043e\u043c 40 \u043b\u0435\u0442 \u043d\u0430 \u0441\u0435\u0440\u0432\u0435\u0440."),
    "guide_h3b": "\u041f\u043e\u0447\u0435\u043c\u0443 \u0434\u043e\u043b\u0433 \u041b\u0435\u043d\u043d\u0438 $1 000 000 \u2014 \u0441\u0430\u043c\u044b\u0439 \u0431\u044b\u0441\u0442\u0440\u044b\u0439 \u0440\u0430\u043d\u043d\u0438\u0439 \u0431\u043e\u043d\u0443\u0441",
    "guide_p3": ("\u041f\u043e\u0433\u0430\u0448\u0435\u043d\u0438\u0435 \u0434\u043e\u043b\u0433\u0430 \u041b\u0435\u043d\u043d\u0438 $1 000 000 \u0434\u0430\u0451\u0442 "
                 "\u0441\u043a\u0438\u043d \u00ab\u041d\u043e\u0432\u0430\u044f \u0433\u043b\u0430\u0432\u0430\u00bb \u0438 \u0440\u0430\u0437\u043e\u0432\u044b\u0435 "
                 "<b>+10 \u043b\u0435\u0442 \u0442\u044e\u0440\u0435\u043c\u043d\u043e\u0433\u043e \u0441\u0440\u043e\u043a\u0430</b>, \u043a\u043e\u0442\u043e\u0440\u044b\u0435 "
                 "\u0441\u0443\u043c\u043c\u0438\u0440\u0443\u044e\u0442\u0441\u044f \u0441\u0432\u0435\u0440\u0445 \u043b\u0438\u043c\u0438\u0442\u0430 \u0441\u0435\u0440\u0432\u0435\u0440\u0430 "
                 "\u0432 40 \u043b\u0435\u0442. \u041f\u043e <b>$100 000 \u0437\u0430 \u0433\u043e\u0434</b> \u044d\u0442\u043e \u0432 <b>5 \u0440\u0430\u0437 "
                 "\u0432\u044b\u0433\u043e\u0434\u043d\u0435\u0435</b> \u043e\u0431\u044b\u0447\u043d\u043e\u0439 \u043a\u043e\u043d\u0432\u0435\u0440\u0442\u0430\u0446\u0438\u0438 \u0430\u043a\u0442\u0438\u0432\u043e\u0432 "
                 "\u043f\u0440\u0438 \u0424\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u0431\u043b\u0430\u0432\u0435."),
    "guide_h3c": "\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0438 \u0438 \u0434\u0430\u0442\u0430 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0438",
    "sources": [
        ("Kefir ROB RUN Help Center \u2014 Federal Raid (Wipe) FAQ",
         KEFIR_URL, "\u043e\u0444\u0438\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0435 \u043f\u0440\u0430\u0432\u0438\u043b\u0430 \u043f\u0435\u0440\u0435\u043d\u043e\u0441\u0430"),
        ("ROB RUN Wiki \u2014 Jail Time & Authority Unlocks",
         WIKI_URL, "\u043f\u043e\u0440\u043e\u0433\u0438 \u0440\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043e\u043a \u0438 \u0441\u0442\u0430\u043a\u0438\u043d\u0433 \u0434\u043e\u043b\u0433\u0430 \u041b\u0435\u043d\u043d\u0438"),
        ("Timesaver.gg \u2014 ROB RUN Jail Time & Nov 17 Patch Limits",
         TS_JAIL_URL, "\u043b\u0438\u043c\u0438\u0442\u044b 40/\u0434\u0435\u043d\u044c \u0438 1 200 \u0432\u0441\u0435\u0433\u043e \u2014 \u0434\u0430\u043d\u043d\u044b\u0435 \u0441\u043e\u043e\u0431\u0449\u0435\u0441\u0442\u0432\u0430"),
        ("Timesaver.gg \u2014 ROB RUN Money Methods Ranked (Nov 2026)",
         TS_MONEY_URL, "\u043f\u0440\u043e\u0432\u0435\u0440\u0435\u043d\u043d\u044b\u0435 \u0431\u0435\u043d\u0447\u043c\u0430\u0440\u043a\u0438 $/\u0447\u0430\u0441"),
        ("robrungame.com \u2014 ROB RUN Wipe Schedule",
         ROBRUNGAME_URL, "\u0442\u0430\u0431\u043b\u0438\u0446\u0430 \u0440\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043e\u043a, \u043a\u043e\u043d\u0444\u0438\u0433 \u0438\u0433\u0440\u044b 0.7.0"),
    ],
    "faq_h": "\u0427\u0430\u0441\u0442\u044b\u0435 \u0432\u043e\u043f\u0440\u043e\u0441\u044b",
    "faq": [
        ("\u041a\u0430\u043a \u0441\u0447\u0438\u0442\u0430\u0435\u0442\u0441\u044f \u0442\u044e\u0440\u0435\u043c\u043d\u044b\u0439 \u0441\u0440\u043e\u043a \u043f\u0440\u0438 \u0424\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u0431\u043b\u0430\u0432\u0435?",
         "\u0418\u0433\u0440\u043e\u043a\u0438 \u0441\u043e\u043e\u0431\u0449\u0430\u044e\u0442: 1 \u0433\u043e\u0434 \u0442\u044e\u0440\u0435\u043c\u043d\u043e\u0433\u043e \u0441\u0440\u043e\u043a\u0430 "
         "\u0437\u0430 $500 000 \u043a\u043e\u043d\u0444\u0438\u0441\u043a\u043e\u0432\u0430\u043d\u043d\u044b\u0445 \u0430\u043a\u0442\u0438\u0432\u043e\u0432 \u0441\u0435\u0440\u0432\u0435\u0440\u0430, "
         "\u0441 \u043e\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u0435\u043c \u0432\u043d\u0438\u0437, \u0434\u043e 40 \u043b\u0435\u0442 ($20 \u043c\u043b\u043d) \u0437\u0430 \u0446\u0438\u043a\u043b \u0441\u0435\u0440\u0432\u0435\u0440\u0430."),
        ("\u041d\u0443\u0436\u043d\u043e \u043b\u0438 \u0441\u0434\u0430\u0432\u0430\u0442\u044c\u0441\u044f \u0444\u0435\u0434\u0435\u0440\u0430\u043b\u0430\u043c \u043f\u0435\u0440\u0435\u0434 \u0432\u0430\u0439\u043f\u043e\u043c?",
         "\u041d\u0435\u0442. \u0410\u043a\u0442\u0438\u0432\u044b \u0441\u0435\u0440\u0432\u0435\u0440\u0430 \u043a\u043e\u043d\u0432\u0435\u0440\u0442\u0438\u0440\u0443\u044e\u0442\u0441\u044f "
         "\u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438 \u0432\u043e \u0432\u0440\u0435\u043c\u044f 7-\u0434\u043d\u0435\u0432\u043d\u043e\u0433\u043e \u0432\u0430\u0439\u043f\u0430 "
         "\u0424\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u0431\u043b\u0430\u0432\u044b, \u0434\u0430\u0436\u0435 \u0435\u0441\u043b\u0438 \u0432\u044b \u043e\u0444\u043b\u0430\u0439\u043d. "
         "\u0420\u0430\u043d\u043d\u044f\u044f \u0441\u0434\u0430\u0447\u0430 \u0444\u0435\u0434\u0435\u0440\u0430\u043b\u0430\u043c \u043d\u0443\u0436\u043d\u0430 \u0432 \u043e\u0441\u043d\u043e\u0432\u043d\u043e\u043c, "
         "\u0447\u0442\u043e\u0431\u044b \u0441\u0440\u0430\u0437\u0443 \u0441\u043c\u0435\u043d\u0438\u0442\u044c \u0441\u0435\u0440\u0432\u0435\u0440."),
        ("\u041a\u0430\u043a\u043e\u0439 \u0441\u0430\u043c\u044b\u0439 \u0431\u044b\u0441\u0442\u0440\u044b\u0439 \u0441\u043e\u043b\u043e-\u043c\u0430\u0440\u0448\u0440\u0443\u0442 \u0444\u0430\u0440\u043c\u0430 \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442\u0430?",
         "\u0411\u0435\u0437 \u0443\u0447\u0430\u0441\u0442\u043a\u0430 \u0441\u043e\u043b\u043e-\u043e\u0433\u0440\u0430\u0431\u043b\u0435\u043d\u0438\u044f \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u043e\u0432 "
         "\u0441 \u043f\u0440\u043e\u0434\u0430\u0436\u0435\u0439 \u0441\u043a\u0443\u043f\u0449\u0438\u043a\u0443 \u0434\u0430\u044e\u0442 \u0432 \u0441\u0440\u0435\u0434\u043d\u0435\u043c "
         "~$200 000/\u0447\u0430\u0441 (~2,5 \u0447\u0430\u0441\u0430 \u043d\u0430 \u0433\u043e\u0434). \u041a\u043e\u0433\u0434\u0430 \u0435\u0441\u0442\u044c "
         "\u0443\u0447\u0430\u0441\u0442\u043e\u043a, \u043f\u0440\u043e\u043a\u0430\u0447\u0430\u043d\u043d\u044b\u0439 \u0433\u0440\u043e\u0443\u0440\u0443\u043c \u043c\u043e\u0436\u0435\u0442 "
         "\u0434\u0430\u0432\u0430\u0442\u044c \u0431\u043e\u043b\u044c\u0448\u0435 $500 000/\u0447\u0430\u0441, \u0435\u0441\u043b\u0438 \u043e\u0442\u0431\u0438\u0432\u0430\u0442\u044c\u0441\u044f "
         "\u043e\u0442 \u0440\u0435\u0439\u0434\u043e\u0432 \u043d\u0430 \u0431\u0430\u0437\u0443."),
        ("\u0414\u0430\u0451\u0442 \u043b\u0438 \u0430\u0440\u0435\u0441\u0442 \u0438\u0433\u0440\u043e\u043a\u043e\u043c-\u043f\u043e\u043b\u0438\u0446\u0435\u0439\u0441\u043a\u0438\u043c \u0442\u044e\u0440\u0435\u043c\u043d\u044b\u0439 \u0441\u0440\u043e\u043a?",
         "\u041d\u0435\u0442. \u0410\u0440\u0435\u0441\u0442\u044b \u0438\u0433\u0440\u043e\u043a\u043e\u043c-\u043f\u043e\u043b\u0438\u0446\u0435\u0439\u0441\u043a\u0438\u043c \u043a\u043e\u043d\u0444\u0438\u0441\u043a\u0443\u044e\u0442 "
         "\u0434\u043e\u0431\u044b\u0447\u0443 \u0438\u0437 \u0441\u0443\u043c\u043a\u0438, \u043d\u043e \u0434\u0430\u044e\u0442 0 \u043b\u0435\u0442 \u0442\u044e\u0440\u0435\u043c\u043d\u043e\u0433\u043e "
         "\u0441\u0440\u043e\u043a\u0430. \u041f\u043e\u0441\u0442\u043e\u044f\u043d\u043d\u044b\u0439 \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442 \u0434\u0430\u044e\u0442 \u0442\u043e\u043b\u044c\u043a\u043e "
         "\u0432\u0430\u0439\u043f\u044b \u0424\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u0431\u043b\u0430\u0432\u044b, \u0441\u0434\u0430\u0447\u0430 \u0444\u0435\u0434\u0435\u0440\u0430\u043b\u0430\u043c "
         "\u0438 \u0434\u043e\u043b\u0433 \u041b\u0435\u043d\u043d\u0438 $1 \u043c\u043b\u043d."),
        ("\u041a\u0430\u043a\u0430\u044f \u0432\u044b\u0441\u0448\u0430\u044f \u043d\u0430\u0433\u0440\u0430\u0434\u0430 \u0437\u0430 \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442 \u0432 ROB RUN?",
         "\u041d\u0430 \u0442\u0440\u0435\u043a\u0435 \u0442\u0430\u0442\u0443 \u00ab\u041d\u0438\u043a\u043e\u043c\u0443 \u043d\u0435 \u0432\u0435\u0440\u044c\u00bb "
         "(Trust No One) \u0443 \u0442\u0430\u0442\u0443-\u043c\u0430\u0441\u0442\u0435\u0440\u0430 \u0432 \u0442\u044e\u0440\u044c\u043c\u0435 "
         "\u0444\u0438\u043d\u0430\u043b\u044c\u043d\u0430\u044f \u043a\u043e\u0441\u043c\u0435\u0442\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u043d\u0430\u0433\u0440\u0430\u0434\u0430 \u2014 "
         "\u043b\u0435\u0433\u0435\u043d\u0434\u0430\u0440\u043d\u0430\u044f \u041c\u0430\u0441\u043a\u0430 \u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044f \u0437\u0430 800 \u043b\u0435\u0442 "
         "\u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442\u0430. \u0412 \u041f\u043e\u0441\u0442\u0430\u0432\u043a\u0430\u0445 DRM-14 Mk3 \u043e\u0442\u043a\u0440\u044b\u0432\u0430\u0435\u0442\u0441\u044f "
         "\u043d\u0430 1 000 \u043b\u0435\u0442."),
    ],
    "research": (
        "\u041f\u0440\u043e\u0432\u0435\u0440\u0435\u043d\u043e 24 \u043d\u043e\u044f\u0431\u0440\u044f 2026 \u0433\u043e\u0434\u0430. "
        "\u041f\u043e \u043e\u043f\u0443\u0431\u043b\u0438\u043a\u043e\u0432\u0430\u043d\u043d\u044b\u043c \u0433\u0430\u0439\u0434\u0430\u043c; \u0434\u0435\u0442\u0430\u043b\u0438 "
        "\u043c\u043e\u0433\u0443\u0442 \u043c\u0435\u043d\u044f\u0442\u044c\u0441\u044f \u0441 \u043f\u0430\u0442\u0447\u0430\u043c\u0438 \u0438 \u043e\u0442\u043a\u0440\u044b\u0442\u0438\u044f\u043c\u0438. "
        "\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0438: "
        "<a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">Kefir: FAQ \u043e \u0424\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u0431\u043b\u0430\u0432\u0435</a>, "
        "<a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">ROB RUN Wiki: Jail Time</a>, "
        "<a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">Timesaver.gg: Jail Time \u0438 \u043b\u0438\u043c\u0438\u0442\u044b 17 \u043d\u043e\u044f\u0431\u0440\u044f</a>, "
        "<a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">Timesaver.gg: \u043c\u0435\u0442\u043e\u0434\u044b \u0437\u0430\u0440\u0430\u0431\u043e\u0442\u043a\u0430</a>, "
        "<a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">robrungame.com: \u0440\u0430\u0441\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0432\u0430\u0439\u043f\u043e\u0432</a>. "
        "BuffForge \u2014 \u043d\u0435\u0437\u0430\u0432\u0438\u0441\u0438\u043c\u044b\u0439 \u0444\u0430\u043d\u0430\u0442\u0441\u043a\u0438\u0439 \u043f\u0440\u043e\u0435\u043a\u0442, "
        "\u043d\u0435 \u0441\u0432\u044f\u0437\u0430\u043d\u043d\u044b\u0439 \u0441 Kefir \u0438\u043b\u0438 Valve. \u041d\u0430\u0448\u043b\u0438 \u043e\u0448\u0438\u0431\u043a\u0443? "
        "\u041d\u0430\u043f\u0438\u0448\u0438\u0442\u0435 \u043d\u0430 "
        "<a href=\"mailto:%s\">%s</a>." % (KEFIR_URL, WIKI_URL, TS_JAIL_URL, TS_MONEY_URL, ROBRUNGAME_URL, EMAIL, EMAIL)),
    "webapp_desc": ("\u0418\u043d\u0442\u0435\u0440\u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0439 \u043a\u0430\u043b\u044c\u043a\u0443\u043b\u044f\u0442\u043e\u0440 ROB RUN "
                    "\u0434\u043b\u044f \u0442\u044e\u0440\u0435\u043c\u043d\u043e\u0433\u043e \u0441\u0440\u043e\u043a\u0430, \u0440\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043e\u043a "
                    "\u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442\u0430, \u043a\u043e\u043d\u0432\u0435\u0440\u0442\u0430\u0446\u0438\u0438 \u0430\u043a\u0442\u0438\u0432\u043e\u0432 "
                    "\u043f\u0440\u0438 \u0432\u0430\u0439\u043f\u0435 \u0438 \u044d\u0444\u0444\u0435\u043a\u0442\u0438\u0432\u043d\u043e\u0441\u0442\u0438 \u0444\u0430\u0440\u043c\u0430."),
    "js": {
    "dec": ",",
    "locale": "ru-RU",
    "storage_key": "buffforge_rob_jailtime_v1-ru",
    "goal_target": "\u0426\u0435\u043b\u044c",
    "goal_current": "\u0422\u0435\u043a\u0443\u0449\u0438\u0439 \u0441\u0440\u043e\u043a",
    "goal_remain": "\u041e\u0441\u0442\u0430\u043b\u043e\u0441\u044c",
    "goal_hours": "\u0427\u0430\u0441\u044b",
    "goal_load": "\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c",
    "goal_delete": "\u0423\u0434\u0430\u043b\u0438\u0442\u044c",
    "deleted": "\u0423\u0434\u0430\u043b\u0435\u043d\u043e.",
    "log_deleted": "\u0417\u0430\u043f\u0438\u0441\u044c \u0443\u0434\u0430\u043b\u0435\u043d\u0430.",
    "log_saved": "\u0412\u0430\u0439\u043f \u0437\u0430\u043f\u0438\u0441\u0430\u043d.",
    "log_years_err": "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043a\u043e\u0440\u0440\u0435\u043a\u0442\u043d\u043e\u0435 \u0447\u0438\u0441\u043b\u043e \u043f\u043e\u043b\u0443\u0447\u0435\u043d\u043d\u044b\u0445 \u043b\u0435\u0442",
    "logs_cleared": "\u0418\u0441\u0442\u043e\u0440\u0438\u044f \u0432\u0430\u0439\u043f\u043e\u0432 \u043e\u0447\u0438\u0449\u0435\u043d\u0430",
    "reset_done": "\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u044f \u0441\u0431\u0440\u043e\u0448\u0435\u043d\u044b \u043a \u0441\u0442\u0430\u043d\u0434\u0430\u0440\u0442\u043d\u044b\u043c",
    "saved": "\u0426\u0435\u043b\u044c \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0430.",
    "loaded": "\u0426\u0435\u043b\u044c \u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043d\u0430.",
    "empty_goals": "\u0422\u0440\u0435\u043a\u0435\u0440 \u0446\u0435\u043b\u0435\u0439 \u0437\u0430\u043f\u043e\u043b\u043d\u0435\u043d (\u043c\u0430\u043a\u0441\u0438\u043c\u0443\u043c 20 \u0446\u0435\u043b\u0435\u0439)",
    "yr_1": "\u0433\u043e\u0434", "yr_234": "\u0433\u043e\u0434\u0430", "yr_5": "\u043b\u0435\u0442",
    "w_1": "\u0432\u0430\u0439\u043f", "w_234": "\u0432\u0430\u0439\u043f\u0430", "w_5": "\u0432\u0430\u0439\u043f\u043e\u0432",
    "cw_1": "\u0446\u0438\u043a\u043b", "cw_234": "\u0446\u0438\u043a\u043b\u0430", "cw_5": "\u0446\u0438\u043a\u043b\u043e\u0432",
    "d_1": "\u0434\u0435\u043d\u044c", "d_234": "\u0434\u043d\u044f", "d_5": "\u0434\u043d\u0435\u0439",
    "h_1": "\u0447", "h_234": "\u0447", "h_5": "\u0447",
    "day_word": "\u0434\u0435\u043d\u044c",
    "milestones": [
        {"years": 1, "title": "\u0422\u0430\u0442\u0443 \u00ab\u0428\u0430\u043d\u0441\u00bb \u0438 \u0433\u043e\u043b\u043e\u0441\u043e\u0432\u043e\u0439 \u0447\u0430\u0442 \u0445\u0430\u0431\u0430",
         "detail": "\u0422\u0440\u0435\u043a \u00ab\u041d\u0438\u043a\u043e\u043c\u0443 \u043d\u0435 \u0432\u0435\u0440\u044c\u00bb 1/23; \u043e\u0442\u043a\u0440\u044b\u0432\u0430\u0435\u0442 \u0442\u0440\u0435\u0431\u043e\u0432\u0430\u043d\u0438\u0435 \u0433\u043e\u043b\u043e\u0441\u043e\u0432\u043e\u0433\u043e \u0447\u0430\u0442\u0430 \u0432 \u0442\u044e\u0440\u044c\u043c\u0435 \u0438 \u043c\u043e\u0442\u0435\u043b\u0435 \u041b\u0435\u043d\u043d\u0438"},
        {"years": 5, "title": "\u0422\u0430\u0442\u0443 \u00ab\u0411\u0435\u0441\u0441\u0442\u0440\u0430\u0448\u0438\u0435\u00bb + AFAK",
         "detail": "\u0422\u0440\u0435\u043a 2/23; \u043e\u0442\u043a\u0440\u044b\u0432\u0430\u0435\u0442 \u043c\u0435\u0434\u0438\u0446\u0438\u043d\u0441\u043a\u0438\u0439 \u043f\u0440\u0435\u0434\u043c\u0435\u0442 AFAK \u0432 \u041f\u043e\u0441\u0442\u0430\u0432\u043a\u0430\u0445"},
        {"years": 15, "title": "\u0422\u0430\u0442\u0443 \u00ab\u0420\u0430\u0434\u043e\u0441\u0442\u044c\u00bb + CB45 Mk1 (\u041f\u041f)",
         "detail": "\u0422\u0440\u0435\u043a 3/23; \u043e\u0442\u043a\u0440\u044b\u0432\u0430\u0435\u0442 CB45 Mk1 \u0432 \u041f\u043e\u0441\u0442\u0430\u0432\u043a\u0430\u0445"},
        {"years": 25, "title": "CB45 Mk2",
         "detail": "\u0420\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0430 \u041f\u041f 2-\u0433\u043e \u0443\u0440\u043e\u0432\u043d\u044f \u0432 \u041f\u043e\u0441\u0442\u0430\u0432\u043a\u0430\u0445"},
        {"years": 30, "title": "Small Security Cabinet (\u043c\u0430\u043b\u044b\u0439 \u0441\u0435\u0439\u0444)",
         "detail": "\u0420\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0430 \u0437\u0430 \u0442\u044e\u0440\u0435\u043c\u043d\u044b\u0439 \u0441\u0440\u043e\u043a \u2014 \u043f\u043e\u0440\u043e\u0433 \u0438\u0437 \u0442\u0430\u0431\u043b\u0438\u0446\u044b \u0440\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043e\u043a robrungame.com"},
        {"years": 35, "title": "CB45 Mk3",
         "detail": "\u0420\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0430 \u041f\u041f 3-\u0433\u043e \u0443\u0440\u043e\u0432\u043d\u044f \u0432 \u041f\u043e\u0441\u0442\u0430\u0432\u043a\u0430\u0445"},
        {"years": 40, "title": "\u041b\u0438\u043c\u0438\u0442 \u0432\u0430\u0439\u043f\u0430 \u043d\u0430 \u043e\u0434\u043d\u043e\u043c \u0441\u0435\u0440\u0432\u0435\u0440\u0435 \u0438 \u0442\u0440\u0435\u043a \u0442\u0430\u0442\u0443",
         "detail": "\u041c\u0430\u043a\u0441\u0438\u043c\u0443\u043c \u043b\u0435\u0442 \u0441 \u043e\u0434\u043d\u043e\u0433\u043e \u0441\u0435\u0440\u0432\u0435\u0440\u0430 (~$20 \u043c\u043b\u043d); \u043d\u043e\u0432\u0430\u044f \u0442\u0430\u0442\u0443 \u043a\u0430\u0436\u0434\u044b\u0435 20 \u043b\u0435\u0442, \u043d\u0430\u0447\u0438\u043d\u0430\u044f \u0441 40"},
        {"years": 60, "title": "\u041f\u043e\u043b\u0438\u0446\u0435\u0439\u0441\u043a\u0430\u044f \u0440\u0430\u0446\u0438\u044f (\u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442)",
         "detail": "\u0420\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0430 \u0432 \u0434\u0435\u0440\u0435\u0432\u0435 \u0438\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u043d\u0438\u0439 \u0434\u043b\u044f \u0440\u0443\u0447\u043d\u043e\u0439 \u043f\u043e\u043b\u0438\u0446\u0435\u0439\u0441\u043a\u043e\u0439 \u0440\u0430\u0446\u0438\u0438"},
        {"years": 75, "title": "Racing Rotor (\u0433\u043e\u043d\u043e\u0447\u043d\u044b\u0439 \u0440\u043e\u0442\u043e\u0440)",
         "detail": "\u0420\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0430 \u0437\u0430 \u0442\u044e\u0440\u0435\u043c\u043d\u044b\u0439 \u0441\u0440\u043e\u043a \u2014 \u043f\u043e\u0440\u043e\u0433 \u0438\u0437 \u0442\u0430\u0431\u043b\u0438\u0446\u044b \u0440\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043e\u043a robrungame.com"},
        {"years": 105, "title": "Alarm System (\u0441\u0438\u0433\u043d\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u044f)",
         "detail": "\u0420\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0430 \u0437\u0430 \u0442\u044e\u0440\u0435\u043c\u043d\u044b\u0439 \u0441\u0440\u043e\u043a \u2014 \u043f\u043e\u0440\u043e\u0433 \u0438\u0437 \u0442\u0430\u0431\u043b\u0438\u0446\u044b \u0440\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043e\u043a robrungame.com"},
        {"years": 140, "title": "Medium Security Cabinet (\u0441\u0440\u0435\u0434\u043d\u0438\u0439 \u0441\u0435\u0439\u0444)",
         "detail": "\u0420\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0430 \u0437\u0430 \u0442\u044e\u0440\u0435\u043c\u043d\u044b\u0439 \u0441\u0440\u043e\u043a \u2014 \u043f\u043e\u0440\u043e\u0433 \u0438\u0437 \u0442\u0430\u0431\u043b\u0438\u0446\u044b \u0440\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043e\u043a robrungame.com"},
        {"years": 180, "title": "\u0412\u0438\u043d\u0442\u043e\u0432\u043a\u0430 STAR-H Mk1 / Mk2 / Mk3",
         "detail": "\u041b\u0438\u043d\u0435\u0439\u043a\u0430 \u0432\u0438\u043d\u0442\u043e\u0432\u043e\u043a \u0432 \u041f\u043e\u0441\u0442\u0430\u0432\u043a\u0430\u0445 \u043d\u0430 180 / 190 / 200 \u043b\u0435\u0442"},
        {"years": 225, "title": "Steel Plate (\u0441\u0442\u0430\u043b\u044c\u043d\u0430\u044f \u043f\u043b\u0430\u0441\u0442\u0438\u043d\u0430)",
         "detail": "\u0420\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0430 \u0437\u0430 \u0442\u044e\u0440\u0435\u043c\u043d\u044b\u0439 \u0441\u0440\u043e\u043a \u2014 \u043f\u043e\u0440\u043e\u0433 \u0438\u0437 \u0442\u0430\u0431\u043b\u0438\u0446\u044b \u0440\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043e\u043a robrungame.com"},
        {"years": 275, "title": "\u041f\u043e\u043b\u0438\u0446\u0435\u0439\u0441\u043a\u0430\u044f \u0440\u0430\u0446\u0438\u044f (\u0430\u043f\u0433\u0440\u0435\u0439\u0434 \u043c\u0430\u0448\u0438\u043d\u044b)",
         "detail": "\u0423\u043b\u0443\u0447\u0448\u0435\u043d\u0438\u0435 \u0430\u0432\u0442\u043e\u043c\u043e\u0431\u0438\u043b\u044f \u2014 \u043f\u043e\u043b\u0438\u0446\u0435\u0439\u0441\u043a\u0430\u044f \u0440\u0430\u0446\u0438\u044f \u043d\u0430 \u043c\u0430\u0448\u0438\u043d\u0435"},
        {"years": 335, "title": "\u041b\u0430\u0431\u043e\u0440\u0430\u0442\u043e\u0440\u043d\u044b\u0435 \u0432\u0435\u0441\u044b",
         "detail": "\u0423\u043b\u0443\u0447\u0448\u0435\u043d\u0438\u0435 \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0441\u0442\u0432\u0430 \u043b\u0430\u0431\u043e\u0440\u0430\u0442\u043e\u0440\u043d\u043e\u0433\u043e \u0441\u0442\u043e\u043b\u0430"},
        {"years": 410, "title": "\u0413\u0440\u0443\u0437\u043e\u0432\u043e\u0439 \u043b\u0438\u0441\u0442 (\u043d\u0430\u043a\u043e\u043f\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439)",
         "detail": "\u041d\u0430\u043a\u043e\u043f\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0435 \u0443\u043b\u0443\u0447\u0448\u0435\u043d\u0438\u0435 \u0433\u0440\u0443\u0437\u043e\u0432\u043e\u0439 \u043b\u043e\u0433\u0438\u0441\u0442\u0438\u043a\u0438"},
        {"years": 500, "title": "Large Security Cabinet (\u0431\u043e\u043b\u044c\u0448\u043e\u0439 \u0441\u0435\u0439\u0444)",
         "detail": "\u0420\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0430 \u0437\u0430 \u0442\u044e\u0440\u0435\u043c\u043d\u044b\u0439 \u0441\u0440\u043e\u043a \u2014 \u043f\u043e\u0440\u043e\u0433 \u0438\u0437 \u0442\u0430\u0431\u043b\u0438\u0446\u044b \u0440\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043e\u043a robrungame.com"},
        {"years": 800, "title": "\u041c\u0430\u0441\u043a\u0430 \u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044f (\u043b\u0435\u0433\u0435\u043d\u0434\u0430\u0440\u043d\u0430\u044f)",
         "detail": "\u0424\u0438\u043d\u0430\u043b\u044c\u043d\u0430\u044f \u043d\u0430\u0433\u0440\u0430\u0434\u0430 (23 \u0438\u0437 23) \u043d\u0430 \u0442\u0440\u0435\u043a\u0435 \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442\u0430 \u00ab\u041d\u0438\u043a\u043e\u043c\u0443 \u043d\u0435 \u0432\u0435\u0440\u044c\u00bb"},
        {"years": 950, "title": "DRM-14 Mk1 / Mk2 / Mk3",
         "detail": "\u042d\u043d\u0434\u0433\u0435\u0439\u043c-\u043b\u0438\u043d\u0435\u0439\u043a\u0430 \u043f\u043e\u043b\u0443\u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0445 \u0432\u0438\u043d\u0442\u043e\u0432\u043e\u043a \u043d\u0430 950 / 975 / 1 000 \u043b\u0435\u0442"},
        {"years": 1200, "title": "\u041e\u0431\u0449\u0438\u0439 \u043b\u0438\u043c\u0438\u0442 \u0442\u044e\u0440\u0435\u043c\u043d\u043e\u0433\u043e \u0441\u0440\u043e\u043a\u0430 \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430",
         "detail": "\u041c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u043e\u0431\u0449\u0438\u0439 \u0442\u044e\u0440\u0435\u043c\u043d\u044b\u0439 \u0441\u0440\u043e\u043a \u043f\u043e \u0434\u0430\u043d\u043d\u044b\u043c \u0441\u043e\u043e\u0431\u0449\u0435\u0441\u0442\u0432\u0430 \u043f\u043e\u0441\u043b\u0435 \u043f\u0430\u0442\u0447\u0430 17 \u043d\u043e\u044f\u0431\u0440\u044f"},
    ],
    "methods": [
        {"id": "store_runs", "name": "\u041e\u0433\u0440\u0430\u0431\u043b\u0435\u043d\u0438\u044f \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u043e\u0432 \u2192 \u0441\u043a\u0443\u043f\u0449\u0438\u043a", "rate": 200000,
         "tags": ["noplot", "solo"], "setup": "\u0411\u0435\u0437 \u0443\u0447\u0430\u0441\u0442\u043a\u0430 \u00b7 \u0441\u043e\u043b\u043e \u0441 Notoriety 4",
         "risk": "\u0421\u0440\u0435\u0434\u043d\u0435-\u0432\u044b\u0441\u043e\u043a\u0438\u0439 (\u043a\u043e\u043f\u044b \u0438 \u0438\u0433\u0440\u043e\u043a\u0438)", "riskClass": "jt-c-amber",
         "note": "\u041e\u0442\u0447\u0451\u0442 \u0441\u043e\u043b\u043e-\u0438\u0433\u0440\u043e\u043a\u0430: ~$600K \u0437\u0430 3 \u0447", "est": False, "disputed": False},
        {"id": "grow_room", "name": "\u0413\u0440\u043e\u0443\u0440\u0443\u043c (6 Uncommon)", "rate": 129600,
         "tags": ["solo"], "setup": "\u0423\u0447\u0430\u0441\u0442\u043e\u043a + \u0433\u0440\u043e\u0443\u0440\u0443\u043c (\u043e\u0442 $250K \u043d\u0430 \u0437\u0430\u043f\u0443\u0441\u043a)",
         "risk": "\u0421\u0440\u0435\u0434\u043d\u0435-\u0432\u044b\u0441\u043e\u043a\u0438\u0439 (\u0440\u0435\u0439\u0434\u044b \u043d\u0430 \u0431\u0430\u0437\u0443)", "riskClass": "jt-c-amber",
         "note": "6 Uncommon: $129,6K/\u0447 \u0447\u0438\u0441\u0442\u044b\u043c\u0438 \u00b7 Timesaver: \u0441\u043f\u043e\u0440\u043d\u043e",
         "est": False, "disputed": True,
         "maxName": "\u0413\u0440\u043e\u0443\u0440\u0443\u043c (\u043f\u0440\u043e\u043a\u0430\u0447\u0430\u043d\u043d\u0430\u044f \u0444\u0435\u0440\u043c\u0430)", "maxRate": 500000,
         "maxNote": "\u041f\u0440\u043e\u043a\u0430\u0447\u0430\u043d\u043d\u0430\u044f \u0444\u0435\u0440\u043c\u0430: $500K+/\u0447 (\u043e\u0446\u0435\u043d\u043a\u0430 \u043e\u0434\u043d\u043e\u0433\u043e \u0438\u0433\u0440\u043e\u043a\u0430)"},
        {"id": "contraband", "name": "\u0412\u0435\u0440\u0441\u0442\u0430\u043a \u043a\u043e\u043d\u0442\u0440\u0430\u0431\u0430\u043d\u0434\u044b", "rate": 49795,
         "tags": ["solo"], "setup": "\u0423\u0447\u0430\u0441\u0442\u043e\u043a + \u0432\u0435\u0440\u0441\u0442\u0430\u043a ($40K/\u0448\u0442)",
         "risk": "\u0421\u0440\u0435\u0434\u043d\u0438\u0439 (\u0437\u0430\u0441\u0430\u0434\u044b \u0443 \u0442\u043e\u0447\u0435\u043a \u0441\u0431\u044b\u0442\u0430)", "riskClass": "jt-c-teal",
         "note": "$49 795/\u0447 \u0447\u0438\u0441\u0442\u044b\u043c\u0438 \u0441 \u0432\u0435\u0440\u0441\u0442\u0430\u043a\u0430 \u00b7 \u0440\u0430\u0441\u0442\u0451\u0442 \u043b\u0438\u043d\u0435\u0439\u043d\u043e",
         "est": False, "disputed": False},
        {"id": "police_shifts", "name": "\u0421\u043c\u0435\u043d\u044b \u0432 \u043f\u043e\u043b\u0438\u0446\u0438\u0438", "rate": 40000,
         "tags": ["noplot", "solo"], "setup": "$0 \u043d\u0430 \u0441\u0442\u0430\u0440\u0442 \u00b7 \u0432\u044b\u0434\u0430\u043d\u043d\u043e\u0435 \u0441\u043d\u0430\u0440\u044f\u0436\u0435\u043d\u0438\u0435 \u0438 \u043f\u0430\u0442\u0440\u0443\u043b\u044c\u043d\u0430\u044f \u043c\u0430\u0448\u0438\u043d\u0430",
         "risk": "\u041d\u0438\u0437\u043a\u0438\u0439 (\u043b\u0438\u043c\u0438\u0442 $1 \u043c\u043b\u043d \u0437\u0430 \u0441\u043c\u0435\u043d\u0443)", "riskClass": "jt-c-teal",
         "note": "$30K \u043e\u0431\u044b\u0447\u043d\u043e / $100K \u0432 \u043f\u0438\u043a \u0437\u0430 45-\u043c\u0438\u043d\u0443\u0442\u043d\u0443\u044e \u0441\u043c\u0435\u043d\u0443",
         "est": False, "disputed": False},
        {"id": "big_heists", "name": "\u041e\u0433\u0440\u0430\u0431\u043b\u0435\u043d\u0438\u044f \u0431\u0430\u043d\u043a\u0430 \u0438 Grand Hotel", "rate": 1000000,
         "tags": ["squad"], "setup": "\u041e\u0442\u0440\u044f\u0434 + \u043f\u043e\u0434\u0433\u043e\u0442\u043e\u0432\u043a\u0430 (\u0434\u0440\u0435\u043b\u044c / \u0433\u043b\u0443\u0448\u0438\u043b\u043a\u0430)",
         "risk": "\u041e\u0447\u0435\u043d\u044c \u0432\u044b\u0441\u043e\u043a\u0438\u0439 (\u0436\u0451\u0441\u0442\u043a\u043e\u0435 PvP \u0438 \u043f\u043e\u043b\u0438\u0446\u0438\u044f)", "riskClass": "jt-c-rose",
         "note": "$424K\u2013$5,9 \u043c\u043b\u043d \u0437\u0430 \u043e\u0433\u0440\u0430\u0431\u043b\u0435\u043d\u0438\u0435 (\u043e\u0446\u0435\u043d\u043a\u0430 ~1 \u0437\u0430 \u0447\u0430\u0441)",
         "est": True, "disputed": False},
        {"id": "clan_battles", "name": "\u041a\u043b\u0430\u043d\u043e\u0432\u044b\u0435 \u0431\u0438\u0437\u043d\u0435\u0441-\u0431\u0438\u0442\u0432\u044b", "rate": 900000,
         "tags": ["squad"], "setup": "\u041a\u043b\u0430\u043d \u043e\u0442 3 \u0438\u0433\u0440\u043e\u043a\u043e\u0432 + \u0437\u0430\u043b\u043e\u0433",
         "risk": "\u0412\u044b\u0441\u043e\u043a\u0438\u0439 (PvP 3v3 / 6v6 / 12v12)", "riskClass": "jt-c-rose",
         "note": "$250K / $500K / $900K \u0437\u0430 \u043e\u0431\u044a\u0435\u043a\u0442 + \u043d\u0430\u043b\u043e\u0433\u0438",
         "est": True, "disputed": False},
    ],
    "unlocks_prefix": "\u041e\u0442\u043a\u0440\u044b\u0432\u0430\u0435\u0442: ",
    "next_ms": "\u0421\u043b\u0435\u0434\u0443\u044e\u0449\u0430\u044f \u0432\u0435\u0445\u0430: ",
    "all_ms": "\u0412\u0441\u0435 \u043e\u0442\u0441\u043b\u0435\u0436\u0438\u0432\u0430\u0435\u043c\u044b\u0435 \u0432\u0435\u0445\u0438 \u043f\u0440\u043e\u0439\u0434\u0435\u043d\u044b",
    "goal_reached": "\u0426\u0435\u043b\u044c \u0434\u043e\u0441\u0442\u0438\u0433\u043d\u0443\u0442\u0430!",
    "yrs_left_tpl": "\u043e\u0441\u0442\u0430\u043b\u043e\u0441\u044c {n} {w}",
    "cap_reached": "\u041b\u0438\u043c\u0438\u0442 \u0441\u0435\u0440\u0432\u0435\u0440\u0430 40 \u043b\u0435\u0442 \u0434\u043e\u0441\u0442\u0438\u0433\u043d\u0443\u0442",
    "to_cap_tpl": "{m} \u0434\u043e \u043b\u0438\u043c\u0438\u0442\u0430 \u0441\u0435\u0440\u0432\u0435\u0440\u0430 40 \u043b\u0435\u0442",
    "no_wipes": "\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u0432\u0430\u0439\u043f\u044b \u043d\u0435 \u043d\u0443\u0436\u043d\u044b",
    "wipes_tpl": "\u041c\u0438\u043d. {n} {w} (7 \u0434\u043d\u0435\u0439 \u043a\u0430\u0436\u0434\u044b\u0439)",
    "wipes_tpl2": "\u041c\u0438\u043d. {n} {cw} (7 \u0434\u043d\u0435\u0439 \u043a\u0430\u0436\u0434\u044b\u0439)",
    "complete": "\u0413\u043e\u0442\u043e\u0432\u043e",
    "target_met": "\u0426\u0435\u043b\u044c \u0434\u043e\u0441\u0442\u0438\u0433\u043d\u0443\u0442\u0430 \u044d\u0442\u0438\u043c \u0432\u0430\u0439\u043f\u043e\u043c!",
    "all_unlocked": "\u0412\u0441\u0435 \u0440\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0438 \u043e\u0442\u043a\u0440\u044b\u0442\u044b",
    "unlocked": "\u041e\u0442\u043a\u0440\u044b\u0442\u043e",
    "locked": "\u0417\u0430\u043a\u0440\u044b\u0442\u043e",
    "target_tag": "\u0426\u0435\u043b\u044c",
    "set_target": "\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0446\u0435\u043b\u044c\u044e",
    "load": "\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c",
    "completed": "\u0412\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u043e!",
    "left_hours_tpl": "\u043e\u0441\u0442\u0430\u043b\u043e\u0441\u044c {n} {w} (~{h} \u0447)",
    "default_note": "\u0412\u0430\u0439\u043f \u0424\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u0431\u043b\u0430\u0432\u044b",
    "active": "\u0410\u043a\u0442\u0438\u0432\u0435\u043d",
    "use_route": "\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u044c \u043c\u0430\u0440\u0448\u0440\u0443\u0442",
    "per_hour": "/\u0447",
    "hrs_per_year_tpl": "{h} {hw} / {yw}",
    "next_year_tpl": "\u0414\u043e\u0431\u0430\u0432\u044c\u0442\u0435 \u0435\u0449\u0451 {m} \u0430\u043a\u0442\u0438\u0432\u043e\u0432 \u043a \u0432\u0430\u0439\u043f\u0443, \u0447\u0442\u043e\u0431\u044b \u043e\u0442\u043a\u0440\u044b\u0442\u044c \u0441\u043b\u0435\u0434\u0443\u044e\u0449\u0438\u0439 \u0433\u043e\u0434 (+\u0438\u0442\u043e\u0433\u043e {n} \u043b\u0435\u0442).",
    "cap_hint": "\u0412\u044b \u0434\u043e\u0441\u0442\u0438\u0433\u043b\u0438 \u043b\u0438\u043c\u0438\u0442\u0430 \u0432\u0430\u0439\u043f\u0430 \u0441\u0435\u0440\u0432\u0435\u0440\u0430 \u0432 40 \u043b\u0435\u0442 ($20 \u043c\u043b\u043d). \u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u0430\u043a\u0442\u0438\u0432\u044b \u043d\u0430 \u044d\u0442\u043e\u043c \u0441\u0435\u0440\u0432\u0435\u0440\u0435 \u0431\u043e\u043b\u044c\u0448\u0435 \u043b\u0435\u0442 \u043d\u0435 \u0434\u0430\u0434\u0443\u0442.",
    "over_cap_tpl": "\u041f\u0440\u0435\u0434\u0443\u043f\u0440\u0435\u0436\u0434\u0435\u043d\u0438\u0435 \u043e \u043f\u0435\u0440\u0435\u043b\u0438\u043c\u0438\u0442\u0435: {m} \u043f\u0440\u0435\u0432\u044b\u0448\u0430\u044e\u0442 \u043b\u0438\u043c\u0438\u0442 $20 \u043c\u043b\u043d / 40 \u043b\u0435\u0442 \u043d\u0430 \u0441\u0435\u0440\u0432\u0435\u0440. \u041f\u043e\u0442\u0440\u0430\u0442\u044c\u0442\u0435 \u0438\u0437\u043b\u0438\u0448\u0435\u043a \u0434\u0435\u043d\u0435\u0433 \u0434\u043e \u0432\u0430\u0439\u043f\u0430, \u0430 \u043d\u0435 \u043a\u043e\u043f\u0438\u0442\u0435 \u0438\u0445.",
    "lenny_on": "\u0412\u043a\u043b\u044e\u0447\u0435\u043d\u043e: $1 \u043c\u043b\u043d \u0437\u0430 +10 \u043b\u0435\u0442 (\u044d\u043a\u043e\u043d\u043e\u043c\u0438\u044f \u0444\u0430\u0440\u043c\u0430 \u043d\u0430 $4 \u043c\u043b\u043d)",
    "lenny_off": "\u0412\u044b\u043a\u043b\u044e\u0447\u0435\u043d\u043e: \u0441\u0442\u0430\u043d\u0434\u0430\u0440\u0442\u043d\u0430\u044f \u0441\u0442\u0430\u0432\u043a\u0430 $500 000/\u0433\u043e\u0434",
    "advice_goal": "\u0426\u0435\u043b\u044c \u0434\u043e\u0441\u0442\u0438\u0433\u043d\u0443\u0442\u0430! \u0422\u0435\u043a\u0443\u0449\u0438\u0439 \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442 \u0440\u0430\u0432\u0435\u043d \u0438\u043b\u0438 \u043f\u0440\u0435\u0432\u044b\u0448\u0430\u0435\u0442 {t} \u043b\u0435\u0442. \u041f\u043e\u0441\u0442\u0430\u0432\u044c\u0442\u0435 \u0446\u0435\u043b\u044c \u043f\u043e\u0432\u044b\u0448\u0435 \u2014 \u043d\u0430\u043f\u0440\u0438\u043c\u0435\u0440, STAR-H (180 \u043b\u0435\u0442) \u0438\u043b\u0438 \u041c\u0430\u0441\u043a\u0430 \u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044f (800 \u043b\u0435\u0442), \u0447\u0442\u043e\u0431\u044b \u043f\u0440\u043e\u0434\u043e\u043b\u0436\u0438\u0442\u044c \u043e\u0442\u0441\u043b\u0435\u0436\u0438\u0432\u0430\u0442\u044c.",
    "advice_lenny": "\u0421\u043e\u0432\u0435\u0442 \u043f\u043e \u044d\u0444\u0444\u0435\u043a\u0442\u0438\u0432\u043d\u043e\u0441\u0442\u0438: \u0435\u0441\u043b\u0438 \u0432\u044b \u0435\u0449\u0451 \u043d\u0435 \u043f\u043e\u0433\u0430\u0441\u0438\u043b\u0438 \u0434\u043e\u043b\u0433 \u041b\u0435\u043d\u043d\u0438 $1 000 000, \u0441\u0434\u0435\u043b\u0430\u0439\u0442\u0435 \u044d\u0442\u043e \u0432 \u043f\u0435\u0440\u0432\u0443\u044e \u043e\u0447\u0435\u0440\u0435\u0434\u044c \u2014 \u044d\u0442\u043e +10 \u043b\u0435\u0442 \u043f\u043e $100 000 \u0437\u0430 \u0433\u043e\u0434 (\u0432 5 \u0440\u0430\u0437 \u0432\u044b\u0433\u043e\u0434\u043d\u0435\u0435 \u043e\u0431\u044b\u0447\u043d\u043e\u0439 \u043a\u043e\u043d\u0432\u0435\u0440\u0442\u0430\u0446\u0438\u0438 \u043f\u0440\u0438 \u0432\u0430\u0439\u043f\u0435) \u0438 \u0441\u0432\u0435\u0440\u0445 \u043b\u0438\u043c\u0438\u0442\u0430 40 \u043b\u0435\u0442.",
    "advice_under": "\u0412\u043d\u0438\u043c\u0430\u043d\u0438\u0435: \u0430\u043a\u0442\u0438\u0432\u044b \u043c\u0435\u043d\u044c\u0448\u0435 $500 000 \u043e\u043a\u0440\u0443\u0433\u043b\u044f\u044e\u0442\u0441\u044f \u0432\u043d\u0438\u0437 \u0434\u043e 0 \u043b\u0435\u0442 \u043f\u0440\u0438 \u0432\u0430\u0439\u043f\u0435. \u0417\u0430\u0439\u043c\u0438\u0442\u0435\u0441\u044c \u043e\u0433\u0440\u0430\u0431\u043b\u0435\u043d\u0438\u044f\u043c\u0438 \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u043e\u0432 \u0438\u043b\u0438 \u0441\u043c\u0435\u043d\u0430\u043c\u0438 \u0432 \u043f\u043e\u043b\u0438\u0446\u0438\u0438, \u0447\u0442\u043e\u0431\u044b \u043d\u0430\u043a\u043e\u043f\u0438\u0442\u044c \u0445\u043e\u0442\u044f \u0431\u044b $500K \u0447\u0438\u0441\u0442\u044b\u043c\u0438 \u0434\u0435\u043d\u044c\u0433\u0430\u043c\u0438 \u0432 \u0431\u0430\u043d\u043a\u0435 \u0434\u043e \u0424\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u0431\u043b\u0430\u0432\u044b.",
    "advice_route": "\u041f\u043b\u0430\u043d \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u0430: \u0441 \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u043e\u043c {method} ({rate}/\u0447) \u0434\u043e\u0441\u0442\u0438\u0447\u044c {t} \u043b\u0435\u0442 \u0437\u0430\u0439\u043c\u0451\u0442 ~{h} \u0447. \u041e\u0442\u043c\u043e\u0439\u0442\u0435 \u0433\u0440\u044f\u0437\u043d\u044b\u0435 \u0434\u0435\u043d\u044c\u0433\u0438 \u0434\u043e \u0432\u0430\u0439\u043f\u0430 \u0438 \u0441\u0442\u0440\u0435\u043c\u0438\u0442\u0435\u0441\u044c \u043a \u0441\u0443\u043c\u043c\u0430\u043c, \u043a\u0440\u0430\u0442\u043d\u044b\u043c $500K, \u0447\u0442\u043e\u0431\u044b \u043d\u0435 \u0442\u0435\u0440\u044f\u0442\u044c \u043d\u0430 \u043e\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u0438.",
    "toast_saved": "\u0426\u0435\u043b\u044c \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0430: {label}",
    "toast_dup": "{t} \u043b\u0435\u0442 \u0443\u0436\u0435 \u0435\u0441\u0442\u044c \u0432 \u0442\u0440\u0435\u043a\u0435\u0440\u0435 \u0446\u0435\u043b\u0435\u0439",
    "toast_reset": "\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u044f \u0441\u0431\u0440\u043e\u0448\u0435\u043d\u044b \u043a \u0441\u0442\u0430\u043d\u0434\u0430\u0440\u0442\u043d\u044b\u043c",
    "toast_route": "\u0410\u043a\u0442\u0438\u0432\u043d\u044b\u0439 \u043c\u0430\u0440\u0448\u0440\u0443\u0442: {name}",
    "toast_target": "\u0426\u0435\u043b\u044c \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0430: {t} \u043b\u0435\u0442",
    "toast_logged": "\u0417\u0430\u043f\u0438\u0441\u0430\u043d\u043e +{y} \u043b\u0435\u0442 \u00b7 \u0418\u0442\u043e\u0433\u043e: {t} \u043b\u0435\u0442",
    "toast_invalid": "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043a\u043e\u0440\u0440\u0435\u043a\u0442\u043d\u043e\u0435 \u0447\u0438\u0441\u043b\u043e \u043f\u043e\u043b\u0443\u0447\u0435\u043d\u043d\u044b\u0445 \u043b\u0435\u0442",
    "toast_cleared": "\u0418\u0441\u0442\u043e\u0440\u0438\u044f \u0432\u0430\u0439\u043f\u043e\u0432 \u043e\u0447\u0438\u0449\u0435\u043d\u0430",
    "est": "\u043e\u0446\u0435\u043d\u043a\u0430",
    "disputed": "\u0421\u043f\u043e\u0440\u043d\u043e",
    "cap_suffix": "\u043b\u0438\u043c\u0438\u0442 40 \u043b\u0435\u0442",
    "risk_label": "\u0420\u0438\u0441\u043a: ",
    "daily_tpl": "{h} \u0447/\u0434\u0435\u043d\u044c",
    "hrs_day_tpl": "{d} {dw} \u043f\u043e {h} \u0447/{day} \u00b7 {method}",
    "min_wipes_tpl": "{n} {w} ({d} {dw})",
    "yrs_unit": "\u043b\u0435\u0442",
    },
    },
}

TARGET_CHIPS = {
    "en": [(5, "AFAK"), (15, "CB45 Mk1"), (40, "1 Full Wipe"), (60, "Police Radio"),
           (180, "STAR-H"), (275, "Car Radio"), (410, "Cargo Sheet"),
           (800, "Silence Mask"), (950, "DRM-14")],
    "ru": [(5, "AFAK"), (15, "CB45 Mk1"), (40, "\u041f\u043e\u043b\u043d\u044b\u0439 \u0432\u0430\u0439\u043f"),
           (60, "\u041f\u043e\u043b\u0438\u0446\u0435\u0439\u0441\u043a\u0430\u044f \u0440\u0430\u0446\u0438\u044f"), (180, "STAR-H"),
           (275, "\u0410\u0432\u0442\u043e\u0440\u0430\u0446\u0438\u044f"), (410, "\u0413\u0440\u0443\u0437\u043e\u0432\u043e\u0439 \u043b\u0438\u0441\u0442"),
           (800, "\u041c\u0430\u0441\u043a\u0430 \u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044f"), (950, "DRM-14")],
}
ASSET_CHIPS = {
    "en": [(500000, "$500K (1 yr)"), (2500000, "$2.5M (5 yrs)"),
           (5000000, "$5M (10 yrs)"), (10000000, "$10M (20 yrs)"),
           (20000000, "$20M (40 yrs cap)")],
    "ru": [(500000, "$500K (1 \u0433\u043e\u0434)"), (2500000, "$2,5M (5 \u043b\u0435\u0442)"),
           (5000000, "$5M (10 \u043b\u0435\u0442)"), (10000000, "$10M (20 \u043b\u0435\u0442)"),
           (20000000, "$20M (\u043b\u0438\u043c\u0438\u0442 40 \u043b\u0435\u0442)")],
}
GROW_LABELS = {
    "en": ("6 Uncommon ($129.6K/h)", "Maxed Farm ($500K/h)"),
    "ru": ("6 Uncommon ($129,6K/\u0447)", "\u041f\u0440\u043e\u043a\u0430\u0447\u0430\u043d\u043d\u0430\u044f \u0444\u0435\u0440\u043c\u0430 ($500K/\u0447)"),
}
ASSETS_PH = {"en": "e.g. 5000000", "ru": "\u043d\u0430\u043f\u0440. 5000000"}
BIG_UNIT = {"en": "yrs", "ru": "\u043b\u0435\u0442"}


def body_html(lang):
    c = JT[lang]
    unit = BIG_UNIT[lang]
    pills = "".join('<span class="wlh-pill">%s</span>' % p for p in c["pills"])
    target_chips = "".join(
        '<button type="button" data-target="%s" class="jt-chip target-chip%s">%s %s \u00b7 %s</button>'
        % (yrs, " active" if yrs == 60 else "", yrs, unit, name)
        for yrs, name in TARGET_CHIPS[lang])
    asset_chips = "".join(
        '<button type="button" data-assets="%s" class="jt-chip asset-chip">%s</button>'
        % (val, label) for val, label in ASSET_CHIPS[lang])
    conv_items = "".join("<li>%s</li>" % x for x in c["conv_list"])
    keep_items = "".join("<li>%s</li>" % x for x in c["keep_list"])
    rules = "".join('<div class="jt-rule">%s</div>' % r for r in c["rules"])
    sources = "".join(
        '<li><a href="%s" target="_blank" rel="noopener noreferrer">%s</a> (%s)</li>'
        % (url, text, note) for text, url, note in c["sources"])
    faq = "".join(
        '<details><summary><h3>%s</h3><span class="plus">+</span></summary>'
        '<p>%s</p></details>' % (q, a) for q, a in c["faq"])
    grow_std, grow_max = GROW_LABELS[lang]
    tabs = (
        '<button type="button" role="tab" data-tab="calculator" aria-selected="true" class="jt-tab">%s</button>'
        '<button type="button" role="tab" data-tab="methods" aria-selected="false" class="jt-tab">%s</button>'
        '<button type="button" role="tab" data-tab="unlocks" aria-selected="false" class="jt-tab">%s</button>'
        '<button type="button" role="tab" data-tab="tracker" aria-selected="false" class="jt-tab"><span>%s</span><span id="trackerBadge" class="jt-count">0</span></button>'
        % (c["tab1"], c["tab2"], c["tab3"], c["tab4"]))
    return (
        '<section class="tool-hero">'
        '<p class="wlh-eyebrow">%s</p><h1>%s</h1>'
        '<p class="lede">%s</p><div class="wlh-pills">%s</div></section>'
        % (c["eyebrow"], c["h1"], c["lede"], pills)
        + '<section class="jt-kpi-grid" aria-label="%s">' % c["tab1"]
        + '<div class="jt-kpi"><div class="jt-kpi-top"><span>%s</span><strong id="kpiPercent">25.0%%</strong></div>'
          '<div id="kpiYearsGap" class="jt-kpi-val">45 %s</div>'
          '<div class="wlh-progress"><span id="kpiProgressBar" style="width: 25%%"></span></div></div>'
          % (c["kpi1"], unit)
        + '<div class="jt-kpi"><div class="jt-kpi-top"><span>%s</span></div>'
          '<div id="kpiWipeGain" class="jt-kpi-val teal">+5 %s</div>'
          '<div id="kpiWipeSub" class="jt-kpi-sub">$17.50M</div></div>' % (c["kpi2"], unit)
        + '<div class="jt-kpi"><div class="jt-kpi-top"><span>%s</span></div>'
          '<div id="kpiCashNeeded" class="jt-kpi-val">$22.50M</div>'
          '<div id="kpiWipesNeeded" class="jt-kpi-sub"></div></div>' % c["kpi3"]
        + '<div class="jt-kpi"><div class="jt-kpi-top"><span>%s</span></div>'
          '<div id="kpiHoursNeeded" class="jt-kpi-val copper">112.5</div>'
          '<div id="kpiDaysSub" class="jt-kpi-sub"></div></div></section>' % c["kpi4"]
        + '<nav class="jt-tabs" role="tablist" aria-label="%s">%s</nav>' % (c["tab1"], tabs)
        + '<section id="panel-calculator" class="jt-grid" aria-label="%s">' % c["tab1"]
        + '<div class="panel">'
        + '<div class="jt-sec-head"><h2>%s</h2><button id="resetInputsBtn" type="button" class="jt-link-btn">%s</button></div>'
          % (c["calc_h"], c["reset"])
        + '<div class="jt-two-col">'
        + '<div class="jt-field-box"><label for="currentJailInput" class="jt-field-label">%s</label>'
          '<div class="jt-big-wrap"><input id="currentJailInput" type="number" min="0" max="1200" step="1" value="15" class="jt-big"><span class="jt-big-unit">%s</span></div>'
          '<p class="jt-field-hint">%s</p></div>' % (c["cur_label"], unit, c["cur_hint"])
        + '<div class="jt-field-box"><label for="targetAuthorityInput" class="jt-field-label">%s</label>'
          '<div class="jt-big-wrap"><input id="targetAuthorityInput" type="number" min="1" max="1200" step="1" value="60" class="jt-big amber"><span class="jt-big-unit">%s</span></div>'
          '<p id="targetMilestoneHint" class="jt-field-hint amber"></p></div></div>' % (c["tgt_label"], unit)
        + '<div style="margin-top:14px;"><div class="jt-field-label">%s</div><div class="jt-chip-row">%s</div></div>'
          % (c["quick_label"], target_chips)
        + '<div class="jt-field-box" style="margin-top:14px;">'
        + '<div style="display:flex;justify-content:space-between;gap:8px;align-items:baseline;"><label for="serverAssetsInput" class="jt-field-label">%s</label><strong id="assetsCapNote" style="color:var(--teal-deep);font-size:var(--fs-small);"></strong></div>'
          % c["assets_label"]
        + '<div class="jt-big-wrap"><span style="font-size:20px;font-weight:700;color:var(--teal-deep);">$</span><input id="serverAssetsInput" type="number" min="0" max="100000000" step="100000" value="2500000" class="jt-big"></div>'
        + '<div class="jt-chip-row">%s</div>' % asset_chips
        + '<p class="jt-field-hint">%s</p></div>' % c["assets_hint"]
        + '<div class="jt-two-col" style="margin-top:14px;">'
        + '<div class="jt-field-box"><div style="display:flex;justify-content:space-between;gap:12px;align-items:flex-start;">'
          '<div><div style="font-size:var(--fs-card);font-weight:700;color:var(--ink);">%s</div><p class="jt-field-hint" style="margin-top:2px;">%s</p></div>'
          '<label class="jt-switch" aria-label="%s"><input id="planLennyToggle" type="checkbox"><span class="jt-slider"></span></label></div>'
          '<p id="lennyStatusText" class="jt-field-hint" style="margin-top:10px;"></p></div>'
          % (c["lenny_title"], c["lenny_sub"], c["lenny_title"])
        + '<div class="jt-field-box"><div style="display:flex;justify-content:space-between;gap:8px;align-items:baseline;">'
          '<label for="dailyHoursRange" style="font-size:var(--fs-card);font-weight:700;color:var(--ink);">%s</label>'
          '<strong id="dailyHoursLabel" style="color:var(--teal-deep);"></strong></div>'
          '<input id="dailyHoursRange" type="range" min="0.5" max="12" step="0.5" value="3" class="jt-range">'
          '<label for="activeMethodSelect" class="jt-field-label" style="margin-top:6px;">%s</label>'
          '<div class="select-wrap"><select id="activeMethodSelect"></select></div></div></div></div>'
          % (c["daily_label"], c["method_label"])
        + '<div class="panel">'
        + '<div class="jt-sec-head"><h2>%s</h2></div>' % c["brk_h"]
        + '<div class="jt-field-box"><div style="display:flex;justify-content:space-between;gap:8px;align-items:baseline;">'
          '<span class="jt-field-label">%s</span><strong id="wipeCapRatio" style="color:var(--teal-deep);"></strong></div>'
          '<div class="wlh-progress" style="margin:10px 0 0;"><span id="wipeCapBar" style="width: 12.5%%"></span></div>'
          '<p id="nextYearHint" class="jt-field-hint" style="margin-top:10px;"></p>'
          '<div id="overCapWarning" class="jt-note-danger jt-hidden"></div></div>' % c["cap_label"]
        + '<div class="jt-kv">'
        + '<div class="jt-kv-row"><span class="jt-kv-label">%s</span><span id="detailPostWipeTotal" class="jt-kv-val copper"></span></div>' % c["kv1"]
        + '<div class="jt-kv-row"><span class="jt-kv-label">%s</span><span id="detailPostWipeGap" class="jt-kv-val"></span></div>' % c["kv2"]
        + '<div class="jt-kv-row"><span class="jt-kv-label">%s</span><span id="detailMinWipes" class="jt-kv-val teal"></span></div>' % c["kv3"]
        + '<div class="jt-kv-row"><span class="jt-kv-label">%s</span><span id="detailHoursPerYear" class="jt-kv-val"></span></div>' % c["kv4"]
        + '<div class="jt-kv-row"><span class="jt-kv-label">%s</span><span id="detailNextUnlock" class="jt-kv-val copper"></span></div></div>' % c["kv5"]
        + '<div id="strategyAdviceBox" class="wlh-note"></div></div></section>'
        + '<section id="panel-methods" class="jt-hidden" aria-label="%s"><div class="panel">' % c["tab2"]
        + '<div class="jt-sec-head" style="flex-wrap:wrap;"><div><h2>%s</h2><p class="jt-field-hint" style="margin-top:3px;">%s</p></div>'
          '<div class="jt-chip-row" style="margin-top:0;">'
          '<button type="button" data-filter="all" class="jt-chip method-filter-btn active">%s</button>'
          '<button type="button" data-filter="noplot" class="jt-chip method-filter-btn">%s</button>'
          '<button type="button" data-filter="solo" class="jt-chip method-filter-btn">%s</button>'
          '<button type="button" data-filter="squad" class="jt-chip method-filter-btn">%s</button>'
          '</div></div>' % (c["meth_h"], c["meth_sub"], c["filter_all"], c["filter_noplot"], c["filter_solo"], c["filter_squad"])
        + '<div class="jt-controls"><div><b>%s</b> <span class="jt-seg">'
          '<button type="button" data-benches="1" class="jt-seg-btn bench-btn active">1</button>'
          '<button type="button" data-benches="2" class="jt-seg-btn bench-btn">2</button>'
          '<button type="button" data-benches="3" class="jt-seg-btn bench-btn">3</button>'
          '<button type="button" data-benches="4" class="jt-seg-btn bench-btn">4</button></span></div>'
          '<div><b>%s</b> <span class="jt-seg">'
          '<button type="button" data-grow="standard" class="jt-seg-btn grow-btn active">%s</button>'
          '<button type="button" data-grow="maxed" class="jt-seg-btn grow-btn">%s</button></span></div></div>'
          % (c["bench_label"], c["grow_label"], grow_std, grow_max)
        + '<div class="jt-field-box"><div style="display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;">'
          '<strong style="font-size:var(--fs-card);color:var(--ink);">%s</strong><span class="jt-field-hint">%s</span></div>'
          '<div class="jt-bars" id="methodsBars"></div></div>' % (c["bars_h"], c["bars_src"])
        + '<div class="jt-table-wrap"><table class="jt-table"><thead><tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th style="text-align:right;">%s</th></tr></thead>'
          '<tbody id="methodsTableBody"></tbody></table></div></div></section>'
          % (c["th1"], c["th2"], c["th3"], c["th4"], c["th5"], c["th6"])
        + '<section id="panel-unlocks" class="jt-hidden jt-grid" aria-label="%s">' % c["tab3"]
        + '<div class="panel"><div class="jt-sec-head"><div><h2>%s</h2><p class="jt-field-hint" style="margin-top:3px;">%s</p></div></div>'
          '<div id="milestonesList" class="jt-ms-list"></div></div>'
          % (c["unlock_h"], c["unlock_sub"])
        + '<div class="jt-stack"><div class="panel">'
        + '<h2 style="margin:0 0 12px;font-size:var(--fs-h4);color:var(--ink);">%s</h2>' % c["conv_h"]
        + '<div class="jt-convert"><div class="jt-convert-box ok"><b>%s</b><ul>%s</ul></div>'
          '<div class="jt-convert-box warn"><b>%s</b><ul>%s</ul></div></div></div>'
          % (c["conv_ok"], conv_items, c["conv_warn"], keep_items)
        + '<div class="panel">'
        + '<h2 style="margin:0 0 10px;font-size:var(--fs-h4);color:var(--ink);">%s</h2>' % c["rules_h"]
        + '<div class="jt-rules">%s</div></div></div></section>' % rules
        + '<section id="panel-tracker" class="jt-hidden jt-grid" aria-label="%s">' % c["tab4"]
        + '<div class="panel">'
        + '<div class="jt-sec-head"><div><h2>%s</h2><p class="jt-field-hint" style="margin-top:3px;">%s</p></div>'
          '<button id="addGoalFromCalcBtn" type="button" class="btn btn-primary" style="height:40px;padding:0 14px;font-size:var(--fs-small);">%s</button></div>'
          % (c["trk_h"], c["trk_sub"], c["trk_add"])
        + '<div id="goalsEmpty" class="jt-empty"><b>%s</b><p style="margin:6px 0 0;font-size:var(--fs-small);">%s</p></div>'
          '<div id="goalsList" class="jt-hidden"></div></div>' % (c["trk_empty_b"], c["trk_empty_p"])
        + '<div class="panel">'
        + '<h2 style="margin:0 0 4px;font-size:var(--fs-h4);color:var(--ink);">%s</h2>' % c["log_h"]
        + '<p class="jt-field-hint" style="margin-bottom:14px;">%s</p>' % c["log_sub"]
        + '<form id="wipeLogForm" style="display:flex;flex-direction:column;gap:10px;">'
        + '<div class="jt-two-col">'
        + '<div class="field"><label for="logYearsInput">%s</label><input id="logYearsInput" type="number" min="1" max="50" value="10" required></div>' % c["log_years"]
        + '<div class="field"><label for="logAssetsInput">%s</label><input id="logAssetsInput" type="number" min="0" step="100000" placeholder="%s"></div></div>' % (c["log_assets"], ASSETS_PH[lang])
        + '<div class="field"><label for="logNoteInput">%s</label><input id="logNoteInput" type="text" placeholder="%s"></div>' % (c["log_note"], c["log_note_ph"])
        + '<button type="submit" class="btn btn-primary" style="width:100%%;">%s</button></form>' % c["log_submit"]
        + '<div style="margin-top:18px;padding-top:14px;border-top:1px solid var(--line);">'
        + '<div class="jt-sec-head" style="margin-bottom:8px;"><span style="font-size:var(--fs-card);font-weight:700;color:var(--ink);">%s</span>'
          '<button id="clearLogsBtn" type="button" class="jt-link-btn danger jt-hidden">%s</button></div>' % (c["hist_h"], c["hist_clear"])
        + '<div id="logsEmpty" class="jt-empty" style="padding:18px;">%s</div>' % c["hist_empty"]
        + '<div id="logsList" class="jt-hidden"></div></div></div></section>'
        + '<article class="wlh-article" id="guide">'
        + '<p class="wlh-eyebrow">%s</p><h2>%s</h2><p>%s</p>' % (c["eyebrow"], c["guide_h"], c["guide_p1"])
        + '<h3>%s</h3><p>%s</p><p class="wlh-note">%s</p>' % (c["guide_h3a"], c["guide_p2"], c["caveat"])
        + '<h3>%s</h3><p>%s</p>' % (c["guide_h3b"], c["guide_p3"])
        + '<h3>%s</h3><ul>%s</ul>' % (c["guide_h3c"], sources)
        + '<div class="faq"><h2>%s</h2>%s</div></article>' % (c["faq_h"], faq)
        + '<p class="data-line">%s</p>' % c["research"]
        + '<div class="wlh-toast" id="toast" role="status" aria-live="polite"></div>')

JT_JS = r"""
(()=>{'use strict';
const STR=__STR__;
const $=id=>document.getElementById(id);
const DOLLARS_PER_YEAR=500000, SERVER_CAP_YEARS=40, OVERALL_CAP_YEARS=1200, LENNY_COST=1000000, LENNY_YEARS=10;
const MILESTONES=STR.milestones;
const BASE_METHODS=STR.methods;
const STORAGE_KEY=STR.storage_key;
const state={currentJailTime:15,targetAuthority:60,serverAssets:2500000,planLenny:false,dailyHours:3,activeMethodId:'store_runs',activeTab:'calculator',methodFilter:'all',benchCount:1,growMode:'standard',goals:[],logs:[]};
let toastTimer=null;
const el={kpiPercent:$('kpiPercent'),kpiYearsGap:$('kpiYearsGap'),kpiProgressBar:$('kpiProgressBar'),kpiWipeGain:$('kpiWipeGain'),kpiWipeSub:$('kpiWipeSub'),kpiCashNeeded:$('kpiCashNeeded'),kpiWipesNeeded:$('kpiWipesNeeded'),kpiHoursNeeded:$('kpiHoursNeeded'),kpiDaysSub:$('kpiDaysSub'),currentJailInput:$('currentJailInput'),targetAuthorityInput:$('targetAuthorityInput'),targetMilestoneHint:$('targetMilestoneHint'),serverAssetsInput:$('serverAssetsInput'),assetsCapNote:$('assetsCapNote'),planLennyToggle:$('planLennyToggle'),lennyStatusText:$('lennyStatusText'),dailyHoursRange:$('dailyHoursRange'),dailyHoursLabel:$('dailyHoursLabel'),activeMethodSelect:$('activeMethodSelect'),resetInputsBtn:$('resetInputsBtn'),wipeCapRatio:$('wipeCapRatio'),wipeCapBar:$('wipeCapBar'),nextYearHint:$('nextYearHint'),overCapWarning:$('overCapWarning'),detailPostWipeTotal:$('detailPostWipeTotal'),detailPostWipeGap:$('detailPostWipeGap'),detailMinWipes:$('detailMinWipes'),detailHoursPerYear:$('detailHoursPerYear'),detailNextUnlock:$('detailNextUnlock'),strategyAdviceBox:$('strategyAdviceBox'),methodsBars:$('methodsBars'),methodsTableBody:$('methodsTableBody'),milestonesList:$('milestonesList'),trackerBadge:$('trackerBadge'),addGoalFromCalcBtn:$('addGoalFromCalcBtn'),goalsEmpty:$('goalsEmpty'),goalsList:$('goalsList'),wipeLogForm:$('wipeLogForm'),logYearsInput:$('logYearsInput'),logAssetsInput:$('logAssetsInput'),logNoteInput:$('logNoteInput'),clearLogsBtn:$('clearLogsBtn'),logsEmpty:$('logsEmpty'),logsList:$('logsList'),toast:$('toast')};
function plural(n,f1,f234,f5){if(n%10===1&&n%100!==11)return f1;if(n%10>=2&&n%10<=4&&(n%100<10||n%100>=20))return f234;return f5}
function yrsWord(n){return plural(n,STR.yr_1,STR.yr_234,STR.yr_5)}
function fmt(x,d){return x.toFixed(d).replace('.',STR.dec)}
function formatMoney(val){if(!Number.isFinite(val))return '$0';if(val>=1000000)return '$'+(val/1000000).toFixed(val%1000000===0?0:2).replace('.',STR.dec)+'M';if(val>=1000)return '$'+Math.round(val/1000).toLocaleString(STR.locale)+'K';return '$'+Math.round(val).toLocaleString(STR.locale)}
function escapeText(x){return String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function showToast(msg){el.toast.textContent=msg;el.toast.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>el.toast.classList.remove('show'),2500)}
function getDynamicMethods(){return BASE_METHODS.map(function(m){const copy=Object.assign({},m);if(copy.id==='contraband'){copy.ratePerHour=m.rate*state.benchCount;copy.name=m.name+' ('+state.benchCount+'x)';}else if(copy.id==='grow_room'){if(state.growMode==='maxed'){copy.ratePerHour=m.maxRate;copy.name=m.maxName;copy.note=m.maxNote;copy.est=true;copy.disputed=false;}else{copy.ratePerHour=m.rate;copy.name=m.name;copy.note=m.note;copy.est=false;copy.disputed=true;}}else{copy.ratePerHour=m.rate;}return copy;});}
function getActiveMethod(){const list=getDynamicMethods();return list.find(m=>m.id===state.activeMethodId)||list[0];}
function loadTracker(){try{const raw=localStorage.getItem(STORAGE_KEY);if(raw){const data=JSON.parse(raw);if(Array.isArray(data.goals))state.goals=data.goals.slice(0,20);if(Array.isArray(data.logs))state.logs=data.logs.slice(0,30);}}catch(e){state.goals=[];state.logs=[];}}
function saveTracker(){try{localStorage.setItem(STORAGE_KEY,JSON.stringify({goals:state.goals.slice(0,20),logs:state.logs.slice(0,30)}));}catch(e){}}
function populateMethodSelect(){const methods=getDynamicMethods();el.activeMethodSelect.innerHTML=methods.map(m=>'<option value="'+m.id+'">'+escapeText(m.name)+' \u00b7 '+formatMoney(m.ratePerHour)+STR.per_hour+(m.est?' '+STR.est:'')+(m.disputed?' ('+STR.disputed+')':'')+'</option>').join('');el.activeMethodSelect.value=state.activeMethodId;}
function findMilestoneLabel(years){const exact=MILESTONES.find(m=>m.years===years);if(exact)return STR.unlocks_prefix+exact.title;const next=MILESTONES.find(m=>m.years>years);if(next)return STR.next_ms+next.years+' '+yrsWord(next.years)+' ('+next.title+')';return STR.all_ms;}
function renderCalculator(){
  const cur=Math.max(0,Math.min(OVERALL_CAP_YEARS,state.currentJailTime));
  const tgt=Math.max(1,Math.min(OVERALL_CAP_YEARS,state.targetAuthority));
  const assets=Math.max(0,state.serverAssets);
  const method=getActiveMethod();
  const rawAssetYears=Math.floor(assets/DOLLARS_PER_YEAR);
  const cappedAssetYears=Math.min(SERVER_CAP_YEARS,rawAssetYears);
  const lennyBonus=state.planLenny?LENNY_YEARS:0;
  const totalThisWipe=Math.min(OVERALL_CAP_YEARS-cur,cappedAssetYears+lennyBonus);
  const remainingYears=Math.max(0,tgt-cur);
  const pct=tgt>0?Math.min(100,(cur/tgt)*100):100;
  let cashForTarget=0, yearsByAssets=remainingYears;
  if(state.planLenny&&remainingYears>0){
    if(remainingYears<=LENNY_YEARS){cashForTarget=LENNY_COST;yearsByAssets=0;}
    else{yearsByAssets=remainingYears-LENNY_YEARS;cashForTarget=LENNY_COST+yearsByAssets*DOLLARS_PER_YEAR;}
  }else{cashForTarget=remainingYears*DOLLARS_PER_YEAR;}
  const wipesNeeded=yearsByAssets>0?Math.ceil(yearsByAssets/SERVER_CAP_YEARS):(remainingYears>0?1:0);
  const hoursNeeded=method.ratePerHour>0?cashForTarget/method.ratePerHour:0;
  const daysNeeded=state.dailyHours>0?Math.ceil(hoursNeeded/state.dailyHours):0;
  const hoursPerYear=method.ratePerHour>0?DOLLARS_PER_YEAR/method.ratePerHour:0;
  el.kpiPercent.textContent=fmt(pct,1)+'%';
  el.kpiProgressBar.style.width=fmt(pct,1)+'%';
  el.kpiYearsGap.textContent=remainingYears===0?STR.goal_reached:STR.yrs_left_tpl.replace('{n}',remainingYears).replace('{w}',yrsWord(remainingYears));
  el.kpiWipeGain.textContent='+'+totalThisWipe+' '+yrsWord(totalThisWipe);
  const cashToCap=Math.max(0,SERVER_CAP_YEARS*DOLLARS_PER_YEAR-assets);
  el.kpiWipeSub.textContent=cappedAssetYears>=SERVER_CAP_YEARS?STR.cap_reached+(state.planLenny?' (+10 Lenny)':''):STR.to_cap_tpl.replace('{m}',formatMoney(cashToCap));
  el.kpiCashNeeded.textContent=formatMoney(cashForTarget);
  el.kpiWipesNeeded.textContent=remainingYears===0?STR.no_wipes:STR.wipes_tpl2.replace('{n}',wipesNeeded).replace('{cw}',plural(wipesNeeded,STR.cw_1,STR.cw_234,STR.cw_5));
  el.kpiHoursNeeded.textContent=fmt(hoursNeeded,1)+' '+plural(Math.floor(hoursNeeded),STR.h_1,STR.h_234,STR.h_5);
  el.kpiDaysSub.textContent=STR.hrs_day_tpl.replace('{d}',daysNeeded).replace('{dw}',plural(daysNeeded,STR.d_1,STR.d_234,STR.d_5)).replace('{h}',fmt(state.dailyHours,1)).replace('{day}',STR.day_word).replace('{method}',method.name.split(' (')[0]);
  el.targetMilestoneHint.textContent=findMilestoneLabel(tgt);
  el.assetsCapNote.textContent='+'+cappedAssetYears+' '+yrsWord(cappedAssetYears)+(state.planLenny?' + 10 Lenny':'')+' ('+STR.cap_suffix+')';
  el.lennyStatusText.textContent=state.planLenny?STR.lenny_on:STR.lenny_off;
  el.dailyHoursLabel.textContent=STR.daily_tpl.replace('{h}',fmt(state.dailyHours,1));
  document.querySelectorAll('.target-chip').forEach(function(btn){const val=parseInt(btn.getAttribute('data-target'),10);btn.classList.toggle('active',val===tgt);});
  const capPct=Math.min(100,(cappedAssetYears/SERVER_CAP_YEARS)*100);
  el.wipeCapRatio.textContent=cappedAssetYears+' / '+SERVER_CAP_YEARS+' '+yrsWord(SERVER_CAP_YEARS);
  el.wipeCapBar.style.width=fmt(capPct,1)+'%';
  if(cappedAssetYears<SERVER_CAP_YEARS){const remainder=assets%DOLLARS_PER_YEAR;const needForNext=DOLLARS_PER_YEAR-remainder;el.nextYearHint.textContent=STR.next_year_tpl.replace('{m}',formatMoney(needForNext)).replace('{n}',cappedAssetYears+1);}
  else{el.nextYearHint.textContent=STR.cap_hint;}
  if(assets>SERVER_CAP_YEARS*DOLLARS_PER_YEAR){const wasted=assets-SERVER_CAP_YEARS*DOLLARS_PER_YEAR;el.overCapWarning.textContent=STR.over_cap_tpl.replace('{m}',formatMoney(wasted));el.overCapWarning.classList.remove('jt-hidden');}
  else{el.overCapWarning.classList.add('jt-hidden');}
  const postWipeTotal=Math.min(OVERALL_CAP_YEARS,cur+totalThisWipe);
  const postWipeGap=Math.max(0,tgt-postWipeTotal);
  el.detailPostWipeTotal.textContent=postWipeTotal+' '+yrsWord(postWipeTotal);
  el.detailPostWipeGap.textContent=postWipeGap===0?STR.target_met:postWipeGap+' '+yrsWord(postWipeGap);
  el.detailMinWipes.textContent=wipesNeeded===0?STR.complete:STR.min_wipes_tpl.replace('{n}',wipesNeeded).replace('{w}',plural(wipesNeeded,STR.w_1,STR.w_234,STR.w_5)).replace('{d}',wipesNeeded*7).replace('{dw}',plural(wipesNeeded*7,STR.d_1,STR.d_234,STR.d_5));
  el.detailHoursPerYear.textContent=STR.hrs_per_year_tpl.replace('{h}',fmt(hoursPerYear,2)).replace('{hw}',plural(Math.floor(hoursPerYear),STR.h_1,STR.h_234,STR.h_5)).replace('{yw}',STR.yr_1);
  const nextMilestone=MILESTONES.find(m=>m.years>cur);
  el.detailNextUnlock.textContent=nextMilestone?nextMilestone.title+' ('+nextMilestone.years+' '+yrsWord(nextMilestone.years)+')':STR.all_unlocked;
  let advice='';
  if(remainingYears===0){advice=STR.advice_goal.replace('{t}',tgt);}
  else if(!state.planLenny&&remainingYears>=10){advice=STR.advice_lenny;}
  else if(assets<DOLLARS_PER_YEAR){advice=STR.advice_under;}
  else{advice=STR.advice_route.replace('{method}',method.name).replace('{rate}',formatMoney(method.ratePerHour)).replace('{t}',tgt).replace('{h}',fmt(hoursNeeded,1));}
  el.strategyAdviceBox.textContent=advice;
}
function renderBars(methods){
  const max=Math.max.apply(null,methods.map(m=>m.ratePerHour).concat([1]));
  el.methodsBars.innerHTML=methods.map(function(m){
    const pct=Math.max(2,Math.round(100*m.ratePerHour/max));
    const flag=m.disputed?' <span class="jt-est">'+STR.disputed+'</span>':m.est?' <span class="jt-est">'+STR.est+'</span>':'';
    return '<div class="jt-bar-row"><b>'+escapeText(m.name)+'</b><span class="jt-bar-track"><span class="jt-bar-fill'+(m.id===state.activeMethodId?' active':'')+'" style="width:'+pct+'%"></span></span><span class="jt-bar-val">'+formatMoney(m.ratePerHour)+STR.per_hour+flag+'</span></div>';
  }).join('');
}
function renderMethods(){
  const methods=getDynamicMethods().filter(m=>state.methodFilter==='all'?true:m.tags.indexOf(state.methodFilter)!==-1);
  el.methodsTableBody.innerHTML=methods.map(function(m){
    const hrsPerYear=DOLLARS_PER_YEAR/m.ratePerHour;
    const hrsFor40=(SERVER_CAP_YEARS*DOLLARS_PER_YEAR)/m.ratePerHour;
    const isSelected=m.id===state.activeMethodId;
    const flag=m.disputed?'<span class="jt-flag disputed">'+STR.disputed+'</span>':m.est?'<span class="jt-flag est">'+STR.est+'</span>':'';
    return '<tr class="'+(isSelected?'selected-row':'')+'"><td><div style="font-weight:700;color:var(--ink);">'+escapeText(m.name)+'</div><div class="jt-src">'+escapeText(m.note)+'</div></td><td class="jt-rate">'+formatMoney(m.ratePerHour)+STR.per_hour+flag+'</td><td class="jt-hpy">'+fmt(hrsPerYear,2)+' '+plural(Math.floor(hrsPerYear),STR.h_1,STR.h_234,STR.h_5)+'</td><td>'+fmt(hrsFor40,1)+' '+plural(Math.floor(hrsFor40),STR.h_1,STR.h_234,STR.h_5)+'</td><td><div>'+escapeText(m.setup)+'</div><div class="'+m.riskClass+'" style="font-size:var(--fs-small);">'+STR.risk_label+escapeText(m.risk)+'</div></td><td style="text-align:right;"><button type="button" data-pick-method="'+m.id+'" class="btn '+(isSelected?'btn-primary':'btn-ghost')+'" style="min-height:32px;padding:4px 10px;font-size:var(--fs-small);">'+(isSelected?STR.active:STR.use_route)+'</button></td></tr>';
  }).join('');
  renderBars(methods);
}
function renderMilestones(){
  const cur=state.currentJailTime, tgt=state.targetAuthority;
  el.milestonesList.innerHTML=MILESTONES.map(function(m){
    const unlocked=cur>=m.years, isTarget=tgt===m.years;
    let tag='<span class="jt-tag">'+STR.locked+'</span>';
    if(unlocked)tag='<span class="jt-tag good">'+STR.unlocked+'</span>';
    else if(isTarget)tag='<span class="jt-tag warn">'+STR.target_tag+'</span>';
    return '<div class="jt-ms-item'+(isTarget?' is-target':'')+'"><div class="jt-ms-left"><div class="jt-ms-year'+(unlocked?' unlocked':'')+'">'+m.years+'<span>'+STR.yrs_unit+'</span></div><div style="min-width:0;"><div style="display:flex;flex-wrap:wrap;align-items:center;gap:8px;"><strong class="jt-ms-title">'+escapeText(m.title)+'</strong>'+tag+'</div><p class="jt-ms-detail">'+escapeText(m.detail)+'</p></div></div>'+(!unlocked?'<button type="button" data-set-milestone="'+m.years+'" class="btn btn-ghost" style="min-height:32px;padding:4px 10px;font-size:var(--fs-small);flex:none;">'+STR.set_target+'</button>':'')+'</div>';
  }).join('');
}
function renderTracker(){
  el.trackerBadge.textContent=state.goals.length;
  const method=getActiveMethod();
  if(!state.goals.length){el.goalsEmpty.classList.remove('jt-hidden');el.goalsList.classList.add('jt-hidden');el.goalsList.innerHTML='';}
  else{
    el.goalsEmpty.classList.add('jt-hidden');el.goalsList.classList.remove('jt-hidden');
    el.goalsList.innerHTML=state.goals.map(function(goal,idx){
      const remaining=Math.max(0,goal.target-state.currentJailTime);
      const pct=goal.target>0?Math.min(100,Math.round(100*state.currentJailTime/goal.target)):0;
      const cashNeeded=remaining*DOLLARS_PER_YEAR;
      const hours=method.ratePerHour>0?cashNeeded/method.ratePerHour:0;
      const remainingWord=remaining===0?STR.goal_reached:remaining+' '+yrsWord(remaining);
      return '<div class="jt-goal"><div class="jt-sec-head"><div style="min-width:0;"><b style="font-size:var(--fs-card);color:var(--ink);">'+escapeText(goal.label)+'</b><div class="jt-goal-meta">'+STR.goal_target+': '+goal.target+' '+yrsWord(goal.target)+' \u00b7 '+STR.goal_current+': '+state.currentJailTime+' '+yrsWord(state.currentJailTime)+' \u00b7 '+STR.goal_remain+': '+remainingWord+'</div></div><span style="flex:none;font-size:var(--fs-h4);font-weight:700;color:var(--teal-deep);">'+pct+'%</span></div><div class="wlh-progress" style="margin:8px 0 6px;"><span style="width:'+pct+'%"></span></div><div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:center;"><span class="jt-field-hint">'+STR.goal_hours+': '+fmt(hours,1)+' '+plural(Math.floor(hours),STR.h_1,STR.h_234,STR.h_5)+' ('+method.name+')</span><span style="display:flex;gap:8px;"><button type="button" data-focus-goal="'+idx+'" class="btn btn-ghost" style="min-height:32px;padding:4px 10px;font-size:var(--fs-small);">'+STR.goal_load+'</button><button type="button" data-del-goal="'+idx+'" class="btn btn-ghost" style="min-height:32px;padding:4px 10px;font-size:var(--fs-small);">'+STR.goal_delete+'</button></span></div></div>';
    }).join('');
  }
  if(!state.logs.length){el.logsEmpty.classList.remove('jt-hidden');el.logsList.classList.add('jt-hidden');el.logsList.innerHTML='';el.clearLogsBtn.classList.add('jt-hidden');}
  else{
    el.logsEmpty.classList.add('jt-hidden');el.logsList.classList.remove('jt-hidden');el.clearLogsBtn.classList.remove('jt-hidden');
    el.logsList.innerHTML=state.logs.map(function(log,idx){
      const assetsText=log.assets?formatMoney(log.assets):'\u2014';
      return '<div class="jt-log"><div class="jt-log-left"><span class="jt-log-years">+'+log.years+' '+yrsWord(log.years)+'</span><span style="color:var(--body);font-size:var(--fs-card);">'+assetsText+'</span>'+(log.note?'<span class="jt-log-note">\u201c'+escapeText(log.note)+'\u201d</span>':'')+'</div><div style="display:flex;align-items:center;gap:10px;"><span style="color:var(--body);font-size:var(--fs-small);white-space:nowrap;">'+log.time+'</span><button type="button" data-del-log="'+idx+'" class="jt-link-btn danger">'+STR.goal_delete+'</button></div></div>';
    }).join('');
  }
}
function renderAll(){populateMethodSelect();renderCalculator();renderMethods();renderMilestones();renderTracker();}
function switchTab(tabName){state.activeTab=tabName;document.querySelectorAll('.jt-tab').forEach(function(btn){const active=btn.getAttribute('data-tab')===tabName;btn.classList.toggle('active',active);btn.setAttribute('aria-selected',active?'true':'false');});['calculator','methods','unlocks','tracker'].forEach(function(name){$('panel-'+name).classList.toggle('jt-hidden',name!==tabName);});if(tabName==='methods')renderMethods();if(tabName==='tracker')renderTracker();}
document.querySelectorAll('.jt-tab').forEach(function(btn){btn.addEventListener('click',function(){switchTab(btn.getAttribute('data-tab'));});});
document.querySelectorAll('.target-chip').forEach(function(btn){btn.addEventListener('click',function(){const v=parseInt(btn.getAttribute('data-target'),10);if(!Number.isNaN(v)){state.targetAuthority=v;el.targetAuthorityInput.value=v;renderCalculator();renderMilestones();renderTracker();}});});
document.querySelectorAll('.asset-chip').forEach(function(btn){btn.addEventListener('click',function(){const v=parseInt(btn.getAttribute('data-assets'),10);if(!Number.isNaN(v)){state.serverAssets=v;el.serverAssetsInput.value=v;renderCalculator();}});});
document.querySelectorAll('.method-filter-btn').forEach(function(btn){btn.addEventListener('click',function(){state.methodFilter=btn.getAttribute('data-filter');document.querySelectorAll('.method-filter-btn').forEach(function(b){b.classList.toggle('active',b===btn);});renderMethods();});});
document.querySelectorAll('.bench-btn').forEach(function(btn){btn.addEventListener('click',function(){state.benchCount=parseInt(btn.getAttribute('data-benches'),10)||1;document.querySelectorAll('.bench-btn').forEach(function(b){b.classList.toggle('active',b===btn);});renderMethods();populateMethodSelect();renderCalculator();});});
document.querySelectorAll('.grow-btn').forEach(function(btn){btn.addEventListener('click',function(){state.growMode=btn.getAttribute('data-grow');document.querySelectorAll('.grow-btn').forEach(function(b){b.classList.toggle('active',b===btn);});renderMethods();populateMethodSelect();renderCalculator();});});
el.currentJailInput.addEventListener('input',function(){state.currentJailTime=Math.max(0,parseInt(el.currentJailInput.value,10)||0);renderCalculator();renderMilestones();renderTracker();});
el.targetAuthorityInput.addEventListener('input',function(){state.targetAuthority=Math.max(1,parseInt(el.targetAuthorityInput.value,10)||1);renderCalculator();renderMilestones();renderTracker();});
el.serverAssetsInput.addEventListener('input',function(){state.serverAssets=Math.max(0,parseInt(el.serverAssetsInput.value,10)||0);renderCalculator();});
el.planLennyToggle.addEventListener('change',function(){state.planLenny=el.planLennyToggle.checked;el.lennyStatusText.textContent=state.planLenny?STR.lenny_on:STR.lenny_off;renderCalculator();});
el.dailyHoursRange.addEventListener('input',function(){state.dailyHours=parseFloat(el.dailyHoursRange.value)||3;renderCalculator();});
el.activeMethodSelect.addEventListener('change',function(){state.activeMethodId=el.activeMethodSelect.value;renderCalculator();renderMethods();});
el.resetInputsBtn.addEventListener('click',function(){state.currentJailTime=15;state.targetAuthority=60;state.serverAssets=2500000;state.planLenny=false;state.dailyHours=3;state.activeMethodId='store_runs';el.currentJailInput.value=15;el.targetAuthorityInput.value=60;el.serverAssetsInput.value=2500000;el.planLennyToggle.checked=false;el.dailyHoursRange.value=3;el.activeMethodSelect.value='store_runs';el.lennyStatusText.textContent=STR.lenny_off;renderCalculator();renderMethods();renderMilestones();renderTracker();showToast(STR.reset_done);});
document.addEventListener('click',function(e){
  const pick=e.target.closest('[data-pick-method]');
  if(pick){state.activeMethodId=pick.getAttribute('data-pick-method');el.activeMethodSelect.value=state.activeMethodId;renderCalculator();renderMethods();return;}
  const set=e.target.closest('[data-set-milestone]');
  if(set){state.targetAuthority=parseInt(set.getAttribute('data-set-milestone'),10);el.targetAuthorityInput.value=state.targetAuthority;renderCalculator();renderMilestones();renderTracker();return;}
  const delG=e.target.closest('[data-del-goal]');
  if(delG){state.goals.splice(parseInt(delG.getAttribute('data-del-goal'),10),1);saveTracker();renderTracker();showToast(STR.deleted);return;}
  const loadG=e.target.closest('[data-focus-goal]');
  if(loadG){const g=state.goals[parseInt(loadG.getAttribute('data-focus-goal'),10)];if(g){state.targetAuthority=g.target;el.targetAuthorityInput.value=g.target;switchTab('calculator');renderCalculator();renderMilestones();showToast(STR.loaded);}return;}
  const delL=e.target.closest('[data-del-log]');
  if(delL){state.logs.splice(parseInt(delL.getAttribute('data-del-log'),10),1);saveTracker();renderTracker();showToast(STR.log_deleted);return;}
});
el.addGoalFromCalcBtn.addEventListener('click',function(){
  if(state.goals.length>=20){showToast(STR.empty_goals);return;}
  const target=state.targetAuthority;
  const milestone=MILESTONES.find(m=>m.years===target);
  const label=milestone?milestone.title:target+' '+yrsWord(target)+' '+STR.yrs_unit;
  state.goals.push({label:label,target:target});
  saveTracker();renderTracker();showToast(STR.saved);
});
el.clearLogsBtn.addEventListener('click',function(){state.logs=[];saveTracker();renderTracker();showToast(STR.logs_cleared);});
el.wipeLogForm.addEventListener('submit',function(e){
  e.preventDefault();
  const years=parseInt(el.logYearsInput.value,10);
  if(!years||years<1||years>50){showToast(STR.log_years_err);return;}
  const assets=parseInt(el.logAssetsInput.value,10);
  const note=el.logNoteInput.value.trim();
  const time=new Date().toLocaleDateString(STR.locale,{month:'short',day:'numeric'});
  state.logs.unshift({years:years,assets:Number.isNaN(assets)?0:assets,note:note,time:time});
  state.logs=state.logs.slice(0,30);
  saveTracker();renderTracker();showToast(STR.log_saved);
  el.logYearsInput.value=10;el.logAssetsInput.value='';el.logNoteInput.value='';
});
loadTracker();
el.lennyStatusText.textContent=STR.lenny_off;
renderAll();
})();
"""


def script_for(lang):
    return JT_JS.replace("__STR__", json.dumps(JT[lang]["js"], ensure_ascii=False))


def jail_page(lang):
    c = JT[lang]
    home = "Home" if lang == "en" else "\u0413\u043b\u0430\u0432\u043d\u0430\u044f"
    home_path = "/" if lang == "en" else "/ru/"
    hub_path = "/rob-run/" if lang == "en" else "/ru/rob-run/"
    canon = c["canonical"]
    alt = {"en": JT["en"]["canonical"], "ru": JT["ru"]["canonical"]}
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": a}}
                             for q, a in c["faq"]]}
    jl = [breadcrumb_jsonld(lang, [(home, home_path), ("ROB RUN", hub_path),
                                   (c["card_title"], canon)]),
          {"@context": "https://schema.org", "@type": "WebApplication",
           "name": c["h1"], "url": BASE + canon, "inLanguage": lang,
           "description": c["webapp_desc"], "applicationCategory": "GameApplication",
           "operatingSystem": "Any modern browser",
           "offers": {"@type": "Offer", "price": "0"}},
          faq_ld]
    body = ('<main id="main" class="wrap">%s%s</main>'
            % (crumbs_html(lang, [("ROB RUN", hub_path), (c["card_title"], None)]),
               body_html(lang)))
    return page(lang, c["title"], c["desc"], canon, alt, body, jsonld=jl,
                games=("rob-run",), tail="<script>%s</script>\n" % script_for(lang))


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", rel)


def main():
    write("rob-run/jail-time-authority-calculator/index.html", jail_page("en"))
    write("ru/rob-run/jail-time-authority-calculator/index.html", jail_page("ru"))
    print("jail time calculator done")


if __name__ == "__main__":
    main()
