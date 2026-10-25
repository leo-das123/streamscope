"""StreamScope — single-file NiceGUI music-listening analytics portfolio.

The application keeps the supplied site's visual identity, page content, and
provided images, while consolidating the web app into one Python entrypoint.

Install:
    python -m pip install nicegui

Run:
    python app.py
"""

from __future__ import annotations

import os
from pathlib import Path

from nicegui import app, ui


# ============================================================
# PATHS / CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

# Support both common layouts used by the supplied project:
#   data-decoded-blog-V1/assets/images
#   data-decoded-blog/assets/img
# The app serves the detected image directory uniformly as /assets/*.png.
IMAGE_CANDIDATES = (
    BASE_DIR / "assets" / "images",
    BASE_DIR / "assets" / "img",
    BASE_DIR / "data-decoded-blog-V1" / "assets" / "images",
    BASE_DIR / "data-decoded-blog-V1" / "assets" / "img",
    BASE_DIR / "data-decoded-blog" / "assets" / "images",
    BASE_DIR / "data-decoded-blog" / "assets" / "img",
    BASE_DIR.parent / "data-decoded-blog-V1" / "assets" / "images",
    BASE_DIR.parent / "data-decoded-blog" / "assets" / "img",
)
IMAGE_DIR = next((path for path in IMAGE_CANDIDATES if path.is_dir()), IMAGE_CANDIDATES[0])
DEFAULT_PORT = 8080


# ============================================================
# GLOBAL STYLES
# ============================================================

