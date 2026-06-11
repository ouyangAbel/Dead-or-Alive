# -*- coding: utf-8 -*-
"""
Updated build script for DOA6 Last Round character guides.
Adds Key Moves, Combo Routes, Matchup Notes sections.
"""
import json, html, re
from pathlib import Path

ROOT = Path(r"D:\chuhaiWEB\Dead or Alive 6 Last Round")
GUIDES = ROOT / 'guides'
GUIDES.mkdir(exist_ok=True)

chars = json.loads((GUIDES / '_characters.json').read_text(encoding='utf-8'))
related_cycle = [c['slug'] for c in chars]

def esc(s):
    return html.escape(str(s), quote=True)

def li(arr):
    return ''.join(f'<li>{esc(x)}</li>' for x in arr)

def key_moves_table(c):
    if 'key_moves' not in c:
        return ''
    rows = ''
    for m in c['key_moves']:
        rows += f'<tr><td><strong>{esc(m["name"])}</strong></td><td><code>{esc(m["notation"])}</code></td><td>{esc(m["desc"])}</td></tr>\n'
    return f'''<div class="moves-table-wrap">
<table class="moves-table">
<thead><tr><th>Move</th><th>Notation</th><th>Notes</th></tr></thead>
<tbody>
{rows}</tbody>
</table></div>'''

def combo_table(c):
    if 'combo_routes' not in c:
        return ''
    rows = ''
    for combo in c['combo_routes']:
        diff_class = combo['difficulty'].lower()
        rows += f'<tr><td><strong>{esc(combo["name"])}</strong></td><td><code>{esc(combo["route"])}</code></td><td><span class="diff-badge diff-{diff_class}">{esc(combo["difficulty"])}</span></td></tr>\n'
    return f'''<div class="moves-table-wrap">
<table class="moves-table">
<thead><tr><th>Combo</th><th>Route</th><th>Difficulty</th></tr></thead>
<tbody>
{rows}</tbody>
</table></div>'''

def matchup_section(c):
    if 'matchup_notes' not in c:
        return ''
    items = ''
    for m in c['matchup_items'] if 'matchup_items' in c else c.get('matchup_notes', []):
        items += f'<div class="matchup-item"><h4>vs {esc(m["vs"])}</h4><p>{esc(m["advice"])}</p></div>\n'
    return f'<div class="matchup-grid">{items}</div>'

def slide_text(c):
    slides = [
        'prefers mid-range control and whiff punishment',
        'thrives on stagger pressure, throw mix-ups, and corner awareness',
        'wants structured oki after knockdowns and stage transitions',
        'rotates between fast checks, safe mids, and callout launchers',
        'looks for meter-efficient routes and consistent wall enders',
        'scales offense with staggers, guard breaks, and delayed timing',
        'reads defensive habits and punishes predictable holds',
        'manages space with approach checks and safe poke structures',
        'routes combos toward wall splats, danger zones, and stage-specific damage',
        'wins by forcing wrong guesses off plus frames and timing changes'
    ]
    return slides[sum(ord(ch) for ch in c['name']) % len(slides)]

def related_cards(c):
    idx = related_cycle.index(c['slug'])
    slugs = [related_cycle[(idx+i+1) % len(related_cycle)] for i in range(4)]
    names = {x['slug']: x['name'] for x in chars}
    return ''.join(
        '<a href="%s.html" class="related-card"><h4>%s</h4><p>Read the full DOA6 Last Round strategy guide for %s.</p></a>' % (s, esc(names[s]), esc(names[s]))
        for s in slugs
    )

