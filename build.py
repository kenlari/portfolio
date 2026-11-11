#!/usr/bin/env python3
"""Build a static portfolio site from markdown. No dependencies beyond
python-markdown (already installed).

    python3 build.py
    python3 build.py --user your-github-name
    python3 -m http.server --directory docs 8000   # preview

Output goes to docs/ so GitHub Pages can serve it with
Settings -> Pages -> Source: main /docs
"""

import argparse
import json
import shutil
from datetime import date
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
HOME = Path.home()
OUT = ROOT / "docs"
CONFIG = ROOT / "config.json"

DEFAULT_CONFIG = {
    "user": "YOUR-USERNAME",
    "site_title": "kennethlari",
    "tagline": "Linux · web security · crypto",
}

CSS = """\
:root{--bg:#0d1117;--fg:#e6edf3;--dim:#8b949e;--line:#30363d;--acc:#58a6ff;--ok:#3fb950;--warn:#d29922;--bad:#f85149}
*{box-sizing:border-box}
html{color-scheme:dark}
body{margin:0;background:var(--bg);color:var(--fg);
 font:16px/1.65 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
header.site{border-bottom:1px solid var(--line);padding:18px 24px;
 display:flex;justify-content:space-between;align-items:center;max-width:960px;margin:0 auto}
header.site .brand{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-weight:600;color:var(--fg)}
header.site nav a{margin-left:18px;color:var(--dim)}
main.wrap{max-width:780px;margin:0 auto;padding:40px 24px 80px}
h1{font-size:2rem;line-height:1.2;margin:.2em 0 .1em;letter-spacing:-.02em}
h2{font-size:1.3rem;margin-top:2.2em;padding-bottom:.3em;border-bottom:1px solid var(--line)}
h3{font-size:1.05rem;margin-top:1.8em}
p.sub{color:var(--dim);margin-top:0;font-size:1.02rem}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.88em;
 background:#161b22;border:1px solid var(--line);border-radius:6px;padding:.12em .38em}
pre{background:#161b22;border:1px solid var(--line);border-radius:10px;
 padding:16px;overflow:auto;line-height:1.5}
pre code{background:none;border:0;padding:0;font-size:.86em}
table{border-collapse:collapse;width:100%;margin:1.2em 0;font-size:.93em;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:8px 12px;text-align:left;vertical-align:top}
th{background:#161b22;font-weight:600}
blockquote{margin:1.2em 0;padding:.2em 1em;border-left:3px solid var(--acc);color:var(--dim);background:#11161d}
hr{border:0;border-top:1px solid var(--line);margin:2.5em 0}
ul,ol{padding-left:1.4em}
footer{max-width:780px;margin:0 auto;padding:24px;border-top:1px solid var(--line);
 color:var(--dim);font-size:.85rem}
.cards{display:grid;gap:16px;margin:2.5em 0}
.card{border:1px solid var(--line);border-radius:12px;padding:20px 22px;background:#11161d}
.card:hover{border-color:var(--acc)}
.card h3{margin:0 0 .3em;font-size:1.1rem}
.card p{margin:0;color:var(--dim);font-size:.93rem}
.card .tags{margin-top:.8em;font-size:.78rem;color:var(--dim);
 font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.kpis{display:flex;flex-wrap:wrap;gap:10px;margin:1.6em 0 0}
.kpi{border:1px solid var(--line);border-radius:999px;padding:5px 12px;font-size:.8rem;color:var(--dim)}
.kpi b{color:var(--fg);font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
"""

TEMPLATE = """\
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · {site_title}</title>
<meta name="description" content="{subtitle}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{subtitle}">
<link rel="stylesheet" href="{css}">
</head>
<body>
<header class="site">
  <a class="brand" href="{home}">{site_title}</a>
  <nav><a href="{home}">index</a><a href="{github}">github</a></nav>
</header>
<main class="wrap">
<h1>{title}</h1>
<p class="sub">{subtitle}</p>
{body}
</main>
<footer>Built {today} · <a href="{github}">{site_title}</a> · static, no trackers</footer>
</body>
</html>
"""

MD_EXT = ["tables", "fenced_code", "toc", "sane_lists", "attr_list", "md_in_html"]


