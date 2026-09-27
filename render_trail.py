#!/usr/bin/env python3
"""TRAIL MIX — Maple and Herbie's monthly outdoors magazine: the cover story, trail picks around Lewiston/Auburn and Maine,
the MapPI3 trip log, gear worth a look, seasonal tips and Herbie's column.

Usage: render_trail.py drafts/<YYYY-MM>.json   -> site/issues/<YYYY-MM>.html + home + back issues
       render_trail.py --build                  (reprint the home page: the newest issue, or a preview before the first)
"""
import datetime as dt, json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
sys.path.insert(0, ROOT)
import pubkit as pk   # noqa: E402
import flipbook as fb   # noqa: E402
from pubkit import e   # noqa: E402

fb.CSS_FILE = "trail-mix.css"
REPO = "https://github.com/real-CAK3D/TrailMix"


def month_name(m):
    return dt.date.fromisoformat(m + "-01").strftime("%B %Y")


def seal():
    return '<a class="seal" href="/" aria-label="Back to The Corner Chronicle">%s</a>' % fb.SEAL


def draw_cover(m):
    d = dt.date.fromisoformat(m + "-01")
    return pk.draw_image(os.path.join(SITE, "img", "covers", m + ".jpg"), (
        "A professional travel-guidebook cover photograph, vertical, full bleed, no text or lettering. A scenic hiking trail in western Maine in %s: "
        "a narrow dirt footpath winding over granite ledges toward a mountain summit view of lakes and rolling forested hills, "
        "one small hiker with a backpack seen from behind far along the trail, bright natural light, rich true-to-life colors, "
        "shot on a full-frame camera, the top third mostly open sky for a title." % pk.SEASONS.get(d.month, "autumn")), size="1024x1536")


def cover(m, no, teaser):
    d = dt.date.fromisoformat(m + "-01")
    art = draw_cover(m)
    return fb.page("Trail Mix", (
        '<div class="tg%s">%s<div class="tg-top"><span class="tg-brand">Trail Mix</span><span class="tg-ed">%s · No. %s</span></div>'
        '<h1 class="tg-place">Maine</h1><div class="tg-sub">Trails · Trip Log · Gear · Seasons</div>'
        '<div class="tg-round">This month&#39;s<b>top trails</b>+ the trip log</div>'
        '<div class="tg-foot"><div class="tg-teaser">%s</div><div class="tg-by"><span>Maple &amp; Herbie&#39;s guide</span><span>Lewiston &amp; beyond</span></div></div>'
        '<div class="tg-seal">%s</div></div>')
        % ("" if art else " tg-noimg", ('<img class="tg-photo" src="../img/covers/%s.jpg" alt="A Maine hiking trail in %s">' % (m, d.strftime("%B"))) if art else "",
           d.strftime("%B %Y").upper(), no, e(teaser), seal()), " hardcover tm-cov")


def back(m, no):
    return fb.page("Back Page", ('<div class="gum"><span>TRAIL MIX · PACK IT IN, PACK IT OUT</span></div><div class="pb-body">%s<h2 class="pb-title">Trail Mix</h2>'
                                 '<p>Mixed by Maple &amp; Herbie from the MapPI3 logs and the trailhead.<br>Leave no trace — except in the Garden Wiki.</p>%s'
                                 '<p class="pb-code">%s · No. %s</p><p><a href="../archive.html">Back issues ›</a></p></div>')
                   % (seal(), fb.back_codes(REPO, "TrailMix"), e(month_name(m)), no), " hardcover back")


