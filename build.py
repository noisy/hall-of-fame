"""Build the noisy coder hall of fame.

A page for viewers who changed the outcome of a stream from the other side of
the screen. One flat wall of badges, newest first - deliberately not grouped by
stream, because most streams do not produce one and a page full of empty
sections would say the wrong thing.

Everything is in ENTRIES. Adding someone is one dict and a re-run.

Two rules that are not style preferences:

  Names are written the way their owner writes them - SwissTourist, not
  swisstourist. The chat logs only keep lowercase logins, so the display
  casing comes from the person's own channel page. Getting somebody's name
  wrong on a page built to thank them defeats the page.

  Citations are what the person did in this channel's chat, in public.
  Nothing researched from anywhere else, and nobody appears until Krzysztof
  has named them on air.

    python3 build.py
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# kind -> (label, glyph, colour); the glyph is monospace, like everything else
# this channel puts on screen
KINDS = {
    "pointer": ("pointed the way", "->", "#3fd8ff"),
    "bug": ("found the crack", "!!", "#ff5f6b"),
    "words": ("gave it words", '""', "#ffb454"),
    "arrival": ("brought the room", "<>", "#b98cff"),
}

ENTRIES = [
    dict(name="SwissTourist", kind="pointer", stream="day 6", date="2026-09-05",
         title="the codex whisperer",
         citation="Runs Codex as Claude's supervisor and has since March, so he "
                  "knew the flags before I did. Verified the usage-limit "
                  "finding, and stopped me running a command live that would "
                  "have printed my email on stream.",
         badge=None),
    dict(name="xFuroo", kind="arrival", stream="day 1", date="2026-08-22",
         title="day one",
         citation="Turned up on the first stream and stayed, back when nobody "
                  "knew whether this channel would last a week.",
         badge="badges/xfuroo-day-one.png"),
]


def badge_art(entry, size=210):
    """Real art when it exists, drawn geometry when it does not.

    The placeholder is deliberately plain so an un-made badge is obvious at a
    glance rather than passing for finished work.
    """
    if entry.get("badge"):
        return (f'<img class="badge" src="{entry["badge"]}" width="{size}" '
                f'height="{size}" alt="{html.escape(entry["name"])} badge">')

    _, glyph, colour = KINDS[entry["kind"]]
    initials = html.escape(entry["name"][:2])
    half = size / 2
    ident = entry["name"].lower()
    return f"""<svg class="badge" viewBox="0 0 {size} {size}" width="{size}"
     height="{size}" role="img" aria-label="badge pending">
  <defs><radialGradient id="g-{ident}" cx="50%" cy="38%">
    <stop offset="0" stop-color="{colour}" stop-opacity=".30"/>
    <stop offset="1" stop-color="{colour}" stop-opacity="0"/>
  </radialGradient></defs>
  <circle cx="{half}" cy="{half}" r="{half - 3}" fill="url(#g-{ident})"/>
  <circle cx="{half}" cy="{half}" r="{half - 9}" fill="none" stroke="{colour}"
          stroke-width="2" stroke-opacity=".85"/>
  <circle cx="{half}" cy="{half}" r="{half - 18}" fill="none" stroke="{colour}"
          stroke-width="1" stroke-opacity=".30" stroke-dasharray="3 7"/>
  <text x="{half}" y="{half - 4}" text-anchor="middle" fill="{colour}"
        font-family="ui-monospace,Menlo,monospace" font-size="27"
        font-weight="700">{initials}</text>
  <text x="{half}" y="{half + 22}" text-anchor="middle" fill="{colour}"
        font-family="ui-monospace,Menlo,monospace" font-size="15"
        opacity=".8">{html.escape(glyph)}</text>
</svg>"""


def card(entry):
    label, _, colour = KINDS[entry["kind"]]
    pending = "" if entry.get("badge") else \
        '<span class="pending">badge in the works</span>'
    return f"""<article class="card">
  {badge_art(entry)}
  <div class="body">
    <h2>{html.escape(entry["name"])}</h2>
    <p class="title" style="color:{colour}">{html.escape(entry["title"])}</p>
    <p class="citation">{html.escape(entry["citation"])}</p>
    <p class="meta">
      <span style="color:{colour}">{label}</span>
      <span class="when">{html.escape(entry["stream"])} &middot; {entry["date"]}</span>
      {pending}
    </p>
  </div>
</article>"""


CSS = """
:root { --bg:#070c12; --line:#1d2b39; --ink:#d3e7f2; --dim:#7f97a8;
        --accent:#3fd8ff; }
* { box-sizing:border-box; }
body { margin:0; min-height:100vh; color:var(--ink);
  font:15px/1.6 ui-monospace,Menlo,Consolas,monospace;
  background:
    radial-gradient(1200px 700px at 12% -10%, rgba(74,31,122,.45), transparent 60%),
    radial-gradient(900px 600px at 95% 8%, rgba(26,92,134,.40), transparent 60%),
    var(--bg); }
header { padding:44px 32px 6px; max-width:1180px; }
h1 { margin:0; font-size:20px; font-weight:400; letter-spacing:.24em;
     color:var(--accent); }
.sub { color:var(--dim); font-size:12px; letter-spacing:.16em; }
.lede { color:var(--dim); max-width:64ch; margin:20px 0 30px; }
main { padding:0 32px 60px; max-width:1180px; }
.grid { display:grid; gap:16px;
        grid-template-columns:repeat(auto-fill,minmax(540px,1fr)); }
.card { display:flex; gap:22px; padding:20px; border-radius:10px;
  border:1px solid var(--line);
  background:linear-gradient(180deg, rgba(20,32,45,.82), rgba(12,20,29,.82)); }
.badge { flex:0 0 auto; align-self:flex-start; }
.card h2 { margin:2px 0 5px; font-size:21px; font-weight:400; letter-spacing:.05em; }
.title { margin:0 0 8px; font-size:12.5px; letter-spacing:.14em;
         text-transform:uppercase; }
.citation { margin:0; font-size:13.5px; opacity:.93; }
.meta { margin:10px 0 0; font-size:11px; letter-spacing:.1em;
        display:flex; gap:14px; flex-wrap:wrap; align-items:center; }
.when { color:var(--dim); }
.pending { color:var(--dim); border:1px solid var(--line); border-radius:4px;
           padding:2px 7px; }
footer { padding:0 32px 48px; max-width:70ch; color:var(--dim); font-size:12px; }
footer a { color:var(--accent); }
@media (max-width:520px) { .card { flex-direction:column; } }
"""


def page():
    cards = "\n".join(card(e) for e in
                      sorted(ENTRIES, key=lambda e: e["date"], reverse=True))
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>hall of fame - noisy coder</title>
<meta name="description" content="Viewers who changed the outcome of a noisy
coder stream.">
<style>{CSS}</style>
</head><body>
<header>
  <h1>HALL OF FAME</h1>
  <p class="sub">noisy coder &middot; people who helped</p>
  <p class="lede">This channel is built live, out loud, with an audience. Now
  and then someone in chat says the thing that unblocks the whole stream. This
  is where those people go.</p>
</header>
<main><div class="grid">
{cards}
</div></main>
<footer>
  Every citation is something the person did in this channel's chat, in public.
  Nobody is listed without being thanked on stream first.
</footer>
</body></html>"""


def main():
    path = os.path.join(HERE, "index.html")
    with open(path, "w") as fh:
        fh.write(page())
    print("wrote", path, f"({len(ENTRIES)} entries)")


if __name__ == "__main__":
    main()
