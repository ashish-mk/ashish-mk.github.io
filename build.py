#!/usr/bin/env python3
"""
Zero-dependency static site generator for Ashish Kulkarni's portfolio & blog.
Parses Markdown posts, renders HTML from templates, and outputs a clean static site to dist/.
"""

import os
import re
import json
import shutil
import html
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
CONTENT_DIR = ROOT_DIR / "content" / "posts"
TEMPLATES_DIR = ROOT_DIR / "templates"
STATIC_DIR = ROOT_DIR / "static"
DIST_DIR = ROOT_DIR / "dist"
CONFIG_FILE = ROOT_DIR / "site_config.json"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_frontmatter(content: str):
    """Extracts frontmatter between leading --- delimiters and returns (metadata, markdown_body)."""
    meta = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            raw_meta = parts[1].strip()
            body = parts[2].strip()

            for line in raw_meta.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip()
                    val = val.strip()
                    # Handle json lists like ["a", "b"]
                    if val.startswith("[") and val.endswith("]"):
                        try:
                            items = json.loads(val)
                            meta[key] = [str(x) for x in items]
                        except Exception:
                            # fallback comma separated
                            raw_items = val.strip("[]").split(",")
                            meta[key] = [x.strip().strip('"\'') for x in raw_items if x.strip()]
                    else:
                        # strip quotes
                        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                            val = val[1:-1]
                        meta[key] = val

    return meta, body


def markdown_to_html(md_text: str) -> str:
    """Converts a Markdown string to clean semantic HTML without external dependencies."""
    lines = md_text.split("\n")
    html_lines = []
    in_code_block = False
    code_lang = ""
    code_lines = []
    in_list = False
    list_type = None
    in_blockquote = False
    bq_lines = []

    def flush_blockquote():
        nonlocal in_blockquote, bq_lines
        if in_blockquote:
            text = " ".join(bq_lines)
            html_lines.append(f"<blockquote>{inline_markdown(text)}</blockquote>")
            bq_lines = []
            in_blockquote = False

    def flush_list():
        nonlocal in_list, list_type
        if in_list:
            tag = "ul" if list_type == "ul" else "ol"
            html_lines.append(f"</{tag}>")
            in_list = False
            list_type = None

    for raw_line in lines:
        line = raw_line.rstrip()

        # Code fences
        if line.startswith("```"):
            if not in_code_block:
                flush_blockquote()
                flush_list()
                in_code_block = True
                code_lang = line[3:].strip()
                code_lines = []
            else:
                in_code_block = False
                escaped_code = html.escape("\n".join(code_lines))
                lang_attr = f' class="language-{html.escape(code_lang)}"' if code_lang else ""
                html_lines.append(f'<pre><code{lang_attr}>{escaped_code}</code></pre>')
                code_lines = []
            continue

        if in_code_block:
            code_lines.append(raw_line)
            continue

        # Blockquote
        if line.startswith(">"):
            flush_list()
            in_blockquote = True
            bq_content = line[1:].strip()
            bq_lines.append(bq_content)
            continue
        elif in_blockquote:
            flush_blockquote()

        # Unordered list
        ul_match = re.match(r"^(\*|-)\s+(.*)$", line)
        if ul_match:
            flush_blockquote()
            if not in_list or list_type != "ul":
                flush_list()
                in_list = True
                list_type = "ul"
                html_lines.append("<ul>")
            item_text = inline_markdown(ul_match.group(2))
            html_lines.append(f"  <li>{item_text}</li>")
            continue

        # Ordered list
        ol_match = re.match(r"^(\d+)\.\s+(.*)$", line)
        if ol_match:
            flush_blockquote()
            if not in_list or list_type != "ol":
                flush_list()
                in_list = True
                list_type = "ol"
                html_lines.append("<ol>")
            item_text = inline_markdown(ol_match.group(2))
            html_lines.append(f"  <li>{item_text}</li>")
            continue

        if in_list:
            flush_list()

        # Blank line
        if not line.strip():
            continue

        # Headers
        if line.startswith("#### "):
            html_lines.append(f"<h4>{inline_markdown(line[5:])}</h4>")
        elif line.startswith("### "):
            html_lines.append(f"<h3>{inline_markdown(line[4:])}</h3>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{inline_markdown(line[3:])}</h2>")
        elif line.startswith("# "):
            html_lines.append(f"<h1>{inline_markdown(line[2:])}</h1>")
        elif line.startswith("---") or line.startswith("***"):
            html_lines.append("<hr>")
        else:
            # Paragraph
            html_lines.append(f"<p>{inline_markdown(line)}</p>")

    flush_blockquote()
    flush_list()
    if in_code_block:
        escaped_code = html.escape("\n".join(code_lines))
        html_lines.append(f'<pre><code>{escaped_code}</code></pre>')

    return "\n".join(html_lines)


