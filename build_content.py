#!/usr/bin/env python3
"""Generate real-content pages for the TC website redesign prototype.

Reads the live site's structured JSON (trackingca-site/out) and produces:
  - resources.html  : filterable hub of real publications, newsletters, videos, news
  - news-<slug>.html: per-article reader pages for the 15 news items
  - patches index.html "Latest news" + "Putting our data to work" with real items
Images referenced by news/newsletters are copied into assets/content/.
External links (journals, Constant Contact, YouTube) are used as-is.
"""
import json, os, re, glob, shutil, html

SRC  = "/Users/joannawilkin/TC-projects/tc-website/trackingca-site/out"
WWW  = "/Users/joannawilkin/TC-projects/tc-website/trackingca-site/www"
ROOT = "/Users/joannawilkin/TC-projects/tc-website-redesign"
CONTENT_DIR = os.path.join(ROOT, "assets/content")
os.makedirs(CONTENT_DIR, exist_ok=True)

PUB_LIMIT, NL_LIMIT = 24, 18

# ---------- helpers ----------
def load(p):
    with open(os.path.join(SRC, p)) as f: return json.load(f)

def copy_img(src):
    """Copy /images/... asset into assets/content/, return new relative path or ''."""
    if not src or not src.startswith("/images/"): return src or ""
    fp = os.path.join(WWW, src.lstrip("/"))
    if not os.path.exists(fp): return ""
    base = os.path.basename(src)
    shutil.copy(fp, os.path.join(CONTENT_DIR, base))
    return "assets/content/" + base

def year_of(d):
    m = re.search(r"\d{4}", str(d or "")); return m.group(0) if m else ""

def sortkey(d):
    s = str(d or "")
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m: return m.group(0)
    y = year_of(s); return (y + "-00-00") if y else "0000-00-00"

def yt_thumb(url):
    m = re.search(r"(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{6,})", url or "")
    return ("https://img.youtube.com/vi/%s/hqdefault.jpg" % m.group(1)) if m else ""

TAG_IMG = {
    "air quality":"assets/img/topic-air.jpg","air":"assets/img/topic-air.jpg",
    "asthma":"assets/img/topic-air.jpg","traffic":"assets/tools/traffic.jpg",
    "water quality":"assets/img/topic-water.jpg","drinking water":"assets/img/topic-water.jpg",
    "water":"assets/img/topic-water.jpg","pfas":"assets/img/topic-water.jpg",
    "climate":"assets/img/topic-climate.jpg","heat":"assets/img/topic-climate.jpg",
    "pesticides":"assets/tools/pesticide.png","lead":"assets/img/infographic.png",
    "childhood lead poisoning":"assets/img/infographic.png",
}
def pub_img(tags):
    for t in tags:
        k=(t or "").lower()
        if k in TAG_IMG: return TAG_IMG[k]
    return "assets/img/infographic.png"

def esc(s): return html.escape(str(s or ""), quote=True)

# ---------- minimal markdown -> html ----------
def md(text):
    text = (text or "").replace("\r\n","\n")
    blocks = re.split(r"\n\s*\n", text)
    out=[]
    for b in blocks:
        b=b.strip()
        if not b: continue
        # standalone image
        im=re.fullmatch(r"!\[[^\]]*\]\(([^)]+)\)", b)
        if im:
            src=copy_img(im.group(1).strip())
            if src: out.append('<p><img src="%s" alt="" style="max-width:100%%;border-radius:8px;"></p>'%esc(src))
            continue
        # heading
        hm=re.match(r"(#{2,4})\s+(.*)", b)
        if hm:
            lvl=len(hm.group(1)); out.append("<h%d>%s</h%d>"%(lvl,inline(hm.group(2)),lvl)); continue
        # list
        if all(re.match(r"\s*[-*]\s+",l) for l in b.split("\n") if l.strip()):
            lis="".join("<li>%s</li>"%inline(re.sub(r"\s*[-*]\s+","",l,1)) for l in b.split("\n") if l.strip())
            out.append("<ul>%s</ul>"%lis); continue
        out.append("<p>%s</p>"%inline(b.replace("\n"," ")))
    return "\n".join(out)

def inline(s):
    s=esc(s)
    # images inline -> copy
    def imgrep(m):
        src=copy_img(m.group(2).strip()); return ('<img src="%s" alt="%s" style="max-width:100%%;border-radius:8px;">'%(esc(src),esc(m.group(1)))) if src else ""
    s=re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", imgrep, s)
    s=re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m:'<a href="%s">%s</a>'%(esc(m.group(2).strip()),m.group(1)), s)
    s=re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return s

# ---------- chrome template from resources.html ----------
with open(os.path.join(ROOT,"resources.html")) as f: base=f.read()
PRE = base[:base.index("<main")]
POST = base[base.index("</main>")+len("</main>"):]
def page(title, desc, main):
    pre=re.sub(r"<title>.*?</title>","<title>%s</title>"%esc(title),PRE,1,flags=re.DOTALL)
    pre=re.sub(r'<meta name="description" content=".*?">','<meta name="description" content="%s">'%esc(desc),pre,1)
    pre=re.sub(r'<meta property="og:title" content=".*?">','<meta property="og:title" content="%s">'%esc(title),pre,1)
    return pre+main+POST

# ---------- gather content ----------
res=[]  # unified resource cards

