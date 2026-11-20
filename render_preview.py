#!/usr/bin/env python3
"""Render a static preview of the Jekyll site without Ruby.

Handles only what this site actually uses: YAML front matter, the
`layout: default` wrapper, `{{ content }}`, and `{{ site.* }}` variables
(plus the one `date` filter in the footer). It is a convenience for
screenshots, NOT a Jekyll replacement — run real Jekyll before publishing.

Usage:  python3 render_preview.py [output_dir]
"""

from __future__ import annotations

import os
import re
import shutil
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "_preview"))


def parse_config(path: str) -> dict[str, str]:
    """Very small YAML reader: flat `key: value` plus `>-` blocks."""
    cfg: dict[str, str] = {}
    lines = open(path, encoding="utf-8").read().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val in (">-", ">", "|", "|-"):
            block = []
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            cfg[key] = " ".join(x for x in block if x).strip()
            continue
        cfg[key] = val.strip().strip('"').strip("'")
        i += 1
    return cfg


def split_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta = {}
    for line in parts[1].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, parts[2].lstrip("\n")


def subst(template: str, ctx: dict[str, str]) -> str:
    def var(match: re.Match) -> str:
        expr = match.group(1).strip()
        if expr == "content":
            return ctx["content"]
        expr = expr.split("|")[0].strip()
        if expr.startswith("site."):
            key = expr[5:]
            if key == "time":
                return datetime.now().strftime("%B %-d, %Y")
            return ctx["site"].get(key, "")
        if expr.startswith("page."):
            return ctx["page"].get(expr[5:], "")
        return ""

    def include(match: re.Match) -> str:
        path = os.path.join(ROOT, "_includes", match.group(1).strip())
        return open(path, encoding="utf-8").read() if os.path.exists(path) else ""

    template = re.sub(r"{%\s*include\s+([^%]+?)\s*%}", include, template)
    template = re.sub(r"{{\s*(.*?)\s*}}", var, template)
    template = re.sub(r"{%.*?%}", "", template)  # drop any remaining tags
    return template


def render(layout: str, ctx: dict[str, str]) -> str:
    # Substitute the page body first, then the layout that wraps it: re.sub()
    # does not rescan replacement text, so doing it in one pass would leave
    # `{{ site.* }}` inside the content untouched.
    ctx = dict(ctx)
    ctx["content"] = subst(ctx["content"], ctx)
    return subst(layout, ctx)


def main() -> None:
    site = parse_config(os.path.join(ROOT, "_config.yml"))
    if OUT.startswith(ROOT) and os.path.isdir(OUT):
        shutil.rmtree(OUT)

    layout_path = os.path.join(ROOT, "_layouts", "default.html")
    layout = open(layout_path, encoding="utf-8").read()

    pages = [p for p in os.listdir(ROOT) if p.endswith((".html", ".md"))]
    rendered = 0
    for name in pages:
        src = os.path.join(ROOT, name)
        raw = open(src, encoding="utf-8").read()
        if not raw.startswith("---"):
            continue  # not a Jekyll page (README, etc.)
        page_meta, body = split_front_matter(raw)
        ctx = {"site": site, "page": page_meta, "content": body}
        html = render(layout, ctx)
        # Strip the project-site baseurl, then make asset URLs relative so the
        # preview renders from any subdirectory of a plain static server.
        baseurl = site.get("baseurl", "")
        if baseurl:
            html = html.replace(baseurl + "/", "/")
        html = html.replace('href="/assets/', 'href="assets/')
        out_name = "index.html" if name in ("index.html", "index.md") else name
        os.makedirs(os.path.join(OUT, os.path.dirname(out_name)), exist_ok=True)
        with open(os.path.join(OUT, out_name), "w", encoding="utf-8") as fh:
            fh.write(html)
        rendered += 1

    assets_src = os.path.join(ROOT, "assets")
    if os.path.isdir(assets_src):
        shutil.copytree(assets_src, os.path.join(OUT, "assets"), dirs_exist_ok=True)

    print(f"rendered {rendered} page(s) -> {OUT}")


if __name__ == "__main__":
    main()
