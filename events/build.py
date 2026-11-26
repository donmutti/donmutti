#!/usr/bin/env python3
"""Render events.json into the English and Russian home and events pages.

All four outputs are written between marker comments, so the surrounding
hand-written HTML stays untouched. Titles, series and venues are copied as
written in events.json. Russian pages get Russian month names and the
surrounding labels; the English card text stays as it has been.

The same pass writes a JSON-LD block on each page (Person and WebSite on
the home pages, Event nodes from events.json on the home and events pages)
so a later rebuild keeps the structured data in sync with the cards.

Whether an event is upcoming or past is derived from its dates, never stored:
an event is past once its last day is behind the day this runs. That means the
pages are only as current as the last build, so a scheduled rebuild keeps them
honest.

Each event in events.json has these fields: title, series, start (ISO time
with offset), venue, link (optional, the Meetup page), and backdrop
(optional, an image URL). The backdrop is linked by its URL, never copied
into this repo, and is drawn behind that event's card under a dark tint;
a card without one keeps the plain background.
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
HOME_RU = ROOT / "ru" / "index.html"
ARCHIVE_RU = ROOT / "ru" / "events" / "index.html"

# Genitive month names, so the date does not depend on the machine locale.
# The English dates stay on strftime, which is how they have always been formed.
RU_MONTHS = (
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
)

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


def when_ru(event):
    """The same date shapes as when(), with Russian month names."""
    start, end = event["_start"], event["_end"]

    def day_month(day, with_year):
        month = RU_MONTHS[day.month - 1]
        if with_year:
            return f"{day.day} {month} {day.year}"
        return f"{day.day} {month}"

    if start == end:
        dates = day_month(start, True)
    elif (start.year, start.month) == (end.year, end.month):
        dates = f"{start.day}-{end.day} {RU_MONTHS[end.month - 1]} {end.year}"
    elif start.year == end.year:
        dates = f"{day_month(start, False)} - {day_month(end, True)}"
    else:
        dates = f"{day_month(start, True)} - {day_month(end, True)}"

    opens, closes = event["_start_time"], event["_end_time"]
    if opens and closes and start == end:
        return f"{dates}, {opens}-{closes}"
    if opens:
        return f"{dates}, {opens}"
    return dates


def backdrop_open(event, pad):
    """The card's opening tag, with the event's backdrop URL when it has one."""
    if not event.get("backdrop"):
        return f'{pad}<div class="next-meetup">'
    url = event["backdrop"].replace('"', "%22")
    return f'{pad}<div class="next-meetup has-backdrop" style="--nm-backdrop: url(&quot;{html.escape(url)}&quot;)">'


def card(event, indent, past=False, when_fn=when, rsvp="Details and RSVP on Meetup", seen="See it on Meetup"):
    """One event card. The same markup on every page."""
    pad = " " * indent
    esc = lambda key: html.escape(event[key], quote=False)
    lines = [
        backdrop_open(event, pad),
        f'{pad}  <div class="nm-head">',
        f'{pad}    <span class="nm-title">{esc("title")}</span>',
        f'{pad}    <span class="nm-kind">{esc("series")}</span>',
        f'{pad}  </div>',
        f'{pad}  <div class="nm-when">{CALENDAR_ICON}{html.escape(when_fn(event), quote=False)}</div>',
        f'{pad}  <div class="nm-where">{PIN_ICON}{esc("venue")}</div>',
    ]
    if event.get("link"):
        label = seen if past else rsvp
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


def fill(home, archive, upcoming, past, when_fn, upcoming_heading, past_heading, rsvp, seen, empty_next, empty_all):
    """Write one language. home is the next event; archive is the full list."""
    if upcoming:
        home_body = card(upcoming[0], 6, when_fn=when_fn, rsvp=rsvp, seen=seen)
    else:
        home_body = f'      <p class="nm-empty">{empty_next}</p>'
    replace_block(home, "next-event", home_body)

    sections = []
    if upcoming:
        sections.append(f"      <h2>{upcoming_heading}</h2>")
        sections.extend(card(e, 6, when_fn=when_fn, rsvp=rsvp, seen=seen) for e in upcoming)
    if past:
        sections.append(f"      <h2>{past_heading}</h2>")
        sections.extend(card(e, 6, past=True, when_fn=when_fn, rsvp=rsvp, seen=seen) for e in past)
    if not sections:
        sections.append(f'      <p class="nm-empty">{empty_all}</p>')
    replace_block(archive, "all-events", "\n".join(sections))


def main():
    events = load()
    today = datetime.date.today()

    # Past once the last day is behind us: an event still shows as upcoming
    # all through the day it happens, which is when people look it up.
    upcoming = sorted([e for e in events if e["_end"] >= today], key=lambda e: e["_start"])
    past = sorted([e for e in events if e["_end"] < today], key=lambda e: e["_start"], reverse=True)

    fill(
        HOME,
        ARCHIVE,
        upcoming,
        past,
        when,
        "Upcoming",
        "Past",
        "Details and RSVP on Meetup",
        "See it on Meetup",
        "Nothing scheduled right now.",
        "No events yet.",
    )
    fill(
        HOME_RU,
        ARCHIVE_RU,
        upcoming,
        past,
        when_ru,
        "Ближайшие",
        "Прошедшие",
        "Подробности и запись на Meetup",
        "Посмотреть на Meetup",
        "Сейчас ничего не запланировано.",
        "Пока нет событий.",
    )

    write_json_ld(upcoming, past)

    print(f"rendered {len(upcoming)} upcoming, {len(past)} past, en and ru")


PERSON_ID = "https://donmutti.com/#person"
WEBSITE_ID = "https://donmutti.com/#website"
SITE = "https://donmutti.com"

# Public profile links already printed on the home pages.
PERSON_SAME_AS = (
    "https://github.com/donmutti",
    "https://linkedin.com/in/donmutti",
    "https://x.com/donmutti0",
)

# The Go Indie Club series is the meetup already linked from the Building section.
GO_INDIE_CLUB_URL = "https://www.meetup.com/goindie/"


def slugify(text):
    """A stable fragment id from a title, for Event and EventSeries @id."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def person_node(lang, full=True):
    """The site owner. Full node on home pages; a short pointer on events pages."""
    if lang == "ru":
        node = {
            "@type": "Person",
            "@id": PERSON_ID,
            "name": "Дмитрий Петухов",
            "alternateName": ["Dmitrii Petukhov", "donmutti"],
            "url": SITE,
            "inLanguage": "ru",
        }
        if full:
            node.update({
                "image": f"{SITE}/assets/userpic.webp",
                "jobTitle": "Инженер-программист и организатор сообществ",
                "description": (
                    "Инженер-программист и организатор сообществ в Люксембурге. "
                    "Создаю продукты с ИИ для работы с историями. "
                    "Развиваю сообщество и платформу для тех, кто хочет начать своё дело."
                ),
                "sameAs": list(PERSON_SAME_AS),
                "affiliation": {
                    "@type": "Organization",
                    "name": "IncaTech",
                    "description": (
                        "Технологическая компания, создающая компаньонов "
                        "на всю жизнь для историй, творчества и работы."
                    ),
                    "sameAs": "https://www.linkedin.com/company/inca-tech",
                },
            })
        return node

    node = {
        "@type": "Person",
        "@id": PERSON_ID,
        "name": "Dmitrii Petukhov",
        "alternateName": ["donmutti", "Дмитрий Петухов"],
        "url": SITE,
        "inLanguage": "en",
    }
    if full:
        node.update({
            "image": f"{SITE}/assets/userpic.webp",
            "jobTitle": "Software engineer and community builder",
            "description": (
                "Software engineer and community builder in Luxembourg. "
                "Creating AI-native products around storytelling, and "
                "infrastructure for moving from employment to ownership."
            ),
            "sameAs": list(PERSON_SAME_AS),
            "affiliation": {
                "@type": "Organization",
                "name": "IncaTech",
                "description": (
                    "A technology company building lifelong companions "
                    "for storytelling, creativity and work."
                ),
                "sameAs": "https://www.linkedin.com/company/inca-tech",
            },
        })
    return node