CSS = r'''
/* ============================================================
   DESIGN TOKENS
   ============================================================ */
:root{
  --ink:        #12151C;
  --ink-soft:   #2A3040;
  --paper:      #F6F4EF;
  --paper-raise:#FFFFFF;
  --navy:       #1F2A44;
  --navy-deep:  #141B2E;
  --teal:       #1E8F79;
  --teal-deep:  #146857;
  --amber:      #D98F31;
  --line:       #DFDAC9;
  --line-soft:  #EAE6D9;
  --muted:      #5B6472;
  --muted-2:    #8A8F98;

  --serif: "Fraunces", Georgia, "Iowan Old Style", serif;
  --sans:  "IBM Plex Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --mono:  "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;

  --measure: 66ch;
  --wrap: 1480px;

  --radius-s: 4px;
  --radius-m: 10px;
}

*,*::before,*::after{ box-sizing:border-box; }
html{ scroll-behavior:smooth; }
body{
  margin:0;
  background:var(--paper);
  color:var(--ink);
  font-family:var(--sans);
  font-size:16px;
  line-height:1.6;
  -webkit-font-smoothing:antialiased;
  text-rendering:optimizeLegibility;
}
img{ max-width:100%; display:block; }
a{ color:inherit; text-decoration:none; }
ul,ol{ padding-left:1.2em; }
button{ font-family:inherit; }

::selection{ background:var(--teal); color:#fff; }

:focus-visible{
  outline:2px solid var(--teal);
  outline-offset:3px;
}

@media (prefers-reduced-motion: reduce){
  *{ animation-duration:0.01ms !important; animation-iteration-count:1 !important; transition-duration:0.01ms !important; scroll-behavior:auto !important; }
}

.wrap{
  max-width:var(--wrap);
  margin:0 auto;
  padding:0 24px;
}

/* ============================================================
   TYPE SCALE
   ============================================================ */
h1,h2,h3,h4{
  font-family:var(--serif);
  color:var(--navy-deep);
  line-height:1.15;
  margin:0 0 0.5em;
  font-weight:600;
  letter-spacing:-0.01em;
}
h1{ font-size:clamp(2.2rem, 4.5vw, 3.6rem); font-weight:600; }
h2{ font-size:clamp(1.5rem, 2.6vw, 2.15rem); }
h3{ font-size:clamp(1.15rem, 1.8vw, 1.4rem); }
p{ margin:0 0 1.1em; color:var(--ink-soft); }
.lede{ font-size:1.2rem; color:var(--muted); line-height:1.55; }

.eyebrow{
  font-family:var(--mono);
  font-size:0.72rem;
  letter-spacing:0.06em;
  color:var(--teal-deep);
  display:inline-flex;
  align-items:center;
  gap:8px;
}
.eyebrow::before{
  content:"";
  width:16px; height:1px;
  background:var(--teal);
}

.stat-figure{
  font-family:var(--mono);
}

/* ============================================================
   HEADER / NAV
   ============================================================ */
.site-header{
  position:sticky; top:0; z-index:50;
  background:rgba(246,244,239,0.92);
  backdrop-filter:blur(10px);
  border-bottom:1px solid var(--line);
}
.header-inner{
  display:flex; align-items:center; justify-content:space-between;
  height:72px;
}
.brand{
  display:flex; align-items:center; gap:10px;
  font-family:var(--serif);
  font-weight:600;
  font-size:1.25rem;
  color:var(--navy-deep);
}
.brand-mark{
  width:30px; height:30px;
  flex:none;
}
.brand small{
  display:block;
  font-family:var(--sans);
  font-weight:400;
  font-size:0.62rem;
  letter-spacing:0.08em;
  color:var(--muted-2);
  margin-top:1px;
}

.main-nav{ display:flex; align-items:center; gap:2px; }
.main-nav a{
  padding:9px 14px;
  font-size:0.92rem;
  color:var(--ink-soft);
  border-radius:6px;
  position:relative;
}
.main-nav a:hover{ color:var(--navy-deep); background:var(--line-soft); }
.main-nav a.active{ color:var(--navy-deep); font-weight:600; }
.main-nav a.active::after{
  content:"";
  position:absolute; left:14px; right:14px; bottom:3px;
  height:2px; background:var(--teal);
}

.nav-toggle{
  display:none;
  background:none; border:none; cursor:pointer;
  width:40px; height:40px;
  align-items:center; justify-content:center;
}
.nav-toggle span, .nav-toggle span::before, .nav-toggle span::after{
  content:""; display:block;
  width:20px; height:2px; background:var(--navy-deep);
  position:relative; transition:transform .2s ease, opacity .2s ease;
}
.nav-toggle span::before{ position:absolute; top:-6px; }
.nav-toggle span::after{ position:absolute; top:6px; }
.nav-toggle.open span{ background:transparent; }
.nav-toggle.open span::before{ transform:translateY(6px) rotate(45deg); }
.nav-toggle.open span::after{ transform:translateY(-6px) rotate(-45deg); }

/* ============================================================
   BUTTONS
   ============================================================ */
.btn{
  display:inline-flex; align-items:center; justify-content:center; gap:8px;
  padding:12px 22px;
  border-radius:7px;
  font-size:0.94rem;
  font-weight:600;
  border:1px solid transparent;
  cursor:pointer;
  transition:background .15s ease, color .15s ease, border-color .15s ease, transform .1s ease;
}
.btn:active{ transform:translateY(1px); }
.btn-primary{ background:var(--navy-deep); color:#fff; }
.btn-primary:hover{ background:var(--teal-deep); }
.btn-outline{ background:transparent; color:var(--navy-deep); border-color:var(--line); }
.btn-outline:hover{ border-color:var(--navy-deep); }
.btn-teal{ background:var(--teal); color:#fff; }
.btn-teal:hover{ background:var(--teal-deep); }
.btn-block{ width:100%; }
.btn-sm{ padding:8px 16px; font-size:0.85rem; }

/* ============================================================
   HERO (home)
   ============================================================ */
.hero{
  position:relative;
  padding:64px 0 72px;
  overflow:hidden;
  background:
    linear-gradient(180deg, var(--paper) 0%, var(--paper) 100%);
}
.hero::before{
  content:"";
  position:absolute; inset:0;
  background-image:
    linear-gradient(var(--line-soft) 1px, transparent 1px),
    linear-gradient(90deg, var(--line-soft) 1px, transparent 1px);
  background-size:44px 44px;
  mask-image:radial-gradient(ellipse 80% 60% at 20% 20%, black 15%, transparent 70%);
  opacity:0.7;
  pointer-events:none;
}
.hero-grid{
  position:relative;
  display:grid;
  grid-template-columns:1.1fr 0.9fr;
  gap:48px;
  align-items:center;
}
.hero-copy p.lede{ max-width:44ch; }
.hero-actions{ display:flex; gap:12px; margin-top:28px; flex-wrap:wrap; }
.hero-meta{
  display:flex; gap:22px; margin-top:40px;
  padding-top:24px; border-top:1px solid var(--line);
  flex-wrap:wrap;
}
.hero-meta div{ min-width:110px; }
.hero-meta .num{ font-family:var(--mono); font-size:1.3rem; color:var(--navy-deep); font-weight:600; }
.hero-meta .lbl{ font-size:0.78rem; color:var(--muted); }

.hero-art{ position:relative; }

/* ============================================================
   CARDS (article / listing cards)
   ============================================================ */
.card-grid{
  display:grid;
  grid-template-columns:repeat(3, minmax(0, 1fr));
  gap:28px;
  align-items:stretch;
}
.article-card{
  display:flex; flex-direction:column;
  background:var(--paper-raise);
  border:1px solid var(--line);
  border-top:3px solid var(--teal);
  border-radius:var(--radius-s);
  overflow:hidden;
  transition:transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}
.article-card:hover{
  transform:translateY(-3px);
  box-shadow:0 14px 28px -18px rgba(20,27,46,0.35);
}
.article-card .card-media{
  aspect-ratio:16/10;
  background:var(--navy-deep);
  position:relative;
  overflow:hidden;
}
.article-card .card-media img{
  width:100%; height:100%; object-fit:cover;
  object-position:center;
}
.article-card .card-body{
  padding:20px 20px 24px;
  display:flex; flex-direction:column; flex:1;
}
.card-cat{
  font-family:var(--mono); font-size:0.68rem; letter-spacing:0.04em;
  color:var(--teal-deep); margin-bottom:10px;
}
.article-card h3{ margin-bottom:10px; }
.article-card h3 a:hover{ color:var(--teal-deep); }
.card-excerpt{ font-size:0.92rem; color:var(--muted); flex:1; }
.card-meta{
  display:flex; align-items:center; gap:10px;
  font-size:0.78rem; color:var(--muted-2);
  margin-top:14px; padding-top:14px; border-top:1px solid var(--line-soft);
}
.card-meta .dot{ width:3px; height:3px; border-radius:50%; background:var(--muted-2); }

/* Blog archive cards: preserve the complete source image at its natural
   aspect ratio instead of cropping every image into the same box. */
.blog-post-grid{
  grid-template-columns:repeat(3, minmax(0, 1fr));
  gap:28px;
}
.blog-post-grid .article-card{
  min-width:0;
  animation:blogCardIn .55s ease both;
  transition:transform .22s ease, box-shadow .22s ease, border-color .22s ease;
}
.blog-post-grid .article-card:hover{
  transform:translateY(-6px);
  box-shadow:0 20px 36px -22px rgba(20,27,46,0.46);
  border-color:#d2ccb9;
}
.blog-post-grid .article-card:nth-child(1){ animation-delay:.03s; }
.blog-post-grid .article-card:nth-child(2){ animation-delay:.08s; }
.blog-post-grid .article-card:nth-child(3){ animation-delay:.13s; }
.blog-post-grid .article-card:nth-child(4){ animation-delay:.18s; }
.blog-post-grid .article-card:nth-child(5){ animation-delay:.23s; }
.blog-post-grid .card-media{
  display:flex;
  align-items:center;
  justify-content:center;
  background:#fff;
  aspect-ratio:auto;
}
.blog-post-grid .card-media img{
  display:block;
  width:100%;
  height:auto;
  max-width:100%;
  max-height:none;
  object-fit:contain;
  object-position:center;
  transition:transform .35s ease, filter .35s ease;
}

.blog-post-grid .strategy-card-media{
  aspect-ratio:16/10;
  background:var(--navy-deep);
  overflow:hidden;
}

.blog-post-grid .strategy-visual{
  display:block;
  width:100%;
  height:100%;
  object-fit:cover;
  transition:transform .35s ease, filter .35s ease;
}

.blog-post-grid .article-card:hover .strategy-visual{
  transform:scale(1.018);
  filter:saturate(1.03);
}
.blog-post-grid .article-card:hover .card-media img{
  transform:scale(1.018);
  filter:saturate(1.03);
}
.blog-post-grid .card-body{
  min-height:250px;
}

@keyframes blogCardIn{
  from{ opacity:0; transform:translateY(12px); }
  to{ opacity:1; transform:translateY(0); }
}

.article-card.featured{
  grid-column:1 / -1;
  flex-direction:row;
  min-height:360px;
}
.article-card.featured .card-media{
  flex:1 1 46%;
  min-width:0;
  aspect-ratio:auto;
  display:flex;
  align-items:center;
  justify-content:center;
  background:var(--navy-deep);
}
.article-card.featured .card-media img{
  width:100%;
  height:100%;
  object-fit:contain;
  object-position:center;
}
.article-card.featured .card-body{ flex:1 1 54%; min-width:0; padding:36px 52px; justify-content:center; }
.article-card.featured h3{ font-size:clamp(1.35rem, 2vw, 1.75rem); line-height:1.12; }

.empty-slot{
  border:1px dashed var(--line);
  border-radius:var(--radius-s);
  display:flex; flex-direction:column; align-items:flex-start; justify-content:center;
  gap:8px; padding:24px;
  color:var(--muted-2);
  font-size:0.88rem;
}

/* ============================================================
   SECTIONS
   ============================================================ */
section{ padding:64px 0; }
.section-head{
  display:flex; align-items:flex-end; justify-content:space-between;
  gap:24px; margin-bottom:32px; flex-wrap:wrap;
}
.section-head h2{ margin:0; }
.section-head .see-all{ font-size:0.88rem; color:var(--teal-deep); font-weight:600; white-space:nowrap; }
.section-head .see-all:hover{ text-decoration:underline; }

.band{ background:var(--navy-deep); color:#fff; }
.band h2, .band h3{ color:#fff; }
.band p{ color:rgba(255,255,255,0.72); }

/* categories */
.cat-grid{
  display:grid; grid-template-columns:repeat(4,1fr); gap:16px;
}
.cat-tile{
  border:1px solid var(--line);
  border-radius:var(--radius-s);
  padding:20px;
  background:var(--paper-raise);
  transition:border-color .15s ease, transform .15s ease;
}
.cat-tile:hover{ border-color:var(--teal); transform:translateY(-2px); }
.cat-tile .n{ font-family:var(--mono); font-size:0.78rem; color:var(--muted-2); }
.cat-tile h4{ margin:6px 0 0; font-size:1.05rem; color:var(--navy-deep); }

/* newsletter */
.newsletter{
  background:var(--teal-deep);
  color:#fff;
  border-radius:var(--radius-m);
  padding:44px;
  display:grid;
  grid-template-columns:1.2fr 1fr;
  gap:36px;
  align-items:center;
}
.newsletter h2{ color:#fff; margin-bottom:10px; }
.newsletter p{ color:rgba(255,255,255,0.82); margin-bottom:0; }
.nl-form{ display:flex; gap:10px; }
.nl-form input{
  flex:1;
  padding:13px 16px;
  border-radius:7px;
  border:1px solid rgba(255,255,255,0.3);
  background:rgba(255,255,255,0.08);
  color:#fff;
  font-size:0.95rem;
}
.nl-form input::placeholder{ color:rgba(255,255,255,0.55); }
.nl-note{ font-size:0.78rem; color:rgba(255,255,255,0.6); margin-top:10px; }

/* ============================================================
   FOOTER
   ============================================================ */
.site-footer{
  border-top:1px solid var(--line);
  padding:52px 0 28px;
  margin-top:40px;
}
.footer-grid{
  display:grid;
  grid-template-columns:1.4fr 1fr 1fr 1fr;
  gap:32px;
  margin-bottom:36px;
}
.footer-grid h5{
  font-size:0.75rem; letter-spacing:0.04em; color:var(--muted-2);
  margin:0 0 14px; font-weight:600; text-transform:uppercase;
}
.footer-grid ul{ list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:9px; }
.footer-grid a{ font-size:0.92rem; color:var(--ink-soft); }
.footer-grid a:hover{ color:var(--teal-deep); }
.footer-brand p{ font-size:0.9rem; color:var(--muted); max-width:34ch; }
.footer-bottom{
  display:flex; justify-content:space-between; align-items:center;
  padding-top:24px; border-top:1px solid var(--line);
  font-size:0.82rem; color:var(--muted-2); flex-wrap:wrap; gap:12px;
}

/* ============================================================
   BLOG LISTING PAGE
   ============================================================ */
.listing-head{
  padding:48px 0 32px;
  border-bottom:1px solid var(--line);
}
.filter-bar{
  display:flex; align-items:center; justify-content:space-between;
  gap:20px; flex-wrap:nowrap;
  padding:20px 0;
  border-bottom:1px solid var(--line);
  margin-bottom:40px;
}
.chip-row{ display:flex; gap:8px; flex-wrap:wrap; min-width:0; }
.chip{
  padding:7px 14px;
  border-radius:20px;
  border:1px solid var(--line);
  font-size:0.84rem;
  color:var(--ink-soft);
  cursor:pointer;
  background:var(--paper-raise);
  transition:all .15s ease;
}
.chip:hover{ border-color:var(--teal); }
.chip.active{ background:var(--navy-deep); border-color:var(--navy-deep); color:#fff; }

.search-box{
  position:relative;
  width:300px;
  min-width:240px;
  flex:0 0 300px;
}
.search-box input{
  width:100%;
  padding:10px 14px 10px 38px;
  border-radius:7px;
  border:1px solid var(--line);
  background:var(--paper-raise);
  font-size:0.9rem;
}
.search-box svg{
  position:absolute; left:12px; top:50%; transform:translateY(-50%);
  width:16px; height:16px; color:var(--muted-2);
}

/* ============================================================
   ARTICLE PAGE
   ============================================================ */
.article-hero{
  padding:44px 0 0;
}
.article-hero .meta-row{
  display:flex; align-items:center; gap:16px; flex-wrap:wrap;
  font-size:0.86rem; color:var(--muted); margin-top:20px;
}
.author-chip{ display:flex; align-items:center; gap:10px; }
.author-avatar{
  width:34px; height:34px; border-radius:50%;
  background:var(--navy-deep); color:#fff;
  display:flex; align-items:center; justify-content:center;
  font-family:var(--serif); font-weight:600; font-size:0.85rem;
}
.article-featured-media{
  margin:32px 0 8px;
  border-radius:var(--radius-m);
  overflow:hidden;
  border:1px solid var(--line);
  background:var(--paper-raise);
  display:flex;
  justify-content:center;
}
.article-featured-media img{
  width:100%;
  height:auto;
  max-height:620px;
  object-fit:contain;
}
.share-rail{
  display:flex; flex-direction:column; gap:10px;
  position:sticky; top:100px;
}
.share-btn{
  width:38px; height:38px; border-radius:50%;
  border:1px solid var(--line);
  display:flex; align-items:center; justify-content:center;
  color:var(--ink-soft);
  transition:all .15s ease;
  background:var(--paper-raise);
}
.share-btn:hover{ border-color:var(--navy-deep); color:var(--navy-deep); }

.article-layout{
  display:grid;
  grid-template-columns:48px minmax(0,var(--measure)) 240px;
  gap:40px;
  align-items:start;
}
.article-layout .col-share{ position:sticky; top:100px; }
.article-body h2{ margin-top:2.2em; scroll-margin-top:90px; }
.article-body h3{ margin-top:1.6em; scroll-margin-top:90px; }
.article-body p{ font-size:1.04rem; }
.article-body figure{ margin:2em 0; }
.article-body figure img{
  width:100%;
  height:auto;
  max-height:620px;
  object-fit:contain;
  background:var(--paper-raise);
  border:1px solid var(--line-soft);
  border-radius:6px;
}
.article-body figcaption{
  font-size:0.85rem; color:var(--muted-2); margin-top:10px; text-align:center;
  font-style:italic;
}
.article-body blockquote{
  margin:1.8em 0; padding:2px 0 2px 22px;
  border-left:3px solid var(--teal);
  font-family:var(--serif); font-size:1.2rem; color:var(--navy-deep);
  font-style:italic;
}
.callout{
  background:#EFF6F3;
  border:1px solid #CFE6DC;
  border-left:4px solid var(--teal);
  border-radius:var(--radius-s);
  padding:20px 22px;
  margin:1.8em 0;
}
.callout.amber{ background:#FBF1E2; border-color:#EAD4A6; border-left-color:var(--amber); }
.callout .callout-label{
  font-family:var(--mono); font-size:0.72rem; letter-spacing:0.05em;
  color:var(--teal-deep); margin-bottom:8px; display:block;
}
.callout.amber .callout-label{ color:#9B6A17; }
.callout p:last-child{ margin-bottom:0; }

.stat-card-row{
  display:grid; grid-template-columns:repeat(4,1fr); gap:14px;
  margin:1.8em 0;
}
.stat-card{
  border:1px solid var(--line);
  background:var(--paper-raise);
  border-radius:var(--radius-s);
  padding:16px;
}
.stat-card .v{ font-family:var(--mono); font-size:1.35rem; color:var(--navy-deep); font-weight:600; }
.stat-card .l{ font-size:0.78rem; color:var(--muted); margin-top:2px; }

table{
  width:100%;
  border-collapse:collapse;
  margin:1.8em 0;
  font-size:0.92rem;
}
thead th{
  text-align:left;
  font-family:var(--mono);
  font-size:0.72rem;
  letter-spacing:0.03em;
  color:var(--muted);
  padding:10px 14px;
  border-bottom:2px solid var(--ink);
  background:var(--line-soft);
}
tbody td{
  padding:11px 14px;
  border-bottom:1px solid var(--line);
  color:var(--ink-soft);
}
tbody tr:hover{ background:var(--line-soft); }

.toc-nav{
  border-left:1px solid var(--line);
  padding-left:20px;
}
.toc-nav .toc-label{
  font-family:var(--mono); font-size:0.7rem; letter-spacing:0.05em;
  color:var(--muted-2); margin-bottom:12px; display:block;
}
.toc-nav ol{
  list-style:none; padding:0; margin:0;
  display:flex; flex-direction:column; gap:9px;
}
.toc-nav a{
  font-size:0.85rem; color:var(--muted);
  display:block; line-height:1.35;
  border-left:2px solid transparent;
  padding-left:10px; margin-left:-12px;
  transition:color .15s ease, border-color .15s ease;
}
.toc-nav a:hover{ color:var(--navy-deep); }
.toc-nav a.active{ color:var(--teal-deep); border-color:var(--teal); font-weight:600; }

.progress-bar{
  position:fixed; top:0; left:0; height:3px; background:var(--teal);
  width:0%; z-index:100; transition:width .1s linear;
}

.author-box{
  margin:56px 0 0;
  padding:28px;
  border:1px solid var(--line);
  border-radius:var(--radius-m);
  display:flex; gap:20px;
  background:var(--paper-raise);
}
.author-box .author-avatar{ width:56px; height:56px; font-size:1.2rem; flex:none; }
.author-box h4{ margin:0 0 4px; }
.author-box p{ margin:0; font-size:0.92rem; color:var(--muted); }

.prev-next{
  display:grid; grid-template-columns:1fr 1fr; gap:16px;
  margin:40px 0;
}
.pn-card{
  border:1px solid var(--line); border-radius:var(--radius-s);
  padding:20px; background:var(--paper-raise);
  transition:border-color .15s ease;
}
.pn-card:hover{ border-color:var(--teal); }
.pn-card .dir{ font-family:var(--mono); font-size:0.7rem; color:var(--muted-2); }
.pn-card.next{ text-align:right; }
.pn-card h5{ margin:8px 0 0; font-family:var(--serif); font-size:1.05rem; color:var(--navy-deep); }

.more-soon{
  border:1px dashed var(--line);
  border-radius:var(--radius-m);
  padding:40px;
  text-align:center;
  color:var(--muted);
}

/* ============================================================
   ABOUT / CONTACT
   ============================================================ */
.page-hero{
  padding:56px 0 40px;
  border-bottom:1px solid var(--line);
}
.two-col{
  display:grid; grid-template-columns:1fr 1fr; gap:56px; align-items:start;
}
.value-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:20px; margin-top:24px;}
.value-item{ padding:22px; border:1px solid var(--line); border-radius:var(--radius-s); background:var(--paper-raise);}
.value-item .idx{ font-family:var(--mono); font-size:0.75rem; color:var(--teal-deep); }

.contact-form{ display:flex; flex-direction:column; gap:16px; }
.field label{ display:block; font-size:0.85rem; font-weight:600; color:var(--ink-soft); margin-bottom:6px; }
.field input, .field textarea, .field select{
  width:100%; padding:12px 14px;
  border:1px solid var(--line); border-radius:7px;
  background:var(--paper-raise); font-family:inherit; font-size:0.95rem;
  color:var(--ink);
}
.field textarea{ resize:vertical; min-height:130px; }
.contact-info-item{ display:flex; gap:14px; padding:18px 0; border-bottom:1px solid var(--line); }
.contact-info-item .ic{ width:38px; height:38px; border-radius:50%; background:var(--line-soft); display:flex; align-items:center; justify-content:center; flex:none; color:var(--navy-deep); }
.contact-info-item h5{ margin:0 0 3px; font-size:0.95rem; color:var(--navy-deep); }
.contact-info-item p{ margin:0; font-size:0.88rem; color:var(--muted); }
.form-status{ font-size:0.88rem; padding:12px 14px; border-radius:7px; display:none; }
.form-status.show{ display:block; }
.form-status.ok{ background:#EFF6F3; color:var(--teal-deep); border:1px solid #CFE6DC; }

/* ============================================================
   MOBILE
   ============================================================ */
@media (max-width: 1100px){
  .blog-post-grid{ grid-template-columns:repeat(2, minmax(0, 1fr)); }
}

@media (max-width: 900px){
  .card-grid{ grid-template-columns:1fr; }
  .blog-post-grid{ grid-template-columns:1fr; }
  .blog-post-grid .card-body{ min-height:0; }
  .article-card.featured{ grid-column:1 / -1; flex-direction:column; min-height:0; }
  .article-card.featured .card-media{ min-height:280px; aspect-ratio:16/10; }
  .article-card.featured .card-body{ padding:28px; }
  .cat-grid{ grid-template-columns:repeat(2,1fr); }
  .hero-grid{ grid-template-columns:1fr; gap:36px; }
  .footer-grid{ grid-template-columns:1fr 1fr; }
  .two-col{ grid-template-columns:1fr; gap:36px; }
  .value-grid{ grid-template-columns:1fr; }
  .newsletter{ grid-template-columns:1fr; padding:30px; }
  .article-layout{ grid-template-columns:1fr; }
  .article-layout .col-toc{ order:-1; }
  .toc-nav{ border-left:none; padding-left:0; border:1px solid var(--line); border-radius:var(--radius-s); padding:18px; margin-bottom:8px; }
  .col-share{ display:none; }
  .prev-next{ grid-template-columns:1fr; }
  .stat-card-row{ grid-template-columns:1fr 1fr; }
}

@media (max-width: 720px){
  .main-nav{
    position:fixed; top:72px; left:0; right:0; bottom:0;
    background:var(--paper);
    flex-direction:column; align-items:stretch;
    padding:20px 24px;
    transform:translateX(100%);
    transition:transform .25s ease;
    overflow-y:auto;
  }
  .main-nav.open{ transform:translateX(0); }
  .main-nav a{ padding:14px 6px; font-size:1.05rem; border-bottom:1px solid var(--line-soft); border-radius:0; }
  .nav-toggle{ display:flex; }
  .header-actions{ display:none; }
}

@media (max-width: 980px){
  .filter-bar{ align-items:flex-start; flex-direction:column; flex-wrap:wrap; }
  .search-box{ width:min(100%, 360px); flex:0 0 auto; }
}

@media (max-width: 620px){
  .wrap{ padding-left:16px; padding-right:16px; }
  .article-card.featured .card-media{ min-height:220px; }
  .article-card.featured .card-body{ padding:24px; }
  section{ padding:44px 0; }
  .filter-bar{ align-items:flex-start; flex-direction:column; }
  .search-box{ width:100%; }
  .stat-card-row{ grid-template-columns:1fr 1fr; }
}

'''


