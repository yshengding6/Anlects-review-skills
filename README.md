# Anlects Review Skills

古典文献研究技能包，基于 Memento-Skills 论文（arXiv:2603.18743）的 Read-Write Reflective Learning 架构。

**仓库地址**: [https://github.com/yshengding6/Anlects-review-skills](https://github.com/yshengding6/Anlects-review-skills)

## 技能组成

### 1. Anlects-review（核心 Skill，v5.0.0）

古典文献深度分析器。原则零 + 四把手术刀 + 6阶段工作流（含圆桌会议）+ 5条核心指令 + 9章输出结构。

### 2. cultural-comparator（独立 Skill，v2.0.0）

中西文化比较器。三层架构：诸子百家横向对话 + 东西方思想纵深对照 + 宗教传统交叉审视。

### 3. classical-content-writer（独立 Skill，v1.0.0）

古典文献内容写作器。完整写作协议 + 文风铁律 + 老丁因子标注 + 格式转换。

## 架构设计

B+D 混合方案（核心自给 + 下游按需覆盖）：
- Anlects-review 内嵌精简写作协议（vendor 模式），80% 场景零摩擦
- 需要深度文化比较时，自动调用 cultural-comparator
- 需要完整写作协议时，自动调用 classical-content-writer

## 安装

将各子目录复制到 `~/.workbuddy/skills/` 下即可：

```bash
# 核心Skill
cp -r literature-review/ ~/.workbuddy/skills/anlects-review/

# 文化比较器
cp -r cultural-comparator/ ~/.workbuddy/skills/

# 内容写作器
cp -r classical-content-writer/ ~/.workbuddy/skills/
```

## 依赖

各 Skill 的 Python 依赖见各自目录下的 `requirements.txt`：

| Skill | 依赖 |
|-------|------|
| anlects-review | markdown>=3.5 |
| cultural-comparator | 无（纯标准库） |
| classical-content-writer | markdown, python-docx, reportlab, weasyprint |

## 许可证

MIT License (2024-2026)
