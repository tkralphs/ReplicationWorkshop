#!/usr/bin/env python3
"""Make a built copy of the site openable straight from disk.

Jekyll writes asset URLs with the project-site prefix
(`/ReplicationWorkshop/assets/...`) because that is where GitHub Pages serves
them. Opened as a local file — or served from any other path — those URLs point
at the filesystem root and the page renders unstyled.

This rewrites the prefix to a relative path in every HTML file, so `index.html`
works from file:// or from any subdirectory of a static server.

Usage:
    python3 make_portable.py <built-site-dir> [--baseurl /ReplicationWorkshop]

`--baseurl` defaults to the `baseurl:` value in this repo's _config.yml.
"""

import argparse
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def config_baseurl() -> str:
    try:
        text = open(os.path.join(HERE, "_config.yml"), encoding="utf-8").read()
    except OSError:
        return ""
    m = re.search(r'^baseurl:\s*"?([^"\n]*)"?\s*$', text, re.M)
    return (m.group(1).strip() if m else "").rstrip("/")


def rewrite(path: str, baseurl: str) -> bool:
    html = open(path, encoding="utf-8").read()
    new = html
    if baseurl:
        new = new.replace(f'href="{baseurl}/', 'href="')
        new = new.replace(f'src="{baseurl}/', 'src="')
    # the site root link collapses to href="" once the prefix is stripped
    new = new.replace('href=""', 'href="index.html"')
    new = new.replace('href="/"', 'href="index.html"')
    if new != html:
        open(path, "w", encoding="utf-8").write(new)
        return True
    return False


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("site_dir", help="directory containing the built site (e.g. _site)")
    ap.add_argument("--baseurl", default=None, help="prefix to strip; defaults to _config.yml")
    args = ap.parse_args()

    baseurl = (args.baseurl if args.baseurl is not None else config_baseurl()).rstrip("/")
    if not os.path.isdir(args.site_dir):
        raise SystemExit(f"not a directory: {args.site_dir}")

    changed = 0
    for root, _dirs, files in os.walk(args.site_dir):
        for name in files:
            if name.endswith(".html"):
                if rewrite(os.path.join(root, name), baseurl):
                    changed += 1

    print(f"rewrote {changed} file(s) in {args.site_dir} (baseurl: {baseurl or 'none'})")


if __name__ == "__main__":
    main()
