# Ashish Kulkarni — Personal Website & Blog

A lightweight, modern, and fast personal portfolio and Markdown-powered blog website.

- **Zero Bloat:** Pure standard library Python 3 static site generator (<50KB total payload). No bulky `node_modules` (>200MB) or external dependencies.
- **Dark & Light Mode:** Instant theme switcher with system preference detection and `localStorage` persistence.
- **Easy Markdown Blogging:** Write articles in standard Markdown; automatic reading-time calculation, tag badges, clean typography, code syntax formatting, and RSS feed generation.
- **Minimal Homepage:** Clean, focused homepage showcasing current role and recent articles.
- **Dedicated About Page:** Comprehensive overview of current role, domain focus, and engineering skill sets.
- **GitHub Pages Ready:** Portable relative URLs that work locally and deploy effortlessly to GitHub Pages.

---

## 🚀 Quick Start

### 1. Preview Locally
In WSL2 / Linux terminal:
```bash
python3 dev.py
```
Open **[http://localhost:8080](http://localhost:8080)** in your browser (works directly in your Windows browser from WSL2).

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
3. Run `python3 build.py` (or keep `python3 dev.py` running).
4. That's it! Your post will automatically:
   - Appear in the **Recent Writing** section on the homepage.
   - Be listed on the **Blog** archive (`/blog/`).
   - Get its own dedicated article page at `/posts/scaling-commodity-data-pipelines/`.
   - Be added to `rss.xml`.

---

## ⚙️ Updating Profile & Information

Personal details, current role, about paragraphs, and social links are managed in:
- `site_config.json`

Edit this file to update your bio, role description, or links without touching any templates or code.
