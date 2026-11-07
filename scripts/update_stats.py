#!/usr/bin/env python3
"""Write _data/stats.yml from the GitHub and PyPI APIs.

Run nightly by .github/workflows/stats.yml. Standard library only.

  python3 scripts/update_stats.py            # writes _data/stats.yml
  python3 scripts/update_stats.py --dry-run  # prints the YAML instead

Environment:
  GITHUB_TOKEN   optional; raises the GitHub API rate limit (the workflow
                 passes the job token).

What is collected (the home page renders only part of it):
  github.public_repos          from the user endpoint
  github.total_stars/forks     summed over repos the user owns that are
                               not themselves forks
  github.active_90d            repos pushed to in the last 90 days
  github.most_recent_push      newest pushed_at, excluding the site repo
  github.repos[owner/name]     stars, forks, pushed_at, latest_release for
                               every repo named in _data/featured.yml plus
                               EXTRA_REPOS below
  pypi[package]                version, last_month (no mirrors), total
                               (no mirrors) for PACKAGES below
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone

USER = "LC-Linkous"
SITE_REPO = f"{USER}/{USER}.github.io"
EXTRA_REPOS = [
    f"{USER}/AntennaCalculationAutotuningTool",
    f"{USER}/nanovna-web",
    f"{USER}/tinysa-web",
    f"{USER}/hackrf-web",
    f"{USER}/fox-hunt-web",
    f"{USER}/fox-bench",
]
PACKAGES = ["tsapython", "nvnapython", "hackrfpy"]
OUT = os.path.join(os.path.dirname(__file__), "..", "_data", "stats.yml")
FEATURED = os.path.join(os.path.dirname(__file__), "..", "_data", "featured.yml")


def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "lc-linkous.github.io stats", **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r), dict(r.headers)


def gh(path):
    headers = {"Accept": "application/vnd.github+json"}
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        headers["Authorization"] = f"Bearer {tok}"
    try:
        data, _ = get(f"https://api.github.com{path}", headers)
        return data
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def gh_paged(path):
    out, page = [], 1
    while True:
        sep = "&" if "?" in path else "?"
        batch = gh(f"{path}{sep}per_page=100&page={page}")
        if not batch:
            break
        out.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return out


def featured_repos():
    if not os.path.exists(FEATURED):
        return []
    return re.findall(r"^\s*repo:\s*(\S+)\s*$", open(FEATURED).read(), re.M)


def github_stats():
    user = gh(f"/users/{USER}")
    repos = gh_paged(f"/users/{USER}/repos?type=owner&sort=pushed")
    own = [r for r in repos if not r.get("fork")]
    cutoff = (datetime.now(timezone.utc) - timedelta(days=90)).isoformat()
    candidates = [r for r in own if r["full_name"] != SITE_REPO]
    newest = max(candidates, key=lambda r: r["pushed_at"]) if candidates else None

    wanted = []
    for name in featured_repos() + EXTRA_REPOS:
        if name not in wanted:
            wanted.append(name)
    per_repo = {}
    by_name = {r["full_name"]: r for r in repos}
    for name in wanted:
        r = by_name.get(name) or gh(f"/repos/{name}")
        if not r:
            continue
        rel = gh(f"/repos/{name}/releases/latest")
        per_repo[name] = {
            "stars": r["stargazers_count"],
            "forks": r["forks_count"],
            "pushed_at": r["pushed_at"][:10],
            "latest_release": rel["tag_name"] if rel else None,
            "latest_release_date": rel["published_at"][:10] if rel else None,
        }
    return {
        "user": USER,
        "public_repos": user["public_repos"],
        "total_stars": sum(r["stargazers_count"] for r in own),
        "total_forks": sum(r["forks_count"] for r in own),
        "active_90d": sum(1 for r in own if r["pushed_at"] >= cutoff),
        "most_recent_push": {"repo": newest["full_name"], "pushed_at": newest["pushed_at"][:10]} if newest else None,
        "repos": per_repo,
    }


def pypi_stats():
    out = {}
    for pkg in PACKAGES:
        try:
            meta, _ = get(f"https://pypi.org/pypi/{pkg}/json")
            recent, _ = get(f"https://pypistats.org/api/packages/{pkg}/recent")
            overall, _ = get(f"https://pypistats.org/api/packages/{pkg}/overall")
        except urllib.error.HTTPError as e:
            print(f"pypi {pkg}: {e}", file=sys.stderr)
            continue
        total = sum(d["downloads"] for d in overall["data"] if d["category"] == "without_mirrors")
        out[pkg] = {
            "version": meta["info"]["version"],
            "last_month": recent["data"]["last_month"],   # pypistats default: mirrors excluded
            "total": total,
        }
    return out


def yaml_scalar(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    return "'" + s.replace("'", "''") + "'"


def to_yaml(obj, indent=0):
    pad = "  " * indent
    lines = []
    for k, v in obj.items():
        if isinstance(v, dict):
            lines.append(f"{pad}{k}:")
            lines.extend(to_yaml(v, indent + 1) if v else [f"{pad}  {{}}"])
        else:
            lines.append(f"{pad}{k}: {yaml_scalar(v)}")
    return lines


def main():
    dry = "--dry-run" in sys.argv
    stats = {
        "updated": date.today().isoformat(),
        "github": github_stats(),
        "pypi": pypi_stats(),
    }
    header = (
        "# Written by scripts/update_stats.py via .github/workflows/stats.yml\n"
        "# (nightly). Do not edit by hand; edits are overwritten on the next run.\n"
        "# Download counts exclude PyPI mirrors. Stars and forks are summed over\n"
        "# repositories the user owns that are not themselves forks.\n"
    )
    text = header + "\n".join(to_yaml(stats)) + "\n"
    if dry:
        print(text)
        return
    old = open(OUT).read() if os.path.exists(OUT) else ""
    # Ignore the date line when deciding whether anything changed.
    strip = lambda t: re.sub(r"^updated: .*$", "", t, flags=re.M)
    if strip(old) == strip(text):
        print("stats unchanged")
        return
    open(OUT, "w").write(text)
    print("stats.yml updated")


if __name__ == "__main__":
    main()