def load_config() -> dict:
    if CONFIG.exists():
        return {**DEFAULT_CONFIG, **json.loads(CONFIG.read_text())}
    CONFIG.write_text(json.dumps(DEFAULT_CONFIG, indent=2) + "\n")
    return dict(DEFAULT_CONFIG)


def page(title, subtitle, body, cfg, css, home, github):
    return TEMPLATE.format(
        title=title, subtitle=subtitle, body=body, site_title=cfg["site_title"],
        css=css, home=home, github=github, today=date.today().isoformat(),
    )


def render_md(path: Path) -> str:
    return markdown.markdown(path.read_text(), extensions=MD_EXT)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", help="GitHub username (overrides config.json)")
    args = ap.parse_args()

    cfg = load_config()
    if args.user:
        cfg["user"] = args.user
        CONFIG.write_text(json.dumps(cfg, indent=2) + "\n")

    github = f"https://github.com/{cfg['user']}"
    PAGES = [
        {
            "slug": "vaultly",
            "title": "Vaultly — web application assessment",
            "subtitle": "Recon → exploitation → remediation report on a deliberately vulnerable notes service.",
            "src": HOME / "portfolio/engagements/vaultly/report.md",
            "extra": [HOME / "portfolio/engagements/vaultly/evidence.log"],
            "cards_title": "Vaultly 1.4.2",
            "blurb": "Unauthenticated credential disclosure, IDOR and OS command injection, chained to full host compromise. Includes CVSS ratings and developer-ready fixes.",
            "tags": "nmap · curl · python · OWASP WSTG",
        },
        {
            "slug": "crypto",
            "title": "Crypto range — seven writeups",
            "subtitle": "From encoding stacks to ECDSA nonce reuse, each break explained and reproduced.",
            "src": HOME / "crypto-lab/writeups/README.md",
            "extra": [],
            "cards_title": "Crypto range",
            "blurb": "Seven graded challenges: XOR key recovery, Vigenère, wordlist cracking, unpadded RSA, and nonce-reuse key recovery on secp256k1.",
            "tags": "python · john · RSA · ECDSA",
        },
    ]

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    (OUT / "style.css").write_text(CSS)
    (OUT / ".nojekyll").write_text("")

    # ---- article pages
    for p in PAGES:
        if not p["src"].exists():
            print(f"  skip {p['slug']}: missing {p['src']}")
            continue
        d = OUT / p["slug"]
        d.mkdir()
        html = page(
            p["title"], p["subtitle"], render_md(p["src"]), cfg, "../style.css", "../index.html", github
        )
        (d / "index.html").write_text(html)
        for e in p["extra"]:
            if e.exists():
                shutil.copy2(e, d / e.name)
        print(f"  built /{p['slug']}/")

    # ---- index
    cards = []
    for p in PAGES:
        if not (OUT / p["slug"] / "index.html").exists():
            continue
        cards.append(
            f'<a class="card" href="{p["slug"]}/">'
            f'<h3>{p["cards_title"]}</h3><p>{p["blurb"]}</p>'
            f'<div class="tags">{p["tags"]}</div></a>'
        )
    index_body = f"""\
<p>{cfg['tagline']}. I break things on purpose, then write up exactly how —
so the fix is obvious to whoever has to ship it.</p>
<div class="kpis">
  <span class="kpi"><b>7</b> crypto challenges solved</span>
  <span class="kpi"><b>3</b> web findings, 1 critical</span>
  <span class="kpi"><b>0</b> dollars spent</span>
</div>
<h2>Work</h2>
<div class="cards">
{''.join(cards)}
</div>
<h2>How this is built</h2>
<p>Markdown in, static HTML out — <code>python3 build.py</code>, no framework, no
trackers, no cost. Hosted free on GitHub Pages.</p>
"""
    (OUT / "index.html").write_text(
        page(cfg["site_title"], cfg["tagline"], index_body, cfg, "style.css", "index.html", github)
    )
    print(f"  built /  ->  {OUT}")
    print(f"\npreview:  python3 -m http.server --directory {OUT} 8000")


if __name__ == "__main__":
    main()
