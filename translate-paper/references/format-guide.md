# Format Guide for Paper Translation

Detailed formatting specifications for translating academic papers into bilingual Chinese-English markdown.

## 1. Bilingual Structure

```markdown
## Section Title 章节标题

English original paragraph...

中文翻译段落...

> [!note] **Concept Explanation**
> Add easy-to-understand explanations for difficult content.
```

## 2. Citation Format

Embed citations directly in the text using `(*Article Title*, Journal/Conference, Year)`.
- Replace original `(Author et al., Year)` with the full article reference format.
- Do not include a separate References section.

Example:
```
人类智能的一个独特特征是能够将面向任务的行动与语言推理（或内心独白，*Inner speech: development, cognitive functions, phenomenology, and neurobiology*, Psychological bulletin, 2015）无缝结合。
```

## 3. Terminology Convention

- **First occurrence**: `中文翻译(English Full Name, Abbreviation)`
- **Subsequent occurrences**: abbreviation only

Examples:
- 首次：大型语言模型(Large Language Model, LLM) / 后续：LLM
- 首次：思维链提示(Chain-of-Thought Prompting, CoT) / 后续：CoT
- 首次：多任务学习(Multi-Task Learning, MTL) / 后续：MTL
- 首次：域外(Out-of-Domain, OOD) / 后续：OOD

Note: Terms without common abbreviations keep the English full name, e.g., 神经符号方法(Neuro-symbolic Methods).

## 4. Formula Handling

### Inline Formulas
Use `$...$` for formulas within text:
- `o_t ∈ O` → `$o_t \in O$`
- `π(a_t | c_t)` → `$\pi(a_t | c_t)$`
- `10^5` → `$10^5$`
- `n/2` → `$n/2$`
- `Â = A ∪ L` → `$\hat{A} = A \cup L$`

### Block Formulas
Use `$$...$$` for formulas on their own line.

### Symbol Mapping
| Symbol | LaTeX |
|--------|-------|
| · · · / ··· | `$\cdots$` |
| → | `$\to$` |
| ∈ | `$\in$` |
| ∪ | `$\cup$` |
| π | `$\pi$` |
| â | `$\hat{a}$` |
| Â | `$\hat{A}$` |

## 5. Images and Examples

- Do not translate text within images.
- Keep large prompt tables and trajectory records in the appendix in English.
- Add note: `*见原论文第X页的完整表格/轨迹*`

## 6. Supplementary Notes

Add `[!note]` explanation boxes for:
- Core concepts (e.g., what is ReAct)
- Technical terms (e.g., multi-hop QA, chain-of-thought)
- Method comparisons (e.g., CoT vs ReAct)
- Potentially confusing content

## 7. Review Checklist

- [ ] All math formulas use `$...$` or `$$...$$`
- [ ] Superscripts/subscripts converted correctly (e.g., `10^3`, `o_{t-1}`)
- [ ] Greek letters use LaTeX (`\pi`, `\alpha`, etc.)
- [ ] Citations use `(*Article Title*, Journal/Conference, Year)` format
- [ ] Section titles are bilingual
- [ ] Code/action formats preserved (e.g., `search[entity]`)

## 8. Example Snippet

```markdown
## 2 Method 方法

At time step $t$, an agent receives an observation $o_t \in O$
from the environment and takes an action $a_t \in A$ following
some policy $\pi(a_t | c_t)$.

在时间步 $t$，智能体从环境接收观察 $o_t \in O$，
并根据某个策略 $\pi(a_t | c_t)$ 采取行动 $a_t \in A$。

> [!note]
> **策略（Policy）**
> 策略就是智能体的"行动指南"，告诉它在什么情况下该做什么。
```

## 9. Notes

1. Percentages and plain numbers do not need LaTeX (e.g., 34%, 500).
2. Dollar amounts like `$140` are currency symbols, not LaTeX formulas.
3. Underscores in filenames (`_`) are not subscripts.
4. Method names like `CoT-SC`, `ReAct-IM` do not need LaTeX.