# ============================================================
# CLIENT-SIDE BEHAVIOR
# ============================================================

JS = r'''

document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.main-nav');

  const closeNav = () => {
    if (!toggle || !nav) return;
    toggle.classList.remove('open');
    nav.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('nav-open');
  };

  const openNav = () => {
    if (!toggle || !nav) return;
    toggle.classList.add('open');
    nav.classList.add('open');
    toggle.setAttribute('aria-expanded', 'true');
    document.body.classList.add('nav-open');
  };

  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      toggle.classList.contains('open') ? closeNav() : openNav();
    });

    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', closeNav);
    });

    document.addEventListener('keydown', event => {
      if (event.key === 'Escape') closeNav();
    });

    window.addEventListener('resize', () => {
      if (window.innerWidth > 720) closeNav();
    });
  }

  const bar = document.querySelector('.progress-bar');

  if (bar) {
    const updateProgress = () => {
      const root = document.documentElement;
      const scrollTop = root.scrollTop || window.scrollY;
      const max = root.scrollHeight - root.clientHeight;
      const progress = max > 0
        ? Math.min(100, Math.max(0, (scrollTop / max) * 100))
        : 0;

      bar.style.width = `${progress}%`;
    };

    window.addEventListener('scroll', updateProgress, { passive: true });
    window.addEventListener('resize', updateProgress);
    updateProgress();
  }

  const tocLinks = document.querySelectorAll('.toc-nav a');

  if (tocLinks.length) {
    const sections = Array.from(tocLinks)
      .map(link => {
        const target = link.getAttribute('href');
        return target ? document.querySelector(target) : null;
      })
      .filter(Boolean);

    const observer = new IntersectionObserver(entries => {
      const active = entries
        .filter(entry => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

      if (!active) return;

      tocLinks.forEach(link => {
        const selected = link.getAttribute('href') === `#${active.target.id}`;

        link.classList.toggle('active', selected);

        if (selected) {
          link.setAttribute('aria-current', 'true');
        } else {
          link.removeAttribute('aria-current');
        }
      });
    }, {
      rootMargin: '-15% 0px -65% 0px',
      threshold: [0, 0.15, 0.3, 0.5]
    });

    sections.forEach(section => observer.observe(section));
  }

  const searchInput = document.querySelector('#blog-search');
  const chips = document.querySelectorAll('.chip');
  const cards = document.querySelectorAll('[data-card]');
  const emptyState = document.querySelector('#no-results');

  const applyFilters = () => {
    const query = (searchInput?.value || '').toLowerCase().trim();
    const activeChip = document.querySelector('.chip.active');
    const category = activeChip?.dataset.cat || 'all';

    let visible = 0;

    cards.forEach(card => {
      const text = (card.dataset.search || '').toLowerCase();
      const cardCategory = card.dataset.cat || '';

      const categories = cardCategory.split(/\s+/).filter(Boolean);
      const show =
        (!query || text.includes(query)) &&
        (category === 'all' || categories.includes(category));

      card.hidden = !show;

      if (show) visible += 1;
    });

    if (emptyState) {
      emptyState.hidden = visible !== 0;
    }
  };

  if (searchInput) {
    searchInput.addEventListener('input', applyFilters);
  }

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      chips.forEach(item => {
        item.classList.remove('active');
        item.setAttribute('aria-pressed', 'false');
      });

      chip.classList.add('active');
      chip.setAttribute('aria-pressed', 'true');

      applyFilters();
    });

    chip.setAttribute(
      'aria-pressed',
      chip.classList.contains('active') ? 'true' : 'false'
    );
  });

  const hashToCategory = {
    '#cat-clustering': 'clustering',
    '#cat-stats': 'stats',
    '#cat-lifecycle': 'lifecycle',
    '#cat-strategy': 'strategy'
  };

  const requestedCategory = hashToCategory[window.location.hash];

  if (requestedCategory) {
    const requestedChip = document.querySelector(`.chip[data-cat="${requestedCategory}"]`);

    if (requestedChip) {
      chips.forEach(item => {
        item.classList.remove('active');
        item.setAttribute('aria-pressed', 'false');
      });

      requestedChip.classList.add('active');
      requestedChip.setAttribute('aria-pressed', 'true');
    }
  }

  applyFilters();

  document.querySelectorAll('form[data-email-submit]').forEach(form => {
    form.addEventListener('submit', event => {
      event.preventDefault();

      const formData = new FormData(form);
      const name = String(formData.get('name') || '').trim();
      const email = String(formData.get('email') || '').trim();
      const topic = String(formData.get('topic') || 'General question').trim();
      const message = String(formData.get('message') || '').trim();
      const subject = encodeURIComponent('[StreamScope] ' + topic);
      const body = encodeURIComponent(
        'Name: ' + name + '\n' +
        'Email: ' + email + '\n' +
        'Topic: ' + topic + '\n\n' +
        message
      );

      const status = form.querySelector('.form-status');
      if (status) {
        status.textContent = 'Your email app will open with this message prepared. Please send it to complete delivery.';
        status.classList.add('show', 'ok');
      }

      window.location.href =
        'mailto:sailee.gore23@pccoepune.org?subject=' + subject + '&body=' + body;
    });
  });

  document.querySelectorAll('[data-copy-link]').forEach(button => {
    button.addEventListener('click', async () => {
      const original =
        button.getAttribute('aria-label') || 'Copy link';

      try {
        await navigator.clipboard.writeText(window.location.href);

        button.setAttribute('aria-label', 'Copied!');
        button.setAttribute('title', 'Copied!');
      } catch (_) {
        button.setAttribute('aria-label', 'Copy failed');
        button.setAttribute('title', 'Copy failed');
      }

      setTimeout(() => {
        button.setAttribute('aria-label', original);
        button.setAttribute('title', original);
      }, 1500);
    });
  });
});

'''


