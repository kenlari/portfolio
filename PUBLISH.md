# Publishing this site (free, ~5 minutes)

Everything is already built and committed locally. You only need a GitHub
account. No card, no server, no domain.

---

## 1. Create the repo

Go to <https://github.com/new> and create a **public** repo named:

```
portfolio
```

Do **not** add a README, .gitignore, or licence — this repo already has them.

> GitHub Pages on the free plan requires a public repo.

## 2. Add the SSH key that already exists on this VM

Public key (copy the whole line):

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJywvNb76iNyZaI0TidW6P+c+lwAkBofyoirgq0Ac/1O kennethlari@kali
```

- Go to <https://github.com/settings/keys> → **New SSH key**
- Title: `kali-vm`
- Type: **Authentication key**
- Paste, then **Add SSH key**

Test it:

```bash
ssh -T git@github.com      # should say "Hi <user>! You've successfully authenticated"
```

You can revoke this key at any time from the same page.

## 3. Point the repo at GitHub and push

Replace `YOUR-USERNAME` with your GitHub username:

```bash
cd ~/portfolio-site
git remote add origin git@github.com:YOUR-USERNAME/portfolio.git
git branch -M main
git push -u origin main
```

## 4. Turn on Pages

Repo → **Settings** → **Pages**:

- **Source**: *Deploy from a branch*
- **Branch**: `main`  ·  **Folder**: `/docs`
- **Save**

Wait ~1 minute. Your site is live at:

```
https://YOUR-USERNAME.github.io/portfolio/
```

## 5. Fix the links to your username

The site currently links to `YOUR-USERNAME`. Set it once and rebuild:

```bash
cd ~/portfolio-site
python3 build.py --user YOUR-USERNAME
git add -A && git commit -m "set github username" && git push
```

---

## Updating content later

Everything is generated from markdown. To add a writeup:

1. Put the `.md` file anywhere (e.g. `~/crypto-lab/writeups/new.md`).
2. Add an entry to the `PAGES` list in `build.py` (slug, title, subtitle, src).
3. `python3 build.py` → commit → push.

## Preview before pushing

```bash
cd ~/portfolio-site
python3 build.py
python3 -m http.server --directory docs 8000
```

Open <http://127.0.0.1:8000>.

---

## Optional: a live demo of the vulnerable app

GitHub Pages only serves static files, so the Vaultly *app* can't run there —
which is fine, the **report** is the deliverable. If you ever want a live demo:

```bash
cd ~/portfolio/engagements/vaultly
python3 app.py &                      # local only
~/.local/bin/cloudflared tunnel --url http://127.0.0.1:8080
```

That gives a temporary public URL to show someone interactively. Stop both when
done. Never leave the tunnel running — the app is deliberately vulnerable.
