<div align="center">

# sitekit

面向静态多语言产品网站的共享生成器和检查工具。

[![CI](https://github.com/ydongy/sitekit/actions/workflows/ci.yml/badge.svg)](https://github.com/ydongy/sitekit/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/ydongy/sitekit)](https://github.com/ydongy/sitekit/releases)

[English](README.md) · **简体中文**

</div>

只依赖 Python 标准库；产物是纯 HTML，直接提交到各个网站仓库。

## 功能特性

- `sitekit/core.py`：`Site` 配置、`Page` 基类（带 canonical、hreflang 和 Open Graph 的 head，以及页眉、页脚、FAQ、法律页面、更新日志），以及 `build()`，由它写出所有页面、`404.html`、`lang.js`、`sitemap.xml` 和 `robots.txt`。
- `sitekit/check_i18n.py`：以英文为基准检查每种语言（结构、HTML 标签、链接、占位符、不含破折号）；可选 `i18n/check-config.json`。
- `sitekit/check_site.py`：每种语言都有全部页面，链接和锚点都能解析，没有违反 Content-Security-Policy 的内容。
- `sitekit/preview.py`：行为与 Cloudflare 静态资源一致的本地预览服务器。
- `vendor.sh`：把 `sitekit/` 复制到网站仓库的 `scripts/sitekit/`。

## 环境要求

Python 3.10 或更新版本（CI 使用 3.10 和 3.12）和 bash。无需安装：sitekit 不发布到包索引，使用方通过 vendor 方式拷贝一份。

## 快速开始

```bash
# 在网站仓库中执行
<sitekit 路径>/vendor.sh .
python3 scripts/sitekit/check_i18n.py
python3 scripts/build.py
python3 scripts/sitekit/check_site.py
```

`vendor.sh <site-repo>` 会用 `sitekit/` 下的 `.py` 文件替换 `<site-repo>/scripts/sitekit/`，并写入 `scripts/sitekit/VERSION`。该文件记录这份拷贝来自哪个 sitekit **git commit hash**（工作区有未提交改动时会附带 `(uncommitted changes)`），只用于追溯 vendor 副本的来源，与 sitekit 的发布版本（`vX.Y.Z` 标签）无关。

## 使用方法

网站仓库自己维护 `i18n/`、`changelog.json`、样式和资源，以及 `scripts/build.py`：其中包含一个 `Site(...)` 和一个实现 `home()` 的 `Page` 子类。各产品之间的差异通过 `Page` 上的钩子或 `Site` 的字段表达。架构和扩展点见 [docs/design.md](docs/design.md)，背后的设计决策见 [docs/adr/](docs/adr/)。

在本地预览已构建的网站（提供网站仓库的 `public/`，默认端口 8765）：

```bash
python3 scripts/sitekit/preview.py [port]
```

## 开发

```bash
python3 -m compileall -q sitekit
python3 -m unittest discover -s tests -v
```

要端到端验证行为变更，请在分支上把它 vendor 到某个网站仓库，再运行该网站的构建和检查；纯重构必须保证网站的 `public/` 逐字节不变。

## 参与贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。提交信息和 Pull Request 标题遵循 [Conventional Commits](https://www.conventionalcommits.org/)，发布由 [release-please](https://github.com/googleapis/release-please) 据此准备。

## 安全

请通过 GitHub Security 的 “Report a vulnerability” 私下报告漏洞：[提交安全公告](https://github.com/ydongy/sitekit/security/advisories/new)。

## 许可证

[MIT](LICENSE)，Copyright (c) 2026 ydongy。
