---
name: translate-paper
description: Translate academic paper PDFs into bilingual Chinese-English Markdown documents. Use this skill whenever the user asks to translate an academic paper, research paper, technical report, or PDF document into Chinese, create a bilingual translation, or mentions translating papers. This skill should also be triggered when the user references a PDF file and asks for translation, summary with translation, or Chinese version of a paper.
version: 1.0.0
---

# 论文翻译 Skill：学术论文 → 中英文对照 Markdown

## Overview

This skill translates academic paper PDFs into bilingual Chinese-English Markdown documents with proper formatting for LaTeX formulas, citations, and technical terminology.

## When to Use

- User asks to translate a PDF paper to Chinese
- User requests bilingual translation of a research paper
- User mentions translating a technical report or academic document
- User references a PDF file and asks for Chinese version
- User requests translation with specific formatting requirements

## Workflow

### Step 1: Extract PDF to Plain Text First (model-agnostic)

> **Why this step exists:** The built-in `Read` tool reads a PDF by sending each page to the model as a non-text content block (rendered image / document). Many LLM backends — especially **text-only models** — reject that input with an error such as `API Error: 400 Model only support text input`. To make this skill work on **any** model (text-only or multimodal), extract the PDF to plain text locally first, then read the text.

**Recommended — use the bundled extractor script** (tries `pdftotext`, then falls back to `pdfplumber` → `pypdf`, so it works in most environments with no manual setup):

```bash
python "references/extract_pdf.py" "<path/to/paper.pdf>" --out "<path/to/paper.txt>"
```

This writes a plain-text file with page markers (`--- Page N ---`) so you can translate in batches without losing page boundaries.

Then use the `Read` tool on the **extracted `.txt` file** (not the PDF):
- Read the first ~400 lines (≈ first 5 pages) to understand structure, then read remaining sections in batches.
- Reading a plain text file never triggers the "text input only" error, so this path is safe on every model.
- Extract paper metadata: title, authors, venue, year.

**Fallback A — direct command line** (if the script is unavailable):

```bash
pdftotext -layout "<path/to/paper.pdf>" "<path/to/paper.txt>"
```

**Fallback B — `Read` the PDF directly** (`pages: "1-5"`, max 20 pages per request): only when you are certain the current model accepts PDF/image input. If you see a `400 ... text input` error, stop and switch to text extraction above — do **not** retry the direct read, it will keep failing on the same model.

### Step 2: Create Markdown Document

- File naming: `{original_filename}_双语对照.md`
- Save in the same directory as the original PDF
- Add author information below the title in this format:
  ```markdown
  > **论文标题**：[English Title]
  >
  > **发表会议**：[Venue + Year]
  >
  > **作者**：[Author1 (Affiliation), Author2 (Affiliation), ...]
  ```

### Step 3: Translation Format Specifications

#### 3.1 Bilingual Structure
```markdown
## Section Title 章节标题

English original paragraph...

Chinese translation paragraph...

> [!note] **Concept Explanation**
> Add accessible explanations for difficult concepts
```

#### 3.2 Citation Format
- **In-text citations**: Use `(*Article Name*, Journal/Conference, Year)` format embedded directly in text, no separate References section
- Example: `人类智能的一个独特特征是能够将面向任务的行动与语言推理（或内心独白，*Inner speech: development, cognitive functions, phenomenology, and neurobiology*, Psychological bulletin, 2015）无缝结合。`
- Replace original `(Author et al., Year)` with `(*Article Name*, Journal/Conference, Year)` format
- Do not keep a separate References list

#### 3.3 Technical Terminology (First Appearance)
- **First appearance**: `中文翻译(English Full Name, Abbreviation)`
- **Subsequent appearances**: Use abbreviation only
- Examples:
  - First: 大型语言模型(Large Language Model, LLM)
  - Subsequent: LLM
  - First: 思维链提示(Chain-of-Thought Prompting, CoT)
  - Subsequent: CoT
  - First: 多任务学习(Multi-Task Learning, MTL)
  - Subsequent: MTL
  - First: 域外(Out-of-Domain, OOD)
  - Subsequent: OOD
- Note: Terms without common abbreviations keep English full name only, e.g.: 神经符号方法(Neuro-symbolic Methods)

#### 3.4 Formula Handling (Critical!)
- **Inline formulas**: Wrap with `$...$`
  - `o_t ∈ O` → `$o_t \notin O$`
  - `π(a_t | c_t)` → `$\pi(a_t | c_t)$`
  - `10^5` → `$10^5$`
  - `n/2` → `$n/2$`
  - `Â = A ∪ L` → `$\hat{A} = A \cup L$`
- **Display formulas**: Wrap with `$$...$$`
  - When formula occupies its own line, use `$$ {formula} $$`
- Special symbols mapping:
  - `· · ·` / `···` → `$\cdots$`
  - `→` → `$\to$`
  - `∈` → `$\in$`
  - `∪` → `$\cup$`
  - `π` → `$\pi$`
  - `â` → `$\hat{a}$`
  - `Â` → `$\hat{A}$`

#### 3.5 Images/Examples Handling
- **Do not translate** text in images
- Keep large prompt tables, trajectory records in appendices in English
- Add note: `*见原论文第X页的完整表格/轨迹*`

#### 3.6 Supplementary Annotations
Add `[!note]` explanation boxes for:
- Core concepts (e.g., what is ReAct)
- Technical terms (e.g., multi-hop QA, chain-of-thought)
- Method comparisons (e.g., CoT vs ReAct differences)
- Easily misunderstood points

### Step 4: Format Checklist

- [ ] All mathematical formulas wrapped with `$...$` or `$$...$$`
- [ ] Superscripts/subscripts correctly converted (e.g., `10^3`, `o_{t-1}`)
- [ ] Greek letters use LaTeX (`\pi`, `\alpha`, etc.)
- [ ] Citations unified to (*Article Name*, Journal/Conference, Year)
- [ ] Section titles in bilingual format
- [ ] Code/action formats preserved (e.g., `search[entity]`)

## Complete Example

```markdown
## 2 Method 方法

At time step $t$, an agent receives an observation $o_t \notin O$ 
from the environment and takes an action $a_t \notin A$ following 
some policy $\pi(a_t | c_t)$.

在时间步 $t$，智能体从环境接收观察 $o_t \notin O$，
并根据某个策略 $\pi(a_t | c_t)$ 采取行动 $a_t \notin A$。

> [!note] 
> **策略（Policy）**
> 策略就是智能体的"行动指南"，告诉它在什么情况下该做什么。
```

## Important Notes

1. Percentages and pure numbers do not need LaTeX (e.g., 34%, 500)
2. Dollar amounts like `$140` are currency symbols, not LaTeX formulas
3. Underscores `_` in filenames are not subscripts
4. Method names like `CoT-SC`, `ReAct-IM` do not need LaTeX
5. Always extract and read the full paper text completely before starting translation (see Step 1 — extract to `.txt` first on text-only models)
6. Maintain consistent terminology throughout the document
7. Preserve original formatting for tables, code blocks, and special sections