STYLE = '''
.article-wrap{max-width:820px;margin:0 auto;padding:6rem 1.5rem 4rem}
.article-breadcrumb{font-family:var(--font-text);font-size:.85rem;color:var(--text-muted);margin-bottom:2rem;display:flex;gap:.5rem;flex-wrap:wrap}
.article-breadcrumb a{color:var(--accent-cyan);text-decoration:none} .article-breadcrumb a:hover{color:var(--accent-red)}
.article-meta{display:flex;gap:1.5rem;flex-wrap:wrap;margin-bottom:1.5rem;font-family:var(--font-text);font-size:.85rem;color:var(--text-muted)}
.article-meta span{display:flex;align-items:center;gap:.3rem}
.article-wrap h1{font-family:var(--font-display);font-size:clamp(1.8rem,4vw,2.8rem);font-weight:900;color:var(--text-bright);line-height:1.2;margin-bottom:1.5rem}
.article-wrap h2{font-family:var(--font-display);font-size:clamp(1.2rem,2.5vw,1.8rem);font-weight:700;color:var(--accent-red);margin:2.5rem 0 1rem;letter-spacing:.03em;padding-top:1rem;border-top:1px solid rgba(230,57,70,.1)}
.article-wrap h3{font-family:var(--font-display);font-size:1.1rem;font-weight:700;color:var(--text-bright);margin:1.5rem 0 .8rem}
.article-wrap p{font-family:var(--font-text);font-size:1.05rem;color:var(--text-muted);line-height:1.9;margin-bottom:1.2rem}
.article-wrap p.lead{font-size:1.15rem;color:var(--text-primary);line-height:1.8}
.article-wrap ul,.article-wrap ol{font-family:var(--font-text);font-size:1.05rem;color:var(--text-muted);line-height:1.9;margin:0 0 1.2rem 1.5rem}
.article-wrap li{margin-bottom:.4rem}
.article-wrap strong{color:var(--text-primary)}
.article-wrap a{color:var(--accent-cyan);text-decoration:none;border-bottom:1px solid rgba(0,240,255,.3);transition:border-color .3s}
.article-wrap a:hover{color:var(--accent-red);border-color:var(--accent-red)}
.article-img{width:100%;border-radius:6px;margin:1.5rem 0;border:1px solid rgba(230,57,70,.15)}
.article-img-caption{font-family:var(--font-text);font-size:.8rem;color:var(--text-muted);text-align:center;margin-top:-.8rem;margin-bottom:1.5rem}
.toc{background:var(--bg-card);border:1px solid rgba(230,57,70,.15);padding:1.5rem 2rem;margin:2rem 0;border-radius:4px}
.toc h4{font-family:var(--font-display);font-size:.75rem;letter-spacing:.2em;color:var(--accent-red);margin-bottom:.8rem}
.toc ol{margin:0;padding-left:1.2rem} .toc li{margin-bottom:.3rem;font-size:.95rem}
.toc a{color:var(--text-muted);text-decoration:none;border:none} .toc a:hover{color:var(--accent-red)}
.faq-section{background:var(--bg-card);border:1px solid rgba(230,57,70,.1);padding:2rem;margin:2rem 0;border-radius:4px}
.faq-item{margin-bottom:1.5rem} .faq-item:last-child{margin-bottom:0}
.faq-q{font-family:var(--font-body);font-weight:700;font-size:1.05rem;color:var(--text-bright);margin-bottom:.5rem}
.faq-a{font-family:var(--font-text);font-size:.95rem;color:var(--text-muted);line-height:1.8}
.article-share{display:flex;flex-wrap:wrap;gap:1rem;margin:2.5rem 0;padding:1.5rem 0;border-top:1px solid rgba(230,57,70,.1);border-bottom:1px solid rgba(230,57,70,.1)}
.share-btn{font-family:var(--font-display);font-size:.6rem;letter-spacing:.1em;padding:.6rem 1.2rem;border:1px solid rgba(230,57,70,.2);background:var(--bg-card);color:var(--text-muted);cursor:pointer;transition:all .3s;text-decoration:none}
.share-btn:hover{border-color:var(--accent-red);color:var(--accent-red);background:rgba(230,57,70,.05)}
.related-articles{margin:3rem 0} .related-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1.5rem;margin-top:1.5rem}
.related-card{background:var(--bg-card);border:1px solid rgba(230,57,70,.1);padding:1.5rem;text-decoration:none;transition:all .3s}
.related-card:hover{border-color:var(--accent-red);transform:translateY(-2px)}
.related-card h4{font-family:var(--font-text);font-size:1rem;font-weight:700;color:var(--text-bright);margin-bottom:.5rem}
.related-card p{font-size:.85rem;color:var(--text-muted);line-height:1.6}
.meta-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem;margin:1.5rem 0;background:var(--bg-card);border:1px solid rgba(230,57,70,.15);padding:1.2rem;border-radius:4px}
.meta-item{font-family:var(--font-text);font-size:.9rem;color:var(--text-muted)} .meta-item strong{color:var(--text-primary)}
.moves-table-wrap{overflow-x:auto;margin:1.5rem 0;border:1px solid rgba(230,57,70,.15);border-radius:4px}
.moves-table{width:100%;border-collapse:collapse;font-family:var(--font-text);font-size:.95rem}
.moves-table thead{background:rgba(230,57,70,.08)}
.moves-table th{font-family:var(--font-display);font-size:.75rem;letter-spacing:.12em;color:var(--accent-red);text-align:left;padding:.8rem 1rem;border-bottom:1px solid rgba(230,57,70,.2)}
.moves-table td{padding:.7rem 1rem;color:var(--text-muted);border-bottom:1px solid rgba(230,57,70,.06);vertical-align:top}
.moves-table tr:last-child td{border-bottom:none}
.moves-table code{color:var(--accent-cyan);font-size:.9rem;background:rgba(0,240,255,.06);padding:.15rem .4rem;border-radius:2px}
.diff-badge{font-family:var(--font-display);font-size:.65rem;letter-spacing:.08em;padding:.2rem .6rem;border-radius:2px;text-transform:uppercase}
.diff-easy{color:#4ade80;background:rgba(74,222,128,.1);border:1px solid rgba(74,222,128,.2)}
.diff-medium{color:#fbbf24;background:rgba(251,191,36,.1);border:1px solid rgba(251,191,36,.2)}
.diff-hard{color:#f87171;background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.2)}
.matchup-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1rem;margin:1.5rem 0}
.matchup-item{background:var(--bg-card);border:1px solid rgba(230,57,70,.1);padding:1.2rem;border-radius:4px}
.matchup-item h4{font-family:var(--font-display);font-size:.85rem;color:var(--text-bright);margin-bottom:.5rem;letter-spacing:.05em}
.matchup-item p{font-size:.9rem;color:var(--text-muted);line-height:1.7;margin:0}
@media(max-width:768px){.article-wrap{padding:5rem 1rem 3rem}.matchup-grid{grid-template-columns:1fr}.meta-grid{grid-template-columns:1fr 1fr}}
'''