def website_node(lang):
    """donmutti.com, the personal site of Dmitrii Petukhov."""
    return {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "name": "donmutti.com",
        "url": SITE + "/",
        "author": {"@id": PERSON_ID},
        "publisher": {"@id": PERSON_ID},
        "inLanguage": lang,
    }


def place_from_venue(venue):
    """A Place from the venue string. No street address is invented.

    "Indie's, Luxembourg" -> name Indie's, locality Luxembourg, country LU.
    A venue that does not name Luxembourg is left as a bare Place name.
    """
    name = venue
    locality = None
    suffix = ", Luxembourg"
    if venue.endswith(suffix):
        name = venue[: -len(suffix)].rstrip()
        locality = "Luxembourg"
    place = {"@type": "Place", "name": name}
    address = {"@type": "PostalAddress"}
    if locality:
        address["addressLocality"] = locality
        address["addressCountry"] = "LU"
    if len(address) > 1:
        place["address"] = address
    return place


def event_node(event, past=False, lang="en"):
    """One Event, using only fields present in events.json."""
    node = {
        "@type": "Event",
        "@id": f"{SITE}/#event-{slugify(event['title'])}",
        "name": event["title"],
        "startDate": event["start"],
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "eventStatus": (
            "https://schema.org/EventCompleted"
            if past
            else "https://schema.org/EventScheduled"
        ),
        "location": place_from_venue(event["venue"]),
        "organizer": {"@id": PERSON_ID},
        "inLanguage": lang,
    }
    if event.get("end"):
        node["endDate"] = event["end"]
    if event.get("link"):
        node["url"] = event["link"]
    series = event.get("series")
    if series:
        super_event = {
            "@type": "EventSeries",
            "@id": f"{SITE}/#series-{slugify(series)}",
            "name": series,
        }
        if series == "Go Indie Club":
            super_event["url"] = GO_INDIE_CLUB_URL
        node["superEvent"] = super_event
    return node


