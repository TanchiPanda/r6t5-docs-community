# r6t5-docs-community（模板仓库）

基于 GitHub Pages 的静态文档站模板：左侧可折叠目录，URL 通过 `?path=` 指定文档，右侧提供「在 GitHub 上编辑」与「复制全文」按钮，页脚带模板署名。

## 账号（r6t5-hub 统一认证）

顶栏右上角的「登录」走统一认证页 `https://myacc.r6t5.dpdns.org/?app=open-platform&country=cf`，不在本站存密码。

- 登录态靠 `ms_user` cookie 识别，作用域 `.r6t5.dpdns.org`，**因此站点必须部署在 `*.r6t5.dpdns.org` 子域下**（GitHub Pages 需在仓库 Pages 设置里绑自定义域名，并在 DNS 里配 CNAME）。
- 跳转登录时会带上 `return=<当前页面>`，认证完自动回到原来那篇文档。
- 退出登录只清本站可见的 `ms_user` cookie，不影响 hub 上其他应用。
- 挂在 `*.github.io` 上时，cookie 无法共享，页面会显示「登录」并跳 hub，但回来后需要重新点。

## 站内右键菜单

在页面上右键会打开站内菜单（输入框内仍是浏览器原生菜单）：

| 项 | 作用 |
|---|---|
| AI 对话 | 带当前文档片段向 Workers AI 提问，需在 `manifest.json` 配 `ai.endpoint` |
| 复制 | 复制选中内容；没选中就复制全文 Markdown |
| 纠错 | 跳到本仓库 Bug Issue 新建页，标题自动填「内容纠错：路径」 |
| 属性 | 路径、字数、文件大小、GitHub 上次提交 |
| 显示更多选项 | 关闭站内菜单，下一次右键恢复浏览器原生菜单 |

AI 后端可直接用 `rtdocs-home` 仓库里的 `worker/`（Cloudflare Workers AI），部署后把地址填进 `manifest.json`：

```json
"ai": { "endpoint": "https://rtdocs-ai.xxx.workers.dev" }
```

留空时「AI 对话」置灰，其余功能不受影响。

## 顶栏搜索

顶栏右侧、复制按钮左侧有搜索框：`⌘K`（Windows 为 `Ctrl+K`）聚焦，支持**文件名标题**与**全文**匹配，回车/点击跳转，`Esc` 关闭。

首次搜索时按 `manifest.json` 一次性拉取所有文档建索引并缓存在内存里；`price > 0` 的付费文档只按标题命中，不索引正文。

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
