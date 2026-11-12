# kenlari — security portfolio

**Live site → https://kenlari.github.io/portfolio/**

A static portfolio of hands-on security work: one complete penetration-test
engagement and a graded cryptography range. Everything here was built and run
on a local Kali VM. No real targets, no client data, no secrets.

| Page | What it shows |
|---|---|
| [Vaultly assessment](https://kenlari.github.io/portfolio/vaultly/) | Recon → exploitation → remediation report on a deliberately vulnerable app: credential disclosure, IDOR and OS command injection, chained to full host compromise. CVSS ratings and developer-ready fixes. |
| [Crypto range](https://kenlari.github.io/portfolio/crypto/) | Seven solved challenges — encoding stacks, XOR key recovery, Vigenère, wordlist cracking, unpadded RSA, ECDSA nonce reuse — with the reasoning, not just flags. |

## Why it exists

Proof of work. Anyone can list tools on a CV; this repo shows the output:
a report written for a developer to act on, and breaks explained well enough
that someone else could reproduce them.

## How it is built

Markdown in, static HTML out. No framework, no build service, no trackers,
no hosting cost.

```bash
python3 build.py                  # markdown -> docs/
python3 build.py --user kenlari   # set the GitHub username in links
python3 -m http.server --directory docs 8000   # preview at :8000
```

- `build.py` — the generator (uses `python-markdown`, already on Kali)
- `config.json` — site title and username
- `docs/` — generated output, served by GitHub Pages (`main` / `docs`)
- `PUBLISH.md` — step-by-step deployment notes

## Scope and ethics

All testing was performed against systems I wrote and own, bound to
`127.0.0.1`. Nothing in this repository targets third-party infrastructure.
The vulnerable app is intentionally insecure and must never be exposed to a
network.

## Licence

Text and reports: CC BY 4.0. Code: MIT.
