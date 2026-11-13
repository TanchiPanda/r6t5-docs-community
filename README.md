# r6t5-docs-community（模板仓库）

基于 GitHub Pages 的静态文档站模板：左侧可折叠目录，URL 通过 `?path=` 指定文档，右侧提供「在 GitHub 上编辑」与「复制全文」按钮，页脚带模板署名。

## 页脚署名与「了解 Pro」入口（不可删改）

社区版页脚包含两样东西，逐字符校验、删改会被自动还原并给出提示：

- 署名：`本站由r6t5-docs提供支持，使用专业版、订制版可去除本标志`（链接必须指向本仓库）
- 入口：右侧「了解 Pro →」按钮（指向 `https://github.com/TanchiPanda/r6t5-docs-docker#readme`）

运行时靠 MutationObserver + 定时复核守住；构建期可用 `python3 scripts/check_attribution.py` 静态校验。
取得专业版/订制版授权后，把 `FOOTER.showProNote` 改成 `false` 即可隐藏提示与入口（署名基础部分仍保留）。


## 功能

- **可折叠文档目录**：由 `manifest.json` 驱动，支持多层分组嵌套。
- **按路径加载文档**：`?path=docs/guide/getting-started.md` 指定任意 Markdown 文档。
- **GitHub 一键编辑**：顶栏按钮跳转当前文档的 GitHub 编辑页面。
- **复制全文**：支持复制 Markdown / XML（渲染后标签）/ 纯文本。
- **浏览器端渲染**：Markdown 经 marked 实时渲染为 HTML，无需本地构建。
- **响应式布局**：窄屏下侧边栏变为抽屉式菜单。
- **页脚署名**：默认显示「本站由 r6t5-docs 提供支持，使用专业版、订制版可去除本标志」。

## 快速使用

1. Fork 本仓库，或复制全部文件到自己的新仓库。
2. 打开 `index.html`，修改顶部配置：

```js
const REPO = '用户名/仓库名';   // 你的仓库，用于拼接编辑链接
const FOOTER = {
  showProNote: true             // 社区版必须为 true；商业授权后可改为 false
};
```

署名规范字符串与链接由 `ATTRIBUTION` 常量统一提供，请勿修改。

3. 在 `docs/` 下编写 Markdown 文档，并在 `manifest.json` 登记目录。
4. 推送 `main` 分支，在 **Settings → Pages** 选择 `main` / `/(root)` 开启站点。

## 目录结构

```text
├── index.html          # 站点渲染器（目录树 + 文档加载 + 复制 + 编辑 + 页脚）
├── manifest.json       # 文档目录清单
├── README.md
└── docs/               # Markdown 示例文档（设置指南）
```

## 本地预览

```bash
python3 -m http.server 8000
# 访问 http://localhost:8000
```

## 新增文档

1. 在 `docs/` 下新建 `.md` 文件；
2. 在 `manifest.json` 对应分组中添加 `{ "title": "...", "path": "..." }`；
3. 推送到 `main` 分支，Pages 自动部署。

## 署名说明

- 社区版页脚必须完整展示：**本站由r6t5-docs提供支持，使用专业版、订制版可去除本标志**，逐字符一致，`r6t5-docs` 必须链接到本模板仓库。
- 取得专业版/订制版授权后，将 `FOOTER.showProNote` 设为 `false` 可隐藏「，使用专业版、订制版可去除本标志」，其余署名仍须保留。
- 完整条款见 [`LICENSE`](LICENSE)。

## 署名校验

仓库内置校验，任何提交/PR 署名不合规都会失败：

```bash
python3 scripts/check_attribution.py              # 校验本地 index.html
python3 scripts/check_attribution.py --url <站点>  # 校验线上站点
```

- `.github/workflows/attribution-guard.yml`：push / PR 自动校验，每周一巡检线上站点。
- `index.html` 运行时守卫：署名被删改时自动恢复并在页面提示。

扫描公开副本是否合规：

```bash
GITHUB_TOKEN=xxx python3 scripts/scan_public_copies.py
```
