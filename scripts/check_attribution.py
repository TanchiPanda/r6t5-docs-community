#!/usr/bin/env python3
"""r6t5-docs 社区版署名校验。

逐字符比对署名文案，任何空格、标点、链接目标的差异都会判定为不合规。

用法：
    python3 scripts/check_attribution.py                     # 校验本地 index.html（社区版）
    python3 scripts/check_attribution.py --file index.html
    python3 scripts/check_attribution.py --url https://xxx.github.io/repo/
    python3 scripts/check_attribution.py --licensed          # 校验已授权（隐藏专业版提示）的站点
"""

import argparse
import html
import re
import sys
import urllib.request

# 规范字符串：与 index.html 中 ATTRIBUTION 常量保持一致，一字不得改
NAME = "r6t5-docs"
BASE = "本站由r6t5-docs提供支持"
PRO_NOTE = "，使用专业版、订制版可去除本标志"
CANONICAL = BASE + PRO_NOTE
TEMPLATE_URL = "https://github.com/TanchiPanda/r6t5-docs-community"

FOOTER_RE = re.compile(r'<footer[^>]*class="site-footer"[^>]*>(.*?)</footer>', re.S)
TAG_RE = re.compile(r"<[^>]+>")
HERF_RE = re.compile(r'<a[^>]+id="footerLink"[^>]+href="([^"]+)"', re.S)
SWITCH_RE = re.compile(r"showProNote\s*:\s*(true|false)")


def extract(text: str):
    m = FOOTER_RE.search(text)
    if not m:
        return None, None
    inner = m.group(1)
    plain = html.unescape(TAG_RE.sub("", inner)).strip()
    href_m = HERF_RE.search(inner)
    href = html.unescape(href_m.group(1)) if href_m else None
    return plain, href


def check(text: str, licensed: bool) -> int:
    plain, href = extract(text)
    ok = True

    if plain is None:
        print("FAIL: 未找到页脚署名节点 <footer class=\"site-footer\">")
        return 1

    if licensed:
        # 授权版本允许静态保留提示文本（运行时由 showProNote=false 移除），
        # 但必须完整包含基础署名且不得改写
        if not plain.startswith(BASE):
            ok = False
            print("FAIL: 署名基础部分必须逐字符为「本站由r6t5-docs提供支持」")
            print(f"  实际: {plain!r}")
        remainder = plain[len(BASE):]
        if remainder not in ("", PRO_NOTE):
            ok = False
            print("FAIL: 署名出现额外内容或文字被改写")
            print(f"  实际: {plain!r}")
        if remainder == PRO_NOTE:
            print("提示: 静态文件含专业版提示，若已授权需确认 FOOTER.showProNote=false 使其运行时隐藏")
    else:
        if plain != CANONICAL:
            ok = False
            print("FAIL: 署名文案与规范不一致")
            print(f"  期望: {CANONICAL!r}")
            print(f"  实际: {plain!r}")
            for i, (a, b) in enumerate(zip(CANONICAL, plain or "")):
                if a != b:
                    print(f"  首个差异位于第 {i + 1} 个字符：期望 {a!r}，实际 {b!r}")
                    break
            else:
                print(f"  长度不一致：期望 {len(CANONICAL)}，实际 {len(plain)}")
        # 社区版不得通过 showProNote=false 私自隐藏提示
        if SWITCH_RE.search(text) is None:
            ok = False
            print("FAIL: 未找到 FOOTER.showProNote 配置")
        elif SWITCH_RE.search(text).group(1) != "true":
            ok = False
            print("FAIL: 社区版 FOOTER.showProNote 必须为 true（去除提示需取得专业版/订制版授权）")

    if href != TEMPLATE_URL:
        ok = False
        print("FAIL: 署名链接必须指向模板仓库")
        print(f"  期望: {TEMPLATE_URL}")
        print(f"  实际: {href}")

    if ok:
        print(f"PASS: 署名校验通过 → {plain}")
        return 0
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="index.html", help="本地 HTML 文件路径")
    ap.add_argument("--url", help="改为校验线上站点 URL")
    ap.add_argument("--licensed", action="store_true", help="按已授权版本校验（不含专业版提示）")
    args = ap.parse_args()

    if args.url:
        with urllib.request.urlopen(args.url, timeout=20) as resp:
            text = resp.read().decode("utf-8", "replace")
    else:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    return check(text, args.licensed)


if __name__ == "__main__":
    sys.exit(main())