# ============================================================
# SHARED PAGE SHELL
# ============================================================

FOOTER = r'''

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="/" class="brand" style="margin-bottom:12px;">
          <svg class="brand-mark" viewBox="0 0 30 30" fill="none"
               xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <rect x="2" y="16" width="4" height="12" rx="1" fill="#1E8F79"/>
            <rect x="9" y="9" width="4" height="19" rx="1" fill="#1F2A44"/>
            <rect x="16" y="2" width="4" height="26" rx="1" fill="#D98F31"/>
            <rect x="23" y="12" width="4" height="16" rx="1" fill="#1F2A44"/>
          </svg>
          <span>StreamScope</span>
        </a>
        <p>
          A blog working through real data analytics case studies —
          statistics, hypothesis testing, and clustering, explained for
          people who'll use the findings, not just study them.
        </p>
      </div>

      <div>
        <h5>Navigate</h5>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/blog">Blog</a></li>
          <li><a href="/about">About</a></li>
          <li><a href="/contact">Contact</a></li>
        </ul>
      </div>

      <div>
        <h5>Topics</h5>
        <ul>
          <li><a href="/blog#cat-lifecycle">Analytics Life Cycle</a></li>
          <li><a href="/blog#cat-stats">Statistical Methods</a></li>
          <li><a href="/blog#cat-clustering">Clustering &amp; ML</a></li>
          <li><a href="/blog#cat-strategy">Business Strategy</a></li>
        </ul>
      </div>

      <div>
        <h5>Featured</h5>
        <ul>
          <li><a href="/article">Decoding the Playlist</a></li>
        </ul>
      </div>
    </div>

    <div class="footer-bottom">
      <span>
        © 2026 StreamScope. All figures in this post are illustrative academic examples.
      </span>
      <span>
        Built for the Data Analytics &amp; Visualization coursework portfolio.
      </span>
    </div>
  </div>
</footer>

'''
ARTICLE_FOOTER = r'''

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-bottom" style="border-top:none;padding-top:0;">
      <span>
        © 2026 StreamScope. All figures in this post are illustrative academic examples.
      </span>
      <a href="/" style="font-weight:600;color:var(--teal-deep);">
        Back to homepage →
      </a>
    </div>
  </div>
</footer>

'''

HEADER_CTA = {
    "home": "Browse posts",
    "blog": "Suggest a dataset",
    "article": "All posts",
    "about": "Read the blog",
    "contact": "Read the blog",
}

NAV_ITEMS = (
    ("home", "/", "Home"),
    ("blog", "/blog", "Blog"),
    ("about", "/about", "About"),
    ("contact", "/contact", "Contact"),
)

HEADER_TEMPLATE = r"""
<header class="site-header">
  <div class="wrap header-inner">
    <a href="/" class="brand">
      <svg class="brand-mark" viewBox="0 0 30 30" fill="none"
           xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <rect x="2" y="16" width="4" height="12" rx="1" fill="#1E8F79"/>
        <rect x="9" y="9" width="4" height="19" rx="1" fill="#1F2A44"/>
        <rect x="16" y="2" width="4" height="26" rx="1" fill="#D98F31"/>
        <rect x="23" y="12" width="4" height="16" rx="1" fill="#1F2A44"/>
      </svg>
      <span>StreamScope<small>MUSIC LISTENING ANALYTICS</small></span>
    </a>

    <nav class="main-nav" id="main-nav" aria-label="Primary navigation">
      {nav_links}
    </nav>

    <div class="header-actions">
      <a href="/blog" class="btn btn-outline btn-sm">
        {cta_text}
      </a>
    </div>

    <button class="nav-toggle"
            type="button"
            aria-label="Toggle navigation"
            aria-expanded="false"
            aria-controls="main-nav">
      <span></span>
    </button>
  </div>
</header>
"""

def build_header(active_page: str) -> str:
    """Build the shared navigation with one active item."""
    nav_links = []

    for route_name, href, label in NAV_ITEMS:
        active = ' class="active"' if route_name == active_page else ""
        nav_links.append(
            f'<a href="{href}" data-route="{route_name}"{active}>{label}</a>'
        )

    return HEADER_TEMPLATE.format(
        nav_links="\n      ".join(nav_links),
        cta_text=HEADER_CTA.get(active_page, "Browse posts"),
    )



# ============================================================
# PAGE CONTENT
# ============================================================

