#!/usr/bin/env python3
"""Render events.json into the home page panel and the events archive page.

Both outputs are written between marker comments, so the surrounding
hand-written HTML stays untouched.

Whether an event is upcoming or past is derived from its dates, never stored:
an event is past once its last day is behind the day this runs. That means the
pages are only as current as the last build, so a scheduled rebuild keeps them
honest.
"""
import datetime
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).parent.parent
EVENTS = ROOT / "events.json"
HOME = ROOT / "index.html"
ARCHIVE = ROOT / "events" / "index.html"

CALENDAR_ICON = (
    '<svg class="nm-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/>'
    '<path d="M3 10h18"/></svg>'
)
ARROW_ICON = (
    '<svg class="nm-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>'
)
PIN_ICON = (
    '<svg class="nm-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 '
    '14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></svg>'
)


def parse(stamp):
    """A date or a local timestamp with offset. Returns (date, time-or-None).

    "2026-11-26"             -> an all-day event, no time to show
    "2026-11-26T18:00:00+01:00" -> 18:00 at the venue, as written
    """
    if "T" not in stamp:
        return datetime.date.fromisoformat(stamp), None
    moment = datetime.datetime.fromisoformat(stamp)
    return moment.date(), moment.strftime("%H:%M")


def load():
    events = json.loads(EVENTS.read_text())
    for e in events:
        e["_start"], e["_start_time"] = parse(e["start"])
        if e.get("end"):
            e["_end"], e["_end_time"] = parse(e["end"])
        else:
            e["_end"], e["_end_time"] = e["_start"], None
        if e["_end"] < e["_start"]:
            raise SystemExit(f"{e['title']}: end is before start")
    return events


def when(event):
    """The dates, then the times, in as few words as carry the meaning.

    26 November 2026                 a day
    26 November 2026, 18:00          an evening
    26 November 2026, 18:00-21:00    an evening that ends
    26-27 November 2026              two days in one month
    30 November - 1 December 2026    two days across months
    31 December 2026 - 1 January 2027  two days across years
    """
    start, end = event["_start"], event["_end"]
    if start == end:
        dates = start.strftime("%-d %B %Y")
    elif (start.year, start.month) == (end.year, end.month):
        dates = f"{start.day}-{end.strftime('%-d %B %Y')}"
    elif start.year == end.year:
        dates = f"{start.strftime('%-d %B')} - {end.strftime('%-d %B %Y')}"
    else:
        dates = f"{start.strftime('%-d %B %Y')} - {end.strftime('%-d %B %Y')}"

    # A time range only reads as one when both ends are the same day.
    opens, closes = event["_start_time"], event["_end_time"]
    if opens and closes and start == end:
        return f"{dates}, {opens}-{closes}"
    if opens:
        return f"{dates}, {opens}"
    return dates


def card(event, indent, past=False):
    """One event card. Identical markup on both pages."""
    pad = " " * indent
    esc = lambda key: html.escape(event[key], quote=False)
    lines = [
        f'{pad}<div class="next-meetup">',
        f'{pad}  <div class="nm-head">',
        f'{pad}    <span class="nm-title">{esc("title")}</span>',
        f'{pad}    <span class="nm-kind">{esc("series")}</span>',
        f'{pad}  </div>',
        f'{pad}  <div class="nm-when">{CALENDAR_ICON}{html.escape(when(event), quote=False)}</div>',
        f'{pad}  <div class="nm-where">{PIN_ICON}{esc("venue")}</div>',
    ]
    if event.get("link"):
        label = "See it on Meetup" if past else "Details and RSVP on Meetup"
        lines.append(f'{pad}  <a class="nm-link" href="{html.escape(event["link"])}">{label}{ARROW_ICON}</a>')
    lines.append(f"{pad}</div>")
    return "\n".join(lines)


def replace_block(path, name, body):
    """Swap whatever sits between <!-- name:start --> and <!-- name:end -->."""
    text = path.read_text()
    pattern = re.compile(
        rf"(<!-- {name}:start -->\n).*?(\s*<!-- {name}:end -->)", re.S
    )
    if not pattern.search(text):
        raise SystemExit(f"missing {name} markers in {path}")
    path.write_text(pattern.sub(lambda m: m.group(1) + body + "\n" + m.group(2).lstrip("\n"), text))


def main():
    events = load()
    today = datetime.date.today()

    # Past once the last day is behind us: an event still shows as upcoming
    # all through the day it happens, which is when people look it up.
    upcoming = sorted([e for e in events if e["_end"] >= today], key=lambda e: e["_start"])
    past = sorted([e for e in events if e["_end"] < today], key=lambda e: e["_start"], reverse=True)

    # Home: the next event only, or nothing at all.
    if upcoming:
        home_body = card(upcoming[0], 6)
    else:
        home_body = '      <p class="nm-empty">Nothing scheduled right now.</p>'
    replace_block(HOME, "next-event", home_body)

    # Archive: everything, upcoming first.
    sections = []
    if upcoming:
        sections.append("      <h2>Upcoming</h2>")
        sections.extend(card(e, 6) for e in upcoming)
    if past:
        sections.append("      <h2>Past</h2>")
        sections.extend(card(e, 6, past=True) for e in past)
    if not sections:
        sections.append('      <p class="nm-empty">No events yet.</p>')
    replace_block(ARCHIVE, "all-events", "\n".join(sections))

    print(f"rendered {len(upcoming)} upcoming, {len(past)} past")


if __name__ == "__main__":
    main()
