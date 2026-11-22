# Ashish Kulkarni — Personal Website & Blog

A lightweight, modern, and fast personal portfolio and Markdown-powered blog website.

- **Zero Bloat:** Pure standard library Python 3 static site generator (<50KB total payload). No bulky `node_modules` (>200MB) or external dependencies.
- **Dark & Light Mode:** Instant theme switcher with system preference detection and `localStorage` persistence.
- **Easy Markdown Blogging:** Write articles in standard Markdown; automatic reading-time calculation, tag badges, clean typography, code syntax formatting, and RSS feed generation.
- **Minimal Homepage:** Clean, focused homepage showcasing recent articles.
- **Dedicated About Page:** Comprehensive overview of current role, domain focus, and engineering skill sets.
- **Live URL:** [https://ashish-mk.github.io/](https://ashish-mk.github.io/)

---

## 🚀 Quick Start

### 1. Preview Locally
In WSL2 / Linux terminal:
```bash
python3 dev.py
```
Open **[http://localhost:8080](http://localhost:8080)** in your browser.

### 2. Manual Build
To generate the static files:
```bash
python3 build.py
```
The compiled, ready-to-serve website is output into the `dist/` directory.

---

## ✍️ How to Write & Publish a Blog Post

1. Create a new `.md` file inside `content/posts/`, for example `content/posts/2026-12-data-pipelines.md`.
2. Add frontmatter at the top:
   ```markdown
   ---
   title: "Scaling Data Ingestion for Commodity Markets"
   date: "2026-12-01"
   summary: "Architectural patterns for reliable high-throughput pipelines."
   tags: ["Data Engineering", "Python", "Quant"]
   slug: "scaling-commodity-data-pipelines"
   ---

   Your content goes here in standard Markdown...
   ```
3. Test locally with `python3 build.py` (or keep `python3 dev.py` running).
4. Deploy with one command:
   ```bash
   ./deploy.sh "Add post on scaling commodity data pipelines"
   ```

---

## 🌐 Deploying to GitHub Pages

Deploying your latest changes to GitHub Pages is as simple as running:
```bash
./deploy.sh
```
This builds the site, commits your changes to `main`, and pushes the updated static distribution to GitHub Pages (`gh-pages` branch).