SHARE = '''
  <div class="article-share">
    <span class="share-btn" onclick="window.open('https://twitter.com/intent/tweet?url='+encodeURIComponent(location.href)+'&text='+encodeURIComponent(document.title),'_blank')">X / TWITTER</span>
    <span class="share-btn" onclick="window.open('https://www.facebook.com/sharer/sharer.php?u='+encodeURIComponent(location.href),'_blank')">FACEBOOK</span>
    <span class="share-btn" onclick="window.open('https://www.reddit.com/submit?url='+encodeURIComponent(location.href)+'&title='+encodeURIComponent(document.title),'_blank')">REDDIT</span>
    <span class="share-btn" onclick="window.open('https://www.linkedin.com/sharing/share-offsite/?url='+encodeURIComponent(location.href),'_blank')">LINKEDIN</span>
    <span class="share-btn" onclick="window.open('https://t.me/share/url?url='+encodeURIComponent(location.href)+'&text='+encodeURIComponent(document.title),'_blank')">TELEGRAM</span>
    <span class="share-btn" onclick="window.open('https://api.whatsapp.com/send?text='+encodeURIComponent(document.title+' '+location.href),'_blank')">WHATSAPP</span>
    <span class="share-btn" onclick="window.open('https://www.pinterest.com/pin/create/button/?url='+encodeURIComponent(location.href)+'&description='+encodeURIComponent(document.title),'_blank')">PINTEREST</span>
    <span class="share-btn" onclick="navigator.clipboard.writeText(location.href);this.textContent='COPIED!';setTimeout(()=>this.textContent='COPY LINK',2000)">COPY LINK</span>
  </div>
'''