# publications (external)
pubs=load("pages/page/publications/articles/index.json")["sections"][0]["items"]
pubs=sorted(pubs,key=lambda x:sortkey(x.get("date")),reverse=True)[:PUB_LIMIT]
for it in pubs:
    res.append(dict(type="paper",label="Publication",cls="type-paper",
        title=it["title"],meta=year_of(it.get("date")),
        href=it.get("target") or "#",ext=True,img=pub_img([t.get("name") for t in it.get("tags",[])]),date=sortkey(it.get("date"))))

# newsletters (external, Constant Contact)
nls=[json.load(open(p)) for p in glob.glob(os.path.join(SRC,"parts/newsletters/*.json"))]
nls=sorted(nls,key=lambda x:sortkey(x.get("date")),reverse=True)[:NL_LIMIT]
for n in nls:
    res.append(dict(type="newsletter",label="Newsletter",cls="type-newsletter",
        title=n["title"],meta=year_of(n.get("date")),href=n.get("url") or "#",ext=True,
        img=copy_img(n.get("image")) or "assets/img/community-voices.jpg",date=sortkey(n.get("date"))))

# videos (YouTube)
vids=[json.load(open(p)) for p in glob.glob(os.path.join(SRC,"parts/videos/*.json"))]
for v in vids:
    res.append(dict(type="video",label="Video",cls="type-report",
        title=v["title"],meta="Video",href=v.get("url") or "#",ext=True,
        img=yt_thumb(v.get("url")) or "assets/img/community-monitoring.jpg",date="0000-00-00"))

# news (internal reader pages)
NEWS=[]
for p in sorted(glob.glob(os.path.join(SRC,"pages/news/*.json"))):
    d=json.load(open(p))
    slug=re.sub(r"[^a-z0-9]+","-",d.get("name","").lower()).strip("-") or re.sub(r"[^a-z0-9]+","-",d["title"].lower())[:40].strip("-")
    NEWS.append(dict(d=d,slug=slug))
    res.append(dict(type="news",label="News",cls="type-commentary",
        title=d["title"],meta=year_of(d.get("date")),href="news-%s.html"%slug,ext=False,
        img=copy_img(d.get("thumbnail")) or "assets/img/community-meeting.jpg",date=sortkey(d.get("date"))))

# ---------- build resources.html ----------
def card(r):
    t='<article class="card" data-type="%s"><div class="thumb"><img src="%s" alt="" loading="lazy"></div><div class="pad"><span class="tag %s">%s</span><h3><a href="%s"%s>%s</a></h3><p class="meta">%s</p></div></article>'
    ext=' target="_blank" rel="noopener"' if r["ext"] else ""
    return t%(r["type"],esc(r["img"]),r["cls"],r["label"],esc(r["href"]),ext,esc(r["title"]),esc(r["meta"]))

res_sorted=sorted(res,key=lambda r:r["date"],reverse=True)
cards="\n".join("        "+card(r) for r in res_sorted)
res_main='''<main id="main">

  <!-- BANNER -->
  <section class="page-banner">
    <div class="wrap">
      <p class="eyebrow">Library</p>
      <h1>Resources</h1>
      <p class="lead">Publications, newsletters, videos, and news from Tracking California.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="filters">
        <span class="label">Filter</span>
        <button class="pill on" data-filter="all">All</button>
        <button class="pill" data-filter="paper">Publications</button>
        <button class="pill" data-filter="newsletter">Newsletters</button>
        <button class="pill" data-filter="video">Videos</button>
        <button class="pill" data-filter="news">News</button>
      </div>
      <div class="grid g3">
%s
      </div>
      <p class="meta" style="margin-top:26px;">Showing a recent selection. The full archive lives on <a href="https://trackingcalifornia.org" target="_blank" rel="noopener">trackingcalifornia.org</a>.</p>
    </div>
  </section>

</main>'''%cards
with open(os.path.join(ROOT,"resources.html"),"w") as f:
    f.write(page("Resources — Tracking California","Publications, newsletters, videos, and news from Tracking California.",res_main))

# ---------- per-article news pages ----------
for n in NEWS:
    d=n["d"]; body=md(d.get("rte_body"))
    hero=copy_img(d.get("thumbnail"))
    heroimg='<div class="card thumb" style="aspect-ratio:16/8;border-radius:var(--radius);margin-bottom:8px;"><img src="%s" alt=""></div>'%esc(hero) if hero else ""
    main='''<main id="main">
  <div class="wrap narrow">
    <p class="breadcrumb"><a href="index.html">Home</a> / <a href="resources.html">Resources</a> / News</p>
  </div>
  <section class="page-banner">
    <div class="wrap narrow">
      <p class="eyebrow">News</p>
      <h1>%s</h1>
      <p class="meta">%s</p>
    </div>
  </section>
  <section class="section" style="padding-top:28px;">
    <div class="wrap narrow">
      %s
      <div class="prose">
%s
      </div>
      <p style="margin-top:28px;"><a class="link-arrow" href="resources.html">Back to all resources</a></p>
    </div>
  </section>
</main>'''%(esc(d["title"]),esc(year_of(d.get("date"))),heroimg,body)
    with open(os.path.join(ROOT,"news-%s.html"%n["slug"]),"w") as f:
        f.write(page(esc(d["title"])+" — Tracking California", esc(d.get("description"))[:180], main))

print("resources cards:",len(res_sorted),"| news pages:",len(NEWS),"| images copied:",len(os.listdir(CONTENT_DIR)))
# expose latest news for homepage patch
latest=[r for r in res_sorted if r["type"]=="news"][:3]
recent_pubs=[r for r in res_sorted if r["type"]=="paper"][:3]
json.dump({"news":latest,"pubs":recent_pubs}, open(os.path.join(ROOT,".content_latest.json"),"w"))
