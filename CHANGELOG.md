# Changelog

All notable changes to the Anlects Review Skills project.

## [5.0.0] - 2026-04-14

### Breaking Changes
- **Architecture split**: Monolithic `literature-review-skill` (v4.3.0) split into three independent Skills:
  - `anlects-review` (core Skill, v5.0.0)
  - `cultural-comparator` (independent Skill, v2.0.0)
  - `classical-content-writer` (independent Skill, v1.0.0)

### Added
- B+D hybrid architecture: Core self-sufficient + downstream on-demand coverage
- Vendor-mode writer protocol embedded in core Skill for zero-friction common paths
- Three-layer cultural comparison: 诸子百家横向对话 → 东西方思想纵深对照 → 宗教传统交叉审视
- Complete writing protocol with 文风铁律 + 老丁因子标注 + 词语温度计
- P3 enhanced routing based on chapter-level dynamic routing from `chapter_graph.json`
- Harness test framework: golden set + route assertions + structure validator
- Memory manager with Read-Write Reflective Learning (aligned with Memento-Skills paper, arXiv:2603.18743)

### Changed
- Renamed from `literature-review-skills` to `Anlects-review-skills`
- Get笔记 integration moved to external tools (no longer bundled)
- Workflow orchestrator moved to cultural-comparator

### Security
- Removed personal file paths from `chapter_graph.json`
- Removed `literature_review_memory.json` from version control (runtime state)
- Removed Get笔记 note IDs from examples
- Replaced hardcoded brand name in `markdown-converter.py`
- Generalized platform-specific references for open-source compatibility
- Expanded `.gitignore` for config files, output, and IDE artifacts
