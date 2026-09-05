# hall of fame

A page for viewers who changed the outcome of a [noisy coder](https://twitch.tv/noisycoder)
stream from the other side of the screen.

Live at **https://noisy.github.io/hall-of-fame/**

## Adding someone

One dict in `build.py`, then re-run it:

```sh
python3 build.py
```

Two rules that are not style preferences:

- **Names are written the way their owner writes them.** Chat logs only keep
  lowercase logins, so the display casing comes from the person's own channel
  page. Getting somebody's name wrong on a page built to thank them defeats
  the page.
- **Citations are what the person did in this channel's chat, in public.**
  Nothing researched from anywhere else, and nobody is listed before being
  thanked on stream.

One flat wall, newest first - deliberately not grouped by stream, because most
streams do not produce an entry and a page of empty sections would say the
wrong thing.

Badge art goes in `badges/`; an entry without one gets drawn placeholder
geometry and a "badge in the works" tag, so an unfinished badge is obvious
rather than passing for done.
