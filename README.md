# Ashish Kulkarni — Personal Website & Blog

A lightweight, modern, and fast personal portfolio and Markdown-powered blog website.

- **Zero Bloat:** Pure standard library Python 3 static site generator (<50KB total payload). No bulky `node_modules` (>200MB) or external dependencies.
- **Dark & Light Mode:** Instant theme switcher with system preference detection and `localStorage` persistence.
- **Easy Markdown Blogging:** Write articles in standard Markdown; automatic reading-time calculation, tag badges, clean typography, code syntax formatting, and RSS feed generation.
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
To just generate the static files:
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

All your personal details, career timeline, education, credentials, and social links are managed in:
- `site_config.json`

Edit this file to update roles, add projects, or update links without touching any templates or code.

---

## 🌐 Deploying to GitHub Pages (When Ready)

When you are ready to publish on GitHub Pages:

### Option A: Using GitHub Actions (Automated on Push)
Create `.github/workflows/deploy.yml` in your repository:
```yaml
name: Deploy Website
on:
  push:
    branches: [ main ]
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: "pages"
  cancel-in-progress: false
jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Build site
        run: python3 build.py
      - name: Setup Pages
        uses: actions/configure-pages@v4
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './dist'
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```
Then in your GitHub repository:
- Go to **Settings** → **Pages**.
- Under **Build and deployment**, set Source to **GitHub Actions**.
- Push your code to GitHub, and your site is live at `https://<username>.github.io`!

### Option B: Deploying Prebuilt `dist/` Directly
You can also push the contents of `dist/` to a `gh-pages` branch.
