#!/usr/bin/env python3
"""扫描 GitHub 上的模板副本，找出署名不合规的仓库。

依赖 GITHUB_TOKEN（需可读 public repo 的 code search 权限）。
用法：
    GITHUB_TOKEN=xxx python3 scripts/scan_public_copies.py --limit 20
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from check_attribution import CANONICAL, TEMPLATE_URL, extract  # noqa: E402

MARKER = "R6T5-DOCS-COMMUNITY-TEMPLATE-V1"
API = "https://api.github.com"


def api_get(url: str, token: str):
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "r6t5-attribution-scanner",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


def raw_get(url: str, token: str) -> str:
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "User-Agent": "r6t5-attribution-scanner",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=20, help="最多扫描多少个仓库")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("缺少 GITHUB_TOKEN 环境变量")
        return 2

    query = urllib.parse.quote(f'"{MARKER}" in:file')
    result = api_get(f"{API}/search/code?q={query}&per_page={args.limit}", token)

    repos = {}
    for item in result.get("items", []):
        repo = item["repository"]["full_name"]
        repos.setdefault(repo, item["path"])

    if not repos:
        print("未发现副本（可能尚未被收录进代码搜索索引）")
        return 0

    bad = []
    for repo, path in repos.items():
        try:
            content = raw_get(
                f"https://raw.githubusercontent.com/{repo}/HEAD/{urllib.parse.quote(path)}",
                token,
            )
        except Exception as exc:  # 网络或权限问题，跳过而不误判
            print(f"跳过 {repo}：{exc}")
            continue
        plain, href = extract(content)
        if plain == CANONICAL and href == TEMPLATE_URL:
            print(f"OK   {repo}")
        else:
            print(f"BAD  {repo}")
            print(f"     署名: {plain!r}")
            print(f"     链接: {href!r}")
            bad.append(repo)

    print()
    print(f"扫描 {len(repos)} 个副本，发现 {len(bad)} 个不合规：")
    for repo in bad:
        print(f"  - https://github.com/{repo}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
