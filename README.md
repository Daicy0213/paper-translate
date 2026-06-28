# 论文翻译 Skill (Translate Paper)

一个用于 **Claude Code / OpenCode** 的 skill，把学术论文 PDF 翻译为**中英文对照 Markdown** 文档，支持 LaTeX 公式、引用转换、专业术语标注与概念解释框。

## 功能

- **模型无关的 PDF 提取**：先用本地脚本把 PDF 提取为纯文本（兼容纯文本模型与多模态模型），避免文本模型报 `400 Model only support text input`
- **双语对照**：英文原文段 + 中文翻译段逐段交替
- **引用转换**：把数字编号引用 `[N]` 转为内嵌格式 `(*Article Title*, Journal/Conference, Year)`，不保留单独 References 节
- **LaTeX 公式**：行内 `$...$`、行间 `$$...$$`，含符号映射表
- **术语标注**：首次出现 `中文(English Full Name, 缩写)`，后续用缩写
- **概念解释**：用 `[!note]` 提示框解释核心概念、易混淆点

## 依赖

PDF 提取脚本 `references/extract_pdf.py` 会按顺序尝试以下后端，**装一个即可**：

| 后端 | 安装方式 | 说明 |
|---|---|---|
| `pdftotext` (poppler) | Windows: [poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases)；macOS: `brew install poppler`；Linux: `apt install poppler-utils` | 保真最好，推荐 |
| `pdfplumber` | `pip install pdfplumber` | 纯 Python 回退 |
| `pypdf` | `pip install pypdf` | 最后兜底 |

此外需要本机有 Python 3.8+。

## 安装

提供三种方式，任选其一。

### 方式一：插件市场（推荐）

适用于 Claude Code 的插件系统：

```bash
claude plugin marketplace add Daicy0213/paper-translate
claude plugin install translate-paper@translate-paper-plugin
```

安装后 skill 会被自动发现并启用。

### 方式二：自然语言安装

直接对 Claude Code 用自然语言下达指令，让 Agent 自动安装：

> 帮我从 GitHub 仓库 https://github.com/Daicy0213/paper-translate 安装论文翻译 skill，把 `translate-paper/` 目录放到我的用户级 skill 目录 `~/.claude/skills/` 下。

Agent 会 clone 仓库并完成复制。

### 方式三：手动复制

```bash
git clone https://github.com/Daicy0213/paper-translate.git
cp -r paper-translate/translate-paper ~/.claude/skills/
```

OpenCode 用户请复制到对应的 skill 目录（如 `~/.local/share/opencode/skill/` 或项目级 `.opencode/skill/`）。

## 使用方法

安装后，Claude Code / OpenCode 会自动发现此 skill。当请求翻译论文时，Agent 会加载并按工作流执行，例如：

> 帮我把这篇论文翻译成中英文对照 markdown：`/path/to/paper.pdf`

也可在工具调用中显式加载：

```
skill({ name: "translate-paper" })
```

## 项目结构

```
paper-translate/
├── .claude-plugin/
│   ├── marketplace.json      # 插件市场清单
│   └── plugin.json           # 插件元数据
├── translate-paper/          # skill 本体
│   ├── SKILL.md              # 主 skill 定义（工作流、格式规范）
│   └── references/
│       ├── extract_pdf.py    # PDF 文本提取脚本（三级回退）
│       └── format-guide.md   # 详细格式规范
├── README.md
└── LICENSE
```

## 许可

MIT