def render(ed):
    m = ed["month"]
    no = (dt.date.fromisoformat(m + "-01").year - 2026) * 12 + dt.date.fromisoformat(m + "-01").month - 8
    cv = ed.get("cover") or {}
    pages = [fb.page("Cover Story", '<div class="tm-feature">%s</div>' % fb.story(cv, lead=True))]
    picks = "".join('<div class="tm-trail"><div class="tm-trail-h"><b>%s</b><span>%s</span></div><div class="tm-stats">%s%s%s</div><p>%s</p>%s</div>'
                    % (e(t.get("name")), e(t.get("where")), ('<i>📏 %s</i>' % e(t["distance"])) if t.get("distance") else "",
                       ('<i>⛰ %s</i>' % e(t["difficulty"])) if t.get("difficulty") else "", ('<i>🍂 %s</i>' % e(t["best_time"])) if t.get("best_time") else "",
                       e(t.get("why")), ('<a href="%s" target="_blank" rel="noopener">Trail details ›</a>' % e(t["url"])) if str(t.get("url", "")).startswith("https://") else "")
                    for t in ed.get("trail_picks") or [] if isinstance(t, dict))
    if picks:
        pages.append(fb.page("Trail Picks", '<h2 class="tm-h">Trail Picks</h2><div class="tm-trails">%s</div>' % picks))
    log = "".join('<li><span class="cu-when">%s</span>%s<span><b>%s</b> — %s</span></li>' % (e(x.get("date")), fb.mug(x.get("agent"), "mug xs"), e(x.get("where")), e(x.get("what")))
                  for x in ed.get("trip_log") or [] if isinstance(x, dict))
    if log:
        pages.append(fb.page("The Trip Log", '<div class="box"><h2>The Trip Log</h2><p class="small">Where Maple, Herbie and MapPI3 went this month</p><ul class="cu">%s</ul></div>' % log))
    gear = "".join('<div class="tm-gear"><b>%s</b><span class="tm-price">%s</span><p>%s</p>%s</div>'
                   % (e(g.get("item")), e(g.get("price")), e(g.get("why")), ('<a href="%s" target="_blank" rel="noopener">Look ›</a>' % e(g["url"])) if str(g.get("url", "")).startswith("https://") else "")
                   for g in ed.get("gear") or [] if isinstance(g, dict))
    tips = "".join("<li>%s</li>" % e(t) for t in ed.get("seasonal") or [] if t)
    if gear or tips:
        pages.append(fb.page("Gear & Season", '<div class="tm-2"><div><h2 class="tm-h">Gear Worth a Look</h2>%s</div><div class="box"><h2>This Season in Maine</h2><ul>%s</ul>%s</div></div>'
                             % (gear or '<p class="small">No gear this month.</p>', tips, ('<p class="small">%s</p>' % e(ed["forecast_note"])) if ed.get("forecast_note") else "")))
    col = ed.get("herbie_column") or {}
    if col.get("body"):
        pages.append(fb.page("Herbie's Column", '<div class="box column"><h2>Herbie\'s Column</h2>%s</div>' % fb.story(dict(col, agent="Herbie"))))
    pages = [cover(m, no, cv.get("title") or "")] + pages + [back(m, no)]
    return fb.book(pages, date=m + "-01", no=no, lists={}, paper="Trail Mix", motto="Salty, sweet, a little nutty",
                   gum="MAINE OUTDOORS · TRAILS · GEAR · SEASONS", price="PRICE: ONE GRANOLA BAR", delivered="MIXED BY MAPLE & HERBIE",
                   flap="Trail Mix · Maple & Herbie's outdoors monthly", body_class="pub-tm", est="MAPLE & HERBIE'S OUTDOORS MONTHLY")


def build():
    pk.sync_portraits(SITE)
    eds = pk.issues(SITE, pattern=r"\d{4}-\d{2}")
    if eds:
        html = open(os.path.join(SITE, "issues", eds[0] + ".html")).read().replace('href="../', 'href="').replace('src="../', 'src="')
        ed = pk.load(os.path.join(ROOT, "drafts", eds[0] + ".json"))
        pk.latest(SITE, "Trail Mix", eds[0] + "-01", (ed.get("cover") or {}).get("title") or month_name(eds[0]), "issues/%s.html" % eds[0], [x + "-01" for x in eds[:10]],
                  cover=("img/covers/%s.jpg" % eds[0]) if os.path.exists(os.path.join(SITE, "img", "covers", eds[0] + ".jpg")) else "")
    else:
        today = dt.date.today()
        nxt = (today.replace(day=1) + dt.timedelta(days=32)).replace(day=1)
        m = today.strftime("%Y-%m")
        pages = [cover(m, 1, "First issue %s" % nxt.strftime("%B 1")),
                 fb.page("Coming Soon", '<div class="box"><h2>The first Trail Mix lands %s</h2><p>On the 1st of every month Maple and Herbie mix up the best trails around '
                         'Lewiston, Auburn and the rest of Maine, the MapPI3 trip log, gear worth a look, what the season is doing, and Herbie\'s column.</p></div>'
                         % e(nxt.strftime("%B 1"))), back(m, 1)]
        html = fb.book(pages, date=m + "-01", no=1, lists={}, paper="Trail Mix", motto="Salty, sweet, a little nutty", gum="MAINE OUTDOORS · TRAILS · GEAR · SEASONS",
                       price="PRICE: ONE GRANOLA BAR", delivered="MIXED BY MAPLE & HERBIE", flap="Trail Mix · Maple & Herbie's outdoors monthly", body_class="pub-tm",
                       est="MAPLE & HERBIE'S OUTDOORS MONTHLY").replace('href="../', 'href="').replace('src="../', 'src="')
        pk.latest(SITE, "Trail Mix", today.isoformat(), "First issue %s" % nxt.strftime("%B 1"), "", [],
                  cover=("img/covers/%s.jpg" % m) if os.path.exists(os.path.join(SITE, "img", "covers", m + ".jpg")) else "")
    open(os.path.join(SITE, "index.html"), "w").write(html)
    pk.archive_page(SITE, os.path.join(ROOT, fb.CSS_FILE), "pub-tm", "Trail Mix", "every issue",
                    "".join('<li><a href="issues/%s.html">%s</a></li>' % (x, month_name(x)) for x in eds), "🥾")


def main():
    if sys.argv[1:] and sys.argv[1] != "--build":
        ed = json.load(open(sys.argv[1]))
        os.makedirs(os.path.join(SITE, "issues"), exist_ok=True)
        open(os.path.join(SITE, "issues", ed["month"] + ".html"), "w").write(render(ed))
        print("rendered Trail Mix", ed["month"])
    build()
    print("trail mix built")


if __name__ == "__main__":
    main()