PAGE_HOME = r'''
<main>
<!-- HERO -->
<section class="hero">
<div class="wrap hero-grid">
<div class="hero-copy">
<span class="eyebrow">MUSIC LISTENING ANALYTICS</span>
<h1>Discover listening patterns. Understand listener segments.</h1>
<p style="font-size:0.82rem;letter-spacing:0.02em;color:var(--muted-2);margin-top:-4px;">Data, Decoded — project portfolio</p>
<p class="lede">Case studies that follow real data analytics work end to end — from a messy business question, through statistics and clustering, to a recommendation a team could actually ship.</p>
<div class="hero-actions">
<a class="btn btn-primary" href="/article">Read the latest case study</a>
<a class="btn btn-outline" href="/blog">Browse all posts</a>
</div>
<div class="hero-meta">
<div>
<div class="num">240</div>
<div class="lbl">listener profiles analyzed</div>
</div>
<div>
<div class="num">4</div>
<div class="lbl">listener segments uncovered</div>
</div>
<div>
<div class="num">3</div>
<div class="lbl">methods applied — stats, testing, clustering</div>
</div>
</div>
</div>
<div aria-hidden="true" class="hero-art">
<svg style="width:100%;height:auto;" viewbox="0 0 460 420" xmlns="http://www.w3.org/2000/svg">
<circle cx="230" cy="210" fill="#1F2A44" opacity="0.04" r="190"></circle>
<g stroke="#DFDAC9" stroke-width="1">
<line x1="40" x2="420" y1="340" y2="340"></line>
<line x1="40" x2="40" y1="60" y2="340"></line>
</g>
<!-- scatter clusters -->
<g>
<circle cx="110" cy="290" fill="#1E8F79" opacity="0.85" r="7"></circle>
<circle cx="95" cy="270" fill="#1E8F79" opacity="0.85" r="6"></circle>
<circle cx="130" cy="300" fill="#1E8F79" opacity="0.85" r="5"></circle>
<circle cx="105" cy="250" fill="#1E8F79" opacity="0.85" r="6"></circle>
<circle cx="140" cy="270" fill="#1E8F79" opacity="0.7" r="6"></circle>
<circle cx="230" cy="150" fill="#D98F31" opacity="0.9" r="8"></circle>
<circle cx="255" cy="175" fill="#D98F31" opacity="0.85" r="6"></circle>
<circle cx="210" cy="180" fill="#D98F31" opacity="0.75" r="5"></circle>
<circle cx="245" cy="120" fill="#D98F31" opacity="0.85" r="6"></circle>
<circle cx="270" cy="150" fill="#D98F31" opacity="0.8" r="7"></circle>
<circle cx="340" cy="240" fill="#1F2A44" opacity="0.85" r="7"></circle>
<circle cx="365" cy="215" fill="#1F2A44" opacity="0.8" r="6"></circle>
<circle cx="320" cy="210" fill="#1F2A44" opacity="0.75" r="5"></circle>
<circle cx="355" cy="270" fill="#1F2A44" opacity="0.8" r="6"></circle>
<circle cx="180" cy="90" fill="#8A8F98" opacity="0.6" r="5"></circle>
<circle cx="200" cy="70" fill="#8A8F98" opacity="0.6" r="6"></circle>
<circle cx="165" cy="65" fill="#8A8F98" opacity="0.6" r="4"></circle>
</g>
<text fill="#8A8F98" font-family="IBM Plex Mono" font-size="11" x="40" y="365">daily minutes</text>
<text fill="#8A8F98" font-family="IBM Plex Mono" font-size="11" transform="rotate(-90 20 60)" x="20" y="60">genre diversity</text>
</svg>
</div>
</div>
</section>
<!-- FEATURED -->
<section>
<div class="wrap">
<div class="section-head">
<h2>Featured case study</h2>
<a class="see-all" href="/blog">All posts →</a>
</div>
<div class="card-grid">
<article class="article-card featured"
    data-card=""
    data-cat="clustering"
    data-search="decoding the playlist music streaming clustering segmentation kmeans hypothesis testing descriptive statistics">
<div class="card-media">
<img alt="K-Means clustering scatter plot of listeners by daily minutes and genre diversity, showing four coloured clusters" loading="eager" src="/assets/image5.png"/>
</div>
<div class="card-body">
<span class="card-cat">Clustering &amp; Machine Learning</span>
<h3><a href="/article">Decoding the Playlist: How Data Analytics Reveals the Way We Really Listen to Music</a></h3>
<p class="card-excerpt">A streaming platform's usage logs hide four distinct listener types. Here's how descriptive statistics, hypothesis testing, and K-Means clustering surface them — and what each segment means for the product.</p>
<div class="card-meta">
<span>Sailee Dilip Gore</span><span class="dot"></span><span>Aug 28, 2026</span><span class="dot"></span><span>12 min read</span>
</div>
</div>
</article>
</div>
</div>
</section>
<!-- CATEGORIES -->
<section class="band">
<div class="wrap">
<div class="section-head">
<h2>Explore by topic</h2>
<a class="see-all" href="/blog" style="color:#fff;">View blog →</a>
</div>
<div class="cat-grid">
<a class="cat-tile" href="/blog#cat-lifecycle" style="background:rgba(255,255,255,0.05);border-color:rgba(255,255,255,0.15);">
<div class="n" style="color:rgba(255,255,255,0.5)">01</div>
<h4 style="color:#fff;">Data Analytics Life Cycle</h4>
</a>
<a class="cat-tile" href="/blog#cat-stats" style="background:rgba(255,255,255,0.05);border-color:rgba(255,255,255,0.15);">
<div class="n" style="color:rgba(255,255,255,0.5)">02</div>
<h4 style="color:#fff;">Statistical Methods</h4>
</a>
<a class="cat-tile" href="/blog#cat-clustering" style="background:rgba(255,255,255,0.05);border-color:rgba(255,255,255,0.15);">
<div class="n" style="color:rgba(255,255,255,0.5)">03</div>
<h4 style="color:#fff;">Clustering &amp; Machine Learning</h4>
</a>
<a class="cat-tile" href="/blog#cat-strategy" style="background:rgba(255,255,255,0.05);border-color:rgba(255,255,255,0.15);">
<div class="n" style="color:rgba(255,255,255,0.5)">04</div>
<h4 style="color:#fff;">Business Strategy</h4>
</a>
</div>
</div>
</section>
<!-- NEWSLETTER -->
<section>
<div class="wrap">
<div class="newsletter">
<div>
<h2>Get the next case study by email</h2>
<p>No spam, no drip campaign — just a note when a new analysis goes up.</p>
</div>
<div>
<form class="nl-form" data-fake-submit="" data-success-message="You're on the list — thanks for subscribing.">
<input aria-label="Email address" placeholder="you@email.com" required="" type="email"/>
<button class="btn btn-teal" style="background:#fff;color:var(--teal-deep);" type="submit">Subscribe</button>
</form>
<p class="nl-note form-status" style="color:#fff;"></p>
</div>
</div>
</div>
</section>
</main>
'''
PAGE_BLOG = r'''
<main>
<div class="wrap listing-head">
<span class="eyebrow">The archive</span>
<h1>All case studies</h1>
<p class="lede" style="max-width:56ch;">Every post here follows the same discipline: frame the business question first, then let descriptive statistics, testing, and modelling answer it — no step skipped.</p>
</div>

<div class="wrap">
<div class="filter-bar">
<div class="chip-row">
<button class="chip active" data-cat="all">All posts</button>
<button class="chip" data-cat="clustering" id="cat-clustering">Clustering &amp; ML</button>
<button class="chip" data-cat="stats" id="cat-stats">Statistical Methods</button>
<button class="chip" data-cat="lifecycle" id="cat-lifecycle">Analytics Life Cycle</button>
<button class="chip" data-cat="strategy" id="cat-strategy">Business Strategy</button>
</div>
<div class="search-box">
<svg fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><line x1="21" x2="16.65" y1="21" y2="16.65"></line></svg>
<input aria-label="Search posts" id="blog-search" placeholder="Search posts…" type="text"/>
</div>
</div>

<div class="card-grid blog-post-grid">

<article class="article-card" 
data-card="" 
data-cat="lifecycle" 
data-search="data analytics life cycle discovery data preparation model planning model building communicate results operationalize analytics lifecycle">
<div class="card-media">
<img alt="Data analytics life cycle diagram showing discovery, data preparation, model planning, model building, communication and operationalization" loading="lazy" src="/assets/image1.png"/>
</div>
<div class="card-body">
<span class="card-cat">Analytics Life Cycle</span>
<h3><a href="/article#lifecycle">From Business Question to Action: The Data Analytics Life Cycle</a></h3>
<p class="card-excerpt">A practical walkthrough of the analytics life cycle — from discovery and data preparation through modelling, communication, and operationalization.</p>
<div class="card-meta">
<span>StreamScope</span><span class="dot"></span><span>Aug 28, 2026</span><span class="dot"></span><span>8 min read</span>
</div>
</div>
</article>

<article class="article-card" data-card="" data-cat="stats" data-search="statistical methods subscription daily listening time free premium average statistics descriptive statistics music streaming">
<div class="card-media">
<img alt="Bar chart comparing average daily listening time for free and premium listeners" loading="lazy" src="/assets/image2.png"/>
</div>
<div class="card-body">
<span class="card-cat">Statistical Methods</span>
<h3><a href="/article#descriptive-stats">What the Summary Statistics Reveal About Listening Habits</a></h3>
<p class="card-excerpt">Start with the basics: means, distributions, and group comparisons that turn raw listener records into a clear statistical picture.</p>
<div class="card-meta">
<span>StreamScope</span><span class="dot"></span><span>Aug 28, 2026</span><span class="dot"></span><span>7 min read</span>
</div>
</div>
</article>

<article class="article-card" data-card="" data-cat="stats" data-search="hypothesis testing t-test p-value free premium skip rate statistical testing significance music streaming">
<div class="card-media">
<img alt="Box plot comparing skip-rate distributions for free and premium listeners" loading="lazy" src="/assets/image3.png"/>
</div>
<div class="card-body">
<span class="card-cat">Statistical Methods</span>
<h3><a href="/article#hypothesis-testing">Does Subscription Type Really Change Listener Behaviour?</a></h3>
<p class="card-excerpt">Use hypothesis testing to separate a visible difference from a statistically meaningful one, with a two-sample t-test as the lens.</p>
<div class="card-meta">
<span>StreamScope</span><span class="dot"></span><span>Aug 28, 2026</span><span class="dot"></span><span>6 min read</span>
</div>
</div>
</article>

<article class="article-card" data-card="" data-cat="clustering" data-search="k-means elbow method model selection within cluster sum squares clustering machine learning k four">
<div class="card-media">
<img alt="Elbow method chart showing the within-cluster sum of squares flattening after four clusters" loading="lazy" src="/assets/image4.png"/>
</div>
<div class="card-body">
<span class="card-cat">Clustering &amp; Machine Learning</span>
<h3><a href="/article#elbow">Choosing the Right Number of Listener Segments</a></h3>
<p class="card-excerpt">See how the elbow method helps choose a practical K for K-Means instead of selecting the number of clusters by guesswork.</p>
<div class="card-meta">
<span>StreamScope</span><span class="dot"></span><span>Aug 28, 2026</span><span class="dot"></span><span>6 min read</span>
</div>
</div>
</article>

<article class="article-card" data-card="" data-cat="clustering" data-search="decoding the playlist k-means listener segmentation genre loyalists playlist hoppers night owl explorers casual listeners">
<div class="card-media">
<img alt="K-Means clustering scatter plot of listeners by daily minutes and genre diversity, showing four coloured clusters" loading="lazy" src="/assets/image5.png"/>
</div>
<div class="card-body">
<span class="card-cat">Clustering &amp; Machine Learning</span>
<h3><a href="/article#segments">Decoding the Playlist: How Data Analytics Reveals the Way We Really Listen to Music</a></h3>
<p class="card-excerpt">Bring the full workflow together to uncover four distinct listener segments and show how clustering turns behavioural data into interpretable groups.</p>
<div class="card-meta">
<span>Sailee Dilip Gore</span><span class="dot"></span><span>Aug 28, 2026</span><span class="dot"></span><span>12 min read</span>
</div>
</div>
</article>

<article class="article-card" data-card="" data-cat="strategy" data-search="business strategy listener segments product strategy marketing strategy recommendation engine retention personalization business insights recommendations">
<div class="card-media strategy-card-media" role="img" aria-label="Business strategy map connecting listener segments to product, retention, recommendation, and marketing actions">
<svg class="strategy-visual" viewBox="0 0 900 520" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<rect width="900" height="520" fill="#141B2E"/>
<g opacity=".18" stroke="#DFDAC9" stroke-width="1">
<path d="M40 100H860M40 200H860M40 300H860M40 400H860"/>
<path d="M160 40V480M320 40V480M480 40V480M640 40V480M800 40V480"/>
</g>
<circle cx="450" cy="255" r="92" fill="#1E8F79" opacity=".18" stroke="#1E8F79" stroke-width="2"/>
<text x="450" y="244" text-anchor="middle" fill="#fff" font-family="IBM Plex Sans, sans-serif" font-size="24" font-weight="600">Listener</text>
<text x="450" y="277" text-anchor="middle" fill="#fff" font-family="IBM Plex Sans, sans-serif" font-size="24" font-weight="600">Segmentation</text>
<g fill="#F6F4EF" font-family="IBM Plex Sans, sans-serif">
<rect x="72" y="62" width="210" height="88" rx="12" fill="#1F2A44" stroke="#DFDAC9"/>
<text x="177" y="96" text-anchor="middle" font-size="16" font-weight="600">Genre Loyalists</text>
<text x="177" y="122" text-anchor="middle" font-size="13" fill="#B8C0CC">Loyalty &amp; catalog depth</text>

<rect x="618" y="62" width="210" height="88" rx="12" fill="#1F2A44" stroke="#DFDAC9"/>
<text x="723" y="96" text-anchor="middle" font-size="16" font-weight="600">Playlist Hoppers</text>
<text x="723" y="122" text-anchor="middle" font-size="13" fill="#B8C0CC">Discovery &amp; skip friction</text>

<rect x="72" y="350" width="210" height="88" rx="12" fill="#1F2A44" stroke="#DFDAC9"/>
<text x="177" y="384" text-anchor="middle" font-size="16" font-weight="600">Night-Owl Explorers</text>
<text x="177" y="410" text-anchor="middle" font-size="13" fill="#B8C0CC">Late-night niche growth</text>

<rect x="618" y="350" width="210" height="88" rx="12" fill="#1F2A44" stroke="#DFDAC9"/>
<text x="723" y="384" text-anchor="middle" font-size="16" font-weight="600">Casual Listeners</text>
<text x="723" y="410" text-anchor="middle" font-size="13" fill="#B8C0CC">Re-engagement &amp; conversion</text>
</g>
<g stroke="#1E8F79" stroke-width="3" fill="none" stroke-linecap="round">
<path d="M282 150L388 225"/>
<path d="M618 150L512 225"/>
<path d="M282 350L388 285"/>
<path d="M618 350L512 285"/>
</g>
<g fill="#D98F31" font-family="IBM Plex Mono, monospace" font-size="12">
<text x="450" y="470" text-anchor="middle">INSIGHT → ACTION → MEASUREMENT</text>
</g>
</svg>
</div>
<div class="card-body">
<span class="card-cat">Business Strategy</span>
<h3><a href="/article#recommendations">Turning Listener Segments into Product Strategy</a></h3>
<p class="card-excerpt">Translate four behavioural segments into practical product, retention, recommendation, and marketing actions — the prescriptive layer of the analysis.</p>
<div class="card-meta">
<span>StreamScope</span><span class="dot"></span><span>Aug 28, 2026</span><span class="dot"></span><span>7 min read</span>
</div>
</div>
</article>

<div class="more-soon" id="no-results" hidden style="grid-column:1/-1;">
<h3 style="margin-bottom:8px;">No posts match that search</h3>
<p style="margin:0;">Try a different keyword, or clear the category filter.</p>
</div>

</div>
</div>
</main>
'''
PAGE_ARTICLE = r'''
<main>
<div class="wrap article-hero">
<span class="eyebrow">Clustering &amp; Machine Learning</span>
<h1 style="max-width:20ch;">Decoding the Playlist</h1>
<p class="lede" style="max-width:56ch;">How data analytics reveals the way we really listen to music — a case study on segmenting music-streaming listeners using descriptive statistics, hypothesis testing, and K-Means clustering.</p>
<div class="meta-row">
<div class="author-chip">
<div class="author-avatar">SG</div>
<div>
<div style="font-weight:600;color:var(--ink-soft);">Sailee Dilip Gore</div>
</div>
</div>
<span>·</span>
<span>August 28, 2026</span>
<span>·</span>
<span>12 min read</span>
</div>
<div class="article-featured-media">
<img alt="K-Means clustering of listeners plotted by daily minutes and genre diversity, showing four coloured clusters" loading="lazy" src="/assets/image5.png"/>
</div>
</div>
<div class="wrap" style="padding-top:40px;">
<div class="article-layout">
<!-- share rail -->
<div class="col-share">
<div class="share-rail">
<button aria-label="Copy link" class="share-btn" data-copy-link="" title="Copy link">
<svg fill="none" height="16" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="16"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
</button>
<a aria-label="Share on X" class="share-btn" href="https://twitter.com/intent/tweet?text=Decoding%20the%20Playlist" rel="noopener" target="_blank">
<svg fill="currentColor" height="15" viewbox="0 0 24 24" width="15"><path d="M18.9 2H22l-7.6 8.7L23 22h-6.9l-5.4-6.9L4.3 22H1l8.1-9.3L1.3 2h7.1l4.9 6.3L18.9 2Z"></path></svg>
</a>
<a aria-label="Share on LinkedIn" class="share-btn" href="https://www.linkedin.com/sharing/share-offsite/?url=" rel="noopener" target="_blank">
<svg fill="currentColor" height="15" viewbox="0 0 24 24" width="15"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05C20.9 8.65 22 11 22 14.5V21h-4v-5.8c0-1.4 0-3.2-1.95-3.2s-2.25 1.5-2.25 3.1V21H9z"></path></svg>
</a>
</div>
</div>
<!-- article body -->
<article class="article-body">
<h2 id="business-problem">1. The Business Problem</h2>
<p>It's 11 p.m. and a listener opens a music-streaming app hoping for something that fits the moment — but the home screen shows the same "Today's Top Hits" playlist it showed at 8 a.m. Within thirty seconds, three songs are skipped and the app is closed.</p>
<p>Multiply that moment across millions of daily sessions and a real business problem emerges: streaming platforms generate enormous volumes of behavioural data — listening duration, skips, saves, replay patterns, time-of-day habits — yet most still recommend music as if every listener behaves the same way.</p>
<p>Generic, one-size-fits-all recommendations quietly hurt the business in three ways: listeners disengage faster, free-tier users convert to paid subscriptions less often, and marketing campaigns waste budget by treating a casual weekend listener the same as a late-night genre explorer. The core question this case study investigates is simple to ask but hard to answer without data:</p>
<blockquote>Can a streaming platform use analytics to discover natural listener "types" hidden inside its usage data, and use that understanding to personalize the experience for each type?</blockquote>
<p>This is precisely where data analytics and visualization earns its place in the business — not as a reporting exercise, but as the engine that turns raw click-and-skip logs into a segmentation strategy the product and marketing teams can act on.</p>
<h2 id="right-lens">2. Why Data Analytics Is the Right Lens for This Problem</h2>
<p>Streaming platforms already collect the data needed to solve this problem — the gap isn't data availability, it's interpretation. Data analytics matters here for three concrete reasons:</p>
<ul>
<li><strong>It moves the business from guessing to evidence.</strong> Instead of assuming "users like variety," statistical summaries reveal what proportion actually do.</li>
<li><strong>It enables personalization at scale.</strong> Once distinct listener groups are identified, product and marketing decisions can be tailored to each group rather than to a mythical "average user."</li>
<li><strong>It directly protects revenue.</strong> Engaged listeners churn less, upgrade to premium more often, and generate more ad impressions on the free tier — so understanding what drives engagement has a measurable financial payoff.</li>
</ul>
<p>The rest of this post walks through exactly how that's done — starting with foundational analytics concepts, moving into statistical methods, and finishing with the clustering technique that ultimately answers the business question.</p>
<h2 id="foundation">3. Laying the Foundation: Introduction to Data Analytics</h2>
<h3 id="four-types">3.1 The Four Types of Analytics, Applied to Music Streaming</h3>
<p>Before touching any data, it helps to place this problem within the four classic categories of analytics:</p>
<ul>
<li><strong>Descriptive Analytics</strong> — What is happening? Summarises how long people listen, how often they skip, and how many genres they explore.</li>
<li><strong>Diagnostic Analytics</strong> — Why is it happening? Hypothesis tests and correlation analysis explain whether factors like subscription type actually drive behaviour differences.</li>
<li><strong>Predictive Analytics</strong> — What is likely to happen next? Once segments are known, predictive models could estimate churn risk or the next skip.</li>
<li><strong>Prescriptive Analytics</strong> — What should we do about it? Segment-specific recommendations, covered in Section 8, turn insight into action.</li>
</ul>
<p>This case study focuses on descriptive and diagnostic analytics, and lays the groundwork for predictive and prescriptive work through clustering.</p>
<h3 id="lifecycle">3.2 The Data Analytics Life Cycle Applied to This Case</h3>
<p>Every analytics project benefits from a structured life cycle rather than jumping straight to modelling. The six phases below structured this study end to end.</p>
<figure>
<img alt="Data analytics life cycle diagram: Discovery, Data Preparation, Model Planning, Model Building, Communicate Results, Operationalize" src="/assets/image1.png"/>
<figcaption>The six-phase data analytics life cycle used to structure this project.</figcaption>
</figure>
<ul>
<li><strong>Discovery</strong> — Framed the business problem and identified the core question: do meaningfully different listener types exist within the usage data?</li>
<li><strong>Data Preparation</strong> — Defined five behavioural features per listener, cleaned unrealistic values (e.g. negative minutes), and standardised units.</li>
<li><strong>Model Planning</strong> — Selected descriptive statistics and an independent-samples t-test for diagnosis, and K-Means clustering — an unsupervised method, since no "correct" listener label exists.</li>
<li><strong>Model Building</strong> — Computed statistics, ran the t-test and correlation analysis, standardised features, and fit K-Means with the elbow method to choose the number of clusters.</li>
<li><strong>Communicate Results</strong> — Translated every statistic and cluster into a plain-language business insight using charts.</li>
<li><strong>Operationalize</strong> — Proposed how the segmentation would be deployed into the recommendation engine and refreshed periodically.</li>
</ul>
<h2 id="data-preparation">4. Data and Preparation</h2>
<p>For this academic demonstration, a representative dataset of 240 listener profiles was constructed to illustrate how a real streaming platform's engagement logs would be analysed. The five behavioural features below were chosen because each captures a different dimension of listening behaviour — volume, patience, variety, timing, and intent to keep music for later.</p>
<table>
<thead><tr><th>Feature</th><th>Description</th><th>Type / unit</th></tr></thead>
<tbody>
<tr><td>Daily minutes</td><td>Average minutes of music streamed per day</td><td>Continuous (minutes)</td></tr>
<tr><td>Skip rate pct</td><td>Percentage of songs skipped before 30 seconds</td><td>Continuous (%)</td></tr>
<tr><td>Genre diversity index</td><td>Number of distinct genres regularly played (weighted)</td><td>Continuous (1–6)</td></tr>
<tr><td>Peak listening hour</td><td>Hour of day (24-hr) with the most listening activity</td><td>Continuous (0–23)</td></tr>
<tr><td>Songs saved per month</td><td>Songs added to a personal playlist or library per month</td><td>Continuous (count)</td></tr>
<tr><td>Subscription type</td><td>Free (ad-supported) or Premium account</td><td>Categorical</td></tr>
</tbody>
</table>
<p>During preparation, implausible values (negative listening minutes, skip rates above 100%) were clipped to realistic bounds. All five numeric features were later standardized (z-scored) before clustering, since K-Means is distance-based — features measured in very different units (minutes versus percentages versus an index) would otherwise unfairly dominate the distance calculation.</p>
<div class="callout amber">
<span class="callout-label">A note on the data</span>
<p>All numerical values and charts in this post are illustrative, generated to demonstrate the data analytics life cycle, statistical methods, and clustering. They should not be interpreted as data from any real streaming organization.</p>
</div>
<h2 id="statistical-analysis">5. Statistical Analysis: Basic Data Analytical Methods</h2>
<h3 id="descriptive-stats">5.1 Descriptive Statistics</h3>
<p>Descriptive statistics give the first honest picture of listener behaviour before any modelling begins. Across the 240 profiles:</p>
<div class="stat-card-row">
<div class="stat-card"><div class="v">83.5 min</div><div class="l">Mean daily listening</div></div>
<div class="stat-card"><div class="v">18.5%</div><div class="l">Mean skip rate</div></div>
<div class="stat-card"><div class="v">2.9</div><div class="l">Mean genre diversity index</div></div>
<div class="stat-card"><div class="v">29.8</div><div class="l">Mean songs saved / month</div></div>
</div>
<table>
<thead><tr><th>Metric</th><th>Mean</th><th>Median</th><th>Std. dev.</th><th>Min</th><th>Max</th></tr></thead>
<tbody>
<tr><td>Daily listening (min)</td><td>83.5</td><td>87.8</td><td>30.2</td><td>15.0</td><td>139.7</td></tr>
<tr><td>Skip rate (%)</td><td>18.5</td><td>15.7</td><td>10.1</td><td>1.0</td><td>45.6</td></tr>
<tr><td>Genre diversity index</td><td>2.9</td><td>2.7</td><td>0.9</td><td>1.0</td><td>5.2</td></tr>
<tr><td>Songs saved / month</td><td>29.8</td><td>31.2</td><td>19.7</td><td>0.0</td><td>70.5</td></tr>
</tbody>
</table>
<p>The average listener streams about 83.5 minutes a day, but a standard deviation of 30.2 minutes shows this figure hides very different behaviours — some listeners barely open the app while others stream for well over two hours. The skip rate tells a similar story: a mean of 18.5% sits above the median of 15.7%, meaning a subset of heavy skippers is pulling the average upward while most listeners skip far less. This spread is exactly the kind of signal that motivates going beyond averages into clustering in Section 6.</p>
<h3 id="hypothesis-testing">5.2 Hypothesis Testing: Does Subscription Type Change Skip Behaviour?</h3>
<p>A common product assumption is that free (ad-supported) listeners skip more because ads interrupt the listening flow. This was tested formally with an independent two-sample t-test comparing the mean skip rate of Free versus Premium listeners.</p>
<table>
<thead><tr><th>Group</th><th>Mean skip rate (%)</th><th>n</th></tr></thead>
<tbody>
<tr><td>Free (ad-supported)</td><td>19.16</td><td>96</td></tr>
<tr><td>Premium</td><td>18.09</td><td>144</td></tr>
</tbody>
</table>
<p class="stat-figure" style="color:var(--muted);font-size:0.9rem;">t = 0.79, p = 0.428 (two-tailed, unequal variances)</p>
<div class="callout">
<span class="callout-label">Finding</span>
<p>Since p is far above the conventional 0.05 threshold, the difference is not statistically significant — subscription type alone does not explain skip behaviour. This redirects the business away from an ad-related fix and toward the idea that skip behaviour is driven by something else, most likely the listener's underlying taste profile — exactly what the clustering in Section 6 goes on to uncover.</p>
</div>
<h3 id="correlation">5.3 Correlation Analysis</h3>
<p>A correlation check across the four numeric features surfaces two relationships worth acting on: skip rate correlates negatively with songs saved per month (r ≈ −0.66), meaning listeners who skip less tend to curate their libraries more — a strong proxy for genuine engagement. Daily listening time correlates positively with songs saved (r ≈ 0.73), reinforcing that time spent and intentional curation move together. Genre diversity shows only a weak relationship with daily minutes (r ≈ 0.05), suggesting that exploring many genres and simply listening a lot are largely independent behaviours — an early hint that more than one type of "heavy listener" exists.</p>
<h3 id="visualising">5.4 Visualising the Statistical Findings</h3>
<figure>
<img alt="Bar chart comparing average daily listening time by subscription type: Free 81.0 minutes vs Premium 79.4 minutes" src="/assets/image2.png"/>
<figcaption>Average daily listening time by subscription type — both groups listen for a similar duration.</figcaption>
</figure>
<figure>
<img alt="Box plot comparing skip-rate distribution for Free versus Premium listeners, showing nearly identical medians and spreads" src="/assets/image3.png"/>
<figcaption>Skip-rate distribution for Free vs Premium listeners — medians and spreads are nearly identical, visually confirming the t-test result.</figcaption>
</figure>
<p>Both charts communicate the same conclusion the numbers already suggested: subscription tier is not a useful predictor of engagement on its own. This is descriptive statistics and visualization working together — the numbers establish the finding, and the chart makes it instantly credible to a non-technical stakeholder.</p>
<h2 id="clustering">6. Advanced Analytics: Discovering Listener Segments with Clustering</h2>
<p>Section 5 showed that averages and simple group comparisons (Free vs Premium) don't explain listener behaviour — the real differences must be hiding along some other dimension. This is precisely the situation clustering is built for: an unsupervised method that groups similar data points together without being told in advance what the groups are or how many exist.</p>
<h3 id="why-kmeans">6.1 Why K-Means, and How It Works</h3>
<p>K-Means was chosen because it's fast, interpretable, and well suited to continuous behavioural features like the ones prepared in Section 4. The algorithm works iteratively: it places <em>k</em> random centroids in the feature space, assigns every listener to the nearest centroid using Euclidean distance, recalculates each centroid as the mean of the listeners assigned to it, and repeats this assignment-and-update cycle until the centroids stop moving. The distance between a listener's feature vector <em>x</em> and a centroid <em>c</em> is calculated as:</p>
<blockquote>distance(x, c) = √Σ(xᵢ − cᵢ)²</blockquote>
<p>Because this distance calculation is sensitive to scale, all five features were standardised (Section 4) before the algorithm was run.</p>
<h3 id="elbow">6.2 Choosing the Number of Clusters: The Elbow Method</h3>
<p>K-Means requires the number of clusters, <em>k</em>, to be decided in advance. The elbow method addresses this by running K-Means for several values of <em>k</em> and plotting the within-cluster sum of squares (WCSS) — the total squared distance between each listener and its assigned centroid — against <em>k</em>. WCSS always decreases as <em>k</em> grows, but the rate of improvement slows sharply once the "natural" number of groups has been found, creating a visible elbow.</p>
<figure>
<img alt="Elbow method chart: within-cluster sum of squares drops sharply up to k=4 and flattens afterward" src="/assets/image4.png"/>
<figcaption>Elbow method — WCSS drops sharply up to k = 4 and flattens afterward, confirming four listener segments.</figcaption>
</figure>
<p>The bend at k = 4 shows that adding a fifth or sixth cluster produces only marginal improvement, so four clusters was chosen as the number that best balances simplicity with explanatory power.</p>
<h3 id="segments">6.3 The Four Listener Segments</h3>
<figure>
<img alt="K-Means clustering of listeners plotted by daily minutes vs genre diversity, showing four visually distinct groups" src="/assets/image5.png"/>
<figcaption>K-Means clustering of listeners (daily minutes vs genre diversity) — four visually distinct groups emerge.</figcaption>
</figure>
<p style="font-size:0.9rem;color:var(--muted);font-style:italic;">Note: clustering was performed on all five standardised features; this chart plots only two for readability, so some colour overlap is expected — clusters that look close here can still be well separated once skip rate, peak hour, and songs saved are considered together, as the centroid table below confirms.</p>
<table>
<thead><tr><th>Segment</th><th>Listeners</th><th>Avg. min/day</th><th>Skip rate</th><th>Genre diversity</th><th>Peak hour</th><th>Saves/month</th></tr></thead>
<tbody>
<tr><td>Genre Loyalists</td><td>89 (37%)</td><td>108.4</td><td>11.4%</td><td>2.4</td><td>9 PM</td><td>48.5</td></tr>
<tr><td>Playlist Hoppers</td><td>60 (25%)</td><td>73.0</td><td>32.8%</td><td>3.7</td><td>3 PM</td><td>10.7</td></tr>
<tr><td>Night-Owl Explorers</td><td>27 (11%)</td><td>112.5</td><td>12.2%</td><td>3.6</td><td>2 AM</td><td>45.2</td></tr>
<tr><td>Casual Listeners</td><td>64 (27%)</td><td>46.5</td><td>17.7%</td><td>2.5</td><td>6 PM</td><td>15.3</td></tr>
</tbody>
</table>
<p>Interpreting the centroids turns four rows of numbers into a business-ready story. <strong>Genre Loyalists</strong> are the platform's most reliable engine of engagement — they listen the longest, skip the least, and save the most songs, but stay within a narrow genre comfort zone. <strong>Playlist Hoppers</strong> listen for a moderate time but skip more than any other group and save the fewest songs — they're the segment most at risk of disengaging entirely. <strong>Night-Owl Explorers</strong> are a small but extremely valuable niche: they listen the most of any group, explore a wide range of genres, and are highly active around 2 a.m., a time slot most platforms under-serve. <strong>Casual Listeners</strong> have the lowest overall engagement across every metric and represent the segment with the greatest room for growth.</p>
<h2 id="connecting">7. Connecting the Three Units into One Story</h2>
<p>The value of this project comes from how the three units build on each other rather than standing alone. The data analytics life cycle provided the process discipline — it made sure the business problem was framed clearly before any statistics were run, and that every later step had a defined purpose. Statistical methods then examined the data at the aggregate level: descriptive statistics revealed that averages hide huge variation, and the t-test ruled out an easy explanation (subscription tier) for that variation — but crucially, it couldn't say what the real explanation was. Clustering picked up exactly where that left off, using the same prepared features to uncover the four hidden listener types that the aggregate statistics had only hinted at.</p>
<h2 id="recommendations">8. Business Insights and Recommendations</h2>
<p>Each segment translates into a distinct, actionable strategy rather than a single generic recommendation:</p>
<ul>
<li><strong>Genre Loyalists</strong> — Reward loyalty with deeper catalog features: rare releases, artist-exclusive content, and "more like this" recommendations within their preferred genres, to protect this high-value group from complacency-driven churn.</li>
<li><strong>Playlist Hoppers</strong> — Redesign the first 15 seconds of recommended tracks and introduce a low-commitment "Discovery Mode" with shorter previews, since their high skip rate signals friction rather than disengagement.</li>
<li><strong>Night-Owl Explorers</strong> — Launch a curated late-night, cross-genre playlist and a sleep-timer feature around 2 a.m., turning an under-served time slot into a competitive advantage for this small but highly engaged niche.</li>
<li><strong>Casual Listeners</strong> — Trigger mood-based, low-effort playlist suggestions and re-engagement notifications, since their low engagement across every metric suggests they simply haven't found a strong content hook yet.</li>
</ul>
<p>At a platform level, this segmentation can directly power the recommendation engine's homepage logic, target push notifications more precisely, and give the marketing team four clear personas to design campaigns around — replacing guesswork with a data-driven operating model.</p>
<h2 id="limitations">9. Limitations and Challenges</h2>
<ul>
<li>The dataset used here is a small, illustrative simulation (240 profiles) built for academic demonstration, not a production-scale extract from a real platform.</li>
<li>K-Means assumes roughly spherical, similarly-sized clusters and requires <em>k</em> to be chosen in advance — the elbow method guides this choice but still involves some subjective judgement.</li>
<li>Behavioural features alone can't explain <em>why</em> a listener behaves a certain way; qualitative context (mood, life events, device type) is missing.</li>
<li>Listener behaviour isn't static — a Playlist Hopper today may become a Genre Loyalist next month, so clusters need periodic re-computation rather than a one-time label.</li>
<li>Using behavioural data for personalization raises legitimate privacy considerations that any real deployment would need to address transparently.</li>
</ul>
<h2 id="future-scope">10. Future Scope</h2>
<ul>
<li>Feed the four segments into a predictive model (e.g. logistic regression or gradient boosting) to estimate churn risk per listener — a natural extension into predictive analytics.</li>
<li>Enrich features with audio-level signals such as tempo, energy, and valence to capture taste more precisely than genre labels alone.</li>
<li>Move from a one-time clustering run to a streaming pipeline that re-clusters listeners weekly, so segments stay current as behaviour evolves.</li>
<li>A/B test segment-specific recommendation changes (e.g. the Discovery Mode for Playlist Hoppers) to measure actual impact on retention before full rollout.</li>
</ul>
<h2 id="conclusion">11. Conclusion</h2>
<p>This study set out to answer one question: can data analytics uncover meaningfully different listener types hidden inside a streaming platform's usage data, and turn that understanding into action? Following the data analytics life cycle gave the project structure; descriptive statistics and hypothesis testing proved that simple explanations like subscription tier weren't the real driver of behaviour; and K-Means clustering revealed four distinct, interpretable listener segments — Genre Loyalists, Playlist Hoppers, Night-Owl Explorers, and Casual Listeners — each requiring a different engagement strategy. The result is a segmentation model any streaming platform could plug directly into its recommendation and marketing systems, replacing a one-size-fits-all homepage with genuinely personalised experiences grounded in evidence rather than intuition.</p>
<h2 id="references">12. References</h2>
<ul style="color:var(--muted);font-size:0.92rem;">
<li>EMC Education Services. <em>Data Science and Big Data Analytics: Discovering, Analyzing, Visualizing and Presenting Data.</em> Wiley.</li>
<li>IBM. "What is Data Analytics?" IBM Data &amp; AI Learning Hub.</li>
<li>scikit-learn developers. "K-Means Clustering." scikit-learn documentation, scikit-learn.org.</li>
<li>Coursera / IBM Data Analyst Professional Certificate. "Introduction to Statistics and Hypothesis Testing."</li>
<li>Investopedia. "Correlation Coefficient: Formula and What It Tells Investors."</li>
<li>Course material: Data Analytics and Visualization (Minor in Data Science), Units I–III, Pimpri Chinchwad College of Engineering.</li>
</ul>
<div class="author-box">
<div class="author-avatar">SG</div>
<div>
<h4>Sailee Dilip Gore</h4>
<p>Author of this case study, written for the Data Analytics and Visualization coursework (Minor in Data Science), Pimpri Chinchwad College of Engineering.</p>
</div>
</div>
<div style="text-align:center;margin:48px 0 8px;">
<a class="btn btn-outline" href="/blog">← Back to all posts</a>
</div>
</article>
<!-- TOC -->
<div class="col-toc">
<nav aria-label="Table of contents" class="toc-nav">
<span class="toc-label">On this page</span>
<ol>
<li><a href="#business-problem">1. The Business Problem</a></li>
<li><a href="#right-lens">2. Why Data Analytics Fits</a></li>
<li><a href="#foundation">3. Laying the Foundation</a></li>
<li><a href="#data-preparation">4. Data and Preparation</a></li>
<li><a href="#statistical-analysis">5. Statistical Analysis</a></li>
<li><a href="#clustering">6. Clustering the Listeners</a></li>
<li><a href="#connecting">7. Connecting the Units</a></li>
<li><a href="#recommendations">8. Business Recommendations</a></li>
<li><a href="#limitations">9. Limitations</a></li>
<li><a href="#future-scope">10. Future Scope</a></li>
<li><a href="#conclusion">11. Conclusion</a></li>
<li><a href="#references">12. References</a></li>
</ol>
</nav>
</div>
</div>
</div>
</main>
'''
PAGE_ABOUT = r'''
<main>
<div class="wrap page-hero">
<span class="eyebrow">About this blog</span>
<h1 style="max-width:22ch;">Data analytics, worked through end to end — not just summarized.</h1>
</div>
<section>
<div class="wrap two-col">
<div>
<h2>Why this blog exists</h2>
<p>Most write-ups about data analytics stop at definitions: what descriptive analytics means, what clustering is, why the data analytics life cycle matters in theory. <strong>StreamScope</strong> takes a different approach — it starts with a real business question and follows one dataset through the entire process: framing the problem, preparing the data, running the statistics, testing assumptions, building a model, and turning the output into a recommendation someone could actually act on.</p>
<p>The first case study on this blog, <a href="/article" style="color:var(--teal-deep);font-weight:600;">Decoding the Playlist</a>, walks through how a music-streaming platform's behavioural data can be segmented into four listener types using descriptive statistics, hypothesis testing, and K-Means clustering — and what each type means for product and marketing decisions.</p>
<h2 style="margin-top:2em;">How each post is built</h2>
<p>Every case study on this blog follows the same discipline, based on the six-phase data analytics life cycle: Discovery, Data Preparation, Model Planning, Model Building, Communicate Results, and Operationalize. Numbers are shown in full — not just conclusions — so the reasoning is checkable, not just the headline.</p>
</div>
<div>
<div class="value-grid" style="grid-template-columns:1fr;">
<div class="value-item">
<div class="idx">Method</div>
<h4 style="margin:6px 0 6px;font-family:var(--serif);font-size:1.05rem;">Problem first, technique second</h4>
<p style="margin:0;font-size:0.9rem;color:var(--muted);">Every post opens with a real business question, not a dataset looking for a use.</p>
</div>
<div class="value-item">
<div class="idx">Method</div>
<h4 style="margin:6px 0 6px;font-family:var(--serif);font-size:1.05rem;">Show the working</h4>
<p style="margin:0;font-size:0.9rem;color:var(--muted);">Descriptive statistics, hypothesis tests, and model outputs are shown in full, with plain-language interpretation next to each one.</p>
</div>
<div class="value-item">
<div class="idx">Method</div>
<h4 style="margin:6px 0 6px;font-family:var(--serif);font-size:1.05rem;">Honest about limits</h4>
<p style="margin:0;font-size:0.9rem;color:var(--muted);">Every case study includes a limitations section — what the data can't tell you is as important as what it can.</p>
</div>
</div>
</div>
</div>
</section>
<section class="band">
<div class="wrap">
<div class="section-head">
<h2>About the author</h2>
</div>
<div style="display:flex;gap:24px;align-items:flex-start;flex-wrap:wrap;">
<div class="author-avatar" style="width:64px;height:64px;font-size:1.3rem;">SG</div>
<div style="max-width:60ch;">
<h3 style="color:#fff;margin-bottom:6px;">Sailee Dilip Gore</h3>
<p>Sailee wrote the "Decoding the Playlist" case study as part of the Data Analytics and Visualization coursework for the Minor in Data Science program. The post applies the data analytics life cycle, statistical testing, and K-Means clustering to a simulated music-streaming dataset, connecting classroom methods to a plausible product decision.</p>
</div>
</div>
</div>
</section>
<section>
<div class="wrap" style="text-align:center;">
<h2>Want to see it in action?</h2>
<p class="lede" style="max-width:50ch;margin:0 auto 24px;">Read the full listener-segmentation case study, worked from business question to business recommendation.</p>
<a class="btn btn-primary" href="/article">Read Decoding the Playlist</a>
</div>
</section>
</main>
'''
PAGE_CONTACT = r'''
<main>
<div class="wrap page-hero">
<span class="eyebrow">Get in touch</span>
<h1 style="max-width:20ch;">Say hello, or suggest a dataset.</h1>
<p class="lede" style="max-width:52ch;margin-top:12px;">Questions about the analysis, dataset suggestions, or feedback on the case study? Get in touch with Sailee.</p>
</div>
<section>
<div class="wrap two-col">
<div>
<form class="contact-form" data-email-submit="">
<div class="field">
<label for="name">Name</label>
<input id="name" name="name" placeholder="Your full name" required="" type="text"/>
</div>
<div class="field">
<label for="email">Email</label>
<input id="email" name="email" placeholder="you@email.com" required="" type="email"/>
</div>
<div class="field">
<label for="topic">Topic</label>
<select id="topic" name="topic">
<option>General question</option>
<option>Suggest a dataset</option>
<option>Correction on a post</option>
<option>Something else</option>
</select>
</div>
<div class="field">
<label for="message">Message</label>
<textarea id="message" name="message" placeholder="What's on your mind?" required=""></textarea>
</div>
<button class="btn btn-primary btn-block" type="submit">Send message</button>
<p class="form-status"></p>
</form>
</div>
<div>
<div class="contact-info-item">
<div class="ic">
<svg fill="none" height="17" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="17"><path d="M4 4h16v16H4z" opacity="0"></path><path d="M22 6 12 13 2 6"></path><path d="M2 6h20v12H2z"></path></svg>
</div>
<div>
<h5>Email</h5>
<p><a href="mailto:sailee.gore23@pccoepune.org">sailee.gore23@pccoepune.org</a></p>
</div>
</div>
<div class="contact-info-item">
<div class="ic">
<svg fill="none" height="17" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="17"><circle cx="12" cy="12" r="10"></circle><path d="M12 6v6l4 2"></path></svg>
</div>
<div>
<h5>Phone</h5>
<p><a href="tel:+919689024423">+91 96890 24423</a></p>
</div>
</div>
<div class="contact-info-item" style="border-bottom:none;">
<div class="ic">
<svg fill="none" height="17" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="17"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
</div>
<div>
<h5>Contact</h5>
<p>Sailee Dilip Gore</p>
</div>
</div>
</div>
</div>
</section>
</main>
'''