for c in chars:
    slug = c['slug']
    title = '%s Guide - DOA6 Last Round Strategy, Combos, Tier Placement, and Matchups' % c['name']
    desc = '%s guide for Dead or Alive 6 Last Round: strengths, weaknesses, key moves, combo strategy, matchup plan, tier placement, and the best ways to use %s effectively.' % (c['name'], c['style'])
    kw = '%s DOA6, Dead or Alive 6 %s, DOA6 Last Round %s, %s combos, %s guide, %s tier' % (c['name'], c['name'], c['name'], c['name'], c['name'], c['name'])
    url = 'https://doa6guide.com/guides/%s.html' % slug
    related = related_cards(c)
    km_table = key_moves_table(c)
    cb_table = combo_table(c)
    mu_section = matchup_section(c)
    
    article = '''<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HFE9TN506X"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-HFE9TN506X');</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s</title>
<meta name="description" content="%s">
<meta name="keywords" content="%s">
<meta name="robots" content="index, follow">
<link rel="canonical" href="%s">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&family=Exo+2:ital,wght@0,300;0,400;0,600;0,700;1,300&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/style.css">
<style>%s</style>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Article","headline":"%s","datePublished":"2026-06-11","dateModified":"2026-06-11","author":{"@type":"Organization","name":"DOA6 Ultimate Guide"},"description":"%s"}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Is %s good in DOA6 Last Round?","acceptedAnswer":{"@type":"Answer","text":"%s is a %s-tier pick in current community rankings and remains competitive when played with a disciplined gameplan."}},{"@type":"Question","name":"What is %s's fighting style in Dead or Alive 6?","acceptedAnswer":{"@type":"Answer","text":"%s uses %s, which defines their pressure tools, spacing habits, and combo structure in DOA6 Last Round."}},{"@type":"Question","name":"How hard is %s to learn in DOA6 Last Round?","acceptedAnswer":{"@type":"Answer","text":"%s rewards stable fundamentals and matchup awareness more than complicated execution."}}]}</script>
</head>
<body>
<nav id="main-nav">
  <div class="nav-inner">
    <a href="../index.html" class="nav-logo">DOA6 LAST ROUND <span>ULTIMATE GUIDE</span></a>
    <button class="nav-toggle" id="nav-toggle"><span></span><span></span><span></span></button>
    <ul class="nav-links" id="nav-links">
      <li><a href="../index.html">HOME</a></li>
      <li><a href="../roster.html" class="active">ROSTER</a></li>
      <li><a href="../combos.html">COMBOS</a></li>
      <li><a href="../mechanics.html">MECHANICS</a></li>
      <li><a href="../tier.html">TIER LIST</a></li>
      <li><a href="../videos.html">VIDEOS</a></li>
      <li><a href="../articles.html">ARTICLES</a></li>
    </ul>
  </div>
</nav>
<article class="article-wrap">
  <nav class="article-breadcrumb">
    <a href="../index.html">Home</a> / <a href="../roster.html">Roster</a> / <span>%s Guide</span>
  </nav>
  <header>
    <div class="article-meta">
      <span>June 11, 2026</span>
      <span>12 min read</span>
      <span>Character Guide</span>
    </div>
    <h1>%s Guide for DOA6 Last Round: Strengths, Weaknesses, Combos, and Matchup Strategy</h1>
    <p class="lead">This %s guide explains how to use %s effectively in Dead or Alive 6 Last Round. You will learn the character's strengths, weaknesses, best approach tools, gameplan structure, matchup priorities, and where %s currently sits on the tier list. The goal is to help you win more consistently by building smarter offense, cleaner punishes, and more reliable round-closing decisions.</p>
  </header>
  <img src="../images/doa6-wiki-hero.svg" alt="%s guide for Dead or Alive 6 Last Round" class="article-img" loading="lazy">
  <div class="article-img-caption">%s rewards players who understand spacing, timing, and how to turn small wins into full rounds.</div>
  <div class="meta-grid">
    <div class="meta-item"><strong>Archetype:</strong> %s</div>
    <div class="meta-item"><strong>Fighting Style:</strong> %s</div>
    <div class="meta-item"><strong>Effective Range:</strong> %s</div>
    <div class="meta-item"><strong>Tier Placement:</strong> %s-Tier</div>
    <div class="meta-item"><strong>Best For:</strong> Players who %s</div>
  </div>
  <div class="toc">
    <h4>TABLE OF CONTENTS</h4>
    <ol>
      <li><a href="#overview">Why Play %s in DOA6 Last Round?</a></li>
      <li><a href="#key-moves">Key Moves and Tools</a></li>
      <li><a href="#combos">Combo Routes</a></li>
      <li><a href="#strengths">Strengths and Weaknesses</a></li>
      <li><a href="#beginner">Beginner Gameplan</a></li>
      <li><a href="#advanced">Advanced Strategy</a></li>
      <li><a href="#matchups">Matchup Priorities</a></li>
      <li><a href="#tier">Tier Placement and Competitive Value</a></li>
      <li><a href="#faq">Frequently Asked Questions</a></li>
    </ol>
  </div>

  <h2 id="overview">Why Play %s in DOA6 Last Round?</h2>
  <p>%s is a strong choice for players who want a character built around %s. In Dead or Alive 6 Last Round, that means the character's tools naturally support %s, giving you a clear identity in neutral, pressure, and combo conversion. The character works best at %s range, where core buttons can force decisions and convert clean hits into structured offense.</p>
  <p>One reason many players pick %s is the balance between usability and depth. The character is welcoming enough for intermediate players, yet still offers advanced layers for tighter timing, better routing, and stronger round management. If you enjoy characters that reward awareness over chaos, %s is a natural fit.</p>
  <p>This guide focuses on practical decision-making. Instead of only listing moves, it explains how %s wants to play the round: what to fish for, what to punish, when to throw, when to stall, and how to use stage positioning to increase reward.</p>
  <p>If you are also evaluating other fighters, pair this guide with the full <a href="../roster.html">DOA6 Last Round roster</a> and the current <a href="../tier.html">tier list</a> to compare tools, matchup value, and overall consistency.</p>

  <h2 id="key-moves">Key Moves and Tools</h2>
  <p>Every character in DOA6 Last Round has a set of core moves that define their gameplan. For %s, these are the tools you will use most often in real matches. Learn their startup speed, block advantage, and when to use each one.</p>
  %s

  <h2 id="combos">Combo Routes</h2>
  <p>Combo efficiency matters in DOA6 because small damage differences decide close rounds. Below are the most important combo routes for %s, from beginner-friendly options to advanced optimized routes. Start with the easy ones and add harder routes as your execution improves.</p>
  %s

  <h2 id="strengths">Strengths and Weaknesses</h2>
  <h3>Core Strengths</h3>
  <ul>%s</ul>
  <p>These strengths define why %s can compete at a high level. The character is especially rewarding for players who like turning simple neutral wins into repeated pressure.</p>
  <h3>Main Weaknesses</h3>
  <ul>%s</ul>
  <p>Understanding weaknesses helps you build better practice habits. Instead of only grinding offense, test how the character handles common threats: fast rushdown, throw-heavy grapplers, evasive stance characters, and patient mid-range fighters.</p>

  <h2 id="beginner">Beginner Gameplan</h2>
  <p>If you are still learning %s, start with a simple, repeatable gameplan. The goal is not to do the flashiest combo; it is to make fewer bad decisions than your opponent. Focus on a small set of tools first, then expand as your comfort grows.</p>
  <ul>%s</ul>
  <p>This foundation works because it mirrors the way DOA6 matches actually unfold. You begin by testing the opponent with safe pressure, then you expand once you see how they defend.</p>
  <p>For beginners, the most important skill is hit confirmation. Build the habit of confirming whether your first hit connected or was blocked, then choose the right follow-up accordingly.</p>

  <h2 id="advanced">Advanced Strategy</h2>
  <p>At higher levels, %s becomes more about timing control and layered reads. You still use the core tools from the beginner gameplan, but you begin mixing in delayed pressure, optimized routing, and tighter matchup-based decisions.</p>
  <ul>%s</ul>
  <p>Advanced players should also think more about stage positioning. If your starter can carry toward the wall, adjust your routing even if the raw damage looks slightly different. Wall pressure often generates more future value than a small damage upgrade in open space.</p>
  <p>Another advanced layer is meter management. The Break Gauge gives you access to powerful options, but only if you spend it at the right time.</p>

  <h2 id="matchups">Matchup Priorities</h2>
  <p>Matchup knowledge is one of the most important parts of DOA6, and %s is no different. Some opponents will force you to play patiently, while others will force you to take control before their offense snowballs.</p>
  <p><strong>Against rushdown characters:</strong> Do not panic-block forever. Look for fast checks, spacing resets, and moments when their offense becomes predictable.</p>
  <p><strong>Against grapplers:</strong> Avoid staying in throw range without reason. Use quick mids to interrupt their preferred spacing and force them to block real starters.</p>
  <p><strong>Against evasive or stance-heavy characters:</strong> Stay compact. Use reliable mids and delayed timing instead of chasing them around the screen.</p>
  <p><strong>General matchup advice:</strong> %s</p>
  <p><strong>Character-specific strategy:</strong> %s</p>
  %s

  <h2 id="tier">Tier Placement and Competitive Value</h2>
  <p>In the current community rankings, %s is a <strong>%s-tier</strong> character. For most players, this means %s is more than capable of climbing ranked, performing in locals, and holding up in long competitive sets when played with the right habits.</p>
  <p>Tier placement is helpful, but it should not be the only reason you choose a main. If your style naturally fits %s, you will likely perform better with %s than with a higher-tier character that feels awkward in your hands.</p>
  <p>If you want to compare %s with other fighters, check the live <a href="../tier.html">tier list</a>, then cross-reference with the full <a href="../roster.html">roster</a> and dedicated <a href="../combos.html">combo guides</a>.</p>

  <h2 id="faq">Frequently Asked Questions</h2>
  <div class="faq-section">
    <div class="faq-item">
      <div class="faq-q">Is %s good for beginners?</div>
      <div class="faq-a">Yes. %s can be learned effectively by focusing on spacing, punishment, and simple decision-making before expanding into advanced routes.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q">What is the best range for %s?</div>
      <div class="faq-a">Most players will find the best results at %s range. That is where the character's main tools force meaningful decisions and convert cleanly into pressure, throws, or combo starters.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q">What should I learn first with %s?</div>
      <div class="faq-a">Start with safe pressure strings, one reliable launcher route, and a simple throw game. Once those are comfortable, add wall routes, counter-hit confirms, and matchup-specific adjustments.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q">Where is %s on the DOA6 Last Round tier list?</div>
      <div class="faq-a">Current rankings place %s in %s-tier. That makes the character a competitive pick with strong long-term potential for players who enjoy %s.</div>
    </div>
  </div>
  %s
  <div class="related-articles">
    <h2>RELATED GUIDES</h2>
    <div class="related-grid">
      <a href="../roster.html" class="related-card"><h4>Character Roster</h4><p>Browse the full DOA6 Last Round fighter database with styles and breakdowns.</p></a>
      <a href="../combos.html" class="related-card"><h4>Combo Guides</h4><p>Check combo routes and damage structure for your main or secondary pick.</p></a>
      <a href="../tier.html" class="related-card"><h4>Tier List</h4><p>See where %s ranks among the current DOA6 Last Round characters.</p></a>
      %s
    </div>
  </div>
</article>
<footer>
  <div class="footer-logo">DOA6 LAST ROUND - ULTIMATE GUIDE</div>
  <div class="footer-links">
    <a href="../index.html">Home</a>
    <a href="../roster.html">Roster</a>
    <a href="../combos.html">Combos</a>
    <a href="../mechanics.html">Mechanics</a>
    <a href="../tier.html">Tier List</a>
    <a href="../videos.html">Videos</a>
  </div>
  <p class="footer-copy">DEAD OR ALIVE 6 LAST ROUND Ultimate Guide &copy; <span id="copyright-year"></span></p>
  <p class="footer-disclaimer">This is a fan-made strategy guide and is not affiliated with KOEI TECMO.</p>
</footer>
<script src="../js/main.js"></script>
<script>document.getElementById('copyright-year').textContent=new Date().getFullYear();</script>
</body>
</html>
''' % (
        esc(title), esc(desc), esc(kw), url, STYLE, esc(title), esc(desc),
        esc(c['name']), esc(c['name']), c['tier'], esc(c['name']), esc(c['style']), esc(c['name']),
        esc(c['name']), esc(c['name']), esc(c['archetype']), slide_text(c),
        esc(c['name']), esc(c['name']), esc(c['archetype']), esc(c['style']), esc(c['range']), esc(c['name']), esc(c['name']), esc(c['name']), esc(c['name']),
        esc(c['name']), km_table,
        esc(c['name']), cb_table,
        li(c['strengths']), esc(c['name']), li(c['weaknesses']), esc(c['name']), li(c['beginner']), esc(c['name']), li(c['advanced']), esc(c['name']), esc(c['name']), esc(c['matchup_tip']), esc(c['strat']), mu_section,
        esc(c['name']), c['tier'], esc(c['name']), esc(c['style']), esc(c['name']), esc(c['name']),
        esc(c['name']), esc(c['name']), esc(c['range']), esc(c['name']), esc(c['name']), esc(c['name']), c['tier'], esc(c['style']), SHARE, esc(c['name']), related
    )
    (GUIDES / '%s.html' % slug).write_text(article, encoding='utf-8')

