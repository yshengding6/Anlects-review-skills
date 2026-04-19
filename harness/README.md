# Anlects Review Skill v6.0.0 - Harness 测试框架

## 概述

本 Harness 测试框架用于验证 Anlects-review-skill 的**原则零**（自适应路径 + 执行确定性）是否正确实现。

### v6.0.0 新增功能（横纵分析法整合）

**双轴分析框架**：
- **纵轴（Diachronic/纵向）**：学术史纵向演变 —— 追踪概念/章句在历代解释中的演变轨迹
- **横轴（Synchronic/横向）**：注疏关系图谱 —— 分析同期不同注疏之间的关系
- **交汇洞察**：横纵交汇洞察 —— 将纵向演变和横向关系结合，产出系统性判断

**核心原则**：
- 所有新增模块为补充性质，不替代原有四把手术刀的任何功能
- 用户可明确指定不执行某模块（可跳过性）
- 证据分级：所有主张必须标注 [实证]/[推论]/[缺失]/[待观察]

**新增章节**：
- 第4章：学术史纵向演变
- 第5章：注疏关系图谱
- 第6章：横纵交汇洞察（整合到老丁因子或独立章节）
- 输出结构从9章扩展至11章

**圆桌会议增强**：
- 学者阵容规则更新：从注疏+原文中识别，6-10位学者范围
- 会议议程扩展：增加横向对话模拟、纵向对照、跨时代对话
- 铁律扩展：增加政治动机追问、时空对照证据锚定

## 组件说明

### 1. golden_set.json
Golden Set 测试用例集，包含 3 个经典《论语》章节的测试数据：
- **八佾章** (bayi_chapter): 政治史全启用场景
- **学而章** (xueer_chapter): 仅基础字词+异常检测
- **乞醯章** (qixi_chapter): 六维解剖+变量替换+异常检测

### 2. route_assertions.py
路由断言模块，验证文本特征→方法论启用的映射：

```bash
# 运行所有 golden set 用例
python route_assertions.py

# 运行指定用例
python route_assertions.py --case bayi

# 自定义文本路由分析
python route_assertions.py --text "孔子谓季氏..."
```

**路由规则**（与 SKILL.md 原则零对应）：
| 方法论工具 | 触发条件 | 输出章节 |
|-----------|---------|---------|
| political_history | 三桓/季氏/公室/君臣/礼制/僭越 | 第2章 政治史还原 |
| anomaly_detection | 异文/脱文/衍文/历代多角度解读 | 第4章 异常检测报告 |
| variable_replacement | 概念可替换性检测 | 第5章 变量替换实验 |
| six_dimension | 用户提供注疏原文 | 第3章 注疏六维解剖 |

### 3. structure_validator.py
9章输出结构验证器，检查：
- 必须章节（1,7,8章）是否存在
- 已启用工具对应的章节是否输出
- 未启用章节是否标注"本篇不适用"
- 老丁因子（第8章）子结构完整性
- 证据锚定标记（[实证]/[推论]/[缺失]）

```python
from structure_validator import StructureValidator, validate_structure

# 验证输出结构
content = "...文献综述输出..."
enabled_tools = ["political", "anomaly"]  # 启用的工具

validator = StructureValidator(content, enabled_tools)
result, issues = validator.validate()
# result: ValidationResult.PASS/WARNING/FAIL

# 便捷函数
passed, issues = validate_structure(content, enabled_tools)
```

### 4. run_regression.py
回归测试入口，整合路由断言和结构验证：

```bash
# 运行完整回归测试
python run_regression.py

# 指定 golden set 路径
python run_regression.py /path/to/golden_set.json
```

## 9章输出结构

```
第1章：原子化扫描结果（必须）
第2章：政治史还原（可选，political_history启用时）
第3章：注疏六维解剖（可选，six_dimension启用时）
第4章：异常检测报告（可选，anomaly_detection启用时）
第5章：变量替换实验（可选，variable_replacement启用时）
第6章：圆桌会议纪要（视需要）
第7章：证据分级综述（必须）
第8章：老丁因子（必须）
第9章：冷知识命题（可选）
```

## 老丁因子结构（第8章）

```
### 核心判断
一句话概括，须违背常见理解

### 证据链
[实证] 级证据逐条列出

### 论证路径
从文本证据到核心判断的推理过程

### 潜在反例
质疑：...
回应：...

### 与主流解释的分歧点
与朱熹/刘宝楠/钱穆等人的差异

### 定位说明
[已论证] / [待挖掘]
```

## 运行测试

```bash
cd ~/.workbuddy/skills/Anlects-review-skill/harness

# 单独运行路由断言
python route_assertions.py

# 单独运行结构验证（通过回归测试）
python run_regression.py

# 全部通过输出示例
# RESULTS: 3 passed, 0 failed
# Pass Rate: 100.0%
```

## 添加新测试用例

在 `golden_set.json` 的 `cases` 数组中添加：

```json
{
  "id": "unique_id",
  "name": "用例名称",
  "input": {
    "topic": "主题描述",
    "text": "原文文本",
    "context": "上下文",
    "provided_commentaries": ["注疏1", "注疏2"]
  },
  "expected_routes": {
    "political_history": true/false,
    "anomaly_detection": true/false,
    "variable_replacement": true/false,
    "six_dimension": true/false
  },
  "expected_chapters": {
    "present": ["存在的章节"],
    "not_applicable": ["标注不适用的章节"],
    "optional": ["可选章节"]
  }
}
```

## 版本历史

- **v5.0.0** (2026-04-14): 拆分架构，原则零自适应路径+执行确定性验证
