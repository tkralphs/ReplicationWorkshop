#!/usr/bin/env python3
"""Tiny structural check for the generated preview: tag balance + local links.

Not a validator — just enough to catch an unclosed <div> or a broken asset path.
"""

import os
import re
import sys
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}


class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"stray </{tag}> at {self.getpos()}")
            return
        open_tag, pos = self.stack.pop()
        if open_tag != tag:
            self.errors.append(f"</{tag}> at {self.getpos()} closes <{open_tag}> from {pos}")

    def close(self):
        super().close()
        for tag, pos in self.stack:
            self.errors.append(f"unclosed <{tag}> opened at {pos}")


def main(path):
    html = open(path, encoding="utf-8").read()
    checker = Checker()
    checker.feed(html)
    checker.close()
    print(f"{path}: {'OK' if not checker.errors else 'PROBLEMS'}")
    for e in checker.errors:
        print("  -", e)

    base = os.path.dirname(path)
    for href in re.findall(r'(?:href|src)="([^"#]+)"', html):
        if href.startswith(("http", "mailto:", "data:")):
            continue
        target = os.path.join(base, href)
        status = "ok" if os.path.exists(target) else "MISSING"
        print(f"  {status}: {href}")
    return 1 if checker.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "_preview/index.html"))