index_cards = ''.join(
    '<a href="%s.html" class="la-card reveal"><div class="la-card-tag">CHARACTER GUIDE</div><h3>%s Guide</h3><p>Strategy, strengths, weaknesses, matchup plan, and tier placement for %s in DOA6 Last Round.</p><span class="la-card-date">June 11, 2026</span></a>' % (c['slug'], esc(c['name']), esc(c['name']))
    for c in chars
)
index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HFE9TN506X"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-HFE9TN506X');</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DOA6 Last Round Character Guides | Strategy, Combos, and Tier Placement</title>
<meta name="description" content="Browse every Dead or Alive 6 Last Round character guide. Each page covers strengths, weaknesses, combo strategy, matchup advice, and current tier placement.">
<meta name="keywords" content="DOA6 Last Round guides, Dead or Alive 6 character guides, DOA6 roster strategy, DOA6 Last Round combos">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://doa6guide.com/guides/index.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&family=Exo+2:ital,wght@0,300;0,400;0,600;0,700;1,300&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/style.css">
</head>
<body>
<nav id="main-nav">
  <div class="nav-inner">
    <a href="../index.html" class="nav-logo">DOA6 LAST ROUND <span>ULTIMATE GUIDE</span></a>
    <button class="nav-toggle" id="nav-toggle"><span></span><span></span><span></span></button>
    <ul class="nav-links" id="nav-links">
      <li><a href="../index.html">HOME</a></li>
      <li><a href="../roster.html" class="active">ROSTER</a></li>
      <li><a href="../combos.html">COMBOS</a></li>
      <li><a href="../mechanics.html">MECHANICS</a></li>
      <li><a href="../tier.html">TIER LIST</a></li>
      <li><a href="../videos.html">VIDEOS</a></li>
      <li><a href="../articles.html">ARTICLES</a></li>
    </ul>
  </div>
