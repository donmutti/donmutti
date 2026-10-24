---
name: events
description: Add, complete or remove an event on donmutti.com. Use when Dmitrii mentions a meetup, talk or session to list on the site, when one has happened, or when a listing needs changing.
---

# Events on donmutti.com

`events.json` at the repo root is the only place event data lives. The home page panel and `/events/` are both generated from it by `events/build.py`, between marker comments. Never hand-edit the generated HTML: the next build overwrites it.

## The shape of an event

```json
{
  "title": "The Leap: From Employment to Ownership",
  "series": "Go Indie",
  "start": "2026-11-26T18:00:00+01:00",
  "venue": "Indie's, Luxembourg",
  "link": "https://www.meetup.com/goindie/"
}
```

| Field | Required | Notes |
| --- | --- | --- |
| `title` | yes | The session's own name, not the series. |
| `series` | yes | Shown as a pill. Keep it short: it must not wrap. |
| `start` | yes | When it begins. See "Writing a time" below. |
| `end` | no | When it ends. Omit for a single day with no stated finish. |
| `venue` | yes | Where it happens, as a person would say it. |
| `link` | no | Where to RSVP. Omit if there is nowhere to send people yet. |

There is no status field. Whether an event is upcoming or past is worked out from its dates every time the site is built.

## Writing a time

Write the local wall-clock time at the venue, with its UTC offset, exactly as a person there would say it:

- `"2026-11-26T18:00:00+01:00"` — 18:00 in Luxembourg in winter.
- `"2026-07-15T18:00:00+02:00"` — 18:00 in Luxembourg in summer. The offset changes, the 18:00 does not.

Luxembourg is `+01:00` from late October to late March, `+02:00` the rest of the year. Getting the offset wrong shifts nothing on the page, which prints the wall-clock time as written, but it makes the ordering wrong against events elsewhere, so set it correctly.

Use a bare date, `"2026-11-26"`, when the time genuinely is not known yet. The card then shows the day alone. Never invent a time to fill the field.

## What gets shown

The soonest upcoming event fills the home page panel; all of them appear under "Upcoming" on `/events/`, soonest first. Past events appear under "Past", newest first, and never on the home page. With nothing upcoming, the home panel reads "Nothing scheduled right now."

Dates are printed as briefly as the meaning allows:

| Data | Shows as |
| --- | --- |
| `start` only, bare date | 26 November 2026 |
| `start` with a time | 26 November 2026, 18:00 |
| `end` the same day, with a time | 26 November 2026, 18:00-21:00 |
| `end` a later day, same month | 26-27 November 2026 |
| `end` a later day, another month | 30 November - 1 December 2026 |

A multi-day event shows its start time only. "26-27 November, 09:00-17:00" would claim both days end at 17:00, which the data does not say.

## The three operations

**Add an event.** Append an object to `events.json`. Ask for any field you were not given; do not invent a time or a venue.

**Complete an event.** Nothing to do. It moves to "Past" on its own once its last day is behind us, and the RSVP link becomes "See it on Meetup". Rebuild to see it move.

**Remove an event.** Delete the object. Only for something cancelled or listed in error; an event that happened stays, as a record.

## After any change

```bash
python3 events/build.py
```

It prints how many upcoming and past events it rendered. Check that against what you expect.

Then look at both pages before saying it is done — a local server rooted at the repo, `/` and `/events/`.

## Things that will bite

- This is a public repo. Everything in `events.json` is published the moment it is pushed, including a venue address.
- The pages are static, so the upcoming/past split is only as fresh as the last render. A GitHub Action re-renders every morning and commits if anything moved, which is what retires a finished event. Run it by hand from the Actions tab ("Re-render events") if you need it sooner.
- Do not list an event with an RSVP link that does not yet show it. Either publish it on Meetup first or omit the link.
- The series pill does not wrap by design. A long series name will be clipped rather than flow onto a second line.
- An `end` before its `start` stops the build rather than rendering nonsense.
