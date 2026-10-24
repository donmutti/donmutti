#!/usr/bin/env python3
"""Render events.json into the home page panel and the events archive page.

Both outputs are written between marker comments, so the surrounding
hand-written HTML stays untouched.
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


def load():
    events = json.loads(EVENTS.read_text())
    for e in events:
        e["_date"] = datetime.date.fromisoformat(e["date"])
    return events


def when(event):
    """26 November 2026, 18:00 — the time is optional."""
    stamp = event["_date"].strftime("%-d %B %Y")
    return f"{stamp}, {event['time']}" if event.get("time") else stamp


def card(event, indent):
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
        label = "Details and RSVP on Meetup" if event["status"] == "upcoming" else "See it on Meetup"
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
    upcoming = sorted([e for e in events if e["status"] == "upcoming"], key=lambda e: e["_date"])
    past = sorted([e for e in events if e["status"] == "past"], key=lambda e: e["_date"], reverse=True)

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
        sections.extend(card(e, 6) for e in past)
    if not sections:
        sections.append('      <p class="nm-empty">No events yet.</p>')
    replace_block(ARCHIVE, "all-events", "\n".join(sections))

    print(f"rendered {len(upcoming)} upcoming, {len(past)} past")


if __name__ == "__main__":
    main()
