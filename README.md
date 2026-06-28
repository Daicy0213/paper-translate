# 论文翻译 Skill

一个 opencode / Claude 可以加载的 skill，用于将学术论文 PDF 翻译为**中英文对照 Markdown** 文档。

## 功能

- 从 PDF 提取纯文本（兼容纯文本和多模态模型）
- 生成双语格式的 Markdown（原文 + 中文翻译逐段对照）
- 自动处理 LaTeX 公式、引用格式、专业术语标注
- 添加概念解释（`[!note]` 提示框）
- 保留代码、表格、附录等原始结构

## 安装

在 Claude Code 或 OpenCode 会话中输入以下命令即可自动安装：

```
install skill Daicy0213/paper-translate
```

Agent 会自动将本仓库的 `translate-paper/` skill 安装到正确的全局目录。

## 使用方法

安装后，opencode 或 Claude 会自动发现此 skill。当请求翻译论文时，agent 会加载并按照工作流执行。

### 手动加载

```
skill({ name: "translate-paper" })
```

### 项目结构

```
translate-paper/
├── SKILL.md                   # 主 skill 定义
└── references/
    └── format-guide.md        # 格式规范参考
```

## 许可

MIT
