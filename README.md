# Workshop on Replication in the Journal Review Process — 2027 site

Draft Jekyll site announcing the workshop at Lehigh University,
**August 19–20, 2027** (immediately after MOPTA 2027, August 17–18).

Built for GitHub Pages now, and for a move to the COR@L web server later.

## Files

```
_config.yml            site title, description, contact + outbound links, url/baseurl
index.md               ALL THE PROSE — edit this for wording changes
_includes/hero.html    hero banner (title, tagline, dates, buttons, LIOS badge)
_includes/facts.html   the four fact cards under the hero
_includes/schedule.html  the two day cards in the Program section
_includes/sponsors.html  the Sponsors band (LIOS / Lehigh ISE)
_layouts/default.html  header / main / footer shell (carries the draft noindex tag)
assets/css/style.css   the whole visual design, no external dependencies
assets/img/sponsors/   sponsor logos (ISE seal for LIOS, ISE banner for Lehigh ISE)
Gemfile                jekyll ~> 4.3
robots.txt             belt-and-braces; see the note inside
.github/workflows/     build + deploy to GitHub Pages
render_preview.py      static preview without Ruby
check_preview.py       tag-balance + local-link check on the preview
make_portable.py       strip the baseurl from a downloaded build
```

Content knobs live in `_config.yml` (`contact_email`, `mopta_url`,
`lehigh_ise_url`, `lios_url`, `url`, `baseurl`).

## Editing the page

`index.md` is ordinary Markdown: `##` headings, paragraphs separated by a blank
line, `-` lists, `[text](url)` links, `**bold**`. Sections are wrapped in the
HTML `<section>`/`<div>` elements that carry the styling, and each wrapper has
`markdown="1"` so kramdown parses what is inside as Markdown.

Two conventions to know:

- A line like `{: .aside}` immediately after a paragraph adds that CSS class to
  it (kramdown inline attribute list). Used for the callout paragraphs.
- The hero, fact strip and day cards are in `_includes/` because they are
  structured HTML; edit those files to change the dates/room labels there.

Anything you add inside a `markdown="1"` wrapper is normal Markdown — no need
to escape it. Headings get automatic `id`s (e.g. `#program`).

## Preview

With Ruby/Jekyll:

```sh
bundle install
bundle exec jekyll serve        # http://127.0.0.1:4000/replication-workshop-2027/
```

Without Ruby (e.g. on the NAS container):

```sh
python3 render_preview.py       # writes _preview/ (baseurl stripped)
python3 check_preview.py _preview/index.html
```

`render_preview.py` understands only what this site uses — front matter, the
`default` layout, `{{ content }}` and `{{ site.* }}`. It is for looking at the
page, not for producing the real build.

## Deploying (GitHub Pages) — currently gated OFF

Repo: `tkralphs/ReplicationWorkshop`.

`.github/workflows/pages.yml` runs on every push to `main` and on manual
dispatch. It **builds** every time; the **deploy** job is skipped unless the
repository variable `DEPLOY_PAGES` is `"true"` (or a manual dispatch sets the
`deploy` input). So while this is a draft, pushes produce a verified `_site/`
artifact and nothing goes live.

To publish when the time comes:

```sh
# 1. enable Pages, building from Actions
gh api -X POST repos/tkralphs/ReplicationWorkshop/pages \
  -f build_type=workflow
# 2. let the workflow deploy
gh variable set DEPLOY_PAGES --repo tkralphs/ReplicationWorkshop --body true
# 3. re-run (or push) — the site appears at the URL below
gh workflow run pages.yml --repo tkralphs/ReplicationWorkshop
```

Site URL: `https://tkralphs.github.io/ReplicationWorkshop/`

`_config.yml` sets `url` + `baseurl` for that project-site URL. The repo
segment is camel-case (`ReplicationWorkshop`); if the site is ever renamed for
public use, rename the repo and update `baseurl` to match.

To stop deploying again: `gh variable set DEPLOY_PAGES --body false` (or delete
the variable). That leaves the last published site up; to unpublish, see below.

### Downloading the rendered site

Every run uploads two artifacts to the run page:

- `github-pages` — the tarball the deploy job publishes (retention 1 day)
- `rendered-site` — a plain `_site/` folder, zipped (retention 30 days)

```sh
gh run download --repo tkralphs/ReplicationWorkshop --name rendered-site --dir rendered-site
```

That copy carries the `/ReplicationWorkshop/` prefix in its asset URLs, so it
is correct when served from that path, but opening `index.html` straight off
disk renders unstyled (the CSS is looked up at the filesystem root). Fix a
downloaded copy with:

```sh
python3 make_portable.py rendered-site      # strips /ReplicationWorkshop from hrefs
```

`render_preview.py` produces `_preview/` the same way (real content, baseurl
stripped, relative asset paths) — that is why `_preview/index.html` opens
standalone and `_site/index.html` does not.

### This is a draft — keep it out of search

- `_layouts/default.html` has `<meta name="robots" content="noindex, nofollow">`.
  **Remove that line when the site goes public.**
- `robots.txt` is included for completeness, but crawlers read `robots.txt` only
  from the origin root (`tkralphs.github.io/robots.txt`), which belongs to the
  blog. The meta tag is the one that works.
- Nothing links here, so the only way in is the URL itself.

### Taking it down

Any of these, in increasing order of severity:

| Action | Effect | Reversible |
|---|---|---|
| Settings → Pages → **Unpublish site**<br>(`gh api -X DELETE repos/tkralphs/ReplicationWorkshop/pages`) | URL starts returning 404 within a minute; repo and history untouched | Yes — re-enable Pages and redeploy |
| Delete the `gh-pages` artifact / disable the workflow | Stops updates; last published site stays up | Yes |
| Delete the repo | URL and repo gone | No |

Caveat that applies to any web takedown: caches, search-engine snippets, and
the Wayback Machine can outlive the page. With `noindex` and no inbound links,
the exposure is minimal.

## Moving to COR@L later

1. Set `url` to the COR@L address and `baseurl: ""`.
2. Remove the `noindex` meta tag.
3. `bundle exec jekyll build`, then copy `_site/` to the web root (or to a
   subdirectory and set `baseurl` to that path).

The same `_site/` output is what the GitHub Actions run produces, so the build
can also be pulled from the Actions artifact instead of building locally.

## Before this goes public

- [ ] Workshop **name** — Luis asked for one; this uses the working title.
- [ ] **Room**: HST 101 is in the text; confirm before publishing.
- [ ] **Agenda**: day blocks + topics only; add session times when settled.
- [ ] **Participants**: deliberately not listed yet.
- [ ] **Registration**: says details are not yet available.
- [ ] **Hotel / travel logistics**: generic placeholder.
- [ ] Remove the `noindex` meta tag.

## Contact

Ted Ralphs — ted@lehigh.edu
