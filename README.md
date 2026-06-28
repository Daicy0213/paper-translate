# 论文翻译 Skill

一个 opencode / Claude 可以加载的 skill，用于将学术论文 PDF 翻译为**中英文对照 Markdown** 文档。

## 功能

- 从 PDF 提取纯文本（兼容纯文本和多模态模型）
- 生成双语格式的 Markdown（原文 + 中文翻译逐段对照）
- 自动处理 LaTeX 公式、引用格式、专业术语标注
- 添加概念解释（`[!note]` 提示框）
- 保留代码、表格、附录等原始结构

## 安装

### 方式一：git clone（推荐）

将仓库克隆到 opencode 或 Claude 的全局 skill 目录：

```bash
# opencode 全局目录
git clone https://github.com/Daicy0213/paper-translate.git %USERPROFILE%\.config\opencode\skills\translate-paper

# 或者 Claude 全局目录
git clone https://github.com/Daicy0213/paper-translate.git %USERPROFILE%\.claude\skills\translate-paper
```

### 方式二：手动复制

将 `.opencode/skills/translate-paper/` 文件夹复制到你的项目或全局 skill 目录中：

| 位置 | 路径 |
|------|------|
| 项目级 (opencode) | `你的项目/.opencode/skills/translate-paper/` |
| 全局 (opencode) | `~/.config/opencode/skills/translate-paper/` |
| 全局 (Claude) | `~/.claude/skills/translate-paper/` |

## 使用方法

安装后，opencode 或 Claude 会自动发现此 skill。当请求翻译论文时，agent 会加载并按照工作流执行。

### 手动加载

```
skill({ name: "translate-paper" })
```

### 项目结构

```
.opencode/
└── skills/
    └── translate-paper/
        ├── SKILL.md                   # 主 skill 定义
        └── references/
            └── format-guide.md        # 格式规范参考
```

## 许可

MIT
