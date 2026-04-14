# -*- coding: utf-8 -*-
"""测试 literature-review 记忆管理器（v5.0.0）"""

import sys
import os
import tempfile
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from memory_manager import MemoryManager

def test_init():
    """测试初始化"""
    with tempfile.TemporaryDirectory() as tmpdir:
        memory_file = Path(tmpdir) / "test_memory.json"
        manager = MemoryManager(memory_path=memory_file)
        data = manager.read()
        assert data["version"] == "5.0.0", f"版本号不正确: {data['version']}"
        assert "blades" in data, "缺少 blades 字段"
        assert "router_config" in data, "缺少 router_config 字段"
        print("[OK] 初始化测试通过")

def test_record_execution():
    """测试执行记录"""
    with tempfile.TemporaryDirectory() as tmpdir:
        memory_file = Path(tmpdir) / "test_memory.json"
        manager = MemoryManager(memory_path=memory_file)
        manager.record_execution(
            chapter="公冶长_5.25",
            blades_used=["political_history_probe", "six_dimension_deconstruct"],
            quality_score=0.88,
            duration_min=15
        )
        data = manager.read()
        assert len(data["execution_log"]) == 1, "执行记录未添加"
        assert data["blades"]["political_history_probe"]["success_count"] == 1
        print("[OK] 执行记录测试通过")

def test_cold_knowledge():
    """测试冷知识"""
    with tempfile.TemporaryDirectory() as tmpdir:
        memory_file = Path(tmpdir) / "test_memory.json"
        manager = MemoryManager(memory_path=memory_file)
        manager.add_cold_knowledge(
            proposition="颜回志向的苦涩意味",
            chapter="公冶长_5.25",
            confidence="推论"
        )
        data = manager.read()
        assert len(data["cold_knowledge_cache"]) == 1
        print("[OK] 冷知识测试通过")

if __name__ == "__main__":
    test_init()
    test_record_execution()
    test_cold_knowledge()
    print("\n所有测试通过！")
