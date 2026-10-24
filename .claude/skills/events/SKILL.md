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
  "date": "2026-11-26",
  "time": "18:00",
  "venue": "Indie's, Luxembourg",
  "link": "https://www.meetup.com/goindie/",
  "status": "upcoming"
}
```

| Field | Required | Notes |
| --- | --- | --- |
| `title` | yes | The session's own name, not the series. |
| `series` | yes | Shown as a pill. Keep it short: it must not wrap. |
| `date` | yes | `YYYY-MM-DD`. |
| `time` | no | `HH:MM`, 24-hour. Omit if unknown rather than guessing. |
| `venue` | yes | Where it happens, as a person would say it. |
| `link` | no | Where to RSVP. Omit if there is nowhere to send people yet. |
| `status` | yes | `upcoming` or `past`. |

## What each status does

- **`upcoming`** — the soonest one fills the home page panel. All of them appear under "Upcoming" on `/events/`.
- **`past`** — appears under "Past" on `/events/`, newest first. Never on the home page.

With no upcoming events, the home panel reads "Nothing scheduled right now."

## The three operations

**Add an event.** Append an object to `events.json` with `status: "upcoming"`. Ask for any field you were not given; do not invent a time or a venue.

**Complete an event.** Change its `status` to `"past"`. Leave the date alone — it is a record of when it happened. The RSVP link becomes "See it on Meetup" automatically.

**Remove an event.** Delete the object. Only for something that was cancelled or listed in error; an event that happened should be completed, not removed.

## After any change

```bash
python3 events/build.py
```

It prints how many upcoming and past events it rendered. Check that against what you expect.

Then look at both pages before saying it is done — a local server rooted at the repo, `/` and `/events/`.

## Things that will bite

- This is a public repo. Everything in `events.json` is published the moment it is pushed, including a venue address.
- Do not list an event as `upcoming` with an RSVP link that does not yet show it. Either publish it on Meetup first or omit the link.
- The series pill does not wrap by design. A long series name will be clipped rather than flow onto a second line.