# ============================================================
# UI HELPERS
# ============================================================

def render_page(
    page_html: str,
    active_page: str,
    *,
    article: bool = False,
) -> None:
    """Render a complete page and normalize legacy image URLs."""
    # Original HTML used both /assets/img/... and /assets/images/....
    # The detected directory is mounted directly at /assets, so normalize
    # every supplied image reference to /assets/imageN.png.
    page_html = (
        page_html
        .replace("/assets/img/image", "/assets/image")
        .replace("/assets/images/image", "/assets/image")
    )

    header = build_header(active_page)
    footer = ARTICLE_FOOTER if article else FOOTER

    document = f"""
    {header}

    {page_html}

    {footer}
    """

    ui.html(document, sanitize=False).classes("w-full")


# ============================================================
# ROUTES
# ============================================================

@ui.page("/")
def home_page() -> None:
    render_page(PAGE_HOME, "home")


@ui.page("/blog")
def blog_page() -> None:
    render_page(PAGE_BLOG, "blog")


@ui.page("/article")
def article_page() -> None:
    render_page(PAGE_ARTICLE, "article", article=True)


@ui.page("/about")
def about_page() -> None:
    render_page(PAGE_ABOUT, "about")


@ui.page("/contact")
def contact_page() -> None:
    render_page(PAGE_CONTACT, "contact")


# ============================================================
# APPLICATION SETUP
# ============================================================

def configure_application() -> None:
    """Configure assets, shared CSS, fonts, and browser behavior."""
    if not IMAGE_DIR.exists():
        expected = "\n".join(f"  - {path}" for path in IMAGE_CANDIDATES)
        raise FileNotFoundError(
            "Missing image directory. Expected one of:\n" + expected
        )

    app.add_static_files("/assets", IMAGE_DIR)

    ui.add_css(CSS, shared=True)

    ui.add_head_html(
        """
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">
        <meta name="theme-color" content="#141B2E">

        <link rel="preconnect"
              href="https://fonts.googleapis.com">
        <link rel="preconnect"
              href="https://fonts.gstatic.com"
              crossorigin>

        <link
          href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap"
          rel="stylesheet">
        """,
        shared=True,
    )

    ui.add_head_html(
        f"<script>{JS}</script>",
        shared=True,
    )


def main() -> None:
    """Start the NiceGUI development/production server."""
    configure_application()

    port = int(os.environ.get("PORT", str(DEFAULT_PORT)))

    ui.run(
        host="0.0.0.0",
        port=port,
        title="StreamScope | Music Listening Analytics",
        reload=False,
    )


if __name__ == "__main__":
    main()
