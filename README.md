# Workshop on Replication in the Journal Review Process — 2027 site

Draft Jekyll site announcing the workshop at Lehigh University,
**August 19–20, 2027** (immediately after MOPTA 2027, August 17–18).

Built for GitHub Pages now, and for a move to the COR@L web server later.

## Files

```
_config.yml            site title, description, contact + outbound links, url/baseurl
index.html             all the content (single page, anchor sections)
_layouts/default.html  header / main / footer shell (carries the draft noindex tag)
assets/css/style.css   the whole visual design, no external dependencies
Gemfile                jekyll ~> 4.3
robots.txt             belt-and-braces; see the note inside
.github/workflows/     build + deploy to GitHub Pages
render_preview.py      static preview without Ruby
check_preview.py       tag-balance + local-link check on the preview
```

Content knobs live in `_config.yml` (`contact_email`, `mopta_url`,
`lehigh_ise_url`, `lios_url`, `url`, `baseurl`).

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

## Deploying (GitHub Pages)

`.github/workflows/pages.yml` builds with `bundle exec jekyll build` and deploys
with `actions/deploy-pages`. Pushing to `main` is the deploy.

One-time setup, in the repo:

1. Settings → Pages → **Source: GitHub Actions**.
2. Push. The run publishes to `https://tkralphs.github.io/replication-workshop-2027/`.

`_config.yml` already sets `url`/`baseurl` for that project-site URL.

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
| Settings → Pages → **Unpublish site**<br>(`gh api -X DELETE repos/tkralphs/replication-workshop-2027/pages`) | URL starts returning 404 within a minute; repo and history untouched | Yes — re-enable Pages and redeploy |
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
