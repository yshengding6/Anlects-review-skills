#!/bin/bash
# Anlects-Review v6.0.0 GitHub 提交脚本

set -e

echo "========================================="
echo "  Anlects-Review v6.0.0 GitHub 提交准备"
echo "========================================="
echo ""

# 配置
REPO="origin"
BRANCH="master"
VERSION="v6.0.0"

# 文件列表
FILES=(
  "skill.md"
  "harness/README.md"
  "CHANGELOG.md"
)

echo ""
echo "准备提交的文件："
for file in "${FILES[@]}"; do
  echo "  - $file"
done
echo ""

# 添加文件
echo ""
echo "正在添加文件到 git..."
git init
git add "${FILES[@]}"

if [ $? -eq 0 ]; then
  echo ""
  echo "✓ 文件添加成功"
else
  echo ""
  echo "✗ 文件添加失败，请检查错误信息"
  exit 1
fi
echo ""

# 创建提交
echo ""
echo "正在创建提交..."
COMMIT_MSG=$(cat <<'EOF'
feat: 整合横纵分析法到文献研究skill

Anlects-review v5.0.0 → v6.0.0
- 新增学术史纵向演变模块（第4章）
- 新增注疏关系图谱模块（第5章）
- 新增横纵交汇洞察模块（第6章）
- 圆桌会议增强：学者阵容6-10位、5议程扩展

cultural-comparator v2.0.0 → v3.0.0
- 架构升级：三层→五层
- 新增西方概念演变史
- 新增跨文化竞争格局分析
- 新增跨文化横纵交汇洞察

classical-content-writer v1.0.0 → v1.1.0
- 开头/结尾灵活化（各5/4种方式）
- 写作结构扩展（基础+增强）
- 小标题支持
- 篇幅控制（3000字）

核心设计原则：所有新增为补充性质，不替代原有功能。
EOF
)

git commit -m "$COMMIT_MSG"

if [ $? -eq 0 ]; then
  echo ""
  echo "✓ 提交成功"
  echo ""
  echo "提交哈希："
  git rev-parse --short HEAD
  echo ""
  echo "分支: $BRANCH"
else
  echo ""
  echo "✗ 提交失败，请检查错误信息"
  exit 1
fi
echo ""

echo ""
echo "========================================="
echo "  下一步："
echo "  1. git remote add origin （如果还没添加）"
echo "  2. git push -u origin $BRANCH"
echo "  3. 创建 Pull Request"
echo ""
echo "========================================="
