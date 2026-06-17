#!/usr/bin/env python3
"""Generate the Our Projects page from the real projects index."""
import json, os, re, shutil, html
SRC="/Users/joannawilkin/TC-projects/tc-website/trackingca-site/out"
WWW="/Users/joannawilkin/TC-projects/tc-website/trackingca-site/www"
ROOT="/Users/joannawilkin/TC-projects/tc-website-redesign"
PDIR=os.path.join(ROOT,"assets/projects"); os.makedirs(PDIR,exist_ok=True)
def esc(s): return html.escape(str(s or ""),quote=True)
def copy(src):
    if not src or not src.startswith("/images/"): return ""
    fp=os.path.join(WWW,src.lstrip("/"))
    if not os.path.exists(fp): return ""
    base=os.path.basename(src); shutil.copy(fp,os.path.join(PDIR,base)); return "assets/projects/"+base

d=json.load(open(os.path.join(SRC,"pages/page/projects/index.json")))
secs={s.get("title"):s.get("items",[]) for s in d["sections"]}
current=secs.get("Current Projects",[]); previous=secs.get("Previous Projects",[])

def card(it,tag):
    img=copy(it.get("cover"))
    thumb='<div class="thumb"><img src="%s" alt="" loading="lazy"></div>'%esc(img) if img else '<div class="thumb"></div>'
    return ('        <article class="card">%s<div class="pad"><span class="tag green">%s</span>'
            '<h3>%s</h3><p>%s</p></div></article>')%(thumb,tag,esc(it["title"]),esc(it.get("description","")))
cur_cards="\n".join(card(it,"Current project") for it in current)
prev_cards="\n".join(card(it,"Previous project") for it in previous)

base=open(os.path.join(ROOT,"resources.html")).read()
PRE=base[:base.index("<main")]; POST=base[base.index("</main>")+len("</main>"):]
PRE=re.sub(r"<title>.*?</title>","<title>Our Projects — Tracking California</title>",PRE,1,flags=re.DOTALL)
PRE=re.sub(r'<meta name="description" content=".*?">','<meta name="description" content="Current and past projects by Tracking California, in partnership with communities across the state.">',PRE,1)
PRE=re.sub(r'<meta property="og:title" content=".*?">','<meta property="og:title" content="Our Projects — Tracking California">',PRE,1)

main='''<main id="main" data-pagefind-body>

  <!-- BANNER -->
  <section class="page-banner">
    <div class="wrap">
      <h1>Our Projects</h1>
      <p class="lead">Research and community projects we run in partnership with organizations across California.</p>
    </div>
  </section>

  <section class="section" id="current">
    <div class="wrap">
      <h2 class="sec-title">Current projects</h2>
      <div class="grid g3">
%s
      </div>
    </div>
  </section>

  <section class="section" id="previous">
    <div class="wrap">
      <h2 class="sec-title">Previous projects</h2>
      <div class="grid g3">
%s
      </div>
    </div>
  </section>

</main>'''%(cur_cards,prev_cards)
open(os.path.join(ROOT,"projects.html"),"w").write(PRE+main+POST)
print("projects.html:",len(current),"current +",len(previous),"previous; covers copied:",len(os.listdir(PDIR)))