def inline_markdown(text: str) -> str:
    """Parses inline bold, italic, code, links, images."""
    code_tokens = []
    def code_sub(m):
        code_tokens.append(m.group(1))
        return f"__INLINE_CODE_{len(code_tokens)-1}__"

    text = re.sub(r"`([^`]+)`", code_sub, text)

    # Images ![alt](url)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', text)

    # Links [title](url)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)

    # Bold **text** or __text__
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__([^_]+)__", r"<strong>\1</strong>", text)

    # Italic *text* or _text_
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"(?<!_)_([^_]+)_(?!_)", r"<em>\1</em>", text)

    # Restore code
    for i, code in enumerate(code_tokens):
        text = text.replace(f"__INLINE_CODE_{i}__", f"<code>{html.escape(code)}</code>")

    return text


def estimate_reading_time(text: str) -> str:
    words = len(text.split())
    minutes = max(1, round(words / 200))
    return f"{minutes} min read"


def format_date(date_str: str) -> str:
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%b %d, %Y")
    except Exception:
        return date_str


def build():
    config = load_config()
    blog_name = config.get("blog_name", "Signals & Systems")
    print(f"Building site for: {config['name']} (Blog: {blog_name})")

    # Prepare dist directory
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    (DIST_DIR / "about").mkdir(parents=True, exist_ok=True)
    (DIST_DIR / "blog").mkdir(parents=True, exist_ok=True)
    (DIST_DIR / "posts").mkdir(parents=True, exist_ok=True)

    # Copy static assets
    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, DIST_DIR / "static")

    # Read templates
    with open(TEMPLATES_DIR / "base.html", "r", encoding="utf-8") as f:
        base_template = f.read()
    with open(TEMPLATES_DIR / "index.html", "r", encoding="utf-8") as f:
        index_template = f.read()
    with open(TEMPLATES_DIR / "about.html", "r", encoding="utf-8") as f:
        about_template = f.read()
    with open(TEMPLATES_DIR / "blog.html", "r", encoding="utf-8") as f:
        blog_template = f.read()
    with open(TEMPLATES_DIR / "post.html", "r", encoding="utf-8") as f:
        post_template = f.read()

    # Process Posts
    posts = []
    if CONTENT_DIR.exists():
        for file in sorted(CONTENT_DIR.glob("*.md"), reverse=True):
            with open(file, "r", encoding="utf-8") as f:
                raw = f.read()
            meta, body = parse_frontmatter(raw)
            slug = meta.get("slug") or file.stem
            post_data = {
                "title": meta.get("title", file.stem),
                "date": meta.get("date", "2026-01-01"),
                "formatted_date": format_date(meta.get("date", "2026-01-01")),
                "summary": meta.get("summary", ""),
                "tags": meta.get("tags", []),
                "slug": slug,
                "body_raw": body,
                "body_html": markdown_to_html(body),
                "reading_time": estimate_reading_time(body)
            }
            posts.append(post_data)

    # Sort posts by date descending
    posts.sort(key=lambda p: p["date"], reverse=True)

    current_year = str(datetime.now().year)

    def apply_base(content: str, title: str, meta_desc: str, base_path: str, is_home=False, is_about=False, is_blog=False):
        page_html = base_template
        page_html = page_html.replace("{{page_title}}", title)
        page_html = page_html.replace("{{meta_description}}", meta_desc)
        page_html = page_html.replace("{{name}}", config["name"])
        page_html = page_html.replace("{{blog_name}}", blog_name)
        page_html = page_html.replace("{{linkedin_url}}", config["linkedin_url"])
        page_html = page_html.replace("{{github_url}}", config["github_url"])
        page_html = page_html.replace("{{year}}", current_year)
        page_html = page_html.replace("{{base_path}}", base_path)
        page_html = page_html.replace("{{nav_home_class}}", "active" if is_home else "")
        page_html = page_html.replace("{{nav_about_class}}", "active" if is_about else "")
        page_html = page_html.replace("{{nav_blog_class}}", "active" if is_blog else "")
        page_html = page_html.replace("{{content}}", content)
        return page_html

    # --- Render Individual Posts ---
    for p in posts:
        post_dir = DIST_DIR / "posts" / p["slug"]
        post_dir.mkdir(parents=True, exist_ok=True)
        base_path = "../../"

        tags_html = " ".join([f'<span class="tag">{html.escape(t)}</span>' for t in p["tags"]])

        content = post_template
        content = content.replace("{{base_path}}", base_path)
        content = content.replace("{{post_title}}", html.escape(p["title"]))
        content = content.replace("{{post_date}}", p["date"])
        content = content.replace("{{post_formatted_date}}", p["formatted_date"])
        content = content.replace("{{post_reading_time}}", p["reading_time"])
        content = content.replace("{{post_tags_html}}", tags_html)
        content = content.replace("{{post_body_html}}", p["body_html"])
        content = content.replace("{{name}}", config["name"])
        content = content.replace("{{blog_name}}", html.escape(blog_name))
        content = content.replace("{{linkedin_url}}", config["linkedin_url"])

        full_html = apply_base(
            content=content,
            title=f"{p['title']} — {blog_name}",
            meta_desc=p["summary"],
            base_path=base_path
        )

        with open(post_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(full_html)

    # --- Helper: Render Post Items for lists ---
    def render_post_list(post_items, base_path):
        if not post_items:
            return '<p style="color: var(--text-muted);">No posts published yet.</p>'
        html_out = []
        for p in post_items:
            tags = " ".join([f'<span class="tag">{html.escape(t)}</span>' for t in p["tags"]])
            item = f"""
            <article class="post-item">
              <h3 class="post-title">
                <a href="{base_path}posts/{p['slug']}/index.html">{html.escape(p['title'])}</a>
              </h3>
              <div class="post-meta">
                <time datetime="{p['date']}">{p['formatted_date']}</time>
                <span>·</span>
                <span>{p['reading_time']}</span>
                <span>·</span>
                <div class="tags" style="display:inline-flex; margin-top:0;">{tags}</div>
              </div>
              <p class="post-summary">{html.escape(p['summary'])}</p>
            </article>
            """
            html_out.append(item)
        return "\n".join(html_out)

    # --- Render Blog Archive ---
    blog_content = blog_template
    blog_content = blog_content.replace("{{blog_name}}", html.escape(blog_name))
    blog_content = blog_content.replace("{{all_posts_html}}", render_post_list(posts, "../"))
    blog_page = apply_base(
        content=blog_content,
        title=f"{blog_name} — {config['name']}",
        meta_desc=f"{blog_name} — Technical writings and articles by {config['name']}",
        base_path="../",
        is_blog=True
    )
    with open(DIST_DIR / "blog" / "index.html", "w", encoding="utf-8") as f:
        f.write(blog_page)

    # --- Render About Page ---
    current_role = config.get("current_role", {})
    about_text_html = "\n".join([f"<p>{html.escape(p)}</p>" for p in config.get("about_paragraphs", [])])

    about_content = about_template
    about_content = about_content.replace("{{base_path}}", "../")
    about_content = about_content.replace("{{name}}", html.escape(config["name"]))
    about_content = about_content.replace("{{title}}", html.escape(config["title"]))
    about_content = about_content.replace("{{current_role_title}}", html.escape(current_role.get("title", "")))
    about_content = about_content.replace("{{current_role_company}}", html.escape(current_role.get("company", "")))
    about_content = about_content.replace("{{current_role_period}}", html.escape(current_role.get("period", "")))
    about_content = about_content.replace("{{current_role_description}}", html.escape(current_role.get("description", "")))
    about_content = about_content.replace("{{about_text_html}}", about_text_html)
    about_content = about_content.replace("{{linkedin_url}}", config["linkedin_url"])
    about_content = about_content.replace("{{github_url}}", config["github_url"])

    about_page = apply_base(
        content=about_content,
        title=f"About — {config['name']}",
        meta_desc=f"About {config['name']} — {config['title']}",
        base_path="../",
        is_about=True
    )
    with open(DIST_DIR / "about" / "index.html", "w", encoding="utf-8") as f:
        f.write(about_page)

    # --- Render Minimal Home Page ---
    recent_posts_html = render_post_list(posts[:3], "./")

    index_content = index_template
    index_content = index_content.replace("{{base_path}}", "./")
    index_content = index_content.replace("{{name}}", html.escape(config["name"]))
    index_content = index_content.replace("{{blog_name}}", html.escape(blog_name))
    index_content = index_content.replace("{{recent_posts_html}}", recent_posts_html)

    home_page = apply_base(
        content=index_content,
        title=f"{config['name']} — Personal Website",
        meta_desc=f"This is a personal website for {config['name']} where he shares his experiences and thoughts.",
        base_path="./",
        is_home=True
    )
    with open(DIST_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(home_page)

    # --- Generate RSS 2.0 Feed ---
    site_url = config.get("site_url", "https://ashish-mk.github.io").rstrip("/")
    rss_items = []
    for p in posts:
        rss_items.append(f"""
    <item>
      <title>{html.escape(p['title'])}</title>
      <link>{site_url}/posts/{p['slug']}/</link>
      <description>{html.escape(p['summary'])}</description>
      <pubDate>{p['date']}</pubDate>
      <guid>{site_url}/posts/{p['slug']}/</guid>
    </item>""")

    rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{html.escape(blog_name)}</title>
    <link>{site_url}</link>
    <description>{html.escape(blog_name)} by {html.escape(config['name'])}</description>
    <language>en-us</language>
    {''.join(rss_items)}
  </channel>
</rss>
"""
    with open(DIST_DIR / "rss.xml", "w", encoding="utf-8") as f:
        f.write(rss_xml)

    print(f"✓ Build complete: generated index.html, about/index.html, blog archive, {len(posts)} posts, and rss.xml into dist/")


if __name__ == "__main__":
    build()