</nav>
<div class="page-header">
  <div class="page-header-content">
    <div class="page-header-tag">CHARACTER GUIDES</div>
    <h1>DOA6 LAST ROUND <span class="red">CHARACTER GUIDES</span></h1>
    <div class="page-header-line"></div>
    <p class="page-header-desc">Detailed character pages for every fighter in the roster. Use these guides to learn strengths, weaknesses, gameplans, combo priorities, and current competitive placement.</p>
  </div>
</div>
<section class="latest-articles" id="character-guides">
  <div class="section-header reveal">
    <div class="section-tag">FULL LIBRARY</div>
    <h2 class="section-title">BROWSE <span class="red">GUIDES</span></h2>
    <div class="section-line"></div>
  </div>
  <div class="la-grid" style="grid-template-columns:repeat(auto-fit,minmax(230px,1fr))">
    %s
  </div>
</section>
<footer>
  <div class="footer-logo">DOA6 LAST ROUND - ULTIMATE GUIDE</div>
  <div class="footer-links">
    <a href="../index.html">Home</a>
    <a href="../roster.html">Roster</a>
    <a href="../combos.html">Combos</a>
    <a href="../mechanics.html">Mechanics</a>
    <a href="../tier.html">Tier List</a>
    <a href="../videos.html">Videos</a>
  </div>
  <p class="footer-copy">DEAD OR ALIVE 6 LAST ROUND Ultimate Guide &copy; <span id="copyright-year"></span></p>
  <p class="footer-disclaimer">This is a fan-made strategy guide and is not affiliated with KOEI TECMO.</p>
</footer>
<script src="../js/main.js"></script>
<script>document.getElementById('copyright-year').textContent=new Date().getFullYear();</script>
</body>
</html>
''' % index_cards
(GUIDES / 'index.html').write_text(index_html, encoding='utf-8')
print('generated', len(chars), 'guide pages with enhanced content')