def json_ld_block(graph):
    """One JSON-LD script tag. < is escaped so the block is safe in HTML."""
    payload = {"@context": "https://schema.org", "@graph": graph}
    dumped = json.dumps(payload, ensure_ascii=False, indent=2)
    dumped = dumped.replace("<", "\\u003c")
    return "  <script type=\"application/ld+json\">\n" + dumped + "\n  </script>\n"


def write_json_ld(upcoming, past):
    """Write the json-ld marker block on all four pages, then parse it back."""
    next_en = [event_node(upcoming[0], lang="en")] if upcoming else []
    next_ru = [event_node(upcoming[0], lang="ru")] if upcoming else []
    archive_en = [event_node(e, lang="en") for e in upcoming] + [
        event_node(e, past=True, lang="en") for e in past
    ]
    archive_ru = [event_node(e, lang="ru") for e in upcoming] + [
        event_node(e, past=True, lang="ru") for e in past
    ]

    pages = (
        (HOME, [person_node("en"), website_node("en"), *next_en]),
        (HOME_RU, [person_node("ru"), website_node("ru"), *next_ru]),
        (ARCHIVE, [person_node("en", full=False), *archive_en]),
        (ARCHIVE_RU, [person_node("ru", full=False), *archive_ru]),
    )
    for path, graph in pages:
        replace_block(path, "json-ld", json_ld_block(graph))
        text = path.read_text()
        match = re.search(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
            text,
            re.S,
        )
        if not match:
            raise SystemExit(f"json-ld script missing after write in {path}")
        json.loads(match.group(1))


if __name__ == "__main__":
    main()
